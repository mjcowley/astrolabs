# AstroLab C1: Composing RGB Images from Telescope Data

Turn three images taken at different wavelengths into one colour picture.

| Time | Software | Activities | Submit |
| :-: | :-: | :-: | :-: |
| About 2 hours | SAOImageDS9 | RGB creation | The C1 proforma on Canvas |

**Start here:** download the [AstroLab C1 proforma](https://github.com/mjcowley/astrolabs/raw/main/C1/AstroLabC1_Proforma.docx) and fill it in as you go. When you've finished both parts, submit it on Canvas as a Word document or PDF by the due date.

**Contents:** [Overview](#overview) · [How to complete this AstroLab](#how-to-complete-this-astrolab) · [Software and data](#software-and-data) · [Part 1: The Carina Nebula](#part-1-the-carina-nebula) · [Part 2: Choose your own object](#part-2-choose-your-own-object) · [Troubleshooting](#troubleshooting) · [Optional extension](#optional-extension)

## Overview

In this AstroLab you'll compose Red-Green-Blue (**RGB**) composite images from astronomical data. In Part 1, you'll build an image of part of the Carina [Nebula](http://astro.vaporia.com/start/nebula.html) using data taken through three [bands](http://astro.vaporia.com/start/spectralband.html) (filters) on the James Webb Space Telescope's ([JWST](https://www.jwst.nasa.gov/index.html)) Near-Infrared Camera ([NIRCam](https://www.jwst.nasa.gov/content/observatory/instruments/nircam.html)). In Part 2, you'll choose one of five objects observed at very different wavelengths and work out the colours yourself.

Astronomical [camera sensors](http://astro.vaporia.com/start/ccd.html) record how much light lands on each pixel, but not its colour. A colour sensor puts a grid of red, green and blue filters over its pixels, so each pixel throws away about two-thirds of the light, which sacrifices too much [sensitivity](http://astro.vaporia.com/start/sensitivityfunction.html). Astronomers also want to choose their own bands, including infrared bands our eyes can't see. Instead, we take separate images through different filters and combine them into an RGB image.

The Cosmic Cliffs are a gaseous cavity within [NGC 3324](https://en.wikipedia.org/wiki/NGC_3324), part of the Carina Nebula. The tallest "peaks" of gas and dust are about 7 light-years high (about 70 trillion km). The cavity has been carved away by intense ultraviolet radiation and stellar winds from extremely massive, hot, young stars, and the pillars that tower above the glowing wall of gas resist this radiation. The blue "steam" that appears to rise from the celestial "mountains" is hot, ionised gas and dust streaming away from the nebula due to the relentless radiation.

JWST lets us observe emerging stellar nurseries and individual stars that are completely hidden in visible-light pictures. Because JWST is sensitive to infrared light, we can peer through cosmic dust to see the once-hidden process of star formation in action.

**By the end of this AstroLab you'll be able to:**

* open and display FITS images in SAOImageDS9
* adjust an image's contrast so faint detail shows up
* read a filter throughput plot
* combine three images into an RGB composite and explain your colour choices
* find out what different wavebands reveal about an object, and compare your image with others

## How to complete this AstroLab

You can complete C1 on campus in your scheduled session, or remotely in your own time. The steps are the same either way, and everyone submits the same proforma.

**On campus**

* Come to your scheduled AstroLab session. SAOImageDS9 is already installed on the lab computers.
* The teaching team will run a live demonstration and help you as you go.

**Remote**

* Watch the walkthrough video on the C1 Canvas page. It covers everything from the live session.
* Install SAOImageDS9 on your own computer, or use QUT's Virtual Desktop Infrastructure (see [Software and data](#software-and-data)).
* Work through [Before you start](#before-you-start) first, so setup problems don't hold you up.
* If you get stuck, contact the teaching team.

## Software and data

This AstroLab uses SAOImageDS9, a free and open-source application for exploring astronomical images. It's pre-installed on QUT's lab computers. To use your own computer, download the version for your system from the [SAOImageDS9 download page](https://sites.google.com/cfa.harvard.edu/saoimageds9/download).

Installing on a Mac? See the macOS install help on Canvas. If you'd rather not install anything, you can use SAOImageDS9 through [QUT's Virtual Desktop Infrastructure](https://gist.github.com/mjcowley/fe60fae650deedb8ea3b4d21cf274365). For help with the software, see the [SAOImageDS9 interface guide](https://ds9.si.edu/doc/user/gui/index.html) and the [SAOImageDS9 Reference Manual](https://ds9.si.edu/doc/ref/).

Click any file name below to download it.

The small NGC 3031 test file is handy for checking your installation works: [NGC_3031_I_MIPS24_bgm2012.fits](https://github.com/mjcowley/astrolabs/raw/main/data/C1/part2/NGC_3031_I_MIPS24_bgm2012.fits)

### Part 1 data

For Part 1 you'll need the three JWST images below. They're cut out from the full NIRCam mosaics in the Space Telescope Science Institute's ([STScI](https://www.stsci.edu/home)) Mikulski Archive for Space Telescopes ([MAST](https://archive.stsci.edu/)), keeping JWST's full resolution. They're compressed FITS files (`.fits.fz`), which SAOImageDS9 opens just like ordinary FITS files.

| File | Filter | Size |
| --- | --- | --- |
| [carina_jwst_f090w.fits.fz](https://github.com/mjcowley/astrolabs/raw/main/data/C1/carina_jwst_f090w.fits.fz) | F090W | 36 MB |
| [carina_jwst_f200w.fits.fz](https://github.com/mjcowley/astrolabs/raw/main/data/C1/carina_jwst_f200w.fits.fz) | F200W | 37 MB |
| [carina_jwst_f444w.fits.fz](https://github.com/mjcowley/astrolabs/raw/main/data/C1/carina_jwst_f444w.fits.fz) | F444W | 10 MB |

### Part 2 data

For Part 2, choose one object and download its three files. They're small, so this is quick.

| Object | Type | Files |
| --- | --- | --- |
| **M16** (Eagle Nebula) | Star-forming region | [m16_herschel70micron.fits](https://github.com/mjcowley/astrolabs/raw/main/data/C1/part2/m16_herschel70micron.fits)<br>[m16_herschel160micron.fits](https://github.com/mjcowley/astrolabs/raw/main/data/C1/part2/m16_herschel160micron.fits)<br>[m16_herschel250micron.fits](https://github.com/mjcowley/astrolabs/raw/main/data/C1/part2/m16_herschel250micron.fits) |
| **NGC 7293** (Helix Nebula) | Planetary nebula | [ngc7293_spitzer3.6micron.fits](https://github.com/mjcowley/astrolabs/raw/main/data/C1/part2/ngc7293_spitzer3.6micron.fits)<br>[ngc7293_spitzer24micron.fits](https://github.com/mjcowley/astrolabs/raw/main/data/C1/part2/ngc7293_spitzer24micron.fits)<br>[ngc7293_herschel250micron.fits](https://github.com/mjcowley/astrolabs/raw/main/data/C1/part2/ngc7293_herschel250micron.fits) |
| **M51** (Whirlpool Galaxy) | Interacting galaxies | [ngc5194_galex2267a.fits](https://github.com/mjcowley/astrolabs/raw/main/data/C1/part2/ngc5194_galex2267a.fits)<br>[ngc5194_spitzer3.6micron.fits](https://github.com/mjcowley/astrolabs/raw/main/data/C1/part2/ngc5194_spitzer3.6micron.fits)<br>[NGC_5194_I_MIPS24_bgm2012.fits](https://github.com/mjcowley/astrolabs/raw/main/data/C1/part2/NGC_5194_I_MIPS24_bgm2012.fits) |
| **M81** (Bode's Galaxy) | Spiral galaxy | [ngc3031_spitzer3.6micron.fits](https://github.com/mjcowley/astrolabs/raw/main/data/C1/part2/ngc3031_spitzer3.6micron.fits)<br>[NGC_3031_I_MIPS24_bgm2012.fits](https://github.com/mjcowley/astrolabs/raw/main/data/C1/part2/NGC_3031_I_MIPS24_bgm2012.fits)<br>[ngc3031_herschel250micron.fits](https://github.com/mjcowley/astrolabs/raw/main/data/C1/part2/ngc3031_herschel250micron.fits) |
| **COSMOS field** | Deep extragalactic field | [cosmos_spitzer3.6micron.fits](https://github.com/mjcowley/astrolabs/raw/main/data/C1/part2/cosmos_spitzer3.6micron.fits)<br>[cosmos_spitzer24micron.fits](https://github.com/mjcowley/astrolabs/raw/main/data/C1/part2/cosmos_spitzer24micron.fits)<br>[cosmos_herschel250micron.fits](https://github.com/mjcowley/astrolabs/raw/main/data/C1/part2/cosmos_herschel250micron.fits) |

The Part 2 images were processed by Dr George Bendo (Jodrell Bank Centre for Astrophysics, University of Manchester) using data from the Spitzer, Herschel and GALEX archives. Our thanks to George for making them available.

### Before you start

If you're working remotely, do these first:

1. Install SAOImageDS9 and open the NGC 3031 test file to check it works.
2. Download the three Part 1 JWST files.
3. Choose your Part 2 object and download its three files.
4. Download the [AstroLab C1 proforma](https://github.com/mjcowley/astrolabs/raw/main/C1/AstroLabC1_Proforma.docx) so you can fill it in as you go.

## Part 1: The Carina Nebula

1. **Watch the demonstration.** Watch the live demo if you're on campus, or the walkthrough video on Canvas if you're remote.

2. **Read the filter plot.** The plot below shows the fraction of incoming photons recorded at each wavelength, combining the filter, the telescope optics and the detector's [quantum efficiency](http://astro.vaporia.com/start/qe.html). Note roughly where F090W, F200W and F444W sit, as you'll use this to decide which filter goes in which colour channel.

   <img src="images/nircam_filters.png" alt="Plot of throughput against wavelength from 0 to 5000 nm for eight NIRCam filters. F090W covers roughly 800 to 1000 nm, F200W roughly 1750 to 2250 nm, and F444W roughly 3900 to 5000 nm." width="700" />

   *NIRCam filter throughput (the fraction of photons recorded at each wavelength)*

3. **Open an RGB frame.** Open SAOImageDS9 and select ***Frame***, then ***New Frame RGB*** from the top menu bar. A small RGB window will open, as shown below. **Keep this window open for the rest of the activity.**

   <img src="images/rgb.png" alt="The small SAOImageDS9 RGB window, with File, Align and Lock menus and Red, Green and Blue rows under Current and View columns." width="300" />

4. **Lock and align the channels.** Click the RGB window, then from its menu bar select ***Lock*** and tick both ***Scale*** and ***Colorbar***. If you can't see the ***Lock*** menu, click the small RGB window first. While you're there, check that ***Align*** is set to ***WCS***. F444W has bigger pixels than the other two filters, so SAOImageDS9 uses sky coordinates (the WCS) to line the images up.

5. **Load the red channel.** Decide which filter belongs in each of the R, G and B channels ([Hint](https://jwst-docs.stsci.edu/jwst-near-infrared-camera/nircam-instrumentation/nircam-filters)). If your image turns out odd, you've likely assigned the wrong filters. To load the red channel, select ***Red*** under the ***Current*** column in the RGB window. Then, in the main SAOImageDS9 window, select ***File***, ***Open*** and choose the relevant file.

6. **Fix the contrast.** Your image will probably look completely black, as if JWST were broken! Never fear, the problem is contrast. Click the ***Scale*** button in the main SAOImageDS9 window, then ***Zscale***, as shown below. Use your mouse wheel to zoom in and out. You should now see a monochrome image of the Carina Nebula.

   <img src="images/scale.png" alt="SAOImageDS9 button bar with the scale button selected in the top row and zscale selected in the second row." width="500" />

7. **Add the green and blue channels.** Repeat steps 5 and 6 to load the green and blue channels. You should now have your final RGB image of the Carina Nebula. Beautiful, isn't it?

8. **Capture your image.** Take a screenshot of the SAOImageDS9 window with the small RGB window visible, and paste it into Part 1 of your proforma. To keep a copy of the image itself, use ***File***, ***Save Image***, ***PNG***, which saves the current view. Then move on to Part 2.

## Part 2: Choose your own object

Now it's your turn to work out the colours. Each of the five objects in [Part 2 data](#part-2-data) was observed at three very different wavelengths, by different telescopes. Pick one, find out what each image shows, and build your own RGB composite.

1. **Choose your object.** Pick one of the five objects and download its three FITS files.

2. **Work out what you have.** The file names tell you the telescope and wavelength of each image, though you may need to look some of them up (MIPS, for example, is an instrument on Spitzer). For each image, find out what that wavelength mainly shows in an object like yours, such as old stars, young stars, warm dust or cold dust. Record this in the table in your proforma.

3. **Decide your colours.** Use the same rule as Part 1: shortest wavelength in blue, middle in green, longest in red. Watch the units, as the wavelengths aren't all given in the same units.

4. **Build your image.** Open a new RGB frame (***Frame***, ***New Frame RGB***), lock ***Scale*** and ***Colorbar***, check ***Align*** is set to ***WCS***, and load each channel as in Part 1. These images come from different telescopes with very different resolutions and pixel sizes, so aligning by WCS really matters here.

5. **Adjust the contrast.** Zscale may not suit every image. Try the other options under ***Scale***, such as ***log***, ***sqrt*** or ***99.5***, until each channel shows structure. If one channel overwhelms the others, untick ***Lock***, ***Scale*** in the RGB window, select that channel under ***Current***, and adjust it on its own.

6. **Capture your image.** Take a screenshot of the SAOImageDS9 window with the small RGB window visible, and paste it into Part 2 of your proforma.

7. **Compare and discuss.** Look up your object online and find at least one other image of it. It will probably look quite different from yours. In your proforma, describe your object and what your colours show, then compare your image with the one you found and suggest why they differ (for example, different telescopes, wavelengths, colour choices or processing).

**Finished?** Submit your completed proforma on Canvas.

## Troubleshooting

* If your image is all black, set ***Scale*** to ***Zscale*** (Part 1, step 6).
* If you can't see the ***Lock*** menu, click the small RGB window first so its menu bar is active.
* If macOS won't open SAOImageDS9, see the macOS install help on Canvas.
* If the three channels don't line up, check that ***Align*** is set to ***WCS*** in the RGB window.
* If the colours look odd, check which file you've loaded into each channel.
* If one channel looks blank or swamps the others in Part 2, try a different scale, or untick ***Lock***, ***Scale*** and adjust that channel on its own (Part 2, step 5).
* If a file won't open, check it downloaded completely. If you right-clicked the link and chose *Save link as*, try clicking it instead.

## Optional extension

The Part 1 images are cut out from much bigger mosaics. Find the full observation yourself: the "jw02731" in the original file names means JWST program 2731. Search for it in the [MAST Portal](https://mast.stsci.edu/) and see which other filters were used. Be warned that each full mosaic is about 5 GB!

## Credits

* Part 1: JWST NIRCam images of NGC 3324 from program 2731 (the JWST Early Release Observations), via MAST. Cut out with [`tools/make_c1_cutouts.py`](../tools/make_c1_cutouts.py).
* Part 2: images processed by Dr George Bendo (University of Manchester) from Spitzer, Herschel and GALEX archive data.
