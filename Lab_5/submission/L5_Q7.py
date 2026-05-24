"""Exercises 5.7-5.8: build the MLP for FPGA with hls4ml + Vitis HLS.

Precision, reuse factor, clock period and output directory come from the
environment so the same script covers every sweep point. Defaults reproduce
5.7 (ap_fixed<8,4>, reuse 1, 200 MHz). After it runs, the latency and
utilisation are in mlp_hls*/myproject_prj/solution1/syn/report.
    PREC="ap_fixed<8,4>" REUSE=1 CLK=5  OUTDIR=mlp_hls           python3 L5_Q7.py  # 5.7, 5.9@200MHz
    PREC="ap_fixed<8,4>" REUSE=1 CLK=10 OUTDIR=mlp_hls_100       python3 L5_Q7.py  # 5.8.1, 5.9@100MHz
    PREC="ap_fixed<4,2>" REUSE=1 CLK=5  OUTDIR=mlp_hls_q22       python3 L5_Q7.py  # 5.8.2
    PREC="ap_fixed<8,4>" REUSE=4 CLK=5  OUTDIR=mlp_hls_reuse4    python3 L5_Q7.py  # 5.8.3
"""
import hls4ml
import os
import shutil
from tensorflow import keras

prec = os.environ.get("PREC", "ap_fixed<8,4>")
reuse = int(os.environ.get("REUSE", "1"))
clk = float(os.environ.get("CLK", "5"))
outdir = os.environ.get("OUTDIR", "mlp_hls")
cosim = os.environ.get("COSIM", "1") == "1"

if os.path.exists(outdir):
    shutil.rmtree(outdir)

model = keras.models.load_model("mlp_model.keras")

config = hls4ml.utils.config_from_keras_model(
    model, default_precision=prec, default_reuse_factor=reuse, granularity="name"
)
config["Model"]["Strategy"] = "Latency"

hls_model = hls4ml.converters.convert_from_keras_model(
    model, hls_config=config, output_dir=outdir,
    part="xcu200-fsgd2104-2-e", backend="Vitis",
    clock_period=clk, io_type="io_parallel",
)
hls_model.build(csim=cosim, synth=True, cosim=cosim)
