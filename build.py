#!/bin/python3

import shutil
from pathlib import Path

print("Building status page...")

with open("status") as f:
    data = [line.strip() for line in f.readlines() if line[0] != "#"]
    assert len(data) in [2, 3]
    if len(data) == 2:
        state, title = data
        description = ""
    else:
        state, title, description = data

assert state in ["good", "bad", "warning"]

print("Current status:")
print(f"State: {state}")
print(f"Title: {title}")
print(f"Description: {description}")


def replace(doc):
    return (
        doc
        .replace("{{state}}", state)
        .replace("{{description}}", description)
        .replace("{{title}}", title)
    )


build_dir = Path(".") / "build"
shutil.rmtree(build_dir, ignore_errors=True)
shutil.copytree(Path("static/"), build_dir)

with open("src/index.html") as f, open(build_dir / "index.html", "w") as o:
    o.write(replace(f.read()))

with open("src/status.json") as f, open(build_dir / "status.json", "w") as o:
    o.write(replace(f.read()))

print("Done!")
