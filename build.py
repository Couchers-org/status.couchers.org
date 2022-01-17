#!/bin/python3

import shutil
from datetime import datetime
from pathlib import Path
from subprocess import check_output

print("Building status page...")

# prints out unix timestamp of last modified
last_updated_raw = (
    check_output(
        [
            "git",
            "log",
            "--date-order",
            "--quiet",
            "--format=tformat:%ct",
            "--max-count=1",
            "--",
            "./status",
        ]
    )
    .decode("utf8")
    .strip()
)

last_updated = datetime.fromtimestamp(int(last_updated_raw))

last_updated_display = f"{last_updated.isoformat()} UTC"
last_updated_timestamp = int(last_updated.timestamp())

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
print(f"last_updated_display: {last_updated_display}")
print(f"last_updated_timestamp: {last_updated_timestamp}")


def replace(doc):
    return (
        doc
        .replace("{{state}}", state)
        .replace("{{title}}", title)
        .replace("{{description}}", description)
        .replace("{{last_updated_display}}", str(last_updated_display))
        .replace("{{last_updated_timestamp}}", str(last_updated_timestamp))
    )


build_dir = Path(".") / "build"
shutil.rmtree(build_dir, ignore_errors=True)
shutil.copytree(Path("static/"), build_dir)

with open("src/index.html") as f, open(build_dir / "index.html", "w") as o:
    o.write(replace(f.read()))

with open("src/status.json") as f, open(build_dir / "status.json", "w") as o:
    o.write(replace(f.read()))

print("Done!")
