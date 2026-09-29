#!/usr/bin/env python3
"""Paper figure: every condition patched into the baseline run, two models.

One panel per model. Each curve is M at the answer position of the BASELINE run
with one condition's residual transplanted at layer l. The substrate is heavy
red, the control dashed blue (an oracle: it states the answer, and is plotted
for completeness, not as a comparison), the seven conventional conditions thin
and coloured, The dashed grey line is the baseline patched with its own residual: flat at the
unpatched margin by construction, and the reader's reference. The control
condition (which states the answer outright) is an oracle rather than a prompt
technique and is deliberately not plotted here; it is reported in the
behavioural table.

    python scripts/plot_patch_paper.py                 # -> patch_paper.png
    python scripts/plot_patch_paper.py --out ../paper/fig_patching.pdf

Reads patch_grid.json only; no GPU.
"""
import argparse, json
from pathlib import Path
HERE=Path(__file__).resolve().parent.parent   # internals/

import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
CONV=[("benchmark_CoT","chain of thought"),("benchmark_encourage","encouragement"),
      ("benchmark_expert","expert role"),("benchmark_hallucination","anti-hallucination"),
      ("benchmark_nomistakes","error avoidance"),("benchmark_threat","threat"),
      ("benchmark_urgency","objective emphasis")]
models=[("llama-3.1-8b","Llama-3.1-8B-Instruct"),("qwen3-8b","Qwen3-8B")]
fig,axes=plt.subplots(1,2,figsize=(13,5.2),constrained_layout=True)
for ax,(mid,title) in zip(axes,models):
    d=json.load(open(HERE/f"results/{mid}/bf16/patch_grid.json"))
    g=d["grid"]; n=d["n_layers"]; b=d["baseline_M_sum"]; x=list(range(n))
    ax.axhline(0,color="0.4",lw=1.0)
    # The baseline donor patched into the baseline run is flat at the baseline
    # margin by construction. Shown here as the reader's reference for where the
    # model sits unpatched; its role as a validity check is stated in the text.
    ax.plot(x,g["baseline"],color="0.35",lw=1.6,ls=(0,(4,2)),zorder=2,
            label="baseline, unpatched")
    for i,(k,lab) in enumerate(CONV):
        ax.plot(x,g[k],lw=1.2,color=plt.cm.tab20(i*2+1),alpha=.95,label=lab)
    ax.plot(x,g["substrate"],color="#d62728",lw=3.0,label="SUBSTRATE",zorder=9)
    c=next((l for l,v in enumerate(g["substrate"]) if v>0),None)
    if c is not None:
        ax.plot([c],[g["substrate"][c]],"o",ms=9,color="#d62728",zorder=10)
        ax.annotate(f"reverses at L{c}",(c,g["substrate"][c]),textcoords="offset points",
                    xytext=(10,-16),fontsize=9,color="#d62728",weight="bold")
    ax.set_title(f"{title}: baseline prompt, donor residual patched at layer $l$",fontsize=11)
    ax.set_xlabel("layer $l$ at which the residual is replaced",fontsize=10)
    # every point is the model's FINAL output margin under one intervention,
    # not a logit-lens reading of layer l
    ax.set_ylabel("final-output M = log P(drive) − log P(walk)   [nats]",fontsize=10)
    ax.tick_params(labelsize=9); ax.margins(x=.01)
axes[0].legend(fontsize=9,loc="upper left",framealpha=.95,ncol=1)
fig.suptitle("Patching every condition into the baseline run. Each point is one full forward pass:\n"
             "the donor residual replaces the baseline's at layer $l$, and M is read at the model's output.",
             fontsize=11.5)
ap=argparse.ArgumentParser()
ap.add_argument("--out",default="patch_paper.png")
args=ap.parse_args()
fig.savefig(args.out,dpi=165,bbox_inches="tight")
print("wrote",args.out)
