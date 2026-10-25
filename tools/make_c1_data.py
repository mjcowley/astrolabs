"""
Make the data files used in AstroLab C1.

Part 1: JWST cutouts of the Cosmic Cliffs.

The full NIRCam mosaics of NGC 3324 (JWST program 2731) are about 5 GB each on
MAST and need well over 1 GB of memory to open together. This script cuts out
the same patch of sky from each filter at full resolution and saves it with
FITS tile compression (.fits.fz), which SAOImageDS9 opens directly.

Only the rows of the mosaic that are needed are downloaded (using HTTP range
requests), so you don't need to download the full files.

Part 2: Spitzer and Herschel images of NGC 7293, cut out from the Spitzer
Enhanced Imaging Products and the Herschel High Level Images on IRSA, so that
all three cover the same patch of sky.

Usage (from the repository root):

    pip install astropy fsspec aiohttp
    python tools/make_c1_data.py
"""

import os
import tempfile
import urllib.request

import numpy as np
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.nddata import Cutout2D
from astropy.wcs import WCS

MAST = "https://mast.stsci.edu/api/v0.1/Download/file?uri=mast:JWST/product/"
FILTERS = ["f090w", "f200w", "f444w"]
OUT = os.path.join("data", "C1")

# Part 1: the ridge, the "steam" above it and the pillars below
CENTRE = SkyCoord(159.2107, -58.6222, unit="deg")
WIDTH = 264 * u.arcsec
HEIGHT = 157 * u.arcsec

# Part 2: the whole of NGC 7293, including its faint outer halo
IRSA = "https://irsa.ipac.caltech.edu/data/"
SEIP = IRSA + "SPITZER/Enhanced/SEIP/images/4/0045/40045030/0/40045030-0/40045030.40045030-0."
HELIX_IMAGES = {
    "ngc7293_spitzer_irac_3.6micron": (SEIP + "IRAC.1.mosaic.fits", 0),
    "ngc7293_spitzer_mips_24micron": (SEIP + "MIPS.1.mosaic.fits", 0),
    "ngc7293_herschel_spire_250micron":
        (IRSA + "Herschel/HHLI/images/22m/SpirePhoto/2229m2050_1342256744_SpirePhoto_L20_PMP250_SPG14.0.fits", 1),
}
HELIX_CENTRE = SkyCoord("22h29m38.55s", "-20d50m13.6s")
HELIX_SIZE = 26 * u.arcmin


def save(data, header, name):
    hdu = fits.CompImageHDU(data.astype("float32"), header=header, compression_type="RICE_1",
                            quantize_level=16, quantize_method=2)
    path = os.path.join(OUT, f"{name}.fits.fz")
    fits.HDUList([fits.PrimaryHDU(), hdu]).writeto(path, overwrite=True)
    print(f"{path}: {data.shape[1]} x {data.shape[0]} pixels, {os.path.getsize(path) / 1e6:.1f} MB")


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

    save(data, new_header, f"carina_jwst_{name}")


def helix_cutout(name, url, extension):
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "image.fits")
        urllib.request.urlretrieve(url, path)
        with fits.open(path) as hdul:
            header = hdul[extension].header
            wcs = WCS(header).celestial
            box = Cutout2D(hdul[extension].data, HELIX_CENTRE, HELIX_SIZE, wcs=wcs,
                           mode="partial", fill_value=np.nan)
            primary = hdul[0].header

    new_header = box.wcs.to_header()
    for key in ["TELESCOP", "INSTRUME", "BUNIT", "OBJECT", "WAVELEN"]:
        for source in (header, primary):
            if key in source:
                new_header[key] = source[key]
                break
    new_header["ORIGIN"] = "IRSA, cut out for QUT AstroLab C1"
    save(box.data, new_header, name)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name in FILTERS:
        cutout(name)
    for name, (url, extension) in HELIX_IMAGES.items():
        helix_cutout(name, url, extension)
