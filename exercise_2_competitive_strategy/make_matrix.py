import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np

fig, ax = plt.subplots(figsize=(11, 9))
fig.patch.set_facecolor("#0f1117")
ax.set_facecolor("#0f1117")

# ── Axes setup ───────────────────────────────────────────────────────────────
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axvline(5, color="#2a2a3a", linewidth=1.2, zorder=1)
ax.axhline(5, color="#2a2a3a", linewidth=1.2, zorder=1)

# Quadrant shading
for (x0, y0, x1, y1, alpha) in [
    (0, 5, 5, 10, 0.04),   # top-left
    (5, 5, 10, 10, 0.07),  # top-right  ← white space
    (0, 0, 5, 5,  0.04),   # bottom-left
    (5, 0, 10, 5, 0.04),   # bottom-right
]:
    ax.add_patch(plt.Rectangle((x0, y0), x1-x0, y1-y0,
                               facecolor="white", alpha=alpha, zorder=0))

# Quadrant labels
quad_style = dict(color="#555566", fontsize=9, ha="center", va="center", style="italic")
ax.text(2.5, 9.3, "Conservative PM", **quad_style)
ax.text(7.5, 9.3, "Agentic Premium", **quad_style)
ax.text(2.5, 0.7, "Bundled PM", **quad_style)
ax.text(7.5, 0.7, "Agentic Bundled", **quad_style)

# ── Players ──────────────────────────────────────────────────────────────────
# (x=agentic score 0–10, y=premium score 0–10, label, color, marker)
players = [
    (2.8, 6.2, "Smartsheet",        "#94A3B8", "o"),
    (5.5, 2.8, "Monday.com",        "#FB923C", "o"),
    (6.8, 3.2, "Asana",             "#F472B6", "o"),
    (8.8, 8.4, "Atlassian\n(Rovo)", "#34D399", "o"),
    (4.2, 7.0, "Meridian\n(today)", "#7DD3FC", "s"),
    (8.0, 7.6, "Meridian\n(Option B)", "#FACC15", "*"),
]

for x, y, label, color, marker in players:
    size = 220 if marker == "*" else 130
    ax.scatter(x, y, s=size, color=color, marker=marker,
               zorder=5, edgecolors="white", linewidths=0.6)

# Labels — nudged to avoid overlap
offsets = {
    "Smartsheet":        (-0.15,  0.45),
    "Monday.com":        ( 0.15, -0.50),
    "Asana":             ( 0.15, -0.50),
    "Atlassian\n(Rovo)": ( 0.15,  0.30),
    "Meridian\n(today)": (-0.15,  0.35),
    "Meridian\n(Option B)": (0.15, 0.30),
}
for x, y, label, color, marker in players:
    dx, dy = offsets[label]
    ax.text(x + dx, y + dy, label, color=color,
            fontsize=9.5, fontweight="bold" if "Meridian" in label else "normal",
            ha="left" if dx > 0 else "right", va="bottom" if dy > 0 else "top",
            zorder=6)

# Arrow: Meridian today → Option B
ax.annotate("", xy=(7.85, 7.45), xytext=(4.55, 7.05),
            arrowprops=dict(arrowstyle="-|>", color="#FACC15",
                            lw=1.6, mutation_scale=14),
            zorder=4)
ax.text(6.15, 7.55, "recommended\nshift", color="#FACC15",
        fontsize=8, ha="center", style="italic")

# White space callout box
ax.add_patch(plt.Rectangle((5.2, 5.2), 4.6, 4.6,
             fill=False, edgecolor="#FACC15", linewidth=1.2,
             linestyle="--", alpha=0.5, zorder=3))
ax.text(9.9, 9.85, "White space:\nEnterprise-grade\nagentic + premium",
        color="#FACC15", fontsize=8, ha="right", va="top",
        alpha=0.75, style="italic")

# ── Axis labels & title ───────────────────────────────────────────────────────
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

# X axis arrow + labels
ax.annotate("", xy=(10, 0.05), xytext=(0, 0.05),
            arrowprops=dict(arrowstyle="-|>", color="#666677", lw=1.2))
ax.text(0.1, 0.35, "PM-centric", color="#888899", fontsize=9, va="bottom")
ax.text(9.9, 0.35, "Agentic-first", color="#888899", fontsize=9, va="bottom", ha="right")

# Y axis arrow + labels
ax.annotate("", xy=(0.05, 10), xytext=(0.05, 0),
            arrowprops=dict(arrowstyle="-|>", color="#666677", lw=1.2))
ax.text(0.35, 0.2,  "Bundled / included", color="#888899", fontsize=9,
        rotation=90, va="bottom")
ax.text(0.35, 9.8, "Premium / add-on", color="#888899", fontsize=9,
        rotation=90, va="top")

ax.set_title("Competitive Positioning — AI Strategy & Pricing Model",
             color="white", fontsize=13, fontweight="bold", pad=16)

# Footnote
fig.text(0.5, 0.01,
         "Sources: cached competitor AI posture summaries, Feb 2026  ·  "
         "Positions are qualitative estimates based on public statements",
         ha="center", color="#555566", fontsize=7.5, style="italic")

plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.savefig("/home/user/UCB-Class/exercise_2_competitive_strategy/positioning_matrix.png",
            dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
print("Saved.")
