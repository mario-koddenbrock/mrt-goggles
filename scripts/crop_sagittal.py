"""Render zoomed crops of all slices of the sagittal T2 series for visual inspection.
usage: crop_sagittal.py <dicom_dir> <out_dir>"""
import sys
from pathlib import Path
import numpy as np
import pydicom
from PIL import Image

root, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir(exist_ok=True)
items = []
for p in root.rglob("*"):
    if p.is_file() and p.read_bytes()[128:132] == b"DICM" and p.name != "DICOMDIR":
        ds = pydicom.dcmread(p)
        if "t2_tse_sag" in ds.SeriesDescription:
            items.append((int(ds.InstanceNumber), ds.pixel_array.astype(float)))
items.sort(key=lambda t: t[0])
for n, a in items:
    c = a[200:1024, 330:720]
    lo, hi = np.percentile(c, [1, 99.5])
    c = np.clip((c - lo) / (hi - lo), 0, 1) ** 0.7
    Image.fromarray((c * 255).astype(np.uint8)).save(out / f"sag_{n:02d}.png")
    print("saved", n, flush=True)
print(f"SUMMARY: {len(items)} slices", flush=True)
