# Sistem Tasarımı (Detaylı)

## 1. Genel Tanım
Görüntü işleme tabanlı, hedef tespiti ve takibi yapan, **ateşleme simülasyonu** içeren otonom bir eğitim sistemi.

## 2. Donanım Katmanları (Öneri)
- **Ana İşlemci:** Raspberry Pi 4B (4/8GB), soğutma + fan, endüstriyel kasa
- **Görüntüleme:** IMX477 geniş açı lens; derinlik için RealSense D435 (opsiyonel); IR aydınlatma
- **Hareket:** Yüksek tork servo; potansiyometre geri bildirimi; metal dişli; stabilizasyon
- **Sensör:** HC-SR04 x3, MPU6050 IMU, sıcaklık/nem, titreşim
- **Ateşleme:** Airsoft **simülatör**; DC motor sürücü **simülasyonu**; mühimmat sayacı; güvenlik kilidi

## 3. Yazılım Mimarisi
- `Core`: Görüntü işleme, takip, servo kontrol, ateşleme simülasyonu
- `Utils`: Kalibrasyon, loglama, güvenlik
- `AI`: Nesne tespiti, hareket tahmini, tehdit skoru
- `Interface`: Web paneli, API, mobil köprü

## 4. Ana Akış (Özet)
1. Kare yakalama → 2. Ön işleme → 3. Çoklu tespit → 4. Önceliklendirme
→ 5. Takip → 6. Hareket tahmini → 7. PID ile yönlendirme → 8. Kilit/ateşleme simülasyonu
→ 9. Güvenlik kontrolleri → 10. Görselleştirme/telemetri

## 5. Güvenlik
- Simülasyon modu varsayılan **açıktır**
- Ateşleme sadece **kilit + güvenli bölge + hız/ivme limitleri** sağlandığında
- Donanım hatalarında otomatik **fail-safe** ve kilit
