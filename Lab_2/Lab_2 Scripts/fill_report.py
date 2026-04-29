"""Substitute REPLACE_* placeholders in the Lab 2 report with measured numbers.

Reads:
    lab2/results/all.jsonl
    lab2/results/extras.jsonl
    lab2/results/q7_run.log
    lab2/results/validate_q6.txt

Edits in place:
    Lab_2/report/Lab2_Daniel_Tyukov_5714699.tex
"""
from __future__ import annotations

import json
import os
import re
import sys
from collections import defaultdict


def load(paths):
    rows = []
    for p in paths:
        if not os.path.exists(p):
            continue
        with open(p) as f:
            for line in f:
                line = line.strip()
                if not line.startswith("{"):
                    continue
                rows.append(json.loads(line))
    return rows


def best_summary(rows, **filt):
    """Lowest min_s among summary rows that match filt."""
    cands = []
    for r in rows:
        if not r.get("summary"):
            continue
        if all(r.get(k) == v for k, v in filt.items()):
            cands.append(r)
    if not cands:
        return None
    return min(cands, key=lambda x: x["min_s"])


def fmt(value, places=2):
    if value is None:
        return "—"
    return f"{value:.{places}f}"


def main(repo_root):
    res = os.path.join(repo_root, "Lab_2/Lab_2 Scripts/results")
    if not os.path.isdir(res):
        # Local copy of AWS results
        res = os.path.join(repo_root, "Lab_2/results")
    rows = load([
        os.path.join(res, "all.jsonl"),
        os.path.join(res, "extras.jsonl"),
    ])

    repl = {}

    # Phase A: sequential MLP and tvb_par at chunk=40
    a_seq_76  = best_summary(rows, mode="seq_mlp", dataset="tvb76",  tag="A_seq")
    a_seq_192 = best_summary(rows, mode="seq_mlp", dataset="tvb192", tag="A_seq")
    a_par_76  = best_summary(rows, mode="par",     dataset="tvb76",  tag="A_par40")
    a_par_192 = best_summary(rows, mode="par",     dataset="tvb192", tag="A_par40")
    if a_seq_76:  repl["REPLACE_A_SEQ_TVB76"]  = fmt(a_seq_76["min_s"])
    if a_seq_192: repl["REPLACE_A_SEQ_TVB192"] = fmt(a_seq_192["min_s"])
    if a_par_76:  repl["REPLACE_A_PAR_TVB76"]  = fmt(a_par_76["min_s"])
    if a_par_192: repl["REPLACE_A_PAR_TVB192"] = fmt(a_par_192["min_s"])
    if a_seq_76 and a_par_76:
        repl["REPLACE_A_R_TVB76"]  = f"{a_seq_76['min_s']/a_par_76['min_s']:.2f}×"
    if a_seq_192 and a_par_192:
        repl["REPLACE_A_R_TVB192"] = f"{a_seq_192['min_s']/a_par_192['min_s']:.2f}×"

    # Phase C* — Cstar tags carry the actual-optimum chunks (40, 128).
    def C(ds, tf):
        return best_summary(rows, mode="par", dataset=ds, tf=tf,
                            tag=f"Cstar_{int(tf)}")
    c76_15  = C("tvb76",  15.0); c76_60  = C("tvb76",  60.0)
    c192_15 = C("tvb192", 15.0); c192_60 = C("tvb192", 60.0)
    if c76_15:  repl["REPLACE_C_TVB76_15"]  = fmt(c76_15["min_s"])
    if c76_60:  repl["REPLACE_C_TVB76_60"]  = fmt(c76_60["min_s"])
    if c192_15: repl["REPLACE_C_TVB192_15"] = fmt(c192_15["min_s"])
    if c192_60: repl["REPLACE_C_TVB192_60"] = fmt(c192_60["min_s"])
    if c76_15 and c76_60:
        repl["REPLACE_C_TVB76_RATIO"] = f"{c76_60['min_s']/c76_15['min_s']:.2f}×"
    if c192_15 and c192_60:
        repl["REPLACE_C_TVB192_RATIO"] = f"{c192_60['min_s']/c192_15['min_s']:.2f}×"

    # Phase D* — par_sm at correct chunks
    d76  = best_summary(rows, mode="par_sm", dataset="tvb76",  tag="Dstar_par_sm")
    d192 = best_summary(rows, mode="par_sm", dataset="tvb192", tag="Dstar_par_sm")
    # tvb998: from the chunk sweep, pick the lowest min_s
    d998_sweep = [r for r in rows if r.get("summary") and r.get("tag") == "D_sm_sweep998"]
    d998 = min(d998_sweep, key=lambda r: r["min_s"]) if d998_sweep else None
    if d76:  repl["REPLACE_D_TVB76_TIME"]  = fmt(d76["min_s"])
    if d192: repl["REPLACE_D_TVB192_TIME"] = fmt(d192["min_s"])
    if d998:
        repl["REPLACE_D_TVB998_TIME"] = fmt(d998["min_s"])
        repl["REPLACE_D_TVB998_BESTCHUNK"] = str(d998["chunk"])
    if d76 and a_par_76:
        repl["REPLACE_D_TVB76_RATIO"]  = f"{a_par_76['min_s']/d76['min_s']:.2f}×"
    if d192 and a_par_192:
        repl["REPLACE_D_TVB192_RATIO"] = f"{a_par_192['min_s']/d192['min_s']:.2f}×"

    # Phase E* — par_smi
    e76  = best_summary(rows, mode="par_smi", dataset="tvb76",  tag="Estar_par_smi")
    e192 = best_summary(rows, mode="par_smi", dataset="tvb192", tag="Estar_par_smi")
    e998_sweep = [r for r in rows if r.get("summary") and r.get("tag") == "E_smi_sweep998"]
    e998 = min(e998_sweep, key=lambda r: r["min_s"]) if e998_sweep else None
    if e76:  repl["REPLACE_E_TVB76_TIME"]  = fmt(e76["min_s"])
    if e192: repl["REPLACE_E_TVB192_TIME"] = fmt(e192["min_s"])
    if e998: repl["REPLACE_E_TVB998_TIME"] = fmt(e998["min_s"])
    if e76 and d76:   repl["REPLACE_E_TVB76_RATIO"]  = f"{d76['min_s']/e76['min_s']:.2f}×"
    if e192 and d192: repl["REPLACE_E_TVB192_RATIO"] = f"{d192['min_s']/e192['min_s']:.2f}×"
    if e998 and d998: repl["REPLACE_E_TVB998_RATIO"] = f"{d998['min_s']/e998['min_s']:.2f}×"

    # Phase F — L2_Q6 timings
    def F(ds):
        cands = [r for r in rows if r.get("tag") == "F_q6"
                 and r.get("dataset") == ds and r.get("rep") is not None]
        if not cands:
            return None
        return min(c["time_s"] for c in cands)
    f76 = F("tvb76"); f192 = F("tvb192"); f998 = F("tvb998")
    if f76:  repl["REPLACE_F_TVB76_TIME"]  = fmt(f76)
    if f192: repl["REPLACE_F_TVB192_TIME"] = fmt(f192)
    if f998: repl["REPLACE_F_TVB998_TIME"] = fmt(f998)
    if e76 and f76:   repl["REPLACE_F_TVB76_SPEEDUP"]  = f"{e76['min_s']/f76:.2f}×"
    if e192 and f192: repl["REPLACE_F_TVB192_SPEEDUP"] = f"{e192['min_s']/f192:.2f}×"
    if e998 and f998: repl["REPLACE_F_TVB998_SPEEDUP"] = f"{e998['min_s']/f998:.2f}×"

    # Phase G — L2_Q7 results, parsed from the printed log
    q7log = os.path.join(res, "q7_run.log")
    par_wall = par_tps = ser_wall = ser_tps = None
    if os.path.exists(q7log):
        with open(q7log) as f:
            log = f.read()
        m_par = re.search(r"\[Q7\]\[parallel-of-sims\]\s+wall=([\d.]+)s\s+throughput=([\d.]+)", log)
        if m_par:
            par_wall = float(m_par.group(1))
            par_tps  = float(m_par.group(2))
            repl["REPLACE_G_PAR_TIME"] = fmt(par_wall)
            repl["REPLACE_G_PAR_TPS"]  = fmt(par_tps, 0)

    # Compute "Q6 back-to-back × 200" from a single Q6 timing on TVB192.
    n_sims = 200
    timesteps_per_sim = int(15.0 / 0.05)  # 300
    if f192:
        ser_wall = n_sims * f192
        ser_tps  = (n_sims * timesteps_per_sim) / ser_wall
        repl["REPLACE_G_SERIAL_TIME"] = fmt(ser_wall)
        repl["REPLACE_G_SERIAL_TPS"]  = fmt(ser_tps, 0)
    if par_tps and ser_tps:
        if par_tps > ser_tps:
            repl["REPLACE_G_VERDICT"] = (
                f"The throughput-oriented \\texttt{{L2\\_Q7}} version is "
                f"\\textbf{{{par_tps/ser_tps:.2f}× faster}} per timestep "
                f"than running \\texttt{{L2\\_Q6}} 200 times back-to-back"
            )
        else:
            repl["REPLACE_G_VERDICT"] = (
                f"\\texttt{{L2\\_Q6}} run 200 times back-to-back is "
                f"\\textbf{{{ser_tps/par_tps:.2f}× faster}} on this 8-vCPU "
                f"machine; the inner pool's vectorised-sparse kernel "
                f"wins because the per-simulation work is large enough "
                f"that the within-simulation parallelism still pays off"
            )

    # Phase H — multithreaded
    def H(ds, tf):
        return best_summary(rows, mode="thr", dataset=ds, tf=tf, tag="H_thr")
    h76_15  = H("tvb76",  15.0); h76_60  = H("tvb76",  60.0)
    h192_15 = H("tvb192", 15.0); h192_60 = H("tvb192", 60.0)
    if h76_15:  repl["REPLACE_H_TVB76_15"]  = fmt(h76_15["min_s"])
    if h76_60:  repl["REPLACE_H_TVB76_60"]  = fmt(h76_60["min_s"])
    if h192_15: repl["REPLACE_H_TVB192_15"] = fmt(h192_15["min_s"])
    if h192_60: repl["REPLACE_H_TVB192_60"] = fmt(h192_60["min_s"])
    if c76_15 and h76_15:
        repl["REPLACE_H_TVB76_R15"]  = f"{c76_15['min_s']/h76_15['min_s']:.2f}×"
    if c192_15 and h192_15:
        repl["REPLACE_H_TVB192_R15"] = f"{c192_15['min_s']/h192_15['min_s']:.2f}×"
    if h76_15 and h76_60:
        repl["REPLACE_H_TVB76_RATIO"]  = f"{h76_60['min_s']/h76_15['min_s']:.2f}×"
    if h192_15 and h192_60:
        repl["REPLACE_H_TVB192_RATIO"] = f"{h192_60['min_s']/h192_15['min_s']:.2f}×"

    # Validation
    vfile = os.path.join(res, "validate_q6.txt")
    if os.path.exists(vfile):
        with open(vfile) as fh:
            text = fh.read()
        m = re.search(r"max \|ref - opt\| = ([\d.eE+-]+)", text)
        if m:
            repl["REPLACE_VALIDATE_Q6"] = m.group(1)

    # Apply substitutions to the .tex file. The placeholders may appear
    # either bare (`REPLACE_A_B`) or LaTeX-escaped (`REPLACE\_A\_B`); we
    # match both forms.
    tex_path = os.path.join(repo_root,
        "Lab_2/report/Lab2_Daniel_Tyukov_5714699.tex")
    with open(tex_path) as fh:
        tex = fh.read()
    n_subs = 0
    for k, v in repl.items():
        # Build a pattern that matches the bare form and the \_-escaped form.
        parts = k.split("_")
        escaped = parts[0] + "".join(rf"(?:\\_|_){p}" for p in parts[1:])
        pat = re.compile(rf"(?<![A-Z0-9_]){escaped}(?![A-Z0-9_])")
        # Use a lambda replacement so re.sub doesn't interpret backslash
        # sequences (\t, \n, \1, ...) inside the value as escapes.
        replacement = str(v)
        new_tex, n = pat.subn(lambda _m, _r=replacement: _r, tex)
        if n:
            n_subs += n
            tex = new_tex
    with open(tex_path, "w") as fh:
        fh.write(tex)

    # Report what we substituted and what's still missing.
    print(f"applied {n_subs} substitutions across {len(repl)} keys")
    remaining = sorted(set(re.findall(r"REPLACE(?:\\?_[A-Z0-9]+)+", tex)))
    if remaining:
        print(f"still missing ({len(remaining)}); filling with '—' for compile:")
        for k in remaining:
            print(f"  {k}")
        tex = re.sub(r"REPLACE(?:\\?_[A-Z0-9]+)+", "---", tex)
        with open(tex_path, "w") as fh:
            fh.write(tex)
    else:
        print("all placeholders filled")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1
         else "/home/danieltyukov/workspace/tud/tud-high-performance-ai-architectures")
