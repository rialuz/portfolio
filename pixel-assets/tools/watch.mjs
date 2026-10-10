// Open a page in headless Edge over the DevTools protocol and sample element positions in real time.
// usage: node watch.mjs <edge.exe> <profile dir> <file url> <seconds between samples> [screenshot.png]
import { spawn } from "node:child_process";
import { writeFileSync } from "node:fs";
const [edge, profile, url, gap, shot] = process.argv.slice(2);
const port = 9333;
const child = spawn(edge, ["--headless=new", "--disable-gpu", `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`,
  "--window-size=1460,2300", "about:blank"], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let target;
for (let i = 0; i < 40 && !target; i++) {
  await sleep(250);
  try { target = (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).find((t) => t.type === "page"); } catch {}
}
const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((r) => (ws.onopen = r));
let id = 0; const waiting = new Map();
ws.onmessage = (m) => { const d = JSON.parse(m.data); if (waiting.has(d.id)) { waiting.get(d.id)(d.result); waiting.delete(d.id); } };
const send = (method, params = {}) => new Promise((r) => { waiting.set(++id, r); ws.send(JSON.stringify({ id, method, params })); });
await send("Page.enable");
await send("Page.navigate", { url });
await sleep(1500);
const probe = `JSON.stringify([...document.querySelectorAll(".cloud,.hero .flag,.road .puff,.road .walker,.hero .luz.idle")].map(e =>
  e.className.replace("px ", "") + " x=" + Math.round(e.getBoundingClientRect().left) + " frame=" + getComputedStyle(e).backgroundPositionX))`;
const read = async () => JSON.parse((await send("Runtime.evaluate", { expression: probe })).result.value);
const a = await read();
await sleep(Number(gap) * 1000);
const b = await read();
a.forEach((line, i) => console.log(line.padEnd(46), "->", b[i], line === b[i] ? "  (no change)" : ""));
if (shot) writeFileSync(shot, Buffer.from((await send("Page.captureScreenshot", { format: "png" })).data, "base64"));
ws.close(); child.kill();
