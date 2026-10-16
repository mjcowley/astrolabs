"""
astrolabs.py - helper functions for the PVB220 Cosmology AstroLabs.

You don't need to read or change this file to complete the labs. It holds the
fiddly bits (downloading data, interactive widgets, plot styling) so the
notebooks can focus on the science. If you're keen to learn more Python, have
a look around: every function has a short description of what it does.

QUT Astrophysics Research Group (QARG)
"""

import os
import urllib.request

import numpy as np
import matplotlib.pyplot as plt

# Where the notebooks and data live online. Used when a file isn't found
# next to the notebook (e.g. when running in Google Colab).
REPO_URL = "https://raw.githubusercontent.com/mjcowley/astrolabs/main/"

# A small, colour-blind friendly palette used across the labs.
COLOURS = {
    "blue": "#1f5aa6",
    "orange": "#e08a1e",
    "teal": "#2a9d8f",
    "red": "#c0392b",
    "grey": "#7f7f7f",
}


# ---------------------------------------------------------------------------
# Setup and data
# ---------------------------------------------------------------------------

def setup():
    """Set a consistent plot style and confirm the key packages are ready."""
    import astropy
    import pandas
    import ipywidgets

    plt.rcParams.update({
        "figure.figsize": (8, 5),
        "figure.dpi": 100,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "font.size": 12,
    })
    print("✅ Setup complete! You're ready to go.")
    print(f"   numpy {np.__version__} | astropy {astropy.__version__} | "
          f"pandas {pandas.__version__} | ipywidgets {ipywidgets.__version__}")


def get_data(path):
    """
    Return the local path to a data file, downloading it if needed.

    `path` is relative to the repository's data/ folder, e.g. "C7/batse_grbs.csv".
    """
    local = os.path.join("data", path)
    if os.path.exists(local):
        return local
    os.makedirs(os.path.dirname(local), exist_ok=True)
    url = REPO_URL + "data/" + path
    print(f"⬇️  Downloading {path} ...")
    try:
        urllib.request.urlretrieve(url, local)
    except Exception as err:
        raise RuntimeError(
            f"Couldn't download {path}. Check your internet connection, or "
            f"download it from Canvas and put it in a folder called data/"
            f"{os.path.dirname(path)} next to this notebook."
        ) from err
    return local


# ---------------------------------------------------------------------------
# Self-check answers
# ---------------------------------------------------------------------------

# question id: (expected value, relative tolerance, hint if wrong)
_ANSWERS = {
    "C7_sun_minutes": (8.3, 0.03, "Divide the Sun's distance by the speed of light, then convert to minutes."),
    "C7_proxima_pc": (1.30, 0.03, "Use .to(u.pc) on Proxima Centauri's distance."),
    "C7_orders": (17.5, 0.03, "Take log10 of (MoM-z14 distance / Moon distance)."),
}


def check(question, value):
    """Give instant feedback on a number you've worked out."""
    if question not in _ANSWERS:
        print(f"🤔 I don't know a question called '{question}'.")
        return
    expected, tol, hint = _ANSWERS[question]
    if value is None:
        print("👉 Replace None with your answer first, then run the cell again.")
        return
    try:
        value = float(getattr(value, "value", value))
    except (TypeError, ValueError):
        print("🤔 That doesn't look like a number. Try again!")
        return
    if abs(value - expected) <= tol * abs(expected):
        print(f"✅ Nice work! {value:.3g} is correct.")
    else:
        print(f"❌ Not quite ({value:.3g}). 💡 Hint: {hint}")


# ---------------------------------------------------------------------------
# Section 1: distance converter
# ---------------------------------------------------------------------------

def distance_converter(objects):
    """
    Interactive widget: pick an object and a unit, see the distance and the
    light travel time. `objects` is a dict of {name: astropy Quantity}.
    """
    import astropy.units as u
    from astropy.constants import c
    import ipywidgets as widgets

    units = {
        "kilometres (km)": u.km,
        "astronomical units (AU)": u.AU,
        "light-years (ly)": u.lyr,
        "parsecs (pc)": u.pc,
    }

    def show(name, unit_name):
        d = objects[name]
        t = (d / c).to(u.s)
        print(f"📏 {name}: {d.to(units[unit_name]).value:,.4g} {unit_name}")
        print(f"⏳ Light travel time: {_nice_time(t)}")
        print(f"   You're seeing it as it was {_nice_time(t)} ago.")

    widgets.interact(
        show,
        name=widgets.Dropdown(options=list(objects), description="Object:"),
        unit_name=widgets.Dropdown(options=list(units), description="Unit:",
                                   style={"description_width": "initial"}),
    )


def _nice_time(t):
    """Turn a time in seconds into something readable."""
    import astropy.units as u
    s = t.to(u.s).value
    for limit, unit, label in [
        (60, u.s, "seconds"),
        (3600, u.min, "minutes"),
        (86400 * 2, u.hour, "hours"),
        (3.156e7 * 2, u.day, "days"),
        (3.156e7 * 2e6, u.yr, "years"),
        (3.156e7 * 2e9, u.Myr, "million years"),
    ]:
        if s < limit:
            return f"{t.to(unit).value:,.3g} {label}"
    return f"{t.to(u.Gyr).value:,.3g} billion years"


