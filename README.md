# wav_to_text

`wav_to_text` Python tabanlı bir uygulamadır. Bu uygulama, `.wav` formatındaki ses dosyalarını metne dönüştürür ve dönüştürülmüş metinleri seçilen klasördeki **transkript** adlı bir alt klasöre kaydeder. Uygulama, ses dosyalarını işlemek için FFmpeg ve ses tanıma için SpeechRecognition kütüphanesini kullanır. Aynı zamanda çoklu işlem desteği sağlayarak büyük sayıda dosyanın daha hızlı işlenmesini sağlar.

## Özellikler

- `.wav` formatındaki ses dosyalarını metne dönüştürme.
- Metin dosyalarını seçilen klasörün içinde **transkript** adlı bir alt klasöre kaydetme.
- Çoklu dosya işleme için paralel iş parçacıkları (multithreading) desteği.
- FFmpeg ile ses dosyalarını uygun formata dönüştürme.

## Gereksinimler

Bu projeyi çalıştırmak için aşağıdaki yazılımlar ve Python kütüphanelerine ihtiyacınız olacak:

### Yazılımlar:
- Python 3.x
- FFmpeg (ses dosyalarını dönüştürmek için)

### Python Kütüphaneleri:
- `speechrecognition`
- `customtkinter`
- `threading`
- `concurrent.futures`

## Kurulum

### 1. Gerekli Python Kütüphanelerini Yükleme

Proje dosyasındaki gerekli Python kütüphanelerini yüklemek için terminal veya komut istemcisine aşağıdaki komutu yazın:

```bash
pip install speechrecognition customtkinter
```

### 2. FFmpeg Yükleme

FFmpeg, ses dosyalarını işlemek için gereklidir. FFmpeg'i sisteminize yüklemek için şu adımları izleyin:

[FFmpeg indir](https://ffmpeg.org/download.html) sayfasına gidin ve işletim sisteminize uygun sürümü indirin.

İndirilen dosyayı kurun ve FFmpeg'i sistem PATH'ine ekleyin.

### 3. Projeyi Klonlama veya İndirme
GitHub'dan projeyi klonlayın veya ZIP dosyası olarak indirin.

```bash
git clone https://github.com/kullaniciadi/wav_to_text.git
cd wav_to_text
```

## Kullanım

### 1. GUI Kullanımı

Klasör Seç butonuna tıklayarak ses dosyalarının bulunduğu klasörü seçin.

Sesi Metne Çevir butonuna tıklayarak tüm .wav dosyalarını metne dönüştürün.

Her bir ses dosyası başarıyla işlendiğinde, metin dosyaları transkript klasörüne kaydedilecektir.

### 2. İşlem Sonuçları
Uygulama tüm dosyalar işlendiğinde "Tüm dosyalar başarıyla çevrildi" mesajını gösterir.

Metin dosyaları, seçilen klasördeki transkript adlı klasöre kaydedilir.
