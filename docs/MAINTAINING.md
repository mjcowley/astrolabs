# Maintaining the AstroLabs

This guide is for anyone who looks after the PVB220 AstroLabs: fixing a typo, changing a widget, updating data or writing a new lab. It explains how the pieces fit together, how to change them safely, and how to get changes onto GitHub without breaking anything for students mid-semester.

## Contents

1. [How the pieces fit together](#1-how-the-pieces-fit-together)
2. [The golden rule: `main` is live](#2-the-golden-rule-main-is-live)
3. [Getting set up](#3-getting-set-up)
4. [Making a change, step by step](#4-making-a-change-step-by-step)
5. [Editing `astrolabs.py`](#5-editing-astrolabspy)
6. [Editing a notebook](#6-editing-a-notebook)
7. [Adding or updating data](#7-adding-or-updating-data)
8. [Testing](#8-testing)
9. [Writing a new lab](#9-writing-a-new-lab)
10. [Canvas pages, questions and answers](#10-canvas-pages-questions-and-answers)
11. [Before each semester](#11-before-each-semester)
12. [Troubleshooting](#12-troubleshooting)

---

## 1. How the pieces fit together

```
astrolabs/
├── C1/, C2/              # instructions, images and proforma for each software lab (C1 to C6)
├── AstroLabC7.ipynb      # one notebook per Python lab (C7 to C11)
├── AstroLabC8.ipynb
├── astrolabs.py          # shared helper module used by every notebook
├── canvas/               # the HTML for each lab's Canvas page
├── data/
│   ├── C1/               # data files for each lab
│   └── C7/
├── docs/
│   └── MAINTAINING.md    # this guide
├── tools/
│   ├── test_notebooks.py # runs every notebook and reports errors
│   ├── make_c1_data.py   # rebuilds the C1 data files
│   └── make_c2_data.py   # rebuilds the C2 data files and figures
├── Images/               # logo used in the README and notebooks
├── README.md             # the public front page
└── requirements.txt      # Python packages the labs need
```

When a student opens a lab in Google Colab or JupyterHub, this is what happens:

1. **The notebook opens.** In Colab it's loaded straight from GitHub via the *Open in Colab* badge.
2. **The setup cell runs.** If `astrolabs.py` isn't already sitting next to the notebook, it's downloaded from
   `https://raw.githubusercontent.com/mjcowley/astrolabs/main/astrolabs.py`.
3. **Data is fetched when needed.** Each notebook calls `al.get_data("C8/some_file.csv")`. That looks for `data/C8/some_file.csv` next to the notebook first, and if it isn't there, downloads it from the same GitHub address into a local `data/` folder.

So the notebooks, the helper and the data all come from the **`main` branch on GitHub**. That's what makes the next section so important.

## 2. The golden rule: `main` is live

> ⚠️ **Anything merged into `main` reaches every student the next time they run a notebook.** There's no separate "release" step.

That means:

* **Never edit `main` directly.** Make changes on a branch and merge them with a pull request (section 4).
* **Never rename or remove a function in `astrolabs.py` that a notebook uses**, even an old lab. Students may be running an older copy of a notebook that still calls it. If you need to change how a function works, add a new function or a new optional argument instead.
* **Never rename, move or delete a data file** that a notebook loads. Add a new file instead.
* **Test before merging** (section 8).
* **Avoid big changes while a lab is running.** Fixes are fine; redesigns are best done between semesters.

## 3. Getting set up

You'll need a GitHub account with write access to `mjcowley/astrolabs`.

**Option A: work in the browser (small changes only).** You can edit files directly on github.com: open the file, click the pencil icon, and choose *Create a new branch for this commit and start a pull request* when you save. This is fine for typos in the README or `astrolabs.py`, but **not for notebooks** (editing notebook JSON by hand is error-prone).

**Option B: work on your own computer (recommended).**

1. Install [Git](https://git-scm.com/downloads) and Python 3.10 or later. [Anaconda](https://www.anaconda.com/) is the easiest way to get Python and Jupyter together.
2. Clone the repository and install the requirements:

   ```bash
   git clone https://github.com/mjcowley/astrolabs.git
   cd astrolabs
   pip install -r requirements.txt jupyterlab nbformat nbclient ipykernel
   ```

3. Start Jupyter with `jupyter lab` and open any notebook. Because `astrolabs.py` and `data/` are already in the folder, nothing is downloaded: you're running your local copy. That's exactly what you want while editing.

If you've never used Git before, [GitHub Desktop](https://desktop.github.com/) gives you buttons for every step in section 4.

## 4. Making a change, step by step

```bash
# 1. Start from the latest main
git checkout main
git pull

# 2. Make a branch with a short, descriptive name
git checkout -b fix-c8-typo

# 3. Edit files, then test (section 8)
python tools/test_notebooks.py

# 4. Commit and push
git add -A
git commit -m "Fix typo in C8 Part 3"
git push -u origin fix-c8-typo
```

Then on GitHub:

5. Open a **pull request** (PR) from your branch into `main`. GitHub shows a yellow banner offering to do this right after you push.
6. Read through the **Files changed** tab to make sure only what you meant to change has changed. (Notebook diffs are hard to read; that's normal.)
7. Click **Squash and merge**. This turns all the commits on your branch into one tidy commit on `main`.
8. Delete the branch when GitHub offers.

Within a few minutes, students will see the change. GitHub's file server can cache the old version for up to about five minutes.

## 5. Editing `astrolabs.py`

`astrolabs.py` holds everything students don't need to see: downloads, interactive widgets, fiddly plots and the answer checks. The science steps (loading data, calculations, simple plots) belong in the notebook, where students can read them.

### How the file is organised

| Section | What's there |
| --- | --- |
| Top of file | `REPO_URL`, the colour palette `COLOURS` |
| Setup and data | `setup()` (plot style and package check), `get_data()` (find or download a data file) |
| Self-check answers | `_ANSWERS` and `check()` |
| One block per lab | Marked with a banner such as `# AstroLab C8: Running the Clock Backwards`. Each holds that lab's widgets and functions |

### Conventions

* **Every function gets a docstring** (the text in triple quotes under `def`) that a student could understand. Students are encouraged to read this file.
* **Interactive widgets** use `ipywidgets.interact` with a nested `show(...)` function that draws one plot. Use `continuous_update=False` on sliders so the plot only redraws when the student lets go; otherwise Colab feels sluggish. Copy an existing explorer (for example `helium_explorer`) as a template.
* **Import inside functions** for anything beyond `numpy` and `matplotlib` (as the existing code does). This keeps `import astrolabs` fast and means a missing package only breaks the one function that needs it.
* **Plots** use the colours in `COLOURS` and the style set by `setup()`, so the labs look consistent.
* **Helper functions that take a notebook function as an argument** (for example `blackbody_fitter(..., model)`) let the maths stay visible in the notebook while the widget code stays hidden. Prefer this pattern over hiding the science in the helper.
* **Australian spelling** (colour, metre, ionise) and **plain language** in anything printed to students.
* **Private helpers** (used only inside the file) start with an underscore, such as `_sky_image`.

### Adding a self-check answer

`check("C8_z_galaxy_C", value)` compares a student's number with an entry in `_ANSWERS`:

```python
"C8_z_galaxy_C": (5.45, 0.015, "Line up the dashed lines with the bright emission lines of galaxy C."),
#                  ^      ^       ^
#                  answer relative tolerance (1.5%)   hint shown if wrong
```

Name keys `C<lab>_<short_name>`. Remember that this file is public, so keen students can read the expected answers here. That's acceptable because Canvas marks are for completion, but **don't** put full Canvas answer sheets in this file.

### Changing an existing function safely

* Adding a new **optional** argument with a default is safe.
* Changing what a function returns, renaming it, or removing an argument is **not** safe (see section 2). Make a new function instead, for example `redshift_explorer_v2`, and switch the notebook to it.

## 6. Editing a notebook

Edit notebooks in Jupyter (or Colab, see below), never by hand in a text editor.

### Conventions used in every lab

* **The first code cell is the setup cell** (`#@title ▶️ Run me first: setup`). Keep it identical across labs apart from the imports a lab needs. It always downloads the latest `astrolabs.py` from `main` and reloads it (falling back to an existing copy when offline), so fixes reach students the next time they run it. This also overwrites any edits a student made to their own copy.
* **Icons:** ▶️ run this cell, 👉 change this value, 🎯 Canvas checkpoint, 💡 hint, 🔍 peek inside, 🚀 stretch activity. They're explained in Part 0 of C7.
* **Canvas checkpoints** are block quotes: `> 🎯 **Canvas checkpoint Q3:** ...`. Number them in order. If you add, remove or reorder one, update the Canvas quiz and the answer file to match.
* **Students never have to write code.** Anything they change should be a single marked value (`# 👉 Change this and re-run`) or a slider.
* **Every lab ends with** "What's Coming Up", Sparkler ideas (C8 onwards), an optional 🚀 stretch activity, and **Data and image credits**.
* **Australian spelling and contractions** (you'll, it's, don't) throughout, matching the lectures.

### Clear outputs before committing

Always save notebooks **without outputs**. In Jupyter: *Edit > Clear Outputs of All Cells* (JupyterLab) or *Kernel > Restart & Clear Output*, then save. Outputs make the files large, produce messy diffs, and can show students the answers before they've done the activity.

### Editing in Colab instead

Colab can save directly back to GitHub: *File > Save a copy in GitHub*, choose `mjcowley/astrolabs`, pick a **new branch name** (never `main`), and untick *Include a link to Colaboratory*. Then open a pull request from that branch on GitHub. Clear outputs first (*Edit > Clear all outputs*).

## 7. Adding or updating data

* Put each lab's files in `data/C<lab>/` and load them with `al.get_data("C<lab>/filename")`.
* **Keep files small.** Students download them every session, sometimes on slow connections. Aim for under about 10 MB per notebook lab. GitHub refuses any file over 100 MB and warns above 50 MB, so keep every file under 50 MB (C1's JWST images are cut out and compressed for this reason). Trim catalogues to the columns and rows the lab uses, and shrink images and maps (C8's CMB maps are stored as 16-bit integers with a scale factor to halve their size).
* **Prefer simple formats:** CSV for tables, FITS for images and maps (also good practice for students, since FITS is the astronomy standard).
* **Never rename or delete a file** a notebook uses (section 2). To replace data, add a new file name and update the notebook.
* **Credit every data source** in the notebook's credits section and the README's *Data credits* section, with the reference paper and archive.
* **Record how you made the file.** Add a short note to the table below (or the commit message) with where the data came from and what you did to it, so it can be rebuilt.

### Where the current data came from

| File | Source | Processing |
| --- | --- | --- |
| `C1/carina_jwst_*.fits.fz` | JWST NIRCam mosaics of NGC 3324 (program 2731, `jw02731-o001_t017_nircam_clear-*_i2d.fits`), MAST | Made with `tools/make_c1_data.py`: the same 264″ × 157″ patch of sky from each filter at full resolution, saved with RICE tile compression (quantize level 16). About 83 MB in total instead of about 12 GB for the full mosaics |
| `C1/ngc7293_*.fits.fz` | Spitzer Enhanced Imaging Products (IRAC 3.6 μm and MIPS 24 μm mosaics, AOR 40045030) and Herschel High Level Images (SPIRE 250 μm, obsid 1342256744), IRSA | Made with `tools/make_c1_data.py`: the same 26′ × 26′ patch of sky centred on NGC 7293 from each, at native resolution, RICE compressed |
| `C2/wasp2_lco_images.zip` | Las Cumbres Observatory archive: ten 15 s Faulkes Telescope North images of WASP-2, 2008-10-05 UT (proposal `johnjohn`) | Unchanged, but renamed in time order: `wasp2_lco_01.fits` to `_10.fits` were `l_e_20081004_494_6_1_1.fits`, `_494_16_`, `_494_26_`, `_494_51_`, `_494_76_`, `_494_101_`, `_494_126_`, `_495_24_`, `_495_49_` and `_495_74_`. The transit runs from about image 4 to image 8, with a depth of about 1.8% |
| `C2/wasp2_tess_sector81.csv` | TESS 2-minute light curve of WASP-2 (TIC 374530847, Sector 81), MAST | Made with `tools/make_c2_data.py`: `PDCSAP_FLUX` with `QUALITY = 0`, divided by its median; time in days since the first measurement. The same script draws the TESS plots and transit diagram in `C2/images/`. The AstroImageJ screenshots and the Aladin Lite view in `C2/images/` were supplied by the unit coordinator. Period 2.152 days, depth about 1.6%, duration about 1.7 hours |
| `C7/batse_grbs.csv` | BATSE 4B catalogue, HEASARC table `batsegrb` | Kept name, RA, Dec and Galactic coordinates |
| `C7/nearby_galaxies.csv` | 2MASS Redshift Survey, VizieR `J/ApJS/199/26/table3` | Kept Galactic coordinates and cz for cz > 0; distance = cz / 70 km/s/Mpc |
| `C7/galaxy_grz.fits` | DESI Legacy Surveys DR10 cutout service | NGC 1365, 800 × 800 pixels at 1″/pixel, g, r, z bands |
| `C8/firas_cmb_spectrum.csv` | COBE FIRAS monopole spectrum, NASA LAMBDA (`firas_monopole_spec_v1.txt`) | Converted cm⁻¹ to GHz and mm; uncertainties from kJy/sr to MJy/sr |
| `C8/jwst_spectra.csv` | JADES DR4 NIRSpec prism `x1d` spectra, MAST HLSP | Five GOODS-S galaxies (IDs 3753, 159438, 202208, 12637, 265801); `EXTRACT5PIX1D` flux × 10²⁰ |
| `C8/cmb_maps.fits` | Planck 2015 SMICA (IRSA), WMAP 9-year K band (LAMBDA) | Mollweide projections in Galactic coordinates with `healpy`; dipole is a model from the Planck 2018 amplitude and direction; patches are 10° × 10° at (l, b) = (240°, −55°) |
| `C9/images/*.jpg` | DESI Legacy Surveys viewer (`jpeg-cutout`), DR9 layer for M87, NGC 4473, NGC 3115 and M74; DR10 for NGC 1300 and NGC 1427A; SDSS layer for M104 | 400 × 400 pixels. DR9/SDSS used where DR10 shows saturation artefacts on bright galaxies |
| `C9/galaxy_spectra.csv` | Brown et al. (2014) atlas, STScI reference atlases (`cdbs/grid/brown`) | Six galaxies, resampled onto a common grid and normalised to 1 at 5500 Å (rest frame) |
| `C9/agn_spectra.csv` | Brown et al. (2019) AGN SED atlas on MAST (`hlsps/agnsedatlas`, observed-frame text files) for 3C 273 and NGC 4151; Brown et al. (2014) for NGC 1068 | 3500 to 10000 Å, each normalised by its median |
| `C9/zfourge_cdfs_galaxies.csv` | ZFOURGE CDFS (Straatman et al. 2016), VizieR `J/ApJ/830/51` tables `zf_cdfs`, `cdfssfr` | `Use = 1` only. Rest-frame U−V and V−J estimated by log-linear interpolation of the photometry (U, IA, HST, FourStar, Ks, IRAC bands with S/N > 2) at 0.365, 0.551 and 1.22 μm |
| `C9/zfourge_xray_matches.csv` | VizieR `J/ApJ/830/51/cdfsxmatch` (`xAGN` flag, Cowley et al. 2016) | Galaxies with `Use = 1` and an X-ray match |
| `C9/chandra_cdfs_7ms.csv` | Luo et al. (2017), VizieR `J/ApJS/228/2/sources` | AGN and galaxies with a redshift (`zF`) and `LX` (erg/s, rest-frame 0.5 to 7 keV, not corrected for absorption; `LXc` is the corrected value) |
| `C10/ngc2403_rotation_curve.csv` | SPARC (Lelli et al. 2016), VizieR `J/AJ/152/157/table2`, NGC 2403 | Kept radius, Vobs, e_Vobs, Vgas; `v_stars` = Vdisk × √0.5 (3.6 μm mass-to-light ratio of 0.5). Best fit with the pseudo-isothermal halo: v∞ ≈ 126 km/s, core ≈ 1.6 kpc, mismatch ≈ 3.7 |
| `C10/gw150914_strain.npz` | GWOSC event API, GWTC-1-confident GW150914 v3, 32 s, 4 kHz `txt.gz` files for H1 and L1 | Stored as float32 arrays `H1`, `L1` with `fs` and `t_start` (seconds relative to GPS 1126259462.4) |
| `C10/gw_catalogue.csv` | GWOSC `eventapi/json/allevents` | Confident events from GWTC-1/2.1/3 confident and GWTC-4.0/4.1/5.0 with p_astro ≥ 0.9 and source-frame masses; latest catalogue kept per event |
| `C11/pantheon_plus_supernovae.csv` | Pantheon+SH0ES data release (`Pantheon+SH0ES.dat`, github.com/PantheonPlusSH0ES/DataRelease) | Kept name, `zHD`, `MU_SH0ES` and its diagonal error; Cepheid calibrator rows removed (1,624 rows). v = cz fit through the origin at 0.01 < z < 0.05 gives H0 ≈ 70.6 km/s/Mpc; best Ω_M, Ω_Λ ≈ 0.3, 0.6 to 0.7 at H0 = 73 |
| `C11/zfourge_cosmos.csv` | ZFOURGE COSMOS (Straatman et al. 2016), VizieR `J/ApJ/830/51` tables `zf_cosmos`, `cosmossfr`, `cosmosz`, `cosxmatch` | `Use = 1` only (11,861 rows). `z_phot` = EAZY `zpk`; `log_sfr` = log10 of the UV + IR SFR (NaN where ≤ 0); `r_eff_arcsec` from van der Wel et al. (2014). 23 of the 161 ZFIRE galaxies match a `Use ≠ 1` source and so have no counterpart here (explained in the notebook) |
| `C11/zfire_cosmos.csv` | ZFIRE (Nanayakkara et al. 2016), VizieR `J/ApJ/828/21/zfire_cos` | `q_zsp = 3` only (161 rows); kept cluster membership, AGN flag and Hα, [N II], Hβ, [O III] fluxes (`FHa`, `FNII`, `FHb`, `FOIII`; the notebook drops zero fluxes before taking logs) |

## 8. Testing

**Before every merge**, run all notebooks from top to bottom:

```bash
python tools/test_notebooks.py                   # every lab
python tools/test_notebooks.py AstroLabC8.ipynb  # just one
```

The script runs each notebook in a temporary folder and lists any cell that fails. It tests your **local** `astrolabs.py`: the setup cell's download from GitHub is skipped during tests, so you can test helper changes before they reach `main`. It knows about the deliberate error in C7's "Fix the broken cell" activity and ignores it. If you add another deliberate error, add it to `EXPECTED_ERRORS` at the top of the script.

The script runs every widget once with its default values, so it catches crashes but not plots that look wrong. **After changing a widget, also open the notebook in Jupyter and try the sliders yourself**, including their extreme values.

Finally, after merging, open the lab from the README's *Open in Colab* badge and run the setup cell plus one data cell, to check the live version downloads correctly.

## 9. Writing a new lab

1. **Read the lecture slides for that week** and build the lab around them: the lab should reuse the lecture's examples, language and numbers.
2. **Plan around one hour** of hands-on time, in five or six parts of about ten minutes each, plus an optional stretch activity.
3. **Start from an existing notebook.** Copy `AstroLabC8.ipynb` to `AstroLabC<n>.ipynb`, keep the header, setup cell and closing sections, and replace the middle.
4. **Put new widgets in a new block** at the end of `astrolabs.py`, with a banner comment naming the lab.
5. **Add data** under `data/C<n>/` (section 7).
6. **Add a row to the README's lab table** with an *Open in Colab* badge (copy the C8 row and change the file name), and add the data credits.
7. **Write the Canvas questions** (section 10).
8. **Test** (section 8), then open a pull request.

Each lab should practise one new Python skill on top of the earlier labs (C7: variables, units, arrays, tables and plots; C8: functions and fitting a model to data), but always in a form students can complete by running cells and moving sliders.

## 10. Canvas pages, questions and answers

### Canvas pages

Each lab has a short Canvas page with a banner, *Start here* buttons linking to the lab on GitHub, the key facts, and how to complete it on campus or remotely. The step-by-step instructions and data live on GitHub, so the Canvas page rarely needs to change.

The HTML for each page is kept in `canvas/` (for example `canvas/C1.html`), so a page can be restored if Canvas's editor garbles it or a course copy breaks it.

* **Edit the copy in `canvas/` first,** then paste it into the Canvas page's HTML editor (*Edit*, then the `</>` button). If you change a page directly in Canvas, copy the HTML back here afterwards so the two don't drift apart.
* **Keep the same layout for every lab:** banner, *Start here*, the four fact boxes, *Overview*, then *How to complete this AstroLab*. Boxes use a full border (`2px solid #003562` for *Start here*, `1px solid #9db3cb` for the others) rather than a coloured edge.
* **Nothing private goes in these pages.** Like everything else here they're public, so link to Canvas items by name (for example the *Assignments* page) rather than pasting Canvas URLs.

### Canvas questions and answers

**Answer files never go in this repository.** The repository is public and indexed by search engines, so anything committed here (even if later deleted) can be found in the history.

For each lab, keep a separate Markdown file (for example `AstroLabC8_canvas.md`) with the instructor, outside the repository. Each question has:

* the checkpoint number matching the notebook,
* four multiple-choice options with the correct one marked,
* short feedback for a wrong answer explaining how to get the right one.

These are then built as H5P quizzes on Canvas. Students get unlimited attempts and marks are for completion.

**If you change a notebook's data or numbers, check whether any Canvas answers change**, and update both the answer file and the Canvas quiz.

## 11. Before each semester

* [ ] Run `python tools/test_notebooks.py`. Package updates in Colab can break things between semesters.
* [ ] Open each lab from its Colab badge and run it all the way through.
* [ ] Check the Canvas quizzes still match the notebooks.
* [ ] Ask QUT's JupyterHub team to make sure `ipywidgets` is installed and widgets display.
* [ ] Optionally, **tag a release** so you can always see exactly what students used:

  ```bash
  git tag 2027-S1
  git push origin 2027-S1
  ```

## 12. Troubleshooting

| Problem | Likely cause and fix |
| --- | --- |
| Students get `Couldn't download ...` | The file isn't on `main` yet (not merged), the path or name is wrong, or the repository has been made private. Check the file opens at `https://raw.githubusercontent.com/mjcowley/astrolabs/main/data/...` |
| A change isn't showing up for students | GitHub caches files for a few minutes. After that, re-running the setup cell downloads and reloads the latest `astrolabs.py`. If a widget still shows the old behaviour, use *Runtime > Disconnect and delete runtime* in Colab (or restart the kernel on JupyterHub) and run from the top. |
| Sliders appear but plots don't update | `ipywidgets` isn't installed or enabled (common on JupyterHub). In Colab, re-run the cell. |
| `AttributeError: module 'astrolabs' has no attribute ...` | The student's copy of `astrolabs.py` is older than the notebook, usually because they were offline when the setup cell ran. Re-run the setup cell with internet access. |
| A notebook works locally but not in Colab | Locally you're using the files in your folder; Colab downloads from `main`. Make sure everything is merged, and check package versions (`al.setup()` prints them). |
| Merge conflict on a pull request | Someone else changed the same lines. On your branch, run `git pull origin main`, fix the marked sections, commit and push again. For notebooks, it's often easiest to redo your edit on a fresh branch from `main`. |
