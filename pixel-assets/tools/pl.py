"""Small PixelLab v2 client. Token is read from the file named by PIXELLAB_TOKEN_FILE.

Every call is appended to the ledger (endpoint, usage, output) so spend stays visible.
A request that errors or times out is never retried automatically, to avoid double charges.
"""
import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE = "https://api.pixellab.ai/v2"
LEDGER = os.environ.get("PIXELLAB_LEDGER", "ledger.jsonl")


def token():
    with open(os.environ["PIXELLAB_TOKEN_FILE"], encoding="utf-8") as f:
        return f.read().strip()


def call(method, path, payload=None, timeout=420):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method)
    req.add_header("Authorization", "Bearer " + token())
    req.add_header("Accept", "application/json")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        try:
            body = json.loads(body)
        except ValueError:
            pass
        return e.code, body


def b64(path):
    with open(path, "rb") as f:
        return {"type": "base64", "base64": base64.b64encode(f.read()).decode(), "format": "png"}


def save(image, path):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    raw = image["base64"]
    if raw.startswith("data:"):
        raw = raw.split(",", 1)[1]
    with open(path, "wb") as f:
        f.write(base64.b64decode(raw))


def log(endpoint, status, usage, out, note=""):
    with open(LEDGER, "a", encoding="utf-8") as f:
        f.write(json.dumps({"t": time.strftime("%H:%M:%S"), "endpoint": endpoint, "http": status,
                            "usage": usage, "out": out, "note": note}) + "\n")


def strip_images(obj):
    """Copy of a response with base64 blobs replaced by their length, for printing."""
    if isinstance(obj, dict):
        return {k: (f"<{len(v)} b64 chars>" if k == "base64" and isinstance(v, str) else strip_images(v))
                for k, v in obj.items()}
    if isinstance(obj, list):
        return [strip_images(x) for x in obj]
    return obj


def poll(job_id, every=6, limit=900):
    start = time.time()
    while time.time() - start < limit:
        status, body = call("GET", f"/background-jobs/{job_id}", timeout=60)
        if status != 200:
            return status, body
        if body.get("status") in ("completed", "failed"):
            return status, body
        time.sleep(every)
    return 0, {"status": "timeout", "id": job_id}


def find_images(obj):
    """All base64 image dicts anywhere in a response, in order."""
    found = []
    if isinstance(obj, dict):
        if isinstance(obj.get("base64"), str):
            found.append(obj)
        else:
            for v in obj.values():
                found.extend(find_images(v))
    elif isinstance(obj, list):
        for v in obj:
            found.extend(find_images(v))
    return found


