#!/usr/bin/env python3
"""Harici (Simpra) fotoğraf linklerini indirip repoya taşır.

menu.json'da `fotoUrl` dolu, `foto` boş olan her ürün için:
  1. Fotoğraf indirilir (aynı link birden çok üründe varsa bir kez).
  2. Küçültülüp webp'ye çevrilir (optimize_images.py ile aynı ayarlar) ve images/<ürün-adı>.webp olarak kaydedilir.
  3. Ürünün `foto` alanı bu dosyanın yoluna ayarlanır, `fotoUrl` temizlenir.

İndirilemeyen (süresi dolmuş vb.) linkler olduğu gibi bırakılır ve sonda listelenir.
Betik tekrar çalıştırılabilir: taşınmış ürünleri atlar.

  python3 _tools/migrate_photos.py --dry-run   # indirir ve doğrular, hiçbir şey yazmaz
  python3 _tools/migrate_photos.py             # taşır
"""
import argparse
import io
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from optimize_images import MAX_SIDE, QUALITY  # noqa: E402
from PIL import ImageOps  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / "images"
MENU = ROOT / "menu.json"
TR = str.maketrans("çğıöşüÇĞİÖŞÜâîû", "cgiosucgiosuaiu")


def slug(text: str) -> str:
    s = text.translate(TR).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "urun"


def fetch(url: str, tries: int = 3) -> bytes:
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (menu-migration)"})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
            if not data:
                raise ValueError("boş yanıt")
            return data
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(1.5 * (i + 1))
    raise last


def to_webp_bytes(data: bytes) -> bytes:
    with Image.open(io.BytesIO(data)) as im:
        im = ImageOps.exif_transpose(im)
        if im.mode in ("P", "LA", "PA"):
            im = im.convert("RGBA")
        elif im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGB")
        im.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
        out = io.BytesIO()
        im.save(out, "WEBP", quality=QUALITY, method=6)
        return out.getvalue()


def products(menu):
    for g in menu.get("gruplar", []):
        for u in g.get("urunler", []):
            yield g, None, u
        for a in g.get("altlar", []):
            for u in a.get("urunler", []):
                yield g, a, u


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="indir ve doğrula, dosya yazma")
    args = ap.parse_args()

    menu = json.loads(MENU.read_text(encoding="utf-8"))
    todo = [u for _, _, u in products(menu) if (u.get("fotoUrl") or "").startswith("http") and not u.get("foto")]
    urls = {}
    for u in todo:
        urls.setdefault(u["fotoUrl"], []).append(u)
    print(f"{len(todo)} ürün, {len(urls)} benzersiz fotoğraf taşınacak" + (" (deneme: yazılmayacak)" if args.dry_run else ""))

    if not args.dry_run:
        IMAGES.mkdir(exist_ok=True)
    taken = {p.name for p in IMAGES.glob("*")} if IMAGES.is_dir() else set()
    ok, failed, total_bytes = 0, [], 0
    for n, (url, users) in enumerate(urls.items(), 1):
        label = ", ".join(u["ad"] for u in users)
        try:
            webp = to_webp_bytes(fetch(url))
        except Exception as e:  # noqa: BLE001
            failed.append((label, f"{type(e).__name__}: {e}"))
            print(f"[{n}/{len(urls)}] HATA  {label}: {e}")
            continue
        total_bytes += len(webp)
        ok += 1
        if args.dry_run:
            print(f"[{n}/{len(urls)}] ok    {label} ({len(webp)//1024} KB)")
            continue
        base, name, k = slug(users[0]["ad"]), None, 2
        name = f"{base}.webp"
        while name in taken:
            name = f"{base}-{k}.webp"
            k += 1
        taken.add(name)
        (IMAGES / name).write_bytes(webp)
        for u in users:
            u["foto"] = f"images/{name}"
            u["fotoUrl"] = ""
        print(f"[{n}/{len(urls)}] ok    {label} -> images/{name} ({len(webp)//1024} KB)")
        time.sleep(0.2)

    if not args.dry_run and ok:
        MENU.write_text(json.dumps(menu, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nÖzet: {ok} fotoğraf {'doğrulandı' if args.dry_run else 'taşındı'} (toplam {total_bytes//1024} KB), {len(failed)} hata")
    for label, why in failed:
        print(f"  - {label}: {why}")
    return 0 if ok or not urls else 1


if __name__ == "__main__":
    sys.exit(main())