# ---------------------------------------------------------------------------
# Section 4: Olbers' paradox toy universe
# ---------------------------------------------------------------------------

def olbers_sky(age=50, expanding=False, npix=300, seed=42):
    """
    Paint a small patch of sky in a toy universe filled evenly with identical
    stars. Light can only reach us from stars closer than the 'horizon'
    (distance = speed of light x age). Returns the sky image (0 = dark,
    1 = as bright as a star's surface) and the fraction of sky covered.

    Distances are in toy units where the speed of light is 1.
    """
    rng = np.random.default_rng(seed)
    patch = 0.2                     # patch width in radians (~11 degrees)
    r_star = 0.2                    # every star has the same radius
    n = 0.05 / (np.pi * r_star**2)  # stars per unit volume
    d_min = 5.0                     # skip stars right on top of us
    horizon = float(age)

    # Number of stars in the cone out to the horizon, placed evenly in volume
    n_stars = rng.poisson(n * patch**2 * (horizon**3 - d_min**3) / 3)
    d = (d_min**3 + rng.random(n_stars) * (horizon**3 - d_min**3)) ** (1 / 3)
    x = (rng.random(n_stars) - 0.5) * patch
    y = (rng.random(n_stars) - 0.5) * patch

    if expanding:
        z = d / 25.0                         # toy redshift grows with distance
        brightness = (1 + z) ** -4           # surface brightness dimming
    else:
        brightness = np.ones(n_stars)

    sky = np.zeros((npix, npix))
    scale = npix / patch                     # pixels per radian
    order = np.argsort(d)[::-1]              # paint far stars first
    cx_all = (x + patch / 2) * scale
    cy_all = (y + patch / 2) * scale
    rad_all = r_star / d * scale

    # Tiny, distant stars cover about one pixel each: paint them all at once
    tiny = order[rad_all[order] < 1.0]
    ix = np.clip(cx_all[tiny].astype(int), 0, npix - 1)
    iy = np.clip(cy_all[tiny].astype(int), 0, npix - 1)
    hit = np.random.default_rng(seed + 1).random(tiny.size) < np.pi * rad_all[tiny] ** 2
    sky[iy[hit], ix[hit]] = brightness[tiny][hit]

    # Bigger, nearer stars are painted as discs on top
    yy, xx = np.mgrid[0:npix, 0:npix]
    for k in order[rad_all[order] >= 1.0]:
        cx = (x[k] + patch / 2) * scale
        cy = (y[k] + patch / 2) * scale
        rad = r_star / d[k] * scale
        x0, x1 = int(max(cx - rad, 0)), int(min(cx + rad + 1, npix))
        y0, y1 = int(max(cy - rad, 0)), int(min(cy + rad + 1, npix))
        if x0 >= x1 or y0 >= y1:
            continue
        sub = (xx[y0:y1, x0:x1] - cx) ** 2 + (yy[y0:y1, x0:x1] - cy) ** 2 <= rad**2
        sky[y0:y1, x0:x1][sub] = brightness[k]

    covered = np.mean(sky > 0)
    return sky, covered


def olbers_explorer():
    """Interactive widget for the Olbers' paradox toy universe."""
    import ipywidgets as widgets

    def show(age, expanding):
        sky, covered = olbers_sky(age, expanding)
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.imshow(sky, cmap="afmhot", vmin=0, vmax=1.6, origin="lower")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
        ax.set_title(f"Age = {age} | {'expanding' if expanding else 'static'}")
        plt.show()
        print(f"⭐ Sky covered by stars: {covered:.0%}")
        print(f"💡 Average sky brightness: {sky.mean():.2f} "
              f"(1.00 would be as bright as the surface of a star!)")

    widgets.interact(
        show,
        age=widgets.IntSlider(value=20, min=10, max=200, step=10,
                              description="Age:", continuous_update=False),
        expanding=widgets.Checkbox(value=False, description="Expanding universe"),
    )


# ---------------------------------------------------------------------------
# Section 5: image explorer
# ---------------------------------------------------------------------------

def image_explorer(image, title="Image"):
    """Interactive widget to change the contrast and stretch of an image."""
    import ipywidgets as widgets
    from astropy.visualization import (ImageNormalize, PercentileInterval,
                                       LinearStretch, SqrtStretch,
                                       LogStretch, AsinhStretch)

    stretches = {
        "linear": LinearStretch(),
        "sqrt": SqrtStretch(),
        "log": LogStretch(),
        "asinh": AsinhStretch(),
    }

    def show(stretch, percentile, cmap):
        norm = ImageNormalize(image, interval=PercentileInterval(percentile),
                              stretch=stretches[stretch])
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.imshow(image, origin="lower", cmap=cmap, norm=norm)
        ax.set_title(f"{title} | {stretch}, {percentile}%")
        ax.grid(False)
        plt.show()

    widgets.interact(
        show,
        stretch=widgets.ToggleButtons(options=list(stretches), value="linear",
                                      description="Stretch:"),
        percentile=widgets.FloatSlider(value=100, min=90, max=100, step=0.1,
                                       description="Clip (%):",
                                       continuous_update=False),
        cmap=widgets.Dropdown(options=["gray", "magma", "viridis", "cividis"],
                              description="Colours:"),
    )


