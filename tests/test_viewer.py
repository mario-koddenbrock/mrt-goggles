"""Load a real DICOM folder in the viewer (headless Chrome) and screenshot it.
Run: MRT_DICOM_DIR=<folder> pytest -s tests/test_viewer.py
"""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
DICOM = os.environ["MRT_DICOM_DIR"]


def test_viewer_loads_series():
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        page = b.new_page(viewport={"width": 1300, "height": 1000})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto((ROOT / "index.html").as_uri())
        page.set_input_files("#pick", DICOM)
        page.wait_for_function("document.querySelectorAll('#series option').length > 0")
        opts = page.eval_on_selector_all("#series option", "o => o.map(x => [x.value, x.textContent])")
        print(opts, flush=True)
        for i, (uid, label) in enumerate(opts):
            page.select_option("#series", uid)
            page.wait_for_function("document.querySelector('#info').textContent.length > 0")
            page.screenshot(path=str(ROOT / f"scratch/series{i}.png"))
        b.close()
        assert not errors, errors
        assert len(opts) == 4
