"""
Run every AstroLab notebook from top to bottom and report any cells that fail.

Usage (from the repository root):

    pip install -r requirements.txt nbformat nbclient ipykernel
    python tools/test_notebooks.py                 # test all notebooks
    python tools/test_notebooks.py AstroLabC8.ipynb   # test one notebook

Each notebook runs in a temporary copy of the repository, so nothing in your
working folder is changed and no outputs are saved into the notebooks.
Interactive widgets run once with their default slider values (see WIDGET_PATCH).
"""

import glob
import os
import shutil
import sys
import tempfile

import nbformat
from nbclient import NotebookClient

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Errors that are part of the lesson, e.g. the "fix the broken cell" activity
EXPECTED_ERRORS = [
    ("NameError", "speed_of_lihgt"),
]


# Headless runs can stall when an interactive widget first draws a plot, so
# replace ipywidgets.interact with a version that calls the function once
# with each widget's default value. The same plotting code still runs.
WIDGET_PATCH = """
import ipywidgets as _widgets

def _run_once(function, **controls):
    function(**{name: getattr(control, "value", control) for name, control in controls.items()})

_widgets.interact = _run_once
"""


def is_expected(error):
    return any(error.ename == name and text in error.evalue for name, text in EXPECTED_ERRORS)


def test(notebook):
    with tempfile.TemporaryDirectory() as tmp:
        for item in ["astrolabs.py", "data", notebook]:
            src = os.path.join(ROOT, item)
            dst = os.path.join(tmp, item)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy(src, dst)

        nb = nbformat.read(os.path.join(tmp, notebook), as_version=4)
        nb.cells.insert(0, nbformat.v4.new_code_cell(WIDGET_PATCH))
        client = NotebookClient(nb, timeout=300, kernel_name="python3",
                                allow_errors=True, resources={"metadata": {"path": tmp}})
        client.execute()

    failures = []
    for number, cell in enumerate(nb.cells[1:]):      # skip the inserted widget patch
        if cell.cell_type != "code":
            continue
        for output in cell.get("outputs", []):
            if output.output_type == "error" and not is_expected(output):
                first_line = cell.source.strip().splitlines()[0] if cell.source.strip() else ""
                failures.append(f"  cell {number} ({first_line[:60]}): {output.ename}: {output.evalue[:200]}")
    return failures


def main():
    notebooks = sys.argv[1:] or sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "AstroLab*.ipynb")))
    all_ok = True
    for notebook in notebooks:
        print(f"Testing {notebook} ...", flush=True)
        failures = test(notebook)
        if failures:
            all_ok = False
            print(f"❌ {notebook}: {len(failures)} failing cell(s)")
            print("\n".join(failures))
        else:
            print(f"✅ {notebook}: all cells ran")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
