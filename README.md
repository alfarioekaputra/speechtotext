# Aplikasi Speech to Text Realtime

Aplikasi speech-to-text realtime dengan menggunakan Python (Flask) dan JavaScript tanpa perlu API pihak ketiga. Aplikasi ini menjalankan speech recognition di server lokal dan menampilkan hasilnya di browser.

## Fitur

- Pengenalan suara realtime
- Transkripsi berkelanjutan atau manual
- Simpan dan salin hasil transkripsi
- Antarmuka web yang responsif
- Tidak memerlukan API pihak ketiga (menggunakan library SpeechRecognition)

## Persyaratan

- Python 3.8+
- Flask
- SpeechRecognition
- PyAudio

## Cara Instalasi

1. Clone repository ini atau download file-file yang diperlukan
2. Buat virtual environment (opsional tapi direkomendasikan):
   ```
   python -m venv venv
   ```
3. Aktifkan virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/MacOS: `source venv/bin/activate`
4. Install dependensi:
   ```
   pip install -r requirements.txt
   ```

## Menjalankan Aplikasi

1. Jalankan server Flask:
   ```
   python app.py
   ```
2. Buka browser dan akses `http://localhost:5000`

## Struktur Proyek

```
/speech-to-text-app
    /templates
        index.html      # Antarmuka web
    /temp_audio         # Folder penyimpanan audio sementara
    app.py              # Server Flask
    requirements.txt    # Daftar dependensi
    README.md           # Dokumentasi
```

## Cara Penggunaan

1. Klik tombol "Mulai Rekam" untuk memulai perekaman
2. Bicara ke mikrofon Anda
3. Hasil transkripsi akan muncul secara otomatis
4. Klik "Berhenti" untuk menghentikan perekaman
5. Gunakan tombol "Salin Teks" untuk menyalin hasil transkripsi
6. Gunakan tombol "Bersihkan" untuk menghapus transkripsi

## Mode Perekaman

- **Berkelanjutan** - Merekam terus-menerus dalam potongan 3 detik dan mengirimkannya untuk diproses
- **Manual** - Merekam sekali dan berhenti setelah tombol "Berhenti" ditekan

## Catatan Penting

- Library SpeechRecognition menggunakan Google Speech Recognition secara default, tetapi bekerja secara lokal tanpa perlu API key
- Pastikan mikrofon Anda diaktifkan dan berfungsi dengan baik
- Anda mungkin memerlukan koneksi internet karena Google Speech Recognition menggunakan API Google
- Untuk penggunaan offline sepenuhnya, pertimbangkan untuk menggunakan mesin pengenalan suara alternatif seperti Sphinx

## Troubleshooting

### Masalah instalasi PyAudio

Pada beberapa sistem, PyAudio mungkin sulit untuk diinstal. Coba langkah-langkah berikut:

- Windows: `pip install pipwin` kemudian `pipwin install pyaudio`
- Linux: `sudo apt-get install python3-pyaudio`
- MacOS: `brew install portaudio` kemudian `pip install pyaudio`

### Izin Mikrofon

Pastikan browser Anda memberikan izin untuk mengakses mikrofon saat diminta.