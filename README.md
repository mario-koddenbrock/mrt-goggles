# mrt-goggles

A small browser viewer for MRI scans in DICOM format, built to look at a cervical spine scan and check by eye whether a vertebra has slipped. It is a prototype. It is not a medical device and gives no diagnosis; the radiologist's report is what counts.

## Use

Open `index.html` in Chrome, click "Open DICOM folder" and pick the folder you got from the radiology center (or drag it onto the page). Everything runs locally; no data leaves your machine.

- Mouse wheel or arrow keys: change slice
- Drag in "Window/Level" mode: contrast and brightness
- "Ruler (mm)": draw a line to get its length and horizontal offset `dx` in mm. For a slip, measure `dx` between the back edges of two neighbouring vertebral bodies on a sagittal T2 slice.

Only uncompressed DICOM is supported.

## Helper scripts and tests

```
conda create -n mrt-goggles python=3.12
conda activate mrt-goggles
pip install -r requirements.txt

python scripts/list_series.py <dicom_dir>              # list series without patient info
python scripts/crop_sagittal.py <dicom_dir> scratch    # zoomed crops of the sagittal T2 slices
MRT_DICOM_DIR=<dicom_dir> pytest -s tests/test_viewer.py
```

The test needs Google Chrome installed. Screenshots and crops go to `scratch/`, which is gitignored. Do not commit scan data.

`vendor/dicomParser.min.js` is [dicom-parser](https://github.com/cornerstonejs/dicomParser) 1.8.21 (MIT).
