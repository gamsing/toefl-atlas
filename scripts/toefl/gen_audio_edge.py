#!/usr/bin/env python3
"""Synthesize missing US/UK word audio and US example readings with edge-tts.

Word Atlas already supplies UK/US lemma recordings for overlapping ids
(CC BY 4.0). This script only fills gaps, then reads every first example
in a US voice. Re-running skips files that already exist.

  pip install edge-tts
  python3 scripts/toefl/gen_audio_edge.py
  python3 scripts/toefl/gen_audio_edge.py --limit 20

Voices (Microsoft Edge neural, via the edge-tts client):
  US lemma / example: en-US-AriaNeural
  UK lemma:           en-GB-SoniaNeural
  Chinese UI lines:   zh-CN-XiaoxiaoNeural
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

import edge_tts

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_dataset import PUB, update_media_flags  # noqa: E402

US = "en-US-AriaNeural"
UK = "en-GB-SoniaNeural"
ZH = "zh-CN-XiaoxiaoNeural"

UI_LINES = {
    ROOT / "public/sfx/splash-voice.mp3": "欢迎来到托词。一词一画，点亮托福。",
    ROOT / "public/sfx/voice-galaxy-hello.mp3": "这是你的托福词汇星图。每学会一个词，就点亮一颗星。",
    ROOT / "public/sfx/voice-galaxy-lit.mp3": "今天的星星，已经点亮。",
}


def entries():
    import json

    out = []
    folder = PUB / "entries"
    for path in sorted(folder.glob("*.json"), key=lambda p: int(p.stem)):
        out.extend(json.loads(path.read_text(encoding="utf-8")))
    return out


async def synth(text: str, voice: str, dest: Path, sem: asyncio.Semaphore, force: bool = False) -> str:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not force and dest.exists() and dest.stat().st_size > 800:
        return "skip"
    async with sem:
        last = None
        for attempt in range(4):
            try:
                await edge_tts.Communicate(text, voice).save(str(dest))
                if dest.exists() and dest.stat().st_size > 400:
                    return "ok"
                last = "empty file"
            except Exception as exc:  # network hiccup; keep going
                last = str(exc)
                await asyncio.sleep(1.5 * (attempt + 1))
        print(f"fail {dest.name}: {last}", file=sys.stderr)
        return "fail"


async def run(limit: int | None, force_ui: bool) -> None:
    sem = asyncio.Semaphore(8)
    for path, text in UI_LINES.items():
        status = await synth(text, ZH, path, sem, force=force_ui or True)
        print(f"ui {path.name} {status}", flush=True)

    jobs = []
    for entry in entries():
        wid = entry["id"]
        word = entry["w"]
        if not (PUB / "audio/uk" / f"{wid}.mp3").exists():
            jobs.append((word, UK, PUB / "audio/uk" / f"{wid}.mp3"))
        if not (PUB / "audio/us" / f"{wid}.mp3").exists():
            jobs.append((word, US, PUB / "audio/us" / f"{wid}.mp3"))
        example = (entry.get("ex") or [{}])[0].get("en") or word
        jobs.append((example, US, PUB / "audio/ex" / f"{wid}.mp3"))
        if limit is not None and len(jobs) >= limit:
            break

    ok = skip = fail = 0
    pending = []
    total = len(jobs)

    async def one(i, text, voice, dest):
        status = await synth(text, voice, dest, sem)
        return i, status

    # Schedule in windows so a failure doesn't hold thousands of tasks.
    step = 80
    for start in range(0, total, step):
        batch = jobs[start : start + step]
        results = await asyncio.gather(*(one(start + n, *job) for n, job in enumerate(batch)))
        for _, status in results:
            if status == "ok":
                ok += 1
            elif status == "skip":
                skip += 1
            else:
                fail += 1
        print(f"audio {min(start + step, total)}/{total} ok={ok} skip={skip} fail={fail}", flush=True)
    print(json_summary(ok, skip, fail))
    update_media_flags()


def json_summary(ok, skip, fail) -> str:
    import json

    return json.dumps({"synthesized": ok, "skipped": skip, "failed": fail})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0, help="max new files to consider (0 = all)")
    args = parser.parse_args()
    asyncio.run(run(args.limit or None, force_ui=True))


if __name__ == "__main__":
    main()
