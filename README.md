# AstroLabs

<img src="Images/qarg_bw_dark.png" alt="QUT Logo" width="500" />

Python and Jupyter notebook practicals for **PVB220 Cosmology** at QUT, developed by the QUT Astrophysics Research Group [(QARG)](https://research.qut.edu.au/qutastrophysics/). Each AstroLab is a self-contained notebook that runs in Google Colab or QUT's JupyterHub with no installation.

These labs follow on from the software-based AstroLabs C1 to C6 in PVB210 (SAOImageDS9, AstroImageJ, TOPCAT). They're designed for students across a university-wide minor, so **no programming experience is needed**: every code cell is already written, and students run cells, change marked values and use sliders to explore real astronomical data. Students who want to learn Python can read and modify all of the code.

Companion repositories: [Astro_Demos](https://github.com/mjcowley/astro_demos) (interactive browser demos) and [Python_Intro](https://github.com/mjcowley/Python_Intro) (a general introduction to Python for physics).

## AstroLabs

| Lab | Week | Topic | Notebook |
| --- | :-: | --- | --- |
| C7 | 2 | Your Python Toolkit for the Universe: distance scales, lookback time, the cosmological principle, Olbers' paradox and your first FITS image | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mjcowley/astrolabs/blob/main/AstroLabC7.ipynb) |
| C8 | 4 | Running the Clock Backwards: Planck units, the scale factor and redshift, the CMB spectrum, the cosmic thermometer and JWST galaxy redshifts | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mjcowley/astrolabs/blob/main/AstroLabC8.ipynb) |
| C9 | 6 | Galaxy colours (UVJ), star formation and AGN | Coming soon |
| C10 | 8 | Gravitational waves | Coming soon |
| C11 | 10 | Cosmology surveys: cross-matching and scaling relations | Coming soon |

## Session format

Each practical runs for two hours: a one-hour presentation on the science and the activity, then one hour of hands-on work supported by demonstrators. Practicals aren't submitted. Students complete multiple-choice **Canvas checkpoints** (marked 🎯 in the notebooks) as they work through each lab, and later choose one of labs C8 to C11 as the basis for their Sparkler poster presentation.

## How the notebooks work

Every notebook uses the same icons:

| Icon | Meaning |
| :-: | --- |
| ▶️ | Run this cell |
| 👉 | Change this value, then re-run the cell |
| 🎯 | Canvas checkpoint |
| 💡 | Hint |
| 🔍 | Peek inside: where to find the code behind a step |
| 🚀 | Stretch activity (optional) |

The first cell of each notebook downloads `astrolabs.py`, a small helper module holding the interactive widgets, data downloads and plot styling. The science steps (loading data, calculations and plots) stay visible in the notebook.

## Running the notebooks

**Google Colab (recommended):** click the *Open in Colab* badge above, then use **File > Save a copy in Drive** to keep your changes. Everything you need is already installed.

**QUT JupyterHub or a local install:** download the notebook (and `astrolabs.py`) into the same folder and open it. For a local install, use Python 3.10 or later and install the requirements:

```bash
pip install -r requirements.txt
```

Data files are downloaded automatically into a `data/` folder the first time a notebook needs them.

## Structure

```
astrolabs/
├── AstroLabC7.ipynb      # one notebook per lab
├── AstroLabC8.ipynb
├── astrolabs.py          # shared helper functions and widgets
├── data/C7/, data/C8/    # data files for each lab
├── Images/
└── requirements.txt
```

## Data credits

Each notebook lists the sources and references for its data at the end. AstroLab C7 uses the BATSE gamma-ray burst catalogue (NASA HEASARC), the 2MASS Redshift Survey (Huchra et al. 2012) and an image of NGC 1365 from the DESI Legacy Imaging Surveys DR10. AstroLab C8 uses the COBE FIRAS CMB spectrum (NASA LAMBDA), JWST NIRSpec spectra from JADES Data Release 4 (MAST), and CMB maps from Planck (NASA/IPAC IRSA) and WMAP (NASA LAMBDA).

## Contributing

Contributions are welcome! If you have ideas for improvements or new labs, feel free to open an issue or submit a pull request.

## Acknowledgements

Special thanks to all contributors and to the open-source communities behind NumPy, pandas, Matplotlib, Astropy and Jupyter that make scientific computing and data visualisation possible.
