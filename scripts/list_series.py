"""List series in a DICOM folder (no patient identifiers printed)."""
import sys
from collections import defaultdict
from pathlib import Path
import pydicom

root = Path(sys.argv[1])
series = defaultdict(list)
for p in sorted(root.rglob("*")):
    if not p.is_file() or p.name == "DICOMDIR" or p.read_bytes()[128:132] != b"DICM":
        continue
    ds = pydicom.dcmread(p, stop_before_pixels=True)
    series[ds.SeriesInstanceUID].append((p, ds))

for uid, items in series.items():
    ds = items[0][1]
    iop = [round(float(v), 2) for v in ds.get("ImageOrientationPatient", [])]
    print(f"{ds.get('Modality')} | {ds.get('SeriesDescription')} | n={len(items)} | "
          f"{ds.Rows}x{ds.Columns} | px={ds.get('PixelSpacing')} | thick={ds.get('SliceThickness')} | "
          f"ts={ds.file_meta.TransferSyntaxUID.name} | iop={iop}", flush=True)
print(f"SUMMARY: {len(series)} series, {sum(len(v) for v in series.values())} files", flush=True)