def run(endpoint, payload, out, is_job=False, note="", show=()):
    # 429 means the single free-plan slot is still busy: the request was rejected before any
    # work ran, so waiting and resubmitting cannot double charge.
    for attempt in range(12):
        status, body = call("POST", endpoint, payload)
        if status != 429:
            break
        time.sleep(6)
    usage = body.get("usage") if isinstance(body, dict) else None
    if status not in (200, 202):
        log(endpoint, status, usage, out, "ERROR " + json.dumps(body)[:300])
        print("ERROR", status, json.dumps(strip_images(body))[:1500])
        return 1
    if is_job:
        job_id = body.get("background_job_id")
        print("job", job_id, "submit usage", usage)
        status, body = poll(job_id)
        usage = body.get("usage") or usage
        if body.get("status") != "completed":
            log(endpoint, status, usage, out, "JOB " + json.dumps(strip_images(body))[:300])
            print("JOB NOT COMPLETED", json.dumps(strip_images(body))[:1500])
            return 1
    images = find_images(body)
    if len(images) == 1 and out.lower().endswith(".png"):
        save(images[0], out)
        saved = [out]
    else:
        saved = []
        for i, im in enumerate(images):
            p = os.path.join(out, f"frame_{i:02d}.png")
            save(im, p)
            saved.append(p)
    log(endpoint, status, usage, out, note)
    meta = strip_images(body)
    print("OK", endpoint, "usage", usage, "saved", len(saved), "->", out)
    for key in show:
        if body.get(key):
            print(key + ":", body[key])
    if is_job:
        print("meta", json.dumps(meta)[:600])
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("balance")

    p = sub.add_parser("pixflux")
    p.add_argument("--out", required=True)
    p.add_argument("--w", type=int, required=True)
    p.add_argument("--h", type=int, required=True)
    p.add_argument("--desc", required=True)
    p.add_argument("--view")
    p.add_argument("--direction")
    p.add_argument("--outline")
    p.add_argument("--shading")
    p.add_argument("--detail")
    p.add_argument("--no-bg", action="store_true")
    p.add_argument("--palette")
    p.add_argument("--init")
    p.add_argument("--init-strength", type=int)
    p.add_argument("--guidance", type=float)
    p.add_argument("--seed", type=int)

    p = sub.add_parser("pixen")
    p.add_argument("--out", required=True)
    p.add_argument("--w", type=int, required=True)
    p.add_argument("--h", type=int, required=True)
    p.add_argument("--desc", required=True)
    p.add_argument("--view")
    p.add_argument("--direction")
    p.add_argument("--outline")
    p.add_argument("--detail")
    p.add_argument("--no-bg", action="store_true")
    p.add_argument("--enhance", action="store_true")
    p.add_argument("--seed", type=int)

    p = sub.add_parser("rotate")
    p.add_argument("--src", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--size", type=int, default=64)
    p.add_argument("--from-direction", default="south")
    p.add_argument("--to-direction", default="east")
    p.add_argument("--view", default="side")
    p.add_argument("--palette")
    p.add_argument("--guidance", type=float)
    p.add_argument("--seed", type=int)

    p = sub.add_parser("animate3")
    p.add_argument("--src", required=True)
    p.add_argument("--out", required=True, help="directory for frames")
    p.add_argument("--action", required=True)
    p.add_argument("--frames", type=int, required=True)
    p.add_argument("--last")
    p.add_argument("--seed", type=int)

    p = sub.add_parser("raw")
    p.add_argument("--endpoint", required=True)
    p.add_argument("--json", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--job", action="store_true")

    a = ap.parse_args()

    if a.cmd == "balance":
        print(json.dumps(call("GET", "/balance", timeout=60)[1]))
        return 0

    if a.cmd == "pixflux":
        body = {"description": a.desc, "image_size": {"width": a.w, "height": a.h}, "no_background": a.no_bg}
        for k in ("view", "direction", "outline", "shading", "detail", "seed"):
            if getattr(a, k) is not None:
                body[k] = getattr(a, k)
        if a.guidance is not None:
            body["text_guidance_scale"] = a.guidance
        if a.palette:
            body["color_image"] = b64(a.palette)
        if a.init:
            body["init_image"] = b64(a.init)
            if a.init_strength:
                body["init_image_strength"] = a.init_strength
        return run("/create-image-pixflux", body, a.out, note=f"seed={a.seed}")

    if a.cmd == "pixen":
        body = {"description": a.desc, "image_size": {"width": a.w, "height": a.h}, "no_background": a.no_bg,
                "enhance_prompt": a.enhance}
        for k in ("view", "direction", "outline", "detail", "seed"):
            if getattr(a, k) is not None:
                body[k] = getattr(a, k)
        return run("/create-image-pixen", body, a.out, note=f"seed={a.seed}", show=("enhanced_prompt", "enhance_usage"))

    if a.cmd == "rotate":
        body = {"image_size": {"width": a.size, "height": a.size}, "from_image": b64(a.src),
                "from_view": a.view, "to_view": a.view,
                "from_direction": a.from_direction, "to_direction": a.to_direction}
        if a.palette:
            body["color_image"] = b64(a.palette)
        if a.guidance is not None:
            body["image_guidance_scale"] = a.guidance
        if a.seed is not None:
            body["seed"] = a.seed
        return run("/rotate", body, a.out, note=f"seed={a.seed}")

    if a.cmd == "animate3":
        body = {"first_frame": b64(a.src), "action": a.action, "frame_count": a.frames, "no_background": True}
        if a.last:
            body["last_frame"] = b64(a.last)
        if a.seed is not None:
            body["seed"] = a.seed
        return run("/animate-with-text-v3", body, a.out, is_job=True, note=f"seed={a.seed}")

    if a.cmd == "raw":
        with open(a.json, encoding="utf-8") as f:
            body = json.load(f)
        return run(a.endpoint, body, a.out, is_job=a.job)


if __name__ == "__main__":
    sys.exit(main())
