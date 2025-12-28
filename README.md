# Alotech Record to Text

WAV ses dosyalarını otomatik olarak metne dönüştüren bir Python masaüstü uygulaması.

## Özellikler

- 📁 Toplu dosya işleme - Klasördeki tüm WAV dosyalarını aynı anda işleyebilir
- 🎯 Türkçe dil desteği - Google Speech Recognition API ile Türkçe ses tanıma
- ⚡ Paralel işleme - 64 thread ile hızlı dönüştürme
- 🖥️ Modern arayüz - CustomTkinter ile kullanıcı dostu GUI
- 📊 İlerleme takibi - Progress bar ile işlem durumu gösterimi

## Gereksinimler

- Python 3.7+
- FFmpeg (sistem PATH'inde olmalı)

## Kurulum

1. Depoyu klonlayın:
```bash
git clone https://github.com/Emre-Kahveci/alotech-record-to-text.git
cd alotech-record-to-text
```

2. Bağımlılıkları yükleyin:
```bash
pip install customtkinter SpeechRecognition
```

3. FFmpeg'i yükleyin:
   - Windows: [FFmpeg İndir](https://ffmpeg.org/download.html) ve PATH'e ekleyin
   - Linux: `sudo apt install ffmpeg`
   - macOS: `brew install ffmpeg`

## Kullanım

1. Uygulamayı başlatın:
```bash
python gui.py
```

2. "Klasör Seç" butonuna tıklayın ve WAV dosyalarının bulunduğu klasörü seçin

3. "Sesi Metne Çevir" butonuna tıklayın

4. Dönüştürülen metinler seçilen klasör içindeki `transkript` klasörüne kaydedilir

## Proje Yapısı

```
alotech-record-to-text/
├── gui.py          # Ana uygulama ve GUI
├── wav_to_text.py  # Ses tanıma modülü
├── .gitignore
└── README.md
```

## Lisans

MIT License
