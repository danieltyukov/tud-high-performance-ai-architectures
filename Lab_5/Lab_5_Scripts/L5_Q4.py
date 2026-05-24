"""Exercises 5.4-5.5: TPUv2 inference in NeuSim.

Wraps the supplied MLPConfig / MLPOpsGenerator, sweeps the batch size and
aggregates NeuSim's per-operator CSV into total time, energy, power and
throughput. --use-vu toggles use_vu_for_small_matmul (5.5.3).
    tpu-env/bin/python L5_Q4.py --batches 1,256,1024,65536
    tpu-env/bin/python L5_Q4.py --batches 1 --use-vu true
"""
import argparse
import csv
import json
from pathlib import Path

from absl import logging
from neusim.configs.models.ModelConfig import ModelConfig
from neusim.npusim.frontend import Operator
import neusim.npusim.frontend.llm_ops_lib as ops_lib
import neusim.npusim.frontend.op_analysis_lib as analysis_lib


class MLPConfig(ModelConfig):
    model_name: str = "MLP"
    model_type: str = "mlp_model"
    num_layers: int = 2
    hidden_dim: int = 128
    input_dim: int = 16
    output_dim: int = 32


class MLPOpsGenerator:
    def __init__(self, config):
        self.config = MLPConfig.model_validate(config) if isinstance(config, dict) else config
        assert self.config.model_type == "mlp_model"

    def generate(self, fusion_id_start=2, dump_to_file=True, **kwargs):
        ops = []
        fid = fusion_id_start
        for lid in range(self.config.num_layers):
            b, h = self.config.global_batch_size, self.config.hidden_dim
            if lid == 0:
                a, w, eq = (b, self.config.input_dim), (self.config.input_dim, h), "bi;ih->bh"
            elif lid == self.config.num_layers - 1:
                a, w, eq = (b, h), (h, self.config.output_dim), "bh;ho->bo"
            else:
                a, w, eq = (b, h), (h, h), "bh;hg->bg"
            ops.append(ops_lib.create_einsum_op(input_a_shape=a, input_b_shape=w,
                       einsum_expr=eq, name=f"MLPModel_Layer{lid}_Linear", fusion_id=fid))
            fid += 1
        ops = analysis_lib.fill_operators_execution_info(ops, self.config)
        if dump_to_file:
            self.dump_to_file(ops)
        return ops

    def compute_memory_footprint_bytes(self):
        return 1024

    def dump_to_file(self, ops):
        rows = [Operator.to_csv_dict(op) for op in ops]
        with open(self.config.output_file_path, "w") as f:
            w = csv.DictWriter(f, fieldnames=rows[0].keys())
            w.writeheader()
            w.writerows(rows)


def run(batch, use_vu=None, out="./results/mlp-inference-v2.csv"):
    npu = json.load(open("./tpuv2.json"))
    if use_vu is not None:
        npu["use_vu_for_small_matmul"] = use_vu
    sys_cfg = json.load(open("./system_config.json"))
    model = {"num_layers": 5, "hidden_dim": 64, "input_dim": 16,
             "output_dim": 10, "global_batch_size": batch}
    cfg = {**sys_cfg, **npu, **model, "output_file_path": out}
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    MLPOpsGenerator(MLPConfig.model_validate(cfg)).generate(dump_to_file=True)
    rows = list(csv.DictReader(open(out)))
    exe = sum(float(r["Execution time"]) for r in rows)
    energy = sum(float(r["total_energy_J"]) for r in rows)
    return exe, energy, [r["Bounded-by"] for r in rows]


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--batches", default="1")
    p.add_argument("--use-vu", choices=["true", "false"], default=None)
    args = p.parse_args()
    uv = None if args.use_vu is None else (args.use_vu == "true")
    logging.set_verbosity(logging.ERROR)
    for b in args.batches.split(","):
        b = int(b)
        exe, energy, bounded = run(b, use_vu=uv)
        print(json.dumps({"batch": b, "exec_ns": exe, "energy_J": energy,
                          "power_W": energy / (exe * 1e-9),
                          "throughput": b / (exe * 1e-9),
                          "bounded_by": bounded}), flush=True)
