"""
Make the JWST cutouts of the Cosmic Cliffs used in AstroLab C1, Part 1.

The full NIRCam mosaics of NGC 3324 (JWST program 2731) are about 5 GB each on
MAST and need well over 1 GB of memory to open together. This script cuts out
the same patch of sky from each filter at full resolution and saves it with
FITS tile compression (.fits.fz), which SAOImageDS9 opens directly.

Only the rows of the mosaic that are needed are downloaded (using HTTP range
requests), so you don't need to download the full files.

Usage (from the repository root):

    pip install astropy fsspec aiohttp
    python tools/make_c1_cutouts.py
"""

import os

import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.wcs import WCS

MAST = "https://mast.stsci.edu/api/v0.1/Download/file?uri=mast:JWST/product/"
FILTERS = ["f090w", "f200w", "f444w"]
OUT = os.path.join("data", "C1")

# The patch of sky to keep: the ridge, the "steam" above it and the pillars below
CENTRE = SkyCoord(159.2107, -58.6222, unit="deg")
WIDTH = 264 * u.arcsec
HEIGHT = 157 * u.arcsec


def cutout(name):
    url = f"{MAST}jw02731-o001_t017_nircam_clear-{name}_i2d.fits"
    with fits.open(url, use_fsspec=True, fsspec_kwargs={"client_kwargs": {"trust_env": True}}) as hdul:
        header = hdul["SCI"].header
        primary = hdul[0].header
        wcs = WCS(header)
        # Work out the rows and columns needed, then download only those
        x, y = wcs.world_to_pixel(CENTRE)
        scale = wcs.proj_plane_pixel_scales()[0].to(u.arcsec)
        half_x, half_y = int(WIDTH / scale / 2), int(HEIGHT / scale / 2)
        x0, y0 = int(round(float(x))) - half_x, int(round(float(y))) - half_y
        x1, y1 = x0 + 2 * half_x, y0 + 2 * half_y
        data = hdul["SCI"].section[y0:y1, x0:x1]

    keep = ["TELESCOP", "INSTRUME", "FILTER", "PUPIL", "TARGPROP", "DATE-OBS", "BUNIT", "PIXAR_SR", "PIXAR_A2"]
    new_header = wcs[y0:y1, x0:x1].to_header()
    for key in keep:
        for source in (header, primary):
            if key in source:
                new_header[key] = source[key]
                break
    new_header["ORIGIN"] = "MAST, JWST program 2731 (NGC 3324), cut out for QUT AstroLab C1"

    hdu = fits.CompImageHDU(data.astype("float32"), header=new_header, compression_type="RICE_1",
                            quantize_level=16, quantize_method=2)
    path = os.path.join(OUT, f"carina_jwst_{name}.fits.fz")
    fits.HDUList([fits.PrimaryHDU(), hdu]).writeto(path, overwrite=True)
    print(f"{path}: {data.shape[1]} x {data.shape[0]} pixels, {os.path.getsize(path) / 1e6:.0f} MB")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name in FILTERS:
        cutout(name)
