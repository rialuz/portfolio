"""Generate the PixelLab pieces of the seasonal kits, one after another.

Reads seasons/gen.json: a list of {season, name, w, h, desc, seed, view?}. An item whose raw
file already exists is skipped, so the batch can be stopped and resumed, and a retry is just
a new name or a deleted file. Every call goes through pl.py, which logs it to the ledger.

usage: season_gen.py <pixel-assets dir> [season ...]
"""
import json
import os
import subprocess
import sys

STYLE = ("Cute pixel art game icon, chunky clean dark outline, simple cel shading, "
         "bright saturated colors, centered, transparent background.")


def main():
    root = sys.argv[1]
    only = set(sys.argv[2:])
    with open(os.path.join(root, "seasons", "gen.json"), encoding="utf-8") as f:
        items = json.load(f)
    pl = os.path.join(root, "tools", "pl.py")
    for it in items:
        if only and it["season"] not in only:
            continue
        out = os.path.join(root, "seasons", it["season"], "raw", it["name"] + ".png")
        if os.path.exists(out):
            continue
        cmd = [sys.executable, "-I", "-u", pl, "pixflux", "--out", out, "--w", str(it["w"]), "--h", str(it["h"]),
               "--desc", it["desc"] + " " + STYLE, "--view", it.get("view", "side"),
               "--outline", "single color black outline", "--shading", "basic shading",
               "--detail", "medium detail", "--no-bg", "--seed", str(it["seed"])]
        print(it["season"], it["name"], flush=True)
        subprocess.run(cmd, check=False)


if __name__ == "__main__":
    main()
