"""
Make the data files and figures used in AstroLab C2.

Part 1 uses ten Faulkes Telescope North images of WASP-2 from the Las Cumbres
Observatory (LCO) archive, taken on 2008-10-05 UT and stored in
data/C2/wasp2_lco_images.zip. They were renamed in time order (see
docs/MAINTAINING.md for the original LCO file names).

Part 2 uses the TESS 2-minute light curve of WASP-2 (TIC 374530847) from
Sector 81, downloaded from MAST. This script saves it as a simple CSV and
draws the two light-curve figures students read values from.

It also draws the transit diagram used in the introduction.

Usage (from the repository root):

    pip install astropy matplotlib numpy
    python tools/make_c2_data.py
"""

import io
import os
import urllib.request

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits

DATA = os.path.join("data", "C2")
IMAGES = os.path.join("C2", "images")
TESS_FILE = "tess2024196212429-s0081-0000000374530847-0276-s_lc.fits"
TESS_URL = "https://mast.stsci.edu/api/v0.1/Download/file?uri=mast:TESS/product/" + TESS_FILE

NAVY = "#003562"
GREY = "#8a9bb0"
INK = "#1f2933"
plt.rcParams.update({"font.size": 12, "axes.edgecolor": "#52606d", "axes.labelcolor": INK,
                     "xtick.color": "#52606d", "ytick.color": "#52606d"})


def tess_light_curve():
    with urllib.request.urlopen(TESS_URL) as response:
        hdul = fits.open(io.BytesIO(response.read()))
    data = hdul[1].data
    good = np.isfinite(data["TIME"]) & np.isfinite(data["PDCSAP_FLUX"]) & (data["QUALITY"] == 0)
    time = data["TIME"][good]
    flux = data["PDCSAP_FLUX"][good]
    days = time - time[0]
    brightness = flux / np.median(flux)

    path = os.path.join(DATA, "wasp2_tess_sector81.csv")
    np.savetxt(path, np.column_stack([days, brightness]), delimiter=",", fmt=["%.5f", "%.5f"],
               header="days_since_start,relative_brightness", comments="")
    print(f"{path}: {len(days)} measurements over {days[-1]:.1f} days")
    return days, brightness


def style(ax):
    ax.grid(True, which="major", color="#d9e2ec", lw=0.8)
    ax.grid(True, which="minor", color="#eef2f6", lw=0.6)
    ax.spines[["top", "right"]].set_visible(False)


def plot_full(days, brightness):
    fig, ax = plt.subplots(figsize=(12, 4.2))
    ax.plot(days, brightness, ".", ms=2, color=NAVY, alpha=0.5)
    ax.set_xlim(0, 27)
    ax.set_ylim(0.975, 1.008)
    ax.set_xticks(np.arange(0, 28, 2))
    ax.set_xticks(np.arange(0, 28, 1), minor=True)
    ax.set_xlabel("Days since TESS started observing")
    ax.set_ylabel("Relative brightness")
    ax.set_title("WASP-2 seen by TESS (July to August 2024)", color=INK, loc="left")
    style(ax)
    fig.tight_layout()
    fig.savefig(os.path.join(IMAGES, "tess_full.png"), dpi=150)
    plt.close(fig)


def plot_transit(days, brightness):
    centre = 16.945                                     # one transit near the middle of the data
    hours = (days - centre) * 24
    window = np.abs(hours) < 2.5
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(hours[window], brightness[window], ".", ms=4, color=GREY, alpha=0.7,
            label="Every 2-minute measurement")
    edges = np.arange(-2.5, 2.51, 1 / 6)                # 10-minute averages
    mids = (edges[:-1] + edges[1:]) / 2
    means = [np.mean(brightness[window][(hours[window] >= a) & (hours[window] < b)])
             for a, b in zip(edges[:-1], edges[1:])]
    ax.plot(mids, means, "o-", ms=5, lw=1.5, color=NAVY, label="10-minute averages")
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(0.975, 1.008)
    ax.set_xticks(np.arange(-2.5, 2.51, 0.5))
    ax.set_xticks(np.arange(-2.5, 2.51, 0.25), minor=True)
    ax.set_yticks(np.arange(0.975, 1.0081, 0.005))
    ax.set_yticks(np.arange(0.975, 1.0081, 0.001), minor=True)
    ax.set_xlabel("Hours from the middle of the transit")
    ax.set_ylabel("Relative brightness")
    ax.set_title("A single transit of WASP-2b seen by TESS", color=INK, loc="left")
    ax.legend(loc="lower right", frameon=False)
    style(ax)
    fig.tight_layout()
    fig.savefig(os.path.join(IMAGES, "tess_transit.png"), dpi=150)
    plt.close(fig)


def transit_diagram():
    positions = [-2.1, -1.0, 0, 1.0, 2.1]
    depth = 0.02

    def covered(x):                                     # fraction of the full dip at each position
        return np.clip((1.14 - np.abs(x)) / 0.28, 0, 1)

    fig, (top, bottom) = plt.subplots(2, 1, figsize=(10, 7.4),
                                      gridspec_kw={"height_ratios": [1.5, 1.1], "hspace": 0.02})
    top.add_patch(plt.Circle((0, 0), 1, color="#f2b233"))
    for x in positions:
        top.add_patch(plt.Circle((x, -0.25), 0.14, color=INK))
    top.annotate("", xy=(2.7, -0.25), xytext=(-2.7, -0.25),
                 arrowprops=dict(arrowstyle="->", color="#52606d", lw=1.2))
    top.set_xlim(-3, 3)
    top.set_ylim(-1.15, 1.15)
    top.set_aspect("equal", adjustable="box")          # keeps the full width, so it lines up below
    top.axis("off")
    x = np.linspace(-3, 3, 600)
    bottom.plot(x, 1 - depth * covered(x), color=NAVY, lw=2.5)
    for xp in positions:
        bottom.plot(xp, 1 - depth * covered(xp), "o", ms=8, color=NAVY)
        bottom.axvline(xp, color="#d9e2ec", lw=1, zorder=0)
    bottom.annotate("", xy=(2.6, 1 - depth), xytext=(2.6, 1),
                    arrowprops=dict(arrowstyle="<->", color="#52606d", lw=1.2))
    bottom.plot([0.6, 2.7], [1 - depth, 1 - depth], ":", color="#52606d", lw=1)
    bottom.text(2.5, 1 - depth / 2, "transit\ndepth", ha="right", va="center", color=INK)
    bottom.set_xlim(-3, 3)
    bottom.set_ylim(1 - 1.4 * depth, 1 + 0.4 * depth)
    bottom.set_xticks([])
    bottom.set_yticks([1, 1 - depth])
    bottom.set_yticklabels(["100%", "98%"])
    bottom.set_xlabel("Time")
    bottom.set_ylabel("Star's brightness")
    bottom.spines[["top", "right"]].set_visible(False)
    fig.savefig(os.path.join(IMAGES, "transit_diagram.png"), dpi=130, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    os.makedirs(IMAGES, exist_ok=True)
    days, brightness = tess_light_curve()
    plot_full(days, brightness)
    plot_transit(days, brightness)
    transit_diagram()
