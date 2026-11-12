# Diagram tool

`make_diagrams.py` rebuilds the three PNG previews in `docs/diagrams/`. It uses the diagram layout data in the script; editable Graphviz `.dot` sources are included beside the SVG and PNG files.

```powershell
python tools/make_diagrams.py
```

Install the optional dependency with `python -m pip install -r requirements-diagrams.txt`. The SVG diagrams are already included and do not need to be rebuilt for normal use.
