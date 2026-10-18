# Lotus Atelier Chocolat

Ormanköy'deki Lotus Atelier Chocolat'nın sitesi. Düz HTML/CSS/JS, build adımı yok;
GitHub Pages'te `main` dalının kökünden yayınlanır: https://omerkartli.github.io/lotus-atelier/

- `index.html` — ana sayfa (masa ayırtma formu hazır WhatsApp mesajı oluşturur)
- `menu.html` — menü sayfası; kategorileri, ürünleri ve fotoğrafları `menu.json` ve `images/`'ten okur
- `menu.json` — kategoriler, alt kategoriler, ürünler, ilaveler ve alerjen notu
- `images/` — ürün fotoğrafları (panelden yüklenir)
- `.pages.yml` — yönetim paneli (Pages CMS) ayarları

Sayfalar `noindex, nofollow` taşır; telefon, adres ve çalışma saatleri gerçek bilgilerle
doldurulana kadar arama motorlarına açılmaz.

## Yönetim paneli

https://app.pagescms.org → GitHub hesabıyla giriş → `lotus-atelier` → **Menü**.

- **Kategori ekle / sil / sırala:** "Kategoriler" listesinde. Sıra, listedeki sıradır; öğeler sürüklenerek taşınır.
- **Alt kategori:** Kategorinin içindeki "Alt kategoriler" listesinden eklenir.
- **Ürün:** Kategorinin (veya alt kategorinin) "Ürünler" listesinden eklenir, düzenlenir, silinir, sürüklenerek sıralanır.
- **Menüde göster:** Kapatılan ürün silinmeden menüden gizlenir.
- **Fotoğraf:** Ürün formundan yüklenir, `images/` klasörüne kaydedilir.
- Ürünü olmayan kategori ve alt kategori menüde görünmez.
- Bir ürünü başka kategoriye taşımak için yeni kategoride yeniden eklenir, eskisi silinir.

Kaydedilen her değişiklik `main` dalına commit olur; menü birkaç dakika içinde güncellenir.
