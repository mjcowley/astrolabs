"""
Make the figures used in AstroLab C1.

europa_orbit.png shows why a moon on a circular orbit seems to swing from
side to side when we see its orbit edge-on from Earth.

Run from the repository root:

    python tools/make_c1_figures.py
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

IMAGES = os.path.join("C1", "images")
os.makedirs(IMAGES, exist_ok=True)

JUP = "#d9a066"
MOON = "#2b6cb0"
INK = "#1f2933"
GREY = "#7b8794"

angles = np.radians(np.arange(0, 360, 45))  # eight positions around the orbit, 0 = nearest Earth
fig, (top, side) = plt.subplots(2, 1, figsize=(8, 7.2), gridspec_kw={"height_ratios": [3.2, 1]})

# ---- looking down on the orbit
t = np.linspace(0, 2 * np.pi, 400)
top.plot(np.sin(t), -np.cos(t), color=GREY, lw=1.2, ls="--")
top.add_patch(plt.Circle((0, 0), 0.16, color=JUP, zorder=3))
top.text(0, 0, "Jupiter", ha="center", va="center", fontsize=9, color=INK, zorder=4)
for k, a in enumerate(angles):
    x, y = np.sin(a), -np.cos(a)
    top.add_patch(plt.Circle((x, y), 0.06, color=MOON, zorder=3))
    top.text(1.18 * x, 1.18 * y, str(k + 1), ha="center", va="center", fontsize=10, color=INK)
    top.plot([x, x], [y, -1.75], color=MOON, lw=0.6, alpha=0.35)
top.annotate("", xy=(1.13, 0.45), xytext=(1.2, -0.3), arrowprops=dict(arrowstyle="->", color=INK, lw=1.2,
             connectionstyle="arc3,rad=0.25"))
top.text(1.3, 0.1, "Europa orbits\nanticlockwise", fontsize=9, color=INK, va="center")
top.annotate("", xy=(0, -1.8), xytext=(0, -1.3), arrowprops=dict(arrowstyle="->", color=INK, lw=1.4))
top.text(0.08, -1.6, "To Earth", fontsize=10, color=INK, va="center")
top.set_title("Looking down on Europa's orbit", fontsize=11, color=INK, loc="left")
top.set_xlim(-1.9, 2.1)
top.set_ylim(-1.9, 1.3)
top.set_aspect("equal", adjustable="box")
top.axis("off")

# ---- the same orbit seen edge-on from Earth
side.axhline(0, color=GREY, lw=1, ls="--")
side.add_patch(plt.Circle((0, 0), 0.16, color=JUP, zorder=2))
for k, a in enumerate(angles):
    x = np.sin(a)
    behind = np.cos(a) < -1e-9
    hidden = abs(x) < 0.16 and behind
    side.add_patch(plt.Circle((x, 0), 0.06, color=MOON, alpha=0.25 if hidden else 1, zorder=1 if behind else 3))
    side.text(x + (0.09 if k in (0, 3, 5) else -0.09 if k in (1, 4, 7) else 0), 0.17 + (0.13 if k in (3, 4, 5) else 0),
              str(k + 1), ha="center", fontsize=9, color=INK)
side.annotate("", xy=(1.0, -0.3), xytext=(0, -0.3), arrowprops=dict(arrowstyle="<->", color=INK, lw=1, shrinkA=0, shrinkB=0))
side.text(0.5, -0.48, "largest distance from Jupiter = the radius of the orbit", ha="center", fontsize=9, color=INK)
side.set_title("What we see from Earth: Europa moves back and forth along a line", fontsize=11, color=INK, loc="left")
side.set_xlim(-1.9, 2.1)
side.set_ylim(-0.62, 0.45)
side.set_aspect("equal", adjustable="box")
side.axis("off")

fig.tight_layout()
fig.savefig(os.path.join(IMAGES, "europa_orbit.png"), dpi=160, facecolor="white")
print("saved", os.path.join(IMAGES, "europa_orbit.png"))
