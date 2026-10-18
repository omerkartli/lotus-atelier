#!/usr/bin/env python3
"""Panelden (Pages CMS) yüklenen fotoğrafları küçültüp webp'ye çevirir.

- images/ içindeki jpg/jpeg/jfif/png dosyaları webp olur (en uzun kenar MAX_SIDE'ı geçmez), özgün dosya silinir.
- Zaten webp olup MAX_SIDE'dan büyük olanlar yerinde küçültülür.
- menu.json ve icerik.json'daki "foto" yolları yeni dosya adlarına güncellenir. Fotoğraf yüklendikten sonra menü
  kaydedilirse eski adla yazılan yol da (webp'si varsa) düzeltilir; bu yüzden betik tekrar çalıştırılabilir.
"""
import json
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / "images"
JSON_FILES = [ROOT / "menu.json", ROOT / "icerik.json"]
RASTER = {".jpg", ".jpeg", ".jfif", ".png"}
MAX_SIDE = 900
QUALITY = 80


def to_webp(src: Path, dst: Path) -> None:
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)
        if im.mode in ("P", "LA", "PA"):
            im = im.convert("RGBA")
        elif im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGB")
        im.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
        im.save(dst, "WEBP", quality=QUALITY, method=6)


def optimize_images() -> dict:
    renamed = {}
    if not IMAGES.is_dir():
        return renamed
    for p in sorted(IMAGES.iterdir()):
        if not p.is_file():
            continue
        ext = p.suffix.lower()
        if ext in RASTER:
            dst, n = p.with_suffix(".webp"), 2
            while dst.exists():
                dst = p.with_name(f"{p.stem}-{n}.webp")
                n += 1
            to_webp(p, dst)
            p.unlink()
            renamed[f"images/{p.name}"] = f"images/{dst.name}"
            print(f"çevrildi: {p.name} -> {dst.name}")
        elif ext == ".webp":
            with Image.open(p) as im:
                big = max(im.size) > MAX_SIDE
            if big:
                tmp = p.with_name(p.stem + ".tmp.webp")
                to_webp(p, tmp)
                tmp.replace(p)
                print(f"küçültüldü: {p.name}")
    return renamed


def fix_json(renamed: dict) -> bool:
    any_changed = False
    for path_ in JSON_FILES:
        if not path_.is_file():
            continue
        data = json.loads(path_.read_text(encoding="utf-8"))
        changed = False

        def fix(path: str) -> str:
            if path in renamed:
                return renamed[path]
            if path.startswith("images/") and not (ROOT / path).exists():
                cand = (ROOT / path).with_suffix(".webp")
                if cand.exists():
                    return f"images/{cand.name}"
            return path

        def walk(node):
            nonlocal changed
            if isinstance(node, dict):
                for k, v in node.items():
                    if k == "foto" and isinstance(v, str) and v:
                        new = fix(v)
                        if new != v:
                            node[k] = new
                            changed = True
                    else:
                        walk(v)
            elif isinstance(node, list):
                for x in node:
                    walk(x)

        walk(data)
        if changed:
            path_.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"{path_.name} güncellendi")
            any_changed = True
    return any_changed


if __name__ == "__main__":
    fix_json(optimize_images())
