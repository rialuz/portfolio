"""PixelLab character pipeline: create from a south-facing sprite, fetch rotations, animate.

usage: char.py create <south.png> <out_dir> <description> [n_directions]
       char.py get <character_id> <out_dir>
       char.py animate <character_id> <out_dir> <json-with-request-fields>
"""
import json
import os
import sys
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pl import b64, call, find_images, log, poll, save, strip_images  # noqa: E402


def show(label, body):
    print(label, json.dumps(strip_images(body))[:1800])


def download(url, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (pixel-asset-kit)"})
    with urllib.request.urlopen(req, timeout=60) as r, open(path, "wb") as f:
        f.write(r.read())


def submit(endpoint, body):
    for _ in range(12):  # 429 = slot busy, rejected before any work ran
        status, resp = call("POST", endpoint, body)
        if status != 429:
            break
        time.sleep(6)
    return status, resp


def get(character_id, out_dir):
    status, body = call("GET", f"/characters/{character_id}", timeout=60)
    slim = {k: v for k, v in body.items() if k not in ("skeletons",)} if isinstance(body, dict) else body
    show("character", slim)
    for direction, url in ((body.get("rotation_urls") or {}) if isinstance(body, dict) else {}).items():
        if url:
            download(url, os.path.join(out_dir, "rotations", direction + ".png"))
            print("saved rotation", direction)
    return body


def create(south, out_dir, description, n_directions):
    body = {"description": description, "name": "Luz", "reference_image": b64(south),
            "n_directions": n_directions, "view": "low top-down", "no_background": True,
            "image_size": {"width": 64, "height": 64}}
    status, resp = submit("/create-character-v3", body)
    show(f"create http={status}", resp)
    if status not in (200, 202):
        log("/create-character-v3", status, None, out_dir, "ERROR " + json.dumps(resp)[:300])
        return 1
    usage = resp.get("usage")
    with open(os.path.join(out_dir, "character.json"), "w", encoding="utf-8") as f:
        json.dump({"character_id": resp["character_id"], "job": resp["background_job_id"]}, f)
    status, job = poll(resp["background_job_id"])
    show("job", job)
    log("/create-character-v3", status, job.get("usage") or usage, out_dir, "character " + resp["character_id"])
    if job.get("status") != "completed":
        return 1
    get(resp["character_id"], out_dir)
    return 0


def animate(character_id, out_dir, fields):
    body = {"character_id": character_id}
    body.update(fields)
    status, resp = submit("/animate-character", body)
    show(f"animate http={status}", resp)
    if status not in (200, 202):
        log("/animate-character", status, None, out_dir, "ERROR " + json.dumps(resp)[:300])
        return 1
    rc = 0
    for direction, job_id in zip(resp.get("directions") or [], resp.get("background_job_ids") or []):
        status, job = poll(job_id, limit=1200)
        show(f"job {direction}", job)
        log("/animate-character", status, job.get("usage") or resp.get("usage"), out_dir,
            json.dumps(fields)[:200])
        if job.get("status") != "completed":
            rc = 1
            continue
        for i, im in enumerate(find_images(job)):
            save(im, os.path.join(out_dir, direction, f"frame_{i:02d}.png"))
        print("saved", len(find_images(job)), "frames inline for", direction)
    return rc


def main():
    cmd = sys.argv[1]
    if cmd == "create":
        os.makedirs(sys.argv[3], exist_ok=True)
        return create(sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]) if len(sys.argv) > 5 else 4)
    if cmd == "get":
        get(sys.argv[2], sys.argv[3])
        return 0
    if cmd == "animate":
        with open(sys.argv[4], encoding="utf-8") as f:
            return animate(sys.argv[2], sys.argv[3], json.load(f))


if __name__ == "__main__":
    sys.exit(main())
