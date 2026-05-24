# Lab 5 code

A 5-layer MLP (16->64->64->64->10, ReLU) deployed across four backends. Each
script runs on the course AWS instance against the supplied model files
(`mlp_model.pkl`, `mlp_model.keras`) and configs (`tpuv2.json`,
`system_config.json`).

| File | Exercises | Backend |
|------|-----------|---------|
| `L5_Q2.py` | 5.1, 5.2 | CPU / GPU latency, throughput, power (JAX) |
| `L5_Q4.py` | 5.4, 5.5 | TPUv2 in NeuSim (run with `tpu-env/bin/python`) |
| `L5_Q7.py` | 5.7, 5.8 | FPGA via hls4ml + Vitis HLS (config from env vars) |
| `make_figures.py` | — | Plots from the `../results/*.jsonl` sweeps |

## 5.9 Vivado power

After building a design with `L5_Q7.py`, edit its `vivado_synth.tcl` to add the
clock and a power report, then run Vivado in that project directory:

```tcl
set tcldir [file dirname [info script]]
source [file join $tcldir project.tcl]
add_files ${project_name}_prj/solution1/syn/verilog
synth_design -top ${project_name} -part $part
create_clock -period 5 [get_ports ap_clk]   ;# 10 for the 100 MHz run
opt_design -retarget -propconst -sweep -bram_power_opt -shift_register_opt
report_utilization -file vivado_synth.rpt
report_power -file vivado_power.rpt
```

```bash
cd mlp_hls && vivado -mode batch -source vivado_synth.tcl
```
