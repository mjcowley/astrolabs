"""
Make the Gaia data files used in AstroLab C4.

The input is the result of this query on the Gaia Archive (gaiadr3.gaia_source),
run in TOPCAT's TAP window with Max Rows raised to 2000000 (306,517 stars):

    SELECT source_id, ra, dec, parallax, pmra, pmdec,
           phot_g_mean_mag, bp_rp, ruwe, phot_bp_rp_excess_factor
    FROM gaiadr3.gaia_source
    WHERE parallax > 10
      AND parallax_over_error > 10
      AND phot_bp_mean_flux_over_error > 10
      AND phot_rp_mean_flux_over_error > 10

That's every star within 100 parsecs with good parallaxes and colours. This
script saves it, plus two smaller files cut from it:

* gaia_dr3_50pc.fits: stars within 50 pc (parallax > 20), the same selection
  students run themselves in Part 1, as a fallback if the archive is busy
* gaia_dr3_taurus.fits: the patch of sky around the Hyades cluster used in Part 2

Usage (from the repository root):

    python tools/make_c4_data.py path/to/gaia_dr3_query.fits
"""

import os
import sys

from astropy.table import Table

OUT = os.path.join("data", "C4")


def save(table, name):
    path = os.path.join(OUT, name)
    table.write(path, overwrite=True)
    print(f"{path}: {len(table)} stars, {os.path.getsize(path) / 1e6:.1f} MB")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    stars = Table.read(sys.argv[1])
    save(stars, "gaia_dr3_100pc.fits")
    save(stars[stars["parallax"] > 20], "gaia_dr3_50pc.fits")
    taurus = (stars["ra"] > 50) & (stars["ra"] < 85) & (stars["dec"] > 0) & (stars["dec"] < 30)
    save(stars[taurus], "gaia_dr3_taurus.fits")
