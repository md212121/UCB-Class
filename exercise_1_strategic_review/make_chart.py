import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

quarters = [
    "Q1\n2022","Q2\n2022","Q3\n2022","Q4\n2022",
    "Q1\n2023","Q2\n2023","Q3\n2023","Q4\n2023",
    "Q1\n2024","Q2\n2024","Q3\n2024","Q4\n2024",
    "Q1\n2025","Q2\n2025","Q3\n2025","Q4\n2025",
]

# ARR by segment (estimated from financials + segments overview)
# Total ARR from CSV; segment splits reconstructed from segments overview
# and earnings call data points anchored at known values
arr_total = [251.6,266.8,279.9,275.4,302.5,316.1,329.8,328.0,
             357.5,367.6,374.1,374.8,398.9,408.5,419.6,412.8]

# Enterprise: $74M Q4 2022 → $138M Q4 2024 → $167M Q4 2025
# SMB: ~38% of ARR Q4 2022 → ~13% Q4 2025 ($52M)
# Mid-market: remainder

enterprise = [None]*16
smb        = [None]*16
midmarket  = [None]*16

# Anchor points from source material
ent_anchors = {3: 74, 11: 138, 15: 167}
smb_anchors = {3: 275.4*0.38, 11: 68, 15: 52}

# Interpolate enterprise
ent_vals = np.interp(range(16), sorted(ent_anchors), [ent_anchors[k] for k in sorted(ent_anchors)])
smb_vals = np.interp(range(16), sorted(smb_anchors), [smb_anchors[k] for k in sorted(smb_anchors)])
mm_vals  = [arr_total[i] - ent_vals[i] - smb_vals[i] for i in range(16)]

x = np.arange(16)
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.patch.set_facecolor("#0f1117")
for ax in axes:
    ax.set_facecolor("#0f1117")

# ── LEFT: Stacked area — ARR mix shift ──────────────────────────────────────
colors = {"Enterprise": "#4C9EFF", "Mid-market": "#A78BFA", "SMB": "#F87171"}
ax = axes[0]
ax.stackplot(x, smb_vals, mm_vals, ent_vals,
             labels=["SMB", "Mid-market", "Enterprise"],
             colors=[colors["SMB"], colors["Mid-market"], colors["Enterprise"]],
             alpha=0.88)

ax.set_xlim(0, 15)
ax.set_ylim(0, 480)
ax.set_xticks(x)
ax.set_xticklabels(quarters, color="#aaaaaa", fontsize=7.5)
ax.set_yticks([0, 100, 200, 300, 400])
ax.set_yticklabels(["$0", "$100M", "$200M", "$300M", "$400M"], color="#aaaaaa", fontsize=8)
ax.set_title("ARR Mix Shift by Segment", color="white", fontsize=12, fontweight="bold", pad=10)
ax.tick_params(colors="#aaaaaa", length=0)
for spine in ax.spines.values():
    spine.set_visible(False)
ax.grid(axis="y", color="#2a2a3a", linewidth=0.6)

# Annotate share labels at Q4 2022 and Q4 2025
for qtr_idx, label_set in [(3, ["38%","35%","27%"]), (15, ["13%","47%","40%"])]:
    cumulative = 0
    for val, color in zip([smb_vals[qtr_idx], mm_vals[qtr_idx], ent_vals[qtr_idx]],
                          [colors["SMB"], colors["Mid-market"], colors["Enterprise"]]):
        mid = cumulative + val / 2
        if val > 18:
            ax.text(qtr_idx, mid, label_set.pop(0), ha="center", va="center",
                    color="white", fontsize=8, fontweight="bold")
        cumulative += val

handles = [mpatches.Patch(color=colors[s], label=s) for s in ["Enterprise","Mid-market","SMB"]]
ax.legend(handles=handles, loc="upper left", framealpha=0, labelcolor="white", fontsize=8)

# ── RIGHT: NRR divergence by segment ────────────────────────────────────────
quarters_kpi = ["Q1\n2024","Q2\n2024","Q3\n2024","Q4\n2024",
                "Q1\n2025","Q2\n2025","Q3\n2025","Q4\n2025"]
x2 = np.arange(8)
nrr_ent = [127,127,126,126,125,125,125,125]
nrr_mm  = [108,107,106,105,104,103,103,102]
nrr_smb = [98, 96, 93, 91, 89, 88, 86, 84]

ax2 = axes[1]
ax2.plot(x2, nrr_ent, color=colors["Enterprise"], linewidth=2.5, marker="o", markersize=5, label="Enterprise")
ax2.plot(x2, nrr_mm,  color=colors["Mid-market"], linewidth=2.5, marker="o", markersize=5, label="Mid-market")
ax2.plot(x2, nrr_smb, color=colors["SMB"],        linewidth=2.5, marker="o", markersize=5, label="SMB")
ax2.axhline(100, color="#555566", linewidth=1, linestyle="--")
ax2.text(7.1, 100.8, "100% = flat", color="#888888", fontsize=7.5)

ax2.set_xlim(-0.3, 7.5)
ax2.set_ylim(78, 132)
ax2.set_xticks(x2)
ax2.set_xticklabels(quarters_kpi, color="#aaaaaa", fontsize=7.5)
ax2.set_yticks([80, 90, 100, 110, 120, 130])
ax2.set_yticklabels(["80%","90%","100%","110%","120%","130%"], color="#aaaaaa", fontsize=8)
ax2.set_title("Net Revenue Retention by Segment", color="white", fontsize=12, fontweight="bold", pad=10)
ax2.tick_params(colors="#aaaaaa", length=0)
for spine in ax2.spines.values():
    spine.set_visible(False)
ax2.grid(axis="y", color="#2a2a3a", linewidth=0.6)
ax2.legend(framealpha=0, labelcolor="white", fontsize=8, loc="lower left")

# End labels
for vals, color in [(nrr_ent, colors["Enterprise"]), (nrr_mm, colors["Mid-market"]), (nrr_smb, colors["SMB"])]:
    ax2.text(7.15, vals[-1], f"{vals[-1]}%", color=color, fontsize=8.5, fontweight="bold", va="center")

fig.suptitle("Meridian Technologies — The Diverging Business", color="white",
             fontsize=14, fontweight="bold", y=1.01)
plt.tight_layout()
plt.savefig("/home/user/UCB-Class/exercise_1_strategic_review/meridian_chart.png",
            dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
print("Saved.")
