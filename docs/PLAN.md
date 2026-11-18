# Plan: MRT goggles prototype

Goal: look at a cervical spine MRI (DICOM) locally and check for a vertebral slip (listhesis).

1. `index.html`: single-file browser viewer, no build step, no server, data stays local.
   - Load a DICOM folder (drag and drop or picker), group by series, scroll slices.
   - Window/level by dragging, ruler in mm (shows horizontal offset dx for listhesis checks).
   - Uncompressed DICOM only (prototype).
2. Test with synthetic DICOM in `tests/`.
3. Scan not yet located: get it from the user, then view it and measure.
