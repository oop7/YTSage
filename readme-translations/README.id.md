<div align="center">

<img src="../branding/svg/ytsage-wordmark.svg" width="400" alt="ytsage-wordmark">
<img src="../branding/screenshots/main.png" width="800" alt="YTSage Interface"/>

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-1f2937?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![PyPI Downloads](https://img.shields.io/pepy/dt/ytsage?color=1f2937&style=for-the-badge&label=downloads&logo=python&logoColor=white)](https://pepy.tech/project/ytsage)
[![GitHub Downloads](https://img.shields.io/github/downloads/oop7/YTSage/total?color=1f2937&style=for-the-badge&label=downloads&logo=github&logoColor=white)](https://github.com/oop7/YTSage/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-1f2937?style=for-the-badge&logo=opensource&logoColor=white)](https://opensource.org/licenses/MIT)
[![Supported Platforms](https://img.shields.io/badge/platform-cross--platform-1f2937?style=for-the-badge&logo=github&logoColor=white)](https://github.com/oop7/YTSage/releases)
[![GitHub Stars](https://img.shields.io/github/stars/oop7/YTSage?color=c90000&style=for-the-badge&logo=github&logoColor=white)](https://github.com/oop7/YTSage/stargazers)
[![PyPI version](https://img.shields.io/pypi/v/ytsage?color=c90000&style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/ytsage/)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/oop7?color=c90000&style=for-the-badge&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/oop7)

**Pengunduh YouTube modern dengan antarmuka PySide6 yang bersih.**  
Unduh video dalam kualitas apa pun, ekstrak audio, dapatkan subtitle, dan banyak lagi.

### 🌍 Bahasa README

Inggris: [EN](../README.md)
| Arab: [AR](README.ar.md)
| Jerman: [DE](README.de.md)
| Spanyol: [ES](README.es.md)
| Prancis: [FR](README.fr.md)
| Hindi: [HI](README.hi.md)
| Indonesia: [ID](README.id.md)
| Italia: [IT](README.it.md)
| Jepang: [JA](README.ja.md)
| Polandia: [PL](README.pl.md)
| Portugis: [PT](README.pt.md)
| Rusia: [RU](README.ru.md)
| Turki: [TR](README.tr.md)
| Mandarin: [ZH](README.zh.md)

<p align="center">
  <a href="#instalasi">Instalasi</a> •
  <a href="#fitur">Fitur</a> •
  <a href="#penggunaan">Penggunaan</a> •
  <a href="#screenshot">Screenshot</a> •
  <a href="#troubleshooting">Troubleshooting</a> •
  <a href="#sponsor">Sponsor</a> •
  <a href="#kontribusi">Kontribusi</a>
</p>

</div>

---

<a id="mengapa-ytsage"></a>
## ❓ Mengapa YTSage?

YTSage dirancang untuk pengguna yang menginginkan **pengunduh YouTube yang sederhana namun kuat**. Tidak seperti alat lainnya, ia menawarkan:

- Antarmuka PySide6 yang modern dan bersih
- Unduh video, audio, dan subtitle sekali klik
- Fitur canggih seperti SponsorBlock, penggabungan subtitle, dan pemilihan playlist
- Mode Generik Opsional untuk situs di luar YouTube yang didukung oleh yt-dlp
- Dukungan lintas platform dan instalasi mudah

<a id="fitur"></a>
## ✨ Fitur

<div align="center">

| Fitur Dasar | Fitur Lanjutan | Fitur Tambahan |
|-----------------------------------|-----------------------------------------|------------------------------------|
| 🎥 Tabel Format | 🚫 Integrasi SponsorBlock | 🎞️ Tampilan FPS/HDR |
| 🎵 Ekstraksi Audio | 📝 Pemilihan & Penggabungan Subtitle | 🔄 Pembaruan yt-dlp Otomatis |
| ✨ Antarmuka Pengguna Sederhana | 💾 Simpan Deskripsi & Thumbnail | 🛠️ Deteksi FFmpeg/yt-dlp/Deno |
| 📋 Dukungan & Pemilih Playlist | 🚀 Pembatas Kecepatan | ⚙️ Perintah Kustom |
| 📑 Integrasi Bab (Chapters) | ✂️ Potong Bagian Video | 🍪 Login Cookie |
| 📜 Riwayat Unduhan | 🔄 Pilihan Saluran Rilis | 🌐 Dukungan Proxy |
| 🎚️ Konversi Format Audio | 🎬 Pengaturan Format Video | 🆙 Tab Pembaruan Terintegrasi |
| 🌍 Mode Generik | 🔊 Normalisasi Audio (EBU R128) | 🌍 Lokalisasi dalam 14 Bahasa |
| 💾 Ekspor Playlist | ⚙️ Kualitas & Subtitle Default | |
</div>

<a id="instalasi"></a>
## 🚀 Instalasi

### ⚡ Instalasi Cepat (Direkomendasikan)

Instal YTSage melalui PyPI:

```bash
pip install ytsage
```

<details>
<summary>🔄 Perbarui Instalasi yang Ada</summary>

```bash
pip install --upgrade ytsage
```

</details>

Kemudian jalankan aplikasi:

```bash
ytsage
```

### 📦 Executable Siap Pakai (Executable)

> [👉 Unduh Rilis Terbaru](https://github.com/oop7/YTSage/releases/latest)

#### 🪟 Windows

| Format | Deskripsi |
|--------|-------------|
| ![Windows EXE](https://img.shields.io/badge/Windows-EXE-0078D6?style=for-the-badge&logo=windows&logoColor=white) | Installer Standar |
| ![Windows FFmpeg](https://img.shields.io/badge/Windows-FFmpeg-0078D6?style=for-the-badge&logo=windows&logoColor=white) | Dilengkapi dengan FFmpeg |
| ![Windows Portable](https://img.shields.io/badge/Windows-Portable-0078D6?style=for-the-badge&logo=windows&logoColor=white) | Versi Portabel, tidak perlu instalasi |
| ![Windows Portable FFmpeg](https://img.shields.io/badge/Windows-Portable%20FFmpeg-0078D6?style=for-the-badge&logo=windows&logoColor=white) | Portabel dengan FFmpeg, dikompresi (ZIP) |

<details>
<summary>🛠️ Langkah Instalasi</summary>

1. **Installer EXE (`.exe`)**: Klik dua kali pada file dan ikuti wizard pengaturan.
2. **Versi Portabel (`.zip`)**: Ekstrak arsip ke lokasi yang diinginkan dan jalankan `ytsage.exe`.
3. **FFmpeg Bawaan**: Jika Anda tidak memiliki FFmpeg di sistem Anda, pilih versi dengan FFmpeg bawaan.
</details>

#### 🐧 Linux

| Format | Deskripsi |
|--------|-------------|
| ![Linux DEB](https://img.shields.io/badge/Linux-DEB-FCC624?style=for-the-badge&logo=linux&logoColor=black) | Paket Debian |
| ![Linux AppImage](https://img.shields.io/badge/Linux-AppImage-FCC624?style=for-the-badge&logo=linux&logoColor=black) | AppImage, Portabel |
| ![Linux RPM](https://img.shields.io/badge/Linux-RPM-FCC624?style=for-the-badge&logo=linux&logoColor=black) | Paket RPM |
| ![Flathub](https://img.shields.io/badge/Linux-Flatpak-FCC624?style=for-the-badge&logo=flathub&logoColor=black) | Bundel Flatpak |

<details>
<summary>🛠️ Langkah Instalasi</summary>

- **DEB (`.deb`)**:
  ```bash
  sudo dpkg -i ytsage_*.deb
  sudo apt-get install -f # Jika perlu perbaiki dependensi yang kurang
  ```
- **RPM (`.rpm`)**:
  ```bash
  sudo rpm -i ytsage-*.rpm
  ```
- **AppImage (`.AppImage`)**:
  ```bash
  chmod +x YTSage-*.AppImage
  ./YTSage-*.AppImage
  ```
- **Flatpak**: Ikuti instruksi di Flathub atau jalankan:
  ```bash
  flatpak install flathub io.github.oop7.ytsage
  ```
</details>

#### 🍎 macOS

| Format | Deskripsi |
|--------|-------------|
| ![macOS ARM64 APP](https://img.shields.io/badge/macOS-ARM64%20APP-000000?style=for-the-badge&logo=apple&logoColor=white) | Aplikasi ZIP untuk Apple Silicon |
| ![macOS ARM64 DMG](https://img.shields.io/badge/macOS-ARM64%20DMG-000000?style=for-the-badge&logo=apple&logoColor=white) | Installer Disk Image untuk Apple Silicon |

<details>
<summary>🛠️ Langkah Instalasi</summary>

- **Installer DMG (`.dmg`)**: Klik dua kali untuk memasang, lalu tarik `YTSage.app` ke folder Applications Anda.
- **Arsip Aplikasi (`.zip`)**: Ekstrak ZIP dan pindahkan `YTSage.app` ke folder Applications Anda.

*Catatan: Jika Anda mendapatkan kesalahan "App is damaged", lihat bagian Troubleshooting macOS di bawah ini.*
</details>

---

<details>
<summary>💻 Instalasi Manual dari Sumber (Source)</summary>

### 1. Kloning Repositori

```bash
git clone https://github.com/oop7/YTSage.git
cd YTSage
```

### 2. Instal Dependensi

#### ⚡ Dengan uv

```bash
uv pip install .
```

#### 📦 Atau dengan pip standar

```bash
pip install .
```

### 3. Jalankan Aplikasi

```bash
python -m ytsage.main
```

</details>

<a id="screenshot"></a>
## 📸 Screenshot

<div align="center">
<table>
  <tr>
    <td><img src="../branding/screenshots/Download-Settings.png" alt="Pengaturan Unduhan" width="400"/></td>
    <td><img src="../branding/screenshots/playlist.png" alt="Unduhan Playlist" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><em>Pengaturan Unduhan</em></td>
    <td align="center"><em>Unduhan Playlist</em></td>
  </tr>
  <tr>
    <td><img src="../branding/screenshots/audio_format.png" alt="Pemilihan Format Audio" width="400"/></td>
    <td><img src="../branding/screenshots/Custom-Option.png" alt="Opsi Kustom" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><em>Format Audio</em></td>
    <td align="center"><em>Opsi Kustom</em></td>
  </tr>
</table>
</div>

<a id="penggunaan"></a>
## 📖 Penggunaan

<details>
<summary>🎯 Penggunaan Dasar</summary>

1. **Luncurkan YTSage**
2. **Tempel URL YouTube** (atau gunakan tombol "Paste URL")
3. **Klik "Analyze"**
4. **Pilih Format:**
   - `Video` untuk unduhan video
   - `Audio Only` untuk ekstraksi audio
5. **Pilih Opsi:**
   - Aktifkan subtitle dan pilih bahasa
   - Aktifkan penggabungan subtitle
   - Simpan thumbnail
   - Hapus bagian sponsor
   - Simpan deskripsi
   - Masukkan bab (chapters)
6. **Pilih Direktori Output**
7. **Klik "Download"**

> 💡 Direktori unduhan bawaan adalah folder "Downloads" pengguna.

</details>

<details>
<summary>📋 Unduhan Playlist</summary>

1. **Tempel URL Playlist**
2. **Klik "Analyze"**
3. **Pilih video dari pemilih playlist (opsional, default semua)**
4. **Pilih format/kualitas yang diinginkan**
5. **Klik "Download"**

> 💡 Aplikasi secara otomatis mengelola antrean unduhan, dan Anda dapat mengekspor entri playlist sebagai file `.txt`, `.csv`, `.m3u`, atau `.json`.

</details>

<details>
<summary>🌍 Mode Generik untuk Situs Selain YouTube</summary>

Gunakan Mode Generik saat Anda ingin YTSage menerima URL dari situs yang didukung oleh yt-dlp seperti Dailymotion, CBC Gem, TikTok, dan lainnya.

Cara menggunakannya:

1. Buka `Download Settings`.
2. Aktifkan `Generic Mode`.
3. Tempel URL video atau playlist yang didukung selain YouTube.
4. Klik `Analyze`.
5. Pilih format dan unduh seperti biasa.

Catatan:

- Mode Generik hanya mengubah validasi URL di dalam YTSage. Situs target harus tetap didukung oleh versi yt-dlp yang Anda instal.
- Beberapa situs memerlukan cookie, login, proxy, atau argumen yt-dlp tambahan tergantung pada ekstraktornya.
- Jika suatu situs gagal, perbarui yt-dlp dari tab pembaruan terintegrasi sebelum melaporkan masalah.

</details>

<details>
<summary>🧰 Opsi Media & Unduhan</summary>

- **Opsi Subtitle:** Filter bahasa dan masukkan subtitle ke dalam file video.
- **Penggabungan Subtitle:** Menggabungkan subtitle ke dalam file video untuk subtitle permanen (hardcoded).
- **Simpan Deskripsi:** Simpan deskripsi video sebagai file teks.
- **Simpan Thumbnail:** Simpan thumbnail video sebagai file gambar.
- **Masukkan Bab (Chapters):** Sertakan penanda bab sebagai metadata untuk pemutar video yang kompatibel.
- **Hapus Bagian Sponsor:** Gunakan SponsorBlock untuk menghapus segmen sponsor dari video.
- **Potong Video:** Unduh hanya bagian tertentu dari video dengan menentukan rentang waktu dalam format `JJ:MM:DD`.

</details>

<details>
<summary>⚙️ Pengaturan Output & File</summary>

- **Pembatas Kecepatan:** Batasi kecepatan unduhan, misalnya `500K` untuk 500 KB/s.
- **Simpan Jalur Unduhan:** Menyimpan jalur unduhan default untuk unduhan di masa mendatang. Tersedia di **Download Settings → Download Path**.
- **Resolusi Video Default:** Atur resolusi video pilihan Anda untuk pemilihan otomatis (misalnya 1080p, 720p). Tersedia di **Download Settings → Default Video Resolution**.
- **Bahasa Subtitle Default:** Atur bahasa subtitle default untuk pemilihan otomatis (dipisahkan koma, misalnya `id,en`). Tersedia di **Download Settings → Default Subtitle Languages**.
- **Format Nama File:** Sesuaikan format nama file output menggunakan variabel seperti `%(title)s`, `%(uploader)s`, `%(playlist_index)s`, dan `%(resolution)s`. Tersedia di **Download Settings → Filename Format**.
- **Paksa Format Output:** Paksa unduhan video ke format kontainer tertentu seperti `mp4`, `webm`, atau `mkv`. Tersedia di **Download Settings → Output Format Settings**.
- **Konversi Format Audio:** Konversi unduhan audio saja ke format pilihan seperti `AAC`, `MP3`, `FLAC`, `WAV`, `Opus`, `M4A`, `Vorbis`, atau `Best`. Tersedia di **Download Settings → Audio Format Settings**.
- **Normalisasi Audio:** Standarisasi volume untuk unduhan audio saja menggunakan EBU R128.
- **Koneksi Serentak:** Tingkatkan kecepatan unduhan secara signifikan dengan mengunduh file dalam beberapa bagian secara bersamaan. Tersedia di **Download Settings → General → Concurrent Connections** (default 1, maksimal 8-10 direkomendasikan untuk menghindari blokir IP).

</details>

<details>
<summary>🌐 Akses & Jaringan</summary>

- **Login Cookie:** Masuk ke YouTube menggunakan cookie untuk mengakses konten pribadi.
  Penggunaan:
  1. **Direkomendasikan:** Gunakan opsi bawaan `Extract cookies from browser` di aplikasi, lalu pilih browser dan opsional profil Anda.
  2. Secara opsional, ekstrak cookie secara manual:
     a. Ekspor cookie dari browser Anda menggunakan ekstensi seperti [cookie-editor](https://github.com/moustachauve/cookie-editor?tab=readme-ov-file)
     b. Salin cookie dalam format Netscape
     c. Buat file bernama `cookies.txt` dan tempel cookie
     d. Pilih file `cookies.txt` di aplikasi
- **Dukungan Proxy:** Gunakan server proxy untuk unduhan, misalnya `http://<server-proxy>:<port>`
- **Mode Generik:** Izinkan YTSage untuk menganalisis dan mengunduh dari situs selain YouTube yang didukung oleh yt-dlp. Aktifkan dari **Download Settings → Generic Mode**.

</details>

<details>
<summary>🛠️ Alat & Pemeliharaan</summary>

- **Perintah Kustom:** Akses fitur yt-dlp tingkat lanjut melalui argumen baris perintah.
- **Tab Pembaruan:** Kelola alat pembaruan bawaan dari satu tempat di Opsi Kustom:
  - **Pembaruan yt-dlp:** Periksa pembaruan dan beralih antara saluran rilis Stable dan Nightly.
  - **Pemeriksa Versi FFmpeg:** Verifikasi versi FFmpeg Anda dan buka panduan instalasi.
  - **Pembaruan Deno:** Periksa dan perbarui runtime Deno.
- **Deteksi FFmpeg/yt-dlp/Deno:** Secara otomatis mendeteksi jalur dan versi FFmpeg, yt-dlp, dan Deno dari dialog About.
- **Riwayat Unduhan:** Lihat unduhan sebelumnya dengan thumbnail dan status dari tombol **History**.

</details>

<details>
<summary>🌍 Lokalisasi</summary>

YTSage mendukung **14 bahasa** untuk jangkauan global. Pilih bahasa pilihan Anda di **Custom Options → Language**.

### Bahasa yang Didukung

| Bahasa | Kode | Bahasa | Kode |
|----------|------|----------|------|
| 🇺🇸 Inggris | `en` | 🇪🇸 Spanyol | `es` |
| 🇸🇦 Arab | `ar` | 🇫🇷 Prancis | `fr` |
| 🇩🇪 Jerman | `de` | 🇮🇳 Hindi | `hi` |
| 🇮🇩 Indonesia | `id` | 🇮🇹 Italia | `it` |
| 🇯🇵 Jepang | `ja` | 🇵🇱 Polandia | `pl` |
| 🇧🇷 Portugis | `pt` | 🇷🇺 Rusia | `ru` |
| 🇹🇷 Turki | `tr` | 🇨🇳 Mandarin | `zh` |

### Terjemahan README

| Bahasa | File | Bahasa | File |
|----------|------|----------|------|
| 🇺🇸 Inggris | [README.md](../README.md) | 🇪🇸 Spanyol | [README.es.md](README.es.md) |
| 🇸🇦 Arab | [README.ar.md](README.ar.md) | 🇫🇷 Prancis | [README.fr.md](README.fr.md) |
| 🇩🇪 Jerman | [README.de.md](README.de.md) | 🇮🇳 Hindi | [README.hi.md](README.hi.md) |
| 🇮🇩 Indonesia | [README.id.md](README.id.md) | 🇮🇹 Italia | [README.it.md](README.it.md) |
| 🇯🇵 Jepang | [README.ja.md](README.ja.md) | 🇵🇱 Polandia | [README.pl.md](README.pl.md) |
| 🇧🇷 Portugis | [README.pt.md](README.pt.md) | 🇷🇺 Rusia | [README.ru.md](README.ru.md) |
| 🇹🇷 Turki | [README.tr.md](README.tr.md) | 🇨🇳 Mandarin | [README.zh.md](README.zh.md) |

> 💡 **Ingin membantu menerjemahkan?** Lihat bagian [Kontribusi](#kontribusi) untuk membantu kami menambahkan lebih banyak bahasa!

</details>

<a id="troubleshooting"></a>
## 🛠️ Troubleshooting

<details>
<summary>Klik untuk melihat masalah umum dan solusinya</summary>

- **Tabel format tidak muncul:** Perbarui yt-dlp ke versi terbaru dan coba beralih ke yt-dlp Nightly.
- **Unduhan gagal:** Periksa koneksi internet Anda dan pastikan video tersedia.
- **Kesalahan Unduhan Spesifik:**
  - **Video Pribadi:** Gunakan autentikasi cookie untuk mengakses konten pribadi.
  - **Konten Dibatasi Usia:** Masuk ke akun YouTube Anda untuk melihat video yang dibatasi usia.
  - **Video yang Diblokir Geo:** Pertimbangkan menggunakan VPN untuk melewati batasan regional.
  - **Video Dihapus:** Video tidak lagi tersedia di YouTube.
  - **Live Stream:** Streaming langsung tidak dapat diunduh saat sedang disiarkan; tunggu hingga streaming selesai.
  - **Kesalahan Jaringan:** Periksa koneksi internet Anda dan coba lagi.
  - **URL Tidak Valid:** Pastikan URL benar dan berasal dari platform yang didukung.
  - **Konten Premium:** Memerlukan langganan YouTube Premium.
  - **Blokir Hak Cipta:** Konten diblokir karena pembatasan hak cipta.
- **File video dan audio terpisah setelah diunduh:** Ini terjadi ketika FFmpeg hilang atau tidak terdeteksi. YTSage memerlukan FFmpeg untuk menggabungkan aliran video dan audio berkualitas tinggi.
  - **Solusi:** Pastikan FFmpeg terinstal dan dapat diakses di PATH sistem Anda. Untuk pengguna Windows, opsi termudah adalah mengunduh file `YTSage-v<version>-ffmpeg.exe`, yang dilengkapi dengan FFmpeg.

---

#### 🛡️ Peringatan Windows Defender / Antivirus

Beberapa perangkat lunak antivirus mungkin menandai file `.exe` sebagai positif palsu (false positive). Ini adalah **batasan umum** dari aplikasi yang dipaketkan.

**Mengapa ini terjadi:**
- Heuristik antivirus mungkin salah mengidentifikasi executable yang dipaketkan sebagai mencurigakan.

**Opsi Aman:**
- ✅ **Gunakan instalasi pip:** `pip install ytsage` (direkomendasikan)
- ✅ **Build dari sumber**: Mengikuti [panduan](../.github/CI_CD_README.md) ini
- ✅ **Whitelist aplikasi** di perangkat lunak antivirus Anda.

#### 🍎 macOS: "App is damaged and can’t be opened"
Jika Anda melihat kesalahan ini di macOS Sonoma atau yang lebih baru, Anda perlu menghapus atribut karantina.

1.  **Buka Terminal** (Anda dapat menemukannya menggunakan Spotlight).
2.  **Ketik perintah berikut** tetapi **JANGAN** tekan Enter dulu. Pastikan untuk menyertakan spasi di akhir:
    ```bash
    xattr -d com.apple.quarantine 
    ```
3.  **Tarik file `YTSage.app` dari jendela Finder Anda** dan lepaskan langsung ke jendela Terminal. Ini akan secara otomatis menempelkan jalur file yang benar.
4.  **Tekan Enter** untuk menjalankan perintah.
5.  **Coba buka kembali YTSage.app.** Sekarang seharusnya dapat diluncurkan dengan benar.

---

#### **Lokasi Konfigurasi (Lanjutan)**
- **Windows:** `%LOCALAPPDATA%\YTSage`
- **macOS:** `~/Library/Application Support/YTSage`
- **Linux:** `~/.local/share/YTSage`

</details>

<a id="sponsor"></a>
## 💖 Sponsor

Jika YTSage menghemat waktu Anda, pertimbangkan untuk mensponsori proyek ini. Sponsor membantu mencakup waktu pengembangan, pengujian di semua platform, dan peningkatan di masa mendatang.

- GitHub Sponsors: https://github.com/sponsors/oop7
- Tautan sponsor tersedia langsung melalui dialog About di dalam aplikasi.

[![Sponsor YTSage](https://img.shields.io/badge/Sponsor-YTSage-EA4AAA?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sponsors/oop7)

<a id="kontribusi"></a>
## 👥 Kontribusi

Kami menerima kontribusi! Berikut cara Anda dapat membantu:

1. 🍴 Fork repositori
2. 🌿 Buat cabang fitur Anda:
  ```bash
  git checkout -b feature/FiturLuarBiasa
  ```
3. 💾 Komit perubahan Anda:
  ```bash
  git commit -m 'Tambah FiturLuarBiasa'
  ```
4. 📤 Push ke cabang:
  ```bash
  git push origin feature/FiturLuarBiasa
  ```
5. 🔄 Buka Pull Request

### 🌍 Berkontribusi pada Terjemahan

- Perbarui file README lokal yang relevan (misalnya `readme-translations/README.id.md`)
- Jaga agar string aplikasi tetap sinkron dengan mengedit `ytsage/languages/<code>.json`
- Jika bahasa Anda belum ada, mulailah dari `README.md` dan buat `README.<code>.md`

<details>
<summary>📂 Struktur Proyek</summary>

## YTSage - Struktur Proyek

Dokumen ini menjelaskan struktur folder yang terorganisir dari YTSage.

### 📁 Struktur Proyek

```
YTSage/
├── 📁 .github/                   # Konfigurasi GitHub
│   ├── 📁 ISSUE_TEMPLATE/         # Templat Issue
│   │   └── 🐛-bug-report.md       # Templat laporan bug
│   ├─── 📁 workflows/              # Alur kerja GitHub Actions
│   │   ├── build-linux.yml        # Alur kerja build Linux
│   │   ├── build-macos.yml        # Alur kerja build macOS
│   │   │── build-windows.yml      # Alur kerja build Windows
|   |   └── release-all.yml          # Alur kerja rilis master
│   └── 📄 CI_CD_README.md        # Dokumentasi CI/CD
├──  📁 branding/                 # Aset branding (screenshot, SVG)
│   ├── 📁 icons/                 # Ikon aplikasi
│   ├── 📁 screenshots/           # Screenshot untuk dokumentasi
│   └── 📁 svg/                   # Aset SVG
├── 📄 LICENSE                    # File lisensi
├── 📄 pyproject.toml             # Metadata proyek dan dependensi
├── 📄 README.md                  # Dokumentasi proyek
├── 📄 requirements.txt           # Dependensi Python (dev)
└── 📁 ytsage/                    # Paket kode sumber
    ├── 📁 assets/                # Aset runtime
    │   ├── 📁 Icon/              # Ikon aplikasi
    │   └── 📁 sound/             # File audio
    ├── 📁 languages/             # File lokalisasi
    │   ├── 📄 ar.json            # Terjemahan Arab
    │   ├── 📄 de.json            # Terjemahan Jerman
    │   ├── 📄 en.json            # Terjemahan Inggris
    │   └── ...                   # Bahasa lainnya
    ├── 📁 core/                  # Logika bisnis inti
    │   ├── 📄 __init__.py        
    │   ├── 📄 ytsage_deno.py     # Integrasi Deno
    │   ├── 📄 ytsage_downloader.py # Fungsionalitas pengunduhan
    │   ├── 📄 ytsage_ffmpeg.py   # Integrasi FFmpeg
    │   ├── 📄 ytsage_utils.py    # Fungsi utilitas
    │   └── 📄 ytsage_yt_dlp.py   # Integrasi yt-dlp
    ├── 📁 gui/                   # Komponen antarmuka pengguna
    │   ├── 📄 __init__.py        
    │   ├── 📄 ytsage_gui_main.py # Jendela utama aplikasi
    │   └── 📁 ytsage_gui_dialogs/ # Kelas dialog
    ├── 📁 utils/                 # Modul utilitas
    │   ├── 📄 __init__.py        
    │   ├── 📄 ytsage_config_manager.py # Manajemen konfigurasi
    │   └── 📄 ytsage_logger.py   # Alat logging
    ├── 📄 __init__.py            # Titik masuk paket
    └── 📄 main.py                # Skrip eksekusi utama
```

</details>

## ⭐️ Riwayat Bintang

<div align="center">

## Star History

<a href="https://www.star-history.com/#oop7/YTSage&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=oop7/YTSage&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=oop7/YTSage&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=oop7/YTSage&type=Date" />
 </picture>
</a>

</div>

## 📜 Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT - lihat file [LICENSE](../LICENSE) untuk detailnya.

## 🙏 Terima Kasih

<details>
<summary>Tampilkan Terima Kasih</summary>

<div align="center">

<p>Terima kasih banyak kepada semua orang yang telah berkontribusi pada proyek ini dengan membuka masalah untuk menyarankan perbaikan atau melaporkan bug.</p>

<table>
    <tr class="section"><th colspan="2">Komponen Utama</th></tr>
    <tr>
        <td width="35%"><a href="https://github.com/yt-dlp/yt-dlp">yt-dlp</a></td>
        <td>Mesin Pengunduhan</td>
    </tr>
    <tr>
        <td><a href="https://ffmpeg.org/">FFmpeg</a></td>
        <td>Pemrosesan Media</td>
    </tr>
    <tr>
        <td><a href="https://deno.com/">Deno</a></td>
        <td>Runtime untuk integrasi yt-dlp</td>
    </tr>
    <tr class="section"><th colspan="2">Pustaka & Framework</th></tr>
    <tr>
        <td><a href="https://wiki.qt.io/Qt_for_Python">PySide6</a></td>
        <td>Framework GUI</td>
    </tr>
    <tr>
        <td><a href="https://python-pillow.org/">Pillow</a></td>
        <td>Pemrosesan Gambar</td>
    </tr>
    <tr>
        <td><a href="https://requests.readthedocs.io/">requests</a></td>
        <td>Permintaan HTTP</td>
    </tr>
    <tr>
        <td><a href="https://packaging.python.org/">packaging</a></td>
        <td>Manajemen Versi & Pemaketan</td>
    </tr>
    <tr>
        <td><a href="https://python-markdown.github.io/">markdown</a></td>
        <td>Rendering Markdown</td>
    </tr>
    <tr>
        <td><a href="https://github.com/Delgan/loguru">loguru</a></td>
        <td>Logging</td>
    </tr>
    <tr class="section"><th colspan="2">Aset & Kontributor</th></tr>
    <tr>
        <td><a href="https://pixabay.com/sound-effects/new-notification-09-352705/">New Notification 09 oleh Universfield</a></td>
        <td>Suara Notifikasi</td>
    </tr>
    <tr>
        <td><a href="https://github.com/viru185">viru185</a></td>
        <td>Kontributor Kode</td>
    </tr>
</table>

</div>

</details>

## ⚠️ Penafian

Alat ini hanya untuk penggunaan pribadi. Harap hormati Ketentuan Layanan YouTube dan hak-hak produser konten.

---

<div align="center">

Dibuat dengan ❤️ oleh [oop7](https://github.com/oop7)

</div>