def rgb_explorer(blue, green, red, title="Colour image"):
    """Interactive widget to build a colour image from three filters."""
    import ipywidgets as widgets
    from astropy.visualization import make_lupton_rgb

    def show(brightness, contrast):
        rgb = make_lupton_rgb(red, green, blue, stretch=brightness, Q=contrast)
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.imshow(rgb, origin="lower")
        ax.set_title(title)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
        plt.show()

    widgets.interact(
        show,
        brightness=widgets.FloatLogSlider(value=0.5, base=10, min=-2, max=1,
                                          step=0.1, description="Stretch:",
                                          continuous_update=False),
        contrast=widgets.FloatSlider(value=8, min=0, max=20, step=1,
                                     description="Q:",
                                     continuous_update=False),
    )


# ---------------------------------------------------------------------------
# Stretch activity: retrograde motion
# ---------------------------------------------------------------------------

def retrograde_explorer():
    """Interactive widget showing why Mars appears to loop backwards."""
    import ipywidgets as widgets

    a_e, p_e = 1.0, 1.0        # Earth: 1 AU, 1 year
    a_m, p_m = 1.524, 1.881    # Mars
    t = np.linspace(0.5, 1.5, 600)
    phase = 2 * np.pi * (1 - 1 / p_m)   # start Mars ahead so Earth overtakes it at t = 1 yr
    ex, ey = a_e * np.cos(2 * np.pi * t / p_e), a_e * np.sin(2 * np.pi * t / p_e)
    mx = a_m * np.cos(2 * np.pi * t / p_m + phase)
    my = a_m * np.sin(2 * np.pi * t / p_m + phase)
    # Direction we look to see Mars from Earth (degrees along the ecliptic)
    lon = np.degrees(np.unwrap(np.arctan2(my - ey, mx - ex)))

    def show(time):
        k = np.searchsorted(t, time)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        circle = np.linspace(0, 2 * np.pi, 200)
        ax1.plot(a_e * np.cos(circle), a_e * np.sin(circle), color=COLOURS["blue"], lw=0.8)
        ax1.plot(a_m * np.cos(circle), a_m * np.sin(circle), color=COLOURS["red"], lw=0.8)
        ax1.plot(0, 0, "o", color="gold", ms=14)
        ax1.plot(ex[k], ey[k], "o", color=COLOURS["blue"], ms=8, label="Earth")
        ax1.plot(mx[k], my[k], "o", color=COLOURS["red"], ms=7, label="Mars")
        dx, dy = mx[k] - ex[k], my[k] - ey[k]
        ax1.plot([ex[k], ex[k] + 3 * dx], [ey[k], ey[k] + 3 * dy], "k--", lw=0.8)
        lim = 1.3 * a_m
        ax1.set_xlim(-lim, lim)
        ax1.set_ylim(-lim, lim)
        ax1.set_aspect("equal")
        ax1.set_title("Looking down on the Solar System")
        ax1.legend(loc="upper right")

        ax2.plot(t, lon, color=COLOURS["grey"], lw=1)
        ax2.plot(t[:k + 1], lon[:k + 1], color=COLOURS["red"], lw=2)
        ax2.set_xlabel("Time (years)")
        ax2.set_ylabel("Position of Mars in our sky (degrees)")
        ax2.set_title("What we see from Earth")
        plt.tight_layout()
        plt.show()

    widgets.interact(
        show,
        time=widgets.FloatSlider(value=0.6, min=0.51, max=1.49, step=0.02,
                                 description="Time (yr):",
                                 continuous_update=False),
    )


# ---------------------------------------------------------------------------
# Section 3: isotropy explorer
# ---------------------------------------------------------------------------

def isotropy_explorer(galaxies, sky_map):
    """
    Interactive widget: include galaxies out to a chosen distance and see how
    evenly they're spread across the sky. `sky_map` is the plotting function
    defined in the notebook.
    """
    import ipywidgets as widgets

    def show(max_distance):
        chosen = galaxies[galaxies["distance_mpc"] < max_distance]
        sky_map(chosen["glon"], chosen["glat"],
                f"{len(chosen)} galaxies closer than {max_distance} Mpc",
                COLOURS["blue"])
        north = (chosen["glat"] > 0).mean()
        print(f"Fraction above the Milky Way plane: {north:.2f} "
              f"(perfectly even would be 0.50)")

    widgets.interact(
        show,
        max_distance=widgets.IntSlider(value=20, min=10, max=300, step=10,
                                       description="Max (Mpc):",
                                       continuous_update=False),
    )
