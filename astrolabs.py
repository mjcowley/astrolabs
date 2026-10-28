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
    In a copy of the whole repository, notebooks sit one folder down (C7/, C8/, ...),
    so the repository's own data/ folder is checked there too.
    """
    local = os.path.join("data", path)
    for candidate in (local, os.path.join("..", "data", path)):
        if os.path.exists(candidate):
            return candidate
    os.makedirs(os.path.dirname(local), exist_ok=True)
    url = REPO_URL + "data/" + path
    print(f"⬇️  Downloading {path} ...")
    try:
        urllib.request.urlretrieve(url, local)
    except Exception as err:
        raise RuntimeError(
            f"Couldn't download {path}. Check your internet connection, or "
            f"download it from github.com/mjcowley/astrolabs and put it in a folder called data/"
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
    "C8_planck_temperature": (1.42e32, 0.05, "Use T_P = sqrt(hbar c^5 / (G k^2)) and convert to kelvin."),
    "C8_z_tenth": (9, 0.01, "Use 1 + z = 1 / a with a = 0.1."),
    "C8_cmb_temperature": (2.725, 0.002, "Move the slider until the curve passes through the data points."),
    "C8_decoupling_z": (1100, 0.03, "Use 1 + z = T_then / T_now with T_then = 3000 K."),
    "C8_helium": (0.25, 0.03, "Use Y = 2 x / (1 + x) with x = 1/7."),
    "C8_z_galaxy_C": (5.45, 0.015, "Line up the dashed lines with the bright emission lines of galaxy C."),
    "C9_E_ngc4473": (4.5, 0.25, "Stretch the ellipse to match the galaxy's outline, then use E = 10 (1 - b/a)."),
    "C9_z_3c273": (0.158, 0.02, "Line up the dashed H-alpha line with the tallest peak, near 7590 Angstroms."),
    "C9_distance_mpc": (667, 0.03, "Use v = cz, then d = v / H0 with H0 = 71 km/s/Mpc."),
    "C9_brightness_ratio": (120, 0.05, "Use 100 ** ((m1 - m2) / 5) with M31's magnitude first."),
    "C9_eddington_mass": (1.2e8, 0.05, "First turn 3C 273's magnitude into a luminosity, then multiply by 3.1e-5."),
    "C9_eddington_rate": (2.9, 0.05, "Multiply the Eddington mass by 2.4e-8."),
    "C10_deflection_sun": (1.75, 0.03, "Use alpha = 4GM/(c^2 b) with b = the radius of the Sun, then convert radians to arcseconds."),
    "C10_halo_speed": (126, 0.12, "Move the halo speed slider until the red curve runs through the flat part of the data."),
    "C10_strain": (1.3e-21, 0.1, "Use h = (GM/c^2) (1/D) (v/c)^2 with v = 2e8 m/s."),
    "C10_delay_ms": (7.0, 0.15, "Slide Livingston until its wiggles line up with Hanford's (and tick 'flip')."),
    "C10_chirp_mass": (31, 0.12, "Move the slider until the white curve follows the bright chirp in the spectrogram."),
    "C11_hubble_constant": (70.6, 0.04, "Fit a straight line through the origin to velocity (cz) against distance."),
    "C11_false_match_percent": (1.9, 0.3, "Count the shifted matches inside your radius and divide by the number of ZFIRE galaxies."),
    "C11_outlier_percent": (1.4, 0.3, "Count galaxies with |z_phot - z_spec| / (1 + z_spec) > 0.15."),
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


# ===========================================================================
# AstroLab C8: Running the Clock Backwards
# ===========================================================================

T_CMB_TODAY = 2.7255   # K (Fixsen 2009)

# Rest-frame wavelengths (in micrometres) of bright lines in galaxy spectra
REST_LINES = {
    "Lyα": 0.1216,
    "[O II]": 0.3727,
    "Hβ": 0.4861,
    "[O III]": 0.5007,
    "Hα": 0.6563,
}

_AGE_TABLE = None


def _age_table():
    """Build a table of the age of the Universe against scale factor (Planck 2018)."""
    global _AGE_TABLE
    if _AGE_TABLE is None:
        import astropy.units as u
        from astropy.cosmology import Planck18
        from scipy.integrate import cumulative_trapezoid
        h0 = Planck18.H0.to(1 / u.s).value
        omega_r = Planck18.Ogamma0 * (1 + 0.2271 * 3.046)   # photons + neutrinos
        omega_m = Planck18.Om0
        omega_l = 1 - omega_m - omega_r
        a = np.logspace(-12, 0, 40000)
        hubble = h0 * np.sqrt(omega_r * a**-4 + omega_m * a**-3 + omega_l)
        t = cumulative_trapezoid(1 / (a * hubble), a, initial=0) + 1 / (2 * hubble[0])
        _AGE_TABLE = (a, t)
    return _AGE_TABLE


def age_of_universe(z):
    """Age of the Universe (as an astropy Quantity) when the light we see at redshift z set off."""
    import astropy.units as u
    a, t = _age_table()
    return (np.interp(1 / (1 + np.asarray(z, dtype=float)), a, t) * u.s).to(u.yr)


def redshift_at_age(age):
    """Redshift at which the Universe had a given age (an astropy time Quantity)."""
    import astropy.units as u
    a, t = _age_table()
    return 1 / np.interp(age.to(u.s).value, t, a) - 1


def expansion_explorer():
    """Interactive widget: stretch space with the scale factor a and watch light stretch too."""
    import ipywidgets as widgets

    # Galaxies spread evenly through space (in coordinates that stretch with it)
    rng = np.random.default_rng(3)
    gx, gy = rng.uniform(-5, 5, (2, 4000))

    def show(a):
        z = 1 / a - 1
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5),
                                       gridspec_kw={"width_ratios": [1, 1.6]})
        inside = (np.abs(gx * a) < 0.5) & (np.abs(gy * a) < 0.5)
        ax1.scatter(gx[inside] * a, gy[inside] * a, s=12, color=COLOURS["orange"])
        ax1.set_xlim(-0.5, 0.5)
        ax1.set_ylim(-0.5, 0.5)
        ax1.set_aspect("equal")
        ax1.set_xticks([])
        ax1.set_yticks([])
        ax1.set_title(f"A fixed patch of space: {inside.sum()} galaxies")

        x = np.linspace(0, 10, 2000)
        emitted = 1.0
        ax2.plot(x, np.sin(2 * np.pi * x / emitted) + 1.5, color=COLOURS["blue"],
                 label="Light when it set off")
        ax2.plot(x, np.sin(2 * np.pi * x / (emitted * (1 + z))) - 1.5, color=COLOURS["red"],
                 label="The same light arriving today")
        ax2.set_yticks([])
        ax2.set_xlabel("Distance along the wave")
        ax2.set_ylim(-3.2, 3.2)
        ax2.legend(loc="upper right", fontsize=10)
        ax2.set_title(f"a = {a:.2f}  →  z = {z:.2f}  (wavelength stretched {1 + z:.1f}×)")
        plt.tight_layout()
        plt.show()
        print(f"When the light set off, the Universe was {a:.0%} of its size today.")

    widgets.interact(
        show,
        a=widgets.FloatSlider(value=0.5, min=0.1, max=1.0, step=0.01,
                              description="Scale factor a:",
                              style={"description_width": "initial"},
                              continuous_update=False),
    )


def blackbody_fitter(frequency, intensity, error, model):
    """
    Interactive widget: change the temperature of a blackbody until it matches
    the COBE FIRAS data. `model(frequency, T)` is the Planck function defined
    in the notebook.
    """
    import ipywidgets as widgets

    fine = np.linspace(frequency.min() * 0.8, frequency.max() * 1.05, 400)

    def show(temperature):
        prediction = model(frequency, temperature)
        mismatch = np.sqrt(np.mean(((intensity - prediction) / error) ** 2))
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.plot(fine, model(fine, temperature), color=COLOURS["red"], lw=2,
                label=f"Blackbody at {temperature:.3f} K")
        ax.errorbar(frequency, intensity, yerr=error * 100, fmt="o", ms=4,
                    color=COLOURS["blue"], label="COBE FIRAS (error bars × 100)")
        ax.set_xlabel("Frequency (GHz)")
        ax.set_ylabel("Intensity (MJy/sr)")
        ax.set_title("The spectrum of the cosmic microwave background")
        ax.legend()
        plt.show()
        print(f"Typical mismatch: {mismatch:,.1f} error bars "
              f"(a perfect match would be about 1)")

    widgets.interact(
        show,
        temperature=widgets.FloatSlider(value=3.2, min=2.0, max=3.5, step=0.005,
                                        readout_format=".3f",
                                        description="Temperature (K):",
                                        style={"description_width": "initial"},
                                        continuous_update=False),
    )


def cmb_rewind(model):
    """
    Interactive widget: run the CMB back in time. Shows the blackbody spectrum
    against wavelength at redshift z, with the visible band marked.
    """
    import ipywidgets as widgets
    from astropy.constants import c as c_light

    wavelength_um = np.logspace(-1, 4, 600)     # 0.1 micron to 1 cm
    freq_ghz = (c_light.value / (wavelength_um * 1e-6)) / 1e9

    def band(lam_um):
        if lam_um < 0.38:
            return "ultraviolet"
        if lam_um < 0.75:
            return "visible light"
        if lam_um < 1000:
            return "infrared"
        return "microwaves"

    def show(z):
        temperature = T_CMB_TODAY * (1 + z)
        with np.errstate(over="ignore"):
            # brightness per unit wavelength, so the peak matches Wien's law
            spectrum = model(freq_ghz, temperature) * freq_ghz**2
        peak_um = 2898 / temperature            # Wien's law, in micrometres
        fig, ax = plt.subplots(figsize=(10, 4.8))
        ax.axvspan(0.38, 0.75, color="gold", alpha=0.35, label="Visible light")
        ax.plot(wavelength_um, spectrum / spectrum.max(), color=COLOURS["red"], lw=2)
        ax.axvline(peak_um, color="k", ls="--", lw=1)
        ax.set_xscale("log")
        ax.set_xlabel("Wavelength (micrometres)")
        ax.set_ylabel("Brightness (scaled to the peak)")
        ax.set_title(f"z = {z:,.0f}   |   T = {temperature:,.1f} K")
        ax.legend(loc="upper right")
        plt.show()
        print(f"🌡️ Temperature: {temperature:,.1f} K")
        print(f"📈 Peak wavelength: {peak_um:,.2f} micrometres ({band(peak_um)})")
        print(f"📏 The Universe was {1 / (1 + z):.2%} of its size today")

    widgets.interact(
        show,
        z=widgets.IntSlider(value=0, min=0, max=1500, step=10,
                            description="Redshift z:",
                            continuous_update=False),
    )


# Epochs from the PVB220 Big Bang lecture: (name, start, end) in years
EPOCHS = [
    ("Nucleosynthesis", 100 / 3.156e7, 1200 / 3.156e7),
    ("Recombination", 3.3e5, 3.8e5),
    ("Dark Ages", 3.8e5, 1.5e8),
    ("Reionisation", 1.5e8, 1.0e9),
    ("Galaxies", 1.0e9, 1.38e10),
]


def time_machine():
    """Interactive widget: travel through cosmic history and read off z, a and T."""
    import astropy.units as u
    import ipywidgets as widgets

    ages = np.logspace(np.log10(60 / 3.156e7), np.log10(1.37e10), 400)   # years
    z_all = redshift_at_age(ages * u.yr)
    temps = T_CMB_TODAY * (1 + z_all)
    colours = ["#e08a1e", "#c0392b", "#4b3b6b", "#2a9d8f", "#1f5aa6"]

    def show(log_age):
        age = 10 ** log_age * u.yr
        z = redshift_at_age(age)
        temp = T_CMB_TODAY * (1 + z)
        fig, ax = plt.subplots(figsize=(10, 5))
        for (name, start, end), col in zip(EPOCHS, colours):
            ax.axvspan(start, end, color=col, alpha=0.18)
            ax.text(np.sqrt(start * end), 3e9 if name != "Recombination" else 3e7, name,
                    ha="center", fontsize=9, rotation=90, va="top")
        ax.plot(ages, temps, color="k", lw=2)
        ax.plot(age.value, temp, "o", color=COLOURS["red"], ms=10)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("Age of the Universe (years)")
        ax.set_ylabel("Temperature (K)")
        ax.set_title("The cosmic thermometer")
        plt.show()
        here = [name for name, start, end in EPOCHS if start <= age.value <= end]
        print(f"⏳ Age: {_nice_time(age.to(u.s))}")
        print(f"🌡️ Temperature: {temp:,.4g} K")
        print(f"🔴 Redshift: z = {z:,.4g}   |   Size compared with today: {1 / (1 + z):.3g}")
        print(f"📍 Epoch: {', '.join(here) if here else 'between epochs'}")

    widgets.interact(
        show,
        log_age=widgets.FloatSlider(value=0.0, min=np.log10(100 / 3.156e7), max=10.139,
                                    step=0.01, description="log₁₀(age / yr):",
                                    style={"description_width": "initial"},
                                    readout_format=".2f", continuous_update=False),
    )


def helium_explorer():
    """Interactive widget: how the neutron to proton ratio sets the helium fraction."""
    import ipywidgets as widgets

    def show(neutrons_per_proton):
        x = neutrons_per_proton
        helium = 2 * x / (1 + x)
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.pie([1 - helium, helium], labels=["Hydrogen", "Helium"],
               colors=[COLOURS["blue"], COLOURS["orange"]],
               autopct="%1.0f%%", startangle=90, textprops={"fontsize": 13})
        ax.set_title("What the first stars were made of (by mass)")
        plt.show()
        print(f"Neutrons per proton: {x:.3f}  →  helium mass fraction Y = {helium:.3f}")

    widgets.interact(
        show,
        neutrons_per_proton=widgets.FloatSlider(value=0.3, min=0.0, max=0.5, step=0.001,
                                                readout_format=".3f",
                                                description="Neutrons per proton:",
                                                style={"description_width": "initial"},
                                                continuous_update=False),
    )


def redshift_explorer(spectra):
    """
    Interactive widget: line up the dashed lines with the emission lines in a
    JWST spectrum to measure its redshift. `spectra` is the table of spectra.
    """
    import ipywidgets as widgets

    def show(galaxy, z):
        s = spectra[spectra["galaxy"] == galaxy]
        fig, ax = plt.subplots(figsize=(11, 5))
        ax.plot(s["wavelength_um"], s["flux"], color="k", lw=1)
        top = np.nanpercentile(s["flux"], 99.7) * 1.15
        for name, rest in REST_LINES.items():
            observed = rest * (1 + z)
            if 0.6 <= observed <= 5.4:
                ax.axvline(observed, color=COLOURS["red"], ls="--", lw=1)
                ax.text(observed, top * 0.97, f" {name}", color=COLOURS["red"],
                        rotation=90, va="top", fontsize=10)
        ax.set_xlim(0.6, 5.4)
        ax.set_ylim(min(-0.05 * top, np.nanmin(s["flux"])), top)
        ax.set_xlabel("Observed wavelength (micrometres)")
        ax.set_ylabel("Flux (10⁻²⁰ erg/s/cm²/Å)")
        ax.set_title(f"Galaxy {galaxy} ({s['jades_id'].iloc[0]})   |   trying z = {z:.2f}")
        plt.show()

    widgets.interact(
        show,
        galaxy=widgets.ToggleButtons(options=sorted(spectra["galaxy"].unique()),
                                     description="Galaxy:"),
        z=widgets.FloatSlider(value=0.0, min=0.0, max=12.0, step=0.01,
                              description="Redshift z:", readout_format=".2f",
                              continuous_update=False),
    )


def _sky_image(ax, image, vmin, vmax, cmap="RdBu_r"):
    """Draw a Mollweide sky image with the outside of the ellipse left blank."""
    ax.imshow(np.ma.masked_invalid(image), origin="lower", cmap=cmap, vmin=vmin, vmax=vmax)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(False)


def cmb_layers_explorer(maps):
    """Interactive widget: peel back the layers of the microwave sky."""
    import ipywidgets as widgets

    dipole, galaxy, cmb = maps["DIPOLE"], maps["GALAXY"], maps["CMB"]
    layers = {
        "1. The whole sky": (T_CMB_TODAY + (dipole + cmb) * 1e-6, 0, 3,
                             "The same 2.725 K in every direction", "K"),
        "2. Zoom ×1,000": (dipole + cmb, -3500, 3500,
                           "Hotter ahead of us, cooler behind: our motion through space", "μK"),
        "3. Remove our motion": (galaxy, -300, 300,
                                 "The Milky Way glows across the middle", "μK"),
        "4. Remove the Milky Way": (cmb, -300, 300,
                                    "The ripples: the Universe 380,000 years after the Big Bang", "μK"),
    }

    def show(layer):
        image, vmin, vmax, caption, unit = layers[layer]
        fig, ax = plt.subplots(figsize=(11, 5.5))
        _sky_image(ax, image, vmin, vmax, cmap="RdBu_r" if unit == "μK" else "inferno")
        ax.set_title(caption)
        cb = fig.colorbar(ax.images[0], ax=ax, orientation="horizontal", fraction=0.05, pad=0.04)
        cb.set_label(f"Temperature ({unit})" if unit == "K" else f"Difference from 2.725 K ({unit})")
        plt.show()

    widgets.interact(show, layer=widgets.ToggleButtons(options=list(layers),
                                                       description="Layer:"))


def resolution_explorer(maps):
    """Interactive widget: the same patch of the CMB seen by COBE, WMAP and Planck."""
    import ipywidgets as widgets

    info = {
        "COBE (1992)": ("PATCH_COBE", "7° resolution"),
        "WMAP (2003)": ("PATCH_WMAP", "0.35° resolution"),
        "Planck (2013)": ("PATCH_PLANCK", "0.08° resolution"),
    }

    def show(mission):
        key, res = info[mission]
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.imshow(maps[key], origin="lower", cmap="RdBu_r", vmin=-300, vmax=300,
                  extent=[-5, 5, -5, 5])
        ax.set_xlabel("Degrees")
        ax.set_ylabel("Degrees")
        ax.grid(False)
        ax.set_title(f"{mission}: {res}")
        plt.show()

    widgets.interact(show, mission=widgets.ToggleButtons(options=list(info),
                                                         description="Mission:"))


# ===========================================================================
# AstroLab C9: Galaxies and Their Monsters
# ===========================================================================

# Hubble types for the galaxy gallery (the answer key for galaxy_classifier)
GALAXY_TYPES = {
    "M87": ["Elliptical (E)"],
    "NGC4473": ["Elliptical (E)"],
    "NGC3115": ["Lenticular (S0)"],
    "M104": ["Lenticular (S0)", "Spiral (S)"],
    "M74": ["Spiral (S)"],
    "NGC1300": ["Barred spiral (SB)"],
    "NGC1427A": ["Irregular (Irr)"],
}

GALAXY_NOTES = {
    "M87": "A giant elliptical in the Virgo Cluster. It hosts the black hole imaged by the Event Horizon Telescope!",
    "NGC4473": "An elliptical in Virgo, clearly squashed compared with M87.",
    "NGC3115": "The 'Spindle Galaxy'. Its thin disc seen edge-on gives it away as a lenticular, not an E7 elliptical.",
    "M104": "The Sombrero. Astronomers still argue about whether it's a lenticular or an Sa spiral: both count!",
    "M74": "A textbook 'grand design' spiral with no bar.",
    "NGC1300": "A classic barred spiral: the arms start from the ends of a bright bar.",
    "NGC1427A": "An irregular galaxy being torn apart as it falls through the Fornax Cluster.",
}


def galaxy_classifier(images):
    """Interactive widget: classify each galaxy in the gallery on the tuning fork."""
    import ipywidgets as widgets

    choices = ["(choose)", "Elliptical (E)", "Lenticular (S0)", "Spiral (S)",
               "Barred spiral (SB)", "Irregular (Irr)"]

    shown = {"galaxy": None}

    def show(galaxy, my_class):
        # A new galaxy always starts with a blank answer
        if galaxy != shown["galaxy"]:
            shown["galaxy"] = galaxy
            if my_class != "(choose)":
                class_menu.value = "(choose)"     # redraws with the menu cleared
                return
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.imshow(images[galaxy])
        ax.set_title(galaxy)
        ax.axis("off")
        plt.show()
        if my_class == "(choose)":
            print("👉 Choose a class from the menu.")
        elif my_class in GALAXY_TYPES[galaxy]:
            print(f"✅ Correct! {GALAXY_NOTES[galaxy]}")
        else:
            print("❌ Not quite. 💡 Look for a disc, spiral arms, a bar, or a smooth oval shape.")

    galaxy_menu = widgets.Dropdown(options=list(images), description="Galaxy:")
    class_menu = widgets.Dropdown(options=choices, description="Your class:",
                                  style={"description_width": "initial"})

    # Also clear the answer as soon as a new galaxy is picked. Together with the
    # check at the top of show(), the old answer is never marked against the
    # new galaxy, whatever order the widget events arrive in.
    def reset_class(change):
        class_menu.value = "(choose)"

    galaxy_menu.observe(reset_class, names="value")

    widgets.interact(show, galaxy=galaxy_menu, my_class=class_menu)


def ellipse_fitter(image, name):
    """Interactive widget: fit an ellipse to a galaxy and work out its E class."""
    import ipywidgets as widgets
    from matplotlib.patches import Ellipse

    ny, nx = image.shape[:2]

    def show(size, axis_ratio, angle):
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.imshow(image)
        ax.add_patch(Ellipse((nx / 2, ny / 2), width=2 * size, height=2 * size * axis_ratio,
                             angle=angle, fill=False, color="cyan", lw=2))
        ax.set_title(name)
        ax.axis("off")
        plt.show()
        e = 10 * (1 - axis_ratio)
        print(f"b/a = {axis_ratio:.2f}   →   E = 10 (1 - b/a) = {e:.1f}   →   class E{int(e + 0.5)}")

    widgets.interact(
        show,
        size=widgets.IntSlider(value=80, min=20, max=190, step=2, description="Size a (px):",
                               style={"description_width": "initial"}, continuous_update=False),
        axis_ratio=widgets.FloatSlider(value=1.0, min=0.3, max=1.0, step=0.01,
                                       description="Axis ratio b/a:",
                                       style={"description_width": "initial"},
                                       continuous_update=False),
        angle=widgets.IntSlider(value=0, min=0, max=180, step=2, description="Angle (°):",
                                style={"description_width": "initial"}, continuous_update=False),
    )


def line_explorer(wavelength, flux, rest_lines, title, zmax=0.5, xlabel="Observed wavelength (Å)"):
    """
    Interactive widget: slide the redshift until the dashed lines (rest
    wavelengths x (1 + z)) sit on the emission lines in a spectrum.
    """
    import ipywidgets as widgets

    wavelength = np.asarray(wavelength)
    flux = np.asarray(flux)

    def show(z):
        fig, ax = plt.subplots(figsize=(11, 5))
        ax.plot(wavelength, flux, color="k", lw=1)
        top = np.nanmax(flux) * 1.1
        for name, rest in rest_lines.items():
            observed = rest * (1 + z)
            if wavelength.min() <= observed <= wavelength.max():
                ax.axvline(observed, color=COLOURS["red"], ls="--", lw=1)
                ax.text(observed, top * 0.98, f" {name}", color=COLOURS["red"],
                        rotation=90, va="top", fontsize=10)
        ax.set_ylim(0, top)
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Brightness (scaled)")
        ax.set_title(f"{title}   |   trying z = {z:.3f}")
        plt.show()

    widgets.interact(
        show,
        z=widgets.FloatSlider(value=0.0, min=0.0, max=zmax, step=0.001, readout_format=".3f",
                              description="Redshift z:", continuous_update=False),
    )


def line_width_explorer(spectra, line=6563.0):
    """
    Interactive widget: match a Gaussian to the H-alpha line of a Seyfert and
    read off how fast the gas is moving.
    """
    import ipywidgets as widgets

    def show(galaxy, speed):
        s = spectra[(spectra["object"] == galaxy) & (spectra["wavelength_A"] > 6250)
                    & (spectra["wavelength_A"] < 6900)]
        w, f = s["wavelength_A"].values, s["flux"].values
        continuum = np.median(np.r_[f[:15], f[-15:]])
        centre = w[np.argmax(f)]
        fwhm = centre * speed / 299792.458              # Doppler: Δλ/λ = v/c
        sigma = fwhm / 2.355
        model = continuum + (f.max() - continuum) * np.exp(-0.5 * ((w - centre) / sigma) ** 2)
        fig, ax = plt.subplots(figsize=(10, 4.5))
        ax.plot(w, f, color="k", lw=1, label=galaxy)
        ax.plot(w, model, color=COLOURS["orange"], lw=2, label="Gas moving at ± your speed")
        ax.set_xlabel("Wavelength (Å)")
        ax.set_ylabel("Brightness (scaled)")
        ax.set_title("The H-alpha line, zoomed in")
        ax.legend()
        plt.show()
        print(f"Line width (FWHM): {fwhm:.0f} Å   →   gas speed ≈ {speed:,} km/s")

    widgets.interact(
        show,
        galaxy=widgets.ToggleButtons(options=["NGC 4151 (Seyfert 1)", "NGC 1068 (Seyfert 2)"],
                                     description="Galaxy:"),
        speed=widgets.IntSlider(value=2000, min=100, max=10000, step=50,
                                description="Gas speed (km/s):",
                                style={"description_width": "initial"},
                                continuous_update=False),
    )


def is_quiescent(u_minus_v, v_minus_j):
    """True for galaxies inside the UVJ 'quiescent' box (Williams et al. 2009 style)."""
    return (u_minus_v > 1.3) & (v_minus_j < 1.6) & (u_minus_v > 0.88 * v_minus_j + 0.69)


def draw_uvj_box(ax):
    """Draw the quiescent box on a UVJ diagram."""
    ax.plot([-0.5, (1.3 - 0.69) / 0.88, 1.6, 1.6], [1.3, 1.3, 0.88 * 1.6 + 0.69, 2.6],
            color="k", lw=2)
    ax.text(0.0, 2.2, "Quiescent\n('red and dead')", fontsize=11)
    ax.text(1.75, 0.5, "Star-forming", fontsize=11, ha="right")


def uvj_explorer(galaxies):
    """Interactive widget: the UVJ diagram in different slices of cosmic time."""
    import ipywidgets as widgets

    good = galaxies.dropna(subset=["U_minus_V", "V_minus_J"])
    good = good[good["log_mass"] > 9.5]

    def show(redshift_range):
        lo, hi = redshift_range
        d = good[(good["z"] > lo) & (good["z"] < hi)]
        quiet = is_quiescent(d["U_minus_V"], d["V_minus_J"])
        age_hi = age_of_universe(lo).to("Gyr").value
        age_lo = age_of_universe(hi).to("Gyr").value
        fig, ax = plt.subplots(figsize=(7, 6))
        ax.scatter(d["V_minus_J"][~quiet], d["U_minus_V"][~quiet], s=6, alpha=0.5,
                   color=COLOURS["blue"])
        ax.scatter(d["V_minus_J"][quiet], d["U_minus_V"][quiet], s=6, alpha=0.6,
                   color=COLOURS["red"])
        draw_uvj_box(ax)
        ax.set_xlim(-0.5, 2.5)
        ax.set_ylim(-0.2, 2.6)
        ax.set_xlabel("V − J colour (rest frame)")
        ax.set_ylabel("U − V colour (rest frame)")
        ax.set_title(f"{lo:.1f} < z < {hi:.1f}  (Universe {age_lo:.1f} to {age_hi:.1f} billion years old)")
        plt.show()
        print(f"Galaxies: {len(d)}   |   quiescent: {quiet.sum()} ({quiet.mean():.0%})")

    widgets.interact(
        show,
        redshift_range=widgets.FloatRangeSlider(value=[2.0, 2.5], min=0.5, max=2.5, step=0.5,
                                                description="Redshift:",
                                                continuous_update=False),
    )


# ===========================================================================
# AstroLab C10: Gravity's Fingerprints
# ===========================================================================

def deflection_explorer():
    """Interactive widget: how much does the Sun bend starlight passing at distance b?"""
    import ipywidgets as widgets

    rad_to_arcsec = 206265.0
    alpha_limb = 4 * 6.674e-11 * 1.989e30 / (2.998e8 ** 2 * 6.957e8) * rad_to_arcsec

    def show(b, newton):
        b_all = np.linspace(1, 20, 300)
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.plot(b_all, alpha_limb / b_all, color=COLOURS["blue"], lw=2, label="Einstein (general relativity)")
        if newton:
            ax.plot(b_all, alpha_limb / 2 / b_all, color=COLOURS["grey"], lw=2, ls="--",
                    label="Newton (half as much)")
        ax.errorbar([1.0], [1.98], yerr=[0.16], fmt="s", color=COLOURS["red"], ms=8,
                    label="Eddington's expedition, 1919 (Sobral)")
        ax.plot(b, alpha_limb / b, "o", color=COLOURS["orange"], ms=12)
        ax.set_xlabel("Closest approach b (in solar radii)")
        ax.set_ylabel("Deflection (arcseconds)")
        ax.set_ylim(0, 2.5)
        ax.legend()
        plt.show()
        print(f"A star seen {b:.1f} solar radii from the Sun's centre is shifted by {alpha_limb / b:.2f}″")

    widgets.interact(
        show,
        b=widgets.FloatSlider(value=1.0, min=1.0, max=20.0, step=0.5,
                              description="b (solar radii):",
                              style={"description_width": "initial"}, continuous_update=False),
        newton=widgets.Checkbox(value=False, description="Show Newton's prediction"),
    )


def halo_speed(radius_kpc, v_inf, core_kpc):
    """Rotation speed from a dark matter halo (a 'pseudo-isothermal' sphere)."""
    r = np.asarray(radius_kpc, dtype=float)
    return v_inf * np.sqrt(1 - core_kpc / r * np.arctan(r / core_kpc))


def rotation_curve_fitter(data):
    """Interactive widget: add a dark matter halo to NGC 2403 until the model fits the data."""
    import ipywidgets as widgets

    r = data["radius_kpc"].values
    v_visible = np.sqrt(data["v_gas"] ** 2 + data["v_stars"] ** 2).values

    def show(v_inf, core):
        v_halo = halo_speed(r, v_inf, core)
        v_total = np.sqrt(v_visible ** 2 + v_halo ** 2)
        mismatch = np.sqrt(np.mean(((data["v_obs"] - v_total) / data["v_err"]) ** 2))
        dark_fraction = v_halo[-1] ** 2 / v_total[-1] ** 2
        fig, ax = plt.subplots(figsize=(10, 5.5))
        ax.errorbar(r, data["v_obs"], yerr=data["v_err"], fmt="o", ms=4, color="k", label="NGC 2403 (measured)")
        ax.plot(r, data["v_stars"], color=COLOURS["orange"], ls=":", label="Stars")
        ax.plot(r, data["v_gas"], color=COLOURS["teal"], ls=":", label="Gas")
        ax.plot(r, v_visible, color=COLOURS["blue"], lw=2, label="All visible matter")
        ax.plot(r, v_halo, color=COLOURS["grey"], ls="--", label="Dark matter halo")
        ax.plot(r, v_total, color=COLOURS["red"], lw=2.5, label="Visible + dark matter")
        ax.set_xlabel("Distance from the centre (kpc)")
        ax.set_ylabel("Rotation speed (km/s)")
        ax.set_ylim(0, 180)
        ax.legend(loc="lower right", fontsize=9)
        plt.show()
        print(f"Typical mismatch: {mismatch:.1f} error bars (smaller is better; the best possible here is about 3.7)")
        print(f"Dark matter share of the mass inside {r[-1]:.0f} kpc: {dark_fraction:.0%}")

    widgets.interact(
        show,
        v_inf=widgets.IntSlider(value=0, min=0, max=250, step=2, description="Halo speed (km/s):",
                                style={"description_width": "initial"}, continuous_update=False),
        core=widgets.FloatSlider(value=3.0, min=0.5, max=10.0, step=0.1, description="Halo core (kpc):",
                                 style={"description_width": "initial"}, continuous_update=False),
    )


def whiten(strain, fs):
    """
    'Whiten' detector data: divide out the detector's noise at each frequency,
    so no frequency drowns out the others.
    """
    from scipy import signal
    freqs, psd = signal.welch(strain, fs, nperseg=4 * fs)
    window = signal.windows.tukey(len(strain), 0.1)
    spectrum = np.fft.rfft(strain * window)
    f = np.fft.rfftfreq(len(strain), 1 / fs)
    asd = np.sqrt(np.interp(f, freqs, psd))
    return np.fft.irfft(spectrum / asd, n=len(strain))


def bandpass(strain, fs, low=35, high=350):
    """Keep only frequencies between low and high (in Hz)."""
    from scipy import signal
    b, a = signal.butter(4, [low, high], btype="band", fs=fs)
    return signal.filtfilt(b, a, strain)


def gw_cleaner(time, raw, whitened, cleaned):
    """Interactive widget: step through the cleaning of the LIGO Hanford data."""
    import ipywidgets as widgets

    steps = {"1. Raw data": (raw, "Strain"),
             "2. Whitened": (whitened, "Whitened strain"),
             "3. Whitened + band-pass": (cleaned, "Whitened strain")}

    def show(step, window):
        y, label = steps[step]
        m = (time > -window) & (time < 0.05)
        fig, ax = plt.subplots(figsize=(11, 4.5))
        ax.plot(time[m], y[m], color=COLOURS["blue"], lw=1)
        ax.set_xlabel("Time from 14 September 2015, 09:50:45.4 UTC (seconds)")
        ax.set_ylabel(label)
        ax.set_title(f"LIGO Hanford: {step}")
        plt.show()

    widgets.interact(
        show,
        step=widgets.ToggleButtons(options=list(steps), description="Step:"),
        window=widgets.FloatSlider(value=0.25, min=0.1, max=2.0, step=0.05,
                                   description="Seconds shown:",
                                   style={"description_width": "initial"}, continuous_update=False),
    )


def time_delay_explorer(time, hanford, livingston):
    """Interactive widget: shift and flip Livingston's signal to match Hanford's."""
    import ipywidgets as widgets

    fs = 1 / (time[1] - time[0])
    m = (time > -0.15) & (time < 0.03)

    def show(shift_ms, flip):
        shifted = np.roll(livingston, int(round(shift_ms / 1000 * fs))) * (-1 if flip else 1)
        match = np.corrcoef(hanford[m], shifted[m])[0, 1]
        fig, ax = plt.subplots(figsize=(11, 4.5))
        ax.plot(time[m], hanford[m], color=COLOURS["blue"], lw=1.5, label="Hanford")
        ax.plot(time[m], shifted[m], color=COLOURS["orange"], lw=1.5, alpha=0.8,
                label=f"Livingston, shifted {shift_ms:+.1f} ms" + (" and flipped" if flip else ""))
        ax.set_xlabel("Time (seconds)")
        ax.set_ylabel("Whitened strain")
        ax.legend(loc="upper left")
        plt.show()
        print(f"Match between the detectors: {match:+.2f} (1.00 would be a perfect match)")

    widgets.interact(
        show,
        shift_ms=widgets.FloatSlider(value=0.0, min=-15, max=15, step=0.25, description="Shift (ms):",
                                     continuous_update=False),
        flip=widgets.Checkbox(value=False, description="Flip Livingston upside down"),
    )


def chirp_frequency(time_to_merger, chirp_mass):
    """Gravitational wave frequency (Hz) a time (s) before merger, for a chirp mass in solar masses."""
    tau = np.asarray(time_to_merger, dtype=float)
    tm = 4.925e-6 * chirp_mass               # G M_chirp / c^3 in seconds
    return (1 / np.pi) * (5 / (256 * tau)) ** (3 / 8) * tm ** (-5 / 8)


def chirp_mass_fitter(time, cleaned, merger_time=0.028):
    """Interactive widget: match a chirp to the spectrogram of GW150914 to weigh the black holes."""
    import ipywidgets as widgets
    from scipy import signal

    fs = 1 / (time[1] - time[0])
    m = (time > -1.0) & (time < 0.5)
    f, t, power = signal.spectrogram(cleaned[m], fs, nperseg=128, noverlap=124, nfft=1024)
    t = t + time[m][0]

    def show(chirp_mass):
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.pcolormesh(t, f, power, shading="auto", cmap="viridis")
        tau = np.linspace(0.5, 0.002, 400)
        ax.plot(merger_time - tau, chirp_frequency(tau, chirp_mass), color="w", lw=2, ls="--")
        ax.set_ylim(20, 400)
        ax.set_xlim(-0.3, 0.05)
        ax.set_xlabel("Time (seconds)")
        ax.set_ylabel("Frequency (Hz)")
        ax.set_title(f"GW150914 spectrogram with a chirp for {chirp_mass:.0f} M☉")
        plt.show()

    widgets.interact(
        show,
        chirp_mass=widgets.IntSlider(value=10, min=1, max=80, step=1, description="Chirp mass (M☉):",
                                     style={"description_width": "initial"}, continuous_update=False),
    )


def chirp_sound(chirp_mass, duration=2.0, fs=4096, start_hz=30):
    """
    Make a simple chirp waveform for a given chirp mass, starting at start_hz
    and ending at merger. Returns (time, waveform) at sample rate fs.
    """
    # time before merger when the frequency is start_hz
    tm = 4.925e-6 * chirp_mass
    tau0 = 5 / 256 * (np.pi * start_hz) ** (-8 / 3) * tm ** (-5 / 3)
    tau0 = min(tau0, duration)
    t = np.arange(0, tau0, 1 / fs)
    tau = np.maximum(tau0 - t, 1e-4)
    f = chirp_frequency(tau, chirp_mass)
    phase = 2 * np.pi * np.cumsum(f) / fs
    wave = (f / f.max()) ** (2 / 3) * np.cos(phase)
    return t - tau0, wave


# ===========================================================================
# AstroLab C11: Surveying the Universe
# ===========================================================================

def cosmology_explorer(supernovae, h0=73.0):
    """
    Interactive widget: choose the amounts of matter and dark energy and compare
    the predicted brightness of supernovae with the Pantheon+ data. Distances
    are shown relative to an empty Universe (no matter, no dark energy).
    """
    import ipywidgets as widgets
    from astropy.cosmology import LambdaCDM

    sn = supernovae[supernovae["z"] > 0.01].sort_values("z")
    empty = LambdaCDM(H0=h0, Om0=0.0, Ode0=0.0)
    z = sn["z"].values
    residual = sn["distance_modulus"].values - empty.distmod(z).value

    # Average the supernovae in redshift bins so the trend is easy to see
    edges = np.logspace(np.log10(0.01), np.log10(2.3), 16)
    centres, means, errors = [], [], []
    for lo, hi in zip(edges[:-1], edges[1:]):
        inside = (z >= lo) & (z < hi)
        if inside.sum() >= 3:
            w = 1 / sn["error"].values[inside] ** 2
            centres.append(np.sqrt(lo * hi))
            means.append(np.sum(w * residual[inside]) / np.sum(w))
            errors.append(1 / np.sqrt(np.sum(w)))

    z_model = np.logspace(-2, np.log10(2.3), 200)

    def show(omega_matter, omega_lambda):
        model = LambdaCDM(H0=h0, Om0=omega_matter, Ode0=omega_lambda)
        curve = model.distmod(z_model).value - empty.distmod(z_model).value
        predicted = model.distmod(z).value
        mismatch = np.sqrt(np.mean(((sn["distance_modulus"].values - predicted) / sn["error"].values) ** 2))
        total = omega_matter + omega_lambda
        q0 = omega_matter / 2 - omega_lambda
        fig, ax = plt.subplots(figsize=(10, 5.5))
        ax.scatter(z, residual, s=4, alpha=0.2, color=COLOURS["grey"], label="Individual supernovae")
        ax.errorbar(centres, means, yerr=errors, fmt="o", color="k", label="Averages")
        ax.plot(z_model, curve, color=COLOURS["red"], lw=2.5,
                label=f"Ω_M = {omega_matter:.2f}, Ω_Λ = {omega_lambda:.2f}")
        ax.axhline(0, color=COLOURS["blue"], ls="--", lw=1, label="Empty Universe")
        ax.set_xscale("log")
        ax.set_ylim(-1.0, 0.8)
        ax.set_xlabel("Redshift z")
        ax.set_ylabel("Magnitudes compared with an empty Universe")
        ax.text(0.99, 0.97, "↑ fainter (further away)", transform=ax.transAxes, ha="right", va="top", fontsize=10)
        ax.text(0.99, 0.03, "↓ brighter (closer)", transform=ax.transAxes, ha="right", va="bottom", fontsize=10)
        ax.legend(loc="lower left", fontsize=9)
        plt.show()
        geometry = "flat" if abs(total - 1) < 0.05 else ("closed" if total > 1 else "open")
        print(f"Typical mismatch: {mismatch:.2f} error bars (smaller is better)")
        print(f"Ω_total = {total:.2f}  →  a {geometry} Universe")
        print(f"Expansion today is {'accelerating' if q0 < 0 else 'slowing down'}")

    widgets.interact(
        show,
        omega_matter=widgets.FloatSlider(value=1.0, min=0.0, max=1.5, step=0.05, description="Ω_M (matter):",
                                         style={"description_width": "initial"}, continuous_update=False),
        omega_lambda=widgets.FloatSlider(value=0.0, min=0.0, max=1.5, step=0.05, description="Ω_Λ (dark energy):",
                                         style={"description_width": "initial"}, continuous_update=False),
    )


def bpt_lines(log_nii_ha, redshift=0.0):
    """
    The Kewley et al. (2013) dividing line between star formation and AGN on the
    BPT diagram, which moves with redshift (redshift = 0 gives Kewley et al. 2001).
    """
    x = np.asarray(log_nii_ha, dtype=float)
    shift = 0.02 + 0.1833 * redshift if redshift > 0 else 0.47
    top = 1.2 + 0.03 * redshift if redshift > 0 else 1.19
    with np.errstate(divide="ignore"):
        y = 0.61 / (x - shift) + top
    return np.where(x < shift, y, np.nan)
