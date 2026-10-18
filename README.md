# Lotus Atelier Chocolat — menü

Menü sayfasının verisi ve fotoğrafları. Sayfanın kendisi (`lotus-menu.html`)
`dijital-cozumlerim` reposunda durur ve bu depodaki `menu.json`'u okur.

- `menu.json` — kategoriler, alt kategoriler, ürünler, ilaveler ve alerjen notu
- `images/` — ürün fotoğrafları (panelden yüklenir)
- `.pages.yml` — yönetim paneli (Pages CMS) ayarları

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

## Yayın

GitHub Pages `main` dalının kökünden yayınlar (Settings → Pages). Menü sayfası
`https://omerkartli.github.io/lotus-atelier/menu.json` adresini okur.
