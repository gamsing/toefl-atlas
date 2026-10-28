#!/usr/bin/env python3
"""Build the TOEFL Atlas dataset from an upstream Word Atlas checkout.

New example sentences are written for every lemma. IPA, senses, collocations,
and word families for overlapping lemmas are adapted from Word Atlas (CC BY 4.0).
Illustrations and UK/US lemma recordings are reused when the same id exists,
and listed in data/reused-from-word-atlas.json.

Usage:
  python3 scripts/toefl/build_dataset.py
  python3 scripts/toefl/build_dataset.py --upstream /tmp/word-atlas
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lexicon import (  # noqa: E402
    CEFR,
    FIRST,
    TOPICS,
    assign_topic,
    clean_tip,
    examples_for,
    include_source,
)
from supplements import SUPPLEMENTS  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
PUB = ROOT / "public" / "atlas"
DATA = ROOT / "data"
CHUNK = 100

TOPIC_INDEX = {k: i for i, (k, _) in enumerate(TOPICS)}
FIRST_INDEX = {w: i for i, w in enumerate(FIRST)}
CEFR_INDEX = {c: i for i, c in enumerate(CEFR)}

# Closest upstream topic illustration, reused as a tile (CC BY 4.0).
TOPIC_ART = {
    "campus": "topic-education.webp",
    "lecture": "topic-thinking.webp",
    "social": "topic-society.webp",
    "natural": "topic-science.webp",
    "arts": "topic-arts.webp",
    "technology": "topic-technology.webp",
    "environment": "topic-environment.webp",
    "health": "topic-health.webp",
    "business": "topic-economy.webp",
    "history": "topic-history.webp",
    "psychology": "topic-emotion.webp",
    "government": "topic-government.webp",
    "media": "topic-media.webp",
}

PALETTE = [
    (242, 196, 109), (239, 143, 107), (143, 208, 200), (159, 184, 255),
    (155, 227, 143), (255, 159, 168), (247, 217, 168), (198, 167, 255),
    (255, 211, 107), (127, 196, 255), (255, 179, 138), (134, 224, 181),
    (224, 176, 255),
]


def load_upstream(upstream: Path) -> list[dict]:
    entries = []
    folder = upstream / "public" / "atlas" / "entries"
    files = sorted(folder.glob("*.json"), key=lambda p: int(p.stem))
    if not files:
        raise SystemExit(f"no upstream entries in {folder}")
    for f in files:
        entries.extend(json.loads(f.read_text(encoding="utf-8")))
    return entries


def sort_key(entry: dict):
    cefr_i = CEFR_INDEX[entry["cefr"]]
    if entry["id"] in FIRST_INDEX:
        return (cefr_i, 0, FIRST_INDEX[entry["id"]])
    mix = int(hashlib.sha1(entry["id"].encode()).hexdigest()[:8], 16)
    return (cefr_i, 1, mix)


def transform(src: dict) -> dict:
    topic = assign_topic(src.get("topic") or "thinking", src["w"], src["id"])
    entry = {
        "id": src["id"],
        "w": src["w"],
        "uk": src.get("uk") or "",
        "us": src.get("us") or "",
        "senses": src["senses"],
        "ex": examples_for({**src, "id": src["id"]}, topic),
        "col": src.get("col") or [],
        "fam": src.get("fam") or [],
        "syn": src.get("syn") or [],
        "ant": src.get("ant") or [],
        "tip": clean_tip(src.get("tip") or "", src["id"]),
        "cefr": src["cefr"],
        "topic": topic,
        "note": (src.get("note") or "").replace("雅思", "托福").replace("IELTS", "TOEFL"),
    }
    return entry


def link_or_copy(src: Path, dst: Path) -> bool:
    if not src.exists() or src.stat().st_size < 400:
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and dst.stat().st_size == src.stat().st_size:
        return True
    if dst.exists():
        dst.unlink()
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)
    return True


def placeholder(img_path: Path, thumb_path: Path, wid: str, topic: str) -> None:
    h = int(hashlib.sha1(wid.encode()).hexdigest()[:8], 16)
    color = PALETTE[TOPIC_INDEX.get(topic, 0) % len(PALETTE)]
    im = Image.new("RGB", (512, 512), (18, 24, 42))
    d = ImageDraw.Draw(im, "RGBA")
    # Warm paper wash and a few flat shapes, so a missing illustration still reads as a card.
    d.rectangle([0, 0, 512, 512], fill=(243, 236, 223, 255))
    d.ellipse([40 + (h % 40), 36, 470, 470], fill=(*color, 230))
    d.ellipse([150 + (h % 30), 90, 430, 390], fill=(255, 248, 236, 210))
    d.rounded_rectangle([78, 300, 250, 430], radius=28, fill=(30, 38, 64, 230))
    d.polygon([(300, 360), (420, 220), (450, 400)], fill=(196, 87, 58, 235))
    d.ellipse([186, 150, 250, 214], fill=(255, 244, 220, 255))
    img_path.parent.mkdir(parents=True, exist_ok=True)
    thumb_path.parent.mkdir(parents=True, exist_ok=True)
    im.save(img_path, "WEBP", quality=72, method=4)
    im.resize((256, 256), Image.Resampling.LANCZOS).save(thumb_path, "WEBP", quality=70, method=4)


def media_bits(wid: str) -> int:
    m = 0
    if (PUB / "img" / f"{wid}.webp").exists() and (PUB / "thumb" / f"{wid}.webp").exists():
        m |= 1
    if (PUB / "audio" / "uk" / f"{wid}.mp3").exists():
        m |= 2
    if (PUB / "audio" / "us" / f"{wid}.mp3").exists():
        m |= 4
    if (PUB / "audio" / "ex" / f"{wid}.mp3").exists():
        m |= 8
    if (PUB / "audio" / "ex2" / f"{wid}.mp3").exists():
        m |= 16
    return m


def update_media_flags() -> dict:
    """Refresh media bits from files on disk. Safe to rerun after audio generation."""
    index_path = PUB / "index.json"
    index = json.loads(index_path.read_text(encoding="utf-8"))
    illustrated = voiced = uk = us = ex = 0
    for n in range((index["count"] + index["chunk"] - 1) // index["chunk"]):
        path = PUB / "entries" / f"{n}.json"
        chunk = json.loads(path.read_text(encoding="utf-8"))
        for i, entry in enumerate(chunk):
            m = media_bits(entry["id"])
            entry["m"] = m
            row = index["words"][n * index["chunk"] + i]
            if row[0] != entry["id"]:
                raise SystemExit(f"index mismatch at {entry['id']}")
            row[6] = m
            illustrated += bool(m & 1)
            uk += bool(m & 2)
            us += bool(m & 4)
            voiced += bool(m & 2 or m & 4)
            ex += bool(m & 8)
        path.write_text(json.dumps(chunk, ensure_ascii=False, separators=(",", ":")))
    index["illustrated"] = illustrated
    index["voiced"] = uk
    index_path.write_text(json.dumps(index, ensure_ascii=False, separators=(",", ":")))
    summary = {"words": index["count"], "illustrated": illustrated, "uk": uk, "us": us, "examplesAudio": ex}
    print(json.dumps(summary))
    return summary


def copy_topic_art(upstream: Path) -> None:
    brand = ROOT / "public" / "brand"
    src_brand = upstream / "public" / "brand"
    for key, filename in TOPIC_ART.items():
        src = src_brand / filename
        dst = brand / f"topic-{key}.webp"
        if src.exists():
            link_or_copy(src, dst)


def write_outputs(entries: list[dict], reused_img: list[str], reused_audio: list[str], placeholder_ids: list[str]) -> None:
    for sub in ("img", "thumb", "audio/uk", "audio/us", "audio/ex", "audio/ex2", "entries"):
        (PUB / sub).mkdir(parents=True, exist_ok=True)
    flags = [media_bits(e["id"]) for e in entries]
    for e, m in zip(entries, flags):
        e["m"] = m
    words = []
    for e, m in zip(entries, flags):
        s0 = e["senses"][0]
        zh = f'{s0["pos"]} {s0["zh"]}'.strip()
        words.append([e["id"], e["w"], zh, e["uk"] or e["us"], CEFR_INDEX[e["cefr"]], TOPIC_INDEX[e["topic"]], m])
    for n in range(0, len(entries), CHUNK):
        chunk = []
        for e in entries[n : n + CHUNK]:
            chunk.append({k: v for k, v in e.items()})
        (PUB / "entries" / f"{n // CHUNK}.json").write_text(json.dumps(chunk, ensure_ascii=False, separators=(",", ":")))
    # Drop stale chunks from a previous larger build.
    for old in (PUB / "entries").glob("*.json"):
        if int(old.stem) >= (len(entries) + CHUNK - 1) // CHUNK:
            old.unlink()
    meta = {
        "id": "toefl-atlas-open",
        "version": 1,
        "name": "TOEFL Atlas",
        "license": "CC BY 4.0",
        "count": len(entries),
        "examples": sum(len(e["ex"]) for e in entries),
        "illustrated": sum(1 for m in flags if m & 1),
        "voiced": sum(1 for m in flags if m & 2),
        "chunk": CHUNK,
        "topics": TOPICS,
        "cefr": CEFR,
        "fields": ["id", "word", "zh", "ipa", "cefr", "topic", "media"],
        "words": words,
    }
    (PUB / "index.json").write_text(json.dumps(meta, ensure_ascii=False, separators=(",", ":")))
    DATA.mkdir(exist_ok=True)
    public = [{k: v for k, v in e.items() if k != "m"} for e in entries]
    (DATA / "toefl-atlas.json").write_text(json.dumps(public, ensure_ascii=False, indent=1) + "\n")
    with (DATA / "toefl-atlas.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "word", "ipa_uk", "ipa_us", "cefr", "topic", "meanings_zh", "definition_en",
                    "example1_en", "example1_zh", "example2_en", "example2_zh", "collocations", "word_family",
                    "synonyms", "antonyms", "tip_zh"])
        for e in public:
            ex = e["ex"] + [{"en": "", "zh": ""}] * (2 - len(e["ex"]))
            w.writerow([
                e["id"], e["w"], e["uk"], e["us"], e["cefr"], e["topic"],
                " | ".join(f'{s["pos"]} {s["zh"]}' for s in e["senses"]),
                " | ".join(s["en"] for s in e["senses"]),
                ex[0]["en"], ex[0]["zh"], ex[1]["en"], ex[1]["zh"],
                " ; ".join(e["col"]), " ; ".join(e["fam"]),
                ", ".join(e["syn"]), ", ".join(e["ant"]), e["tip"],
            ])
    manifest = {
        "source": "Word Atlas (词光) by designfuchen and Word Atlas contributors",
        "sourceUrl": "https://github.com/designfuchen/word-atlas",
        "license": "CC BY 4.0",
        "whatWasReused": "For the ids listed, the illustration (img + thumb) and the UK/US lemma pronunciation were copied unchanged from Word Atlas. Senses, IPA, collocations, and word families were adapted from that dataset. Example sentences are new.",
        "placeholders": placeholder_ids,
        "imageIds": reused_img,
        "lemmaAudioIds": reused_audio,
    }
    (DATA / "reused-from-word-atlas.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n")
    print(json.dumps({
        "count": meta["count"],
        "examples": meta["examples"],
        "illustrated": meta["illustrated"],
        "voicedUk": meta["voiced"],
        "reusedImages": len(reused_img),
        "placeholders": len(placeholder_ids),
        "topics": {name: sum(1 for e in entries if e["topic"] == key) for key, name in TOPICS},
    }, ensure_ascii=False))


def build(upstream: Path) -> None:
    raw = load_upstream(upstream)
    by_id = {}
    for src in raw:
        if not include_source(src):
            continue
        entry = transform(src)
        if entry["topic"] not in TOPIC_INDEX or entry["cefr"] not in CEFR_INDEX:
            raise SystemExit(f"bad topic/cefr {entry['id']}")
        by_id[entry["id"]] = entry
    for extra in SUPPLEMENTS:
        if extra["id"] in by_id:
            continue
        topic = extra["topic"]
        entry = {
            "id": extra["id"],
            "w": extra["w"],
            "uk": extra["uk"],
            "us": extra["us"],
            "senses": extra["senses"],
            "ex": extra["ex"],
            "col": extra["col"],
            "fam": extra["fam"],
            "syn": extra.get("syn") or [],
            "ant": extra.get("ant") or [],
            "tip": extra.get("tip") or "",
            "cefr": extra["cefr"],
            "topic": topic,
            "note": extra.get("note") or "",
        }
        # Prefer the hand-written examples; still run them through the headword check below.
        by_id[entry["id"]] = entry
    entries = list(by_id.values())
    entries.sort(key=sort_key)
    ids = [e["id"] for e in entries]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate ids")
    for e in entries:
        if len(e["ex"]) < 2:
            raise SystemExit(f"need two examples: {e['id']}")
        for ex in e["ex"]:
            if e["w"].lower() not in ex["en"].lower() or not ex["zh"]:
                raise SystemExit(f"example missing headword or translation: {e['id']}: {ex['en']}")
        if not e["senses"] or not e["senses"][0]["zh"]:
            raise SystemExit(f"no sense: {e['id']}")
    reused_img, reused_audio, placeholders = [], [], []
    src_img = upstream / "public" / "atlas" / "img"
    src_thumb = upstream / "public" / "atlas" / "thumb"
    for e in entries:
        wid = e["id"]
        img_src = src_img / f"{wid}.webp"
        thumb_src = src_thumb / f"{wid}.webp"
        if img_src.exists() and img_src.stat().st_size > 400:
            link_or_copy(img_src, PUB / "img" / f"{wid}.webp")
            if not link_or_copy(thumb_src, PUB / "thumb" / f"{wid}.webp"):
                with Image.open(PUB / "img" / f"{wid}.webp") as im:
                    thumb = PUB / "thumb" / f"{wid}.webp"
                    thumb.parent.mkdir(parents=True, exist_ok=True)
                    im.convert("RGB").resize((256, 256), Image.Resampling.LANCZOS).save(thumb, "WEBP", quality=70, method=4)
            reused_img.append(wid)
        else:
            placeholder(PUB / "img" / f"{wid}.webp", PUB / "thumb" / f"{wid}.webp", wid, e["topic"])
            placeholders.append(wid)
        got_uk = link_or_copy(upstream / "public" / "atlas" / "audio" / "uk" / f"{wid}.mp3", PUB / "audio" / "uk" / f"{wid}.mp3")
        got_us = link_or_copy(upstream / "public" / "atlas" / "audio" / "us" / f"{wid}.mp3", PUB / "audio" / "us" / f"{wid}.mp3")
        if got_uk or got_us:
            reused_audio.append(wid)
    copy_topic_art(upstream)
    write_outputs(entries, reused_img, reused_audio, placeholders)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--upstream", default="/tmp/word-atlas")
    p.add_argument("--flags-only", action="store_true", help="recompute media bits from files")
    args = p.parse_args()
    if args.flags_only:
        update_media_flags()
        return
    build(Path(args.upstream))


if __name__ == "__main__":
    main()
