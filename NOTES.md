# Notlar

Bu dosya, projeye bir süre ara verince hatırlanması gerekenleri tutar.

## Yayın durumu

- Site şu an GitHub Pages adresinden yayında: https://omerkartli.github.io/lotus-atelier/
- 18 Ekim 2026'da `noindex` kaldırıldı; sayfalar arama motorlarına açık.
- **Kendi alan adı henüz yok.** İşyeri sahibi domain verdikten sonra aşağıdaki
  "Domain bağlanınca" listesi yapılacak.

## Domain bağlanınca yapılacaklar

1. Depo köküne `CNAME` dosyası ekle (içinde yalnızca alan adı, örn. `www.ornek.com`).
2. GitHub → Settings → Pages → Custom domain'e aynı adı yaz; DNS yayılınca "Enforce HTTPS"i işaretle.
3. DNS kayıtları (Dünya Flowers ile aynı düzen):

   | Tür | Ad | Değer |
   |---|---|---|
   | A | @ | 185.199.108.153 |
   | A | @ | 185.199.109.153 |
   | A | @ | 185.199.110.153 |
   | A | @ | 185.199.111.153 |
   | CNAME | www | omerkartli.github.io |

   Eski kayıtlar varsa silinir; MX ve TXT kayıtlarına dokunulmaz.
4. `index.html` ve `menu.html` içine yeni adresi yaz: `<link rel="canonical">`, `og:url`,
   `og:image` (paylaşım görseli) ve `LocalBusiness` JSON-LD (`url`, `sameAs`: Instagram, adres,
   telefon, çalışma saatleri). Şu an bunlar yok çünkü adres değişecek.
5. `robots.txt` ve `sitemap.xml` ekle (adresler yeni alan adıyla).
6. Google Search Console'a siteyi ekleyip sitemap'i gönder; Google işletme profilindeki
   "Web sitesi" alanına yeni adresi yaz (şu an boş, profilde "Web sitesi ekle" görünüyor).
7. Menü sayfası `menu.json`'u göreli adresle okuduğu için ayrıca bir değişiklik gerekmez.

## İşyeri sahibinden teyit beklenenler

- **WhatsApp numarası:** Rezervasyonlar `905444824334` (0544 482 43 34) numarasına
  WhatsApp mesajı olarak açılıyor (`index.html` içindeki `WA_NUMBER`). Bu numaranın
  WhatsApp'ta kayıtlı olduğu doğrulanmadı.
- **Çalışma saatleri:** Google'a göre her gün 08:30 – 00:30. Google'da Salı "01:30–00:30"
  yazıyor (yazım hatası sanılıyor); Instagram biyografisi 09:00 – 00:00 diyor. Rezervasyon saatleri
  09:00–23:00 saatlik (`SLOTS`).
- **Fotoğrafsız ürünler:** 27 ürünün fotoğrafı yok; panelden yüklenebilir.

## Teknik notlar

- Menü verisi `menu.json`, fotoğraflar `images/`; ikisi de Pages CMS panelinden yönetilir
  (`.pages.yml`). Panel sekmesi eski açık kalırsa kayıtta alanlar kaybolabilir (bir kez yaşandı) — kaydetmeden önce sayfayı yenile.
- `images/`'e yüklenen jpg/png otomatik 900 px webp'ye çevrilir (`.github/workflows/optimize-images.yml`).
- `_tools/migrate_photos.py` eski Simpra fotoğraflarını repoya taşımak için kullanıldı (108 fotoğraf); artık taşınacak link yok.
- Google'da yorum yazma bağlantısı `index.html`'deki "Yorum Yap" butonunda; doğrudan yorum penceresini açıp
  açmadığı telefonda denenmeli (açmazsa işletmenin Google sayfası açılır, oradaki "Yorum yaz" kullanılır).
