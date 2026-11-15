"""Run kmeans.py and dump what the explainer draws to data.json. Numbers are never typed into the HTML."""
import json
import os
import runpy

HERE = os.path.dirname(os.path.abspath(__file__))
g = runpy.run_path(os.path.join(HERE, "kmeans.py"))

r = lambda v: round(v, 3)
data = {
    "points": [[r(x), r(y)] for x, y in g["points"]],
    "k": g["K"],
    "rounds": [{"centres": [[r(x), r(y)] for x, y in h["centres"]], "labels": h["labels"], "moved": r(h["moved"])}
               for h in g["history"]],
    "final": [[r(x), r(y)] for x, y in g["centres"]],
    "inertia": r(g["inertia"]),
    "true": [list(c) for c in g["TRUE_CENTRES"]],
}
with open(os.path.join(HERE, "data.json"), "w") as f:
    f.write(json.dumps(data, allow_nan=False))
assert round(data["inertia"], 1) == round(g["inertia"], 1) and len(data["rounds"]) == len(g["history"])
print(f"data.json: {len(data['points'])} points, {len(data['rounds'])} rounds, inertia {data['inertia']}")
