# Geliştirilmiş Hava Savunma Sistemi (Eğitim ve Simülasyon Projesi)

> **Amaç:** Görüntü işleme ile hedef tespiti, takip ve **ateşleme simülasyonu** yapan otonom bir sistemin eğitim amaçlı prototipi.
> **Not:** Bu depo yalnızca **simülasyon ve eğitim** içindir. Gerçek ateşleme mekanizmaları ile kullanılmamalıdır. Güvenlik protokollerini okuyup uygulamadan çalıştırmayın.

## Özellikler
- Gerçek zamanlı görüntü analizi (OpenCV)
- Çoklu tespit yöntemi: YOLOv5 + renk tabanlı + hareket tabanlı
- PID kontrollü servo yönlendirme (simülasyon)
- Hedef önceliklendirme ve tehdit değerlendirme (basit kurallar)
- Web paneli ve API (yerel)
- Güvenlik katmanı (kilit, fail-safe, sınırlı hız/menzil)
- Donanım soyutlama: Simülasyon modu ile donanım olmadan çalıştırılabilir

## Donanım (Öneri)
- **Raspberry Pi 4B (4/8GB)**, soğutma + endüstriyel kasa
- **Kameralar:** IMX477 (ana), Intel RealSense D435 (derinlik, opsiyonel)
- IR aydınlatma (gece)
- Yüksek torklu servo'lar (MG996R veya üstü), metal dişli mekanizma
- IMU (MPU6050), ultrasonik sensörler (HC-SR04 x3), sıcaklık/nem, titreşim
- (Simülasyon) Airsoft BB fırlatma **simülatörü**, DC motor sürücü **simülasyonu**

## Hızlı Başlangıç (Simülasyon Modu)
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/main.py --sim true --camera 0
```

## Proje Yapısı
```
src/
  core/
    vision_processing.py
    tracking_algorithm.py
    servo_controller.py
    firing_mechanism.py
  utils/
    calibration.py
    logger.py
    safety_protocols.py
  ai/
    object_detection.py
    prediction_model.py
    threat_assessment.py
  interface/
    web_dashboard.py
    api_server.py
    mobile_app_connector.py
  main.py
config/
  config.yaml
docs/
  system_design.md
```

## Uyarı ve Sorumluluk Reddi
Bu proje **eğitim/simülasyon** içindir. Her türlü gerçek mühimmat, ateşleme, insanlara/ hayvanlara/ mallara zarar verecek kullanım **yasaktır**. Yerel mevzuata uyun, kapalı test sahaları dışında kullanmayın. Geliştirici herhangi bir zarardan sorumlu değildir.
