import os
import subprocess
import customtkinter as ctk
from tkinter import filedialog
import speech_recognition as sr
import wav_to_text
import threading
from concurrent.futures import ThreadPoolExecutor

class FolderSelectorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("wav_to_text")
        self.geometry("700x150")
        self.resizable(False, False)

        # Ana çerçeve (tek satır için)
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(padx=10, pady=20, fill="x")

        # Progress bar ve sayaç label (başlangıçta gizli)
        self.progress_frame = ctk.CTkFrame(self)
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, width=550)
        self.progress_bar.set(0)
        self.progress_bar.pack(side="left", padx=(0, 10))

        self.progress_label = ctk.CTkLabel(self.progress_frame, text="0/0", width=80)
        self.progress_label.pack(side="left")

        # Başlangıçta görünmesin
        self.progress_frame.pack_forget()

        # Textbox (klasör yolu)
        self.folder_entry = ctk.CTkEntry(self.main_frame, width=400)
        self.folder_entry.pack(side="left", padx=(0, 10), fill="x", expand=True)

        # Klasör seç butonu
        self.select_button = ctk.CTkButton(self.main_frame, text="Klasör Seç", command=self.select_folder, width=100)
        self.select_button.pack(side="left", padx=(0, 10))

        # Sesleri düzelt butonu
        self.process_button = ctk.CTkButton(self.main_frame, text="Sesi Metne Çevir", command=self.process_audio_files, width=120)
        self.process_button.pack(side="left")

        # Bilgi etiketi (alt kısım)
        self.path_label = ctk.CTkLabel(self, text="", wraplength=700, font=("Arial", 12))
        self.path_label.pack(pady=(0, 10))

        self.total_files = 0  # Toplam dosya sayısı
        self.processed_files = 0  # İşlenen dosya sayısı

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_entry.delete(0, "end")
            self.folder_entry.insert(0, folder_path)
            self.path_label.configure(text=f"Seçilen klasör:\n{folder_path}")
        else:
            self.path_label.configure(text="Klasör seçilmedi.")

    def process_audio_files(self):
        # Thread başlat
        self.progress_frame.pack(pady=(0, 10))  # Progress bar'ı görünür yap
        threading.Thread(target=self._process_audio_files_thread, daemon=True).start()

    def _process_audio_files_thread(self):
        self.path_label.configure(text="Ses dosyaları metne döndürülmeye başlandı.")

        folder_path = self.folder_entry.get().strip()
        if not folder_path or not os.path.isdir(folder_path):
            self.path_label.configure(text="Geçerli bir klasör seçilmedi.")
            return

        wav_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".wav")]

        if not wav_files:
            self.path_label.configure(text="Klasörde .wav uzantılı dosya bulunamadı.")
            return

        # "transkript" klasörünü oluştur
        transcript_folder = os.path.join(folder_path, "transkript")
        os.makedirs(transcript_folder, exist_ok=True)

        self.total_files = len(wav_files)  # Toplam dosya sayısını ayarla
        self.processed_files = 0  # Başlangıçta işlenen dosya sayısı 0

        self.progress_label.configure(text=f"{self.processed_files}/{self.total_files}")

        # Thread pool kullanarak paralel işlem
        with ThreadPoolExecutor(max_workers=64) as executor:  # İhtiyaca göre max_workers sayısını ayarlayabilirsiniz
            for filename in wav_files:
                executor.submit(self.process_single_audio, filename, folder_path, transcript_folder)

    def process_single_audio(self, filename, folder_path, transcript_folder):
        wr = wav_to_text.SpeechToText()
        recognizer = sr.Recognizer()

        original_path = os.path.join(folder_path, filename)
        name_root = os.path.splitext(filename)[0]
        ext = os.path.splitext(filename)[1]
        backup_path = os.path.join(folder_path, f"{name_root}_old{ext}")
        temp_output_path = os.path.join(folder_path, f"{name_root}_temp{ext}")

        try:
            os.rename(original_path, backup_path)
        except Exception as e:
            self.update_status(f"Hata: {filename} yeniden adlandırılamadı.\n{e}")
            return

        cmd = [
            "ffmpeg",
            "-y",
            "-i", backup_path,
            "-acodec", "pcm_s16le",
            "-ac", "1",
            "-ar", "16000",
            temp_output_path
        ]

        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            os.rename(temp_output_path, original_path)
            os.remove(backup_path)
        except subprocess.CalledProcessError:
            os.rename(backup_path, original_path)
            self.update_status(f"Hata: {filename} dönüştürülemedi.")
            return
        except Exception as e:
            self.update_status(f"Hata: {filename} işlenirken sorun oluştu.\n{e}")
            return

        try:
            with sr.AudioFile(original_path) as source:
                recognizer.adjust_for_ambient_noise(source)
                audio_data = recognizer.record(source)

            text = wr.speech_to_text(audio_data)

            # Metin dosyasını "transkript" klasörüne kaydet
            txt_path = os.path.join(transcript_folder, f"{name_root}.txt")
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(text)

        except Exception as e:
            self.update_status(f"Hata: {filename} için metne çevirme başarısız.\n{e}")
            return

        self.processed_files += 1  # İşlenen dosya sayısını artır
        self.update_status(f"{filename} başarıyla metne çevirildi.")

        # Tüm dosyalar işlendiyse son mesajı göster
        if self.processed_files == self.total_files:
            self.update_status("Tüm dosyalar başarıyla çevrildi.")

    def update_progress_bar(self):
        if self.total_files > 0:
            progress = self.processed_files / self.total_files
            self.progress_bar.set(progress)
            self.progress_label.configure(text=f"{self.processed_files}/{self.total_files}")


    def update_status(self, status_text):
        self.path_label.configure(text=status_text)
        self.update_progress_bar()


# Uygulama başlat
if __name__ == "__main__":
    app = FolderSelectorApp()
    app.mainloop()