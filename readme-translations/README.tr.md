<div align="center">

<img src="../branding/svg/ytsage-wordmark.svg" width="400" alt="ytsage-wordmark">
<img src="../branding/screenshots/main.png" width="800" alt="YTSage Arayüzü"/>

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-1f2937?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![PyPI Downloads](https://img.shields.io/pepy/dt/ytsage?color=1f2937&style=for-the-badge&label=downloads&logo=python&logoColor=white)](https://pepy.tech/project/ytsage)
[![GitHub Downloads](https://img.shields.io/github/downloads/oop7/YTSage/total?color=1f2937&style=for-the-badge&label=downloads&logo=github&logoColor=white)](https://github.com/oop7/YTSage/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-1f2937?style=for-the-badge&logo=opensource&logoColor=white)](https://opensource.org/licenses/MIT)
[![Supported Platforms](https://img.shields.io/badge/platform-cross--platform-1f2937?style=for-the-badge&logo=github&logoColor=white)](https://github.com/oop7/YTSage/releases)
[![GitHub Stars](https://img.shields.io/github/stars/oop7/YTSage?color=c90000&style=for-the-badge&logo=github&logoColor=white)](https://github.com/oop7/YTSage/stargazers)
[![PyPI version](https://img.shields.io/pypi/v/ytsage?color=c90000&style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/ytsage/)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/oop7?color=c90000&style=for-the-badge&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/oop7)

**Temiz bir PySide6 arayüzüne sahip modern bir YouTube indiricisi.**  
Videoları herhangi bir kalitede indirin, sesleri çıkarın, altyazıları alın ve daha fazlasını yapın.

### 🌍 README Dilleri

İngilizce: [EN](../README.md)
| Arapça: [AR](README.ar.md)
| Almanca: [DE](README.de.md)
| İspanyolca: [ES](README.es.md)
| Fransızca: [FR](README.fr.md)
| Hintçe: [HI](README.hi.md)
| Endonezce: [ID](README.id.md)
| İtalyanca: [IT](README.it.md)
| Japonca: [JA](README.ja.md)
| Lehçe: [PL](README.pl.md)
| Portekizce: [PT](README.pt.md)
| Rusça: [RU](README.ru.md)
| Türkçe: [TR](README.tr.md)
| Çince: [ZH](README.zh.md)

<p align="center">
  <a href="#kurulum">Kurulum</a> •
  <a href="#özellikler">Özellikler</a> •
  <a href="#kullanım">Kullanım</a> •
  <a href="#ekran-görüntüleri">Ekran Görüntüleri</a> •
  <a href="#sorun-giderme">Sorun Giderme</a> •
  <a href="#sponsor-olun">Sponsor Olun</a> •
  <a href="#katkıda-bulunma">Katkıda Bulunma</a>
</p>

</div>

---

<a id="neden-ytsage"></a>
## ❓ Neden YTSage?

YTSage, **basit ama güçlü bir YouTube indiricisi** isteyen kullanıcılar için tasarlanmıştır. Diğer araçların aksine şunları sunar:

- Modern ve temiz bir PySide6 arayüzü
- Tek tıkla video, ses ve altyazı indirme
- SponsorBlock, altyazı birleştirme ve oynatma listesi seçimi gibi gelişmiş özellikler
- yt-dlp tarafından desteklenen YouTube dışındaki siteler için isteğe bağlı "Genel Mod"
- Çoklu platform desteği ve kolay kurulum

<a id="özellikler"></a>
## ✨ Özellikler

<div align="center">

| Temel Özellikler | Gelişmiş Özellikler | Ekstra Özellikler |
|-----------------------------------|-----------------------------------------|------------------------------------|
| 🎥 Format Tablosu | 🚫 SponsorBlock Entegrasyonu | 🎞️ FPS/HDR Gösterimi |
| 🎵 Ses Çıkarma | 📝 Altyazı Seçimi ve Birleştirme | 🔄 Otomatik yt-dlp Güncellemesi |
| ✨ Basit Kullanıcı Arayüzü | 💾 Açıklama ve Küçük Resim Kaydetme | 🛠️ FFmpeg/yt-dlp/Deno Algılama |
| 📋 Oynatma Listesi Desteği | 🚀 Hız Sınırlayıcı | ⚙️ Özel Komutlar |
| 📑 Bölüm Entegrasyonu | ✂️ Video Kırpma | 🍪 Çerez ile Giriş |
| 📜 İndirme Geçmişi | 🔄 Yayın Kanalı Seçimi | 🌐 Proxy Desteği |
| 🎚️ Ses Formatı Dönüştürme | 🎬 Video Format Ayarları | 🆙 Entegre Güncelleme Sekmesi |
| 🌍 Genel Mod | 🔊 Ses Normalizasyonu (EBU R128) | 🌍 14 Dilde Yerelleştirme |
| 💾 Oynatma Listesi Dışa Aktarma | ⚙️ Varsayılan Kalite ve Altyazı | |
</div>

<a id="kurulum"></a>
## 🚀 Kurulum

### ⚡ Hızlı Kurulum (Önerilen)

YTSage'i PyPI üzerinden yükleyin:

```bash
pip install ytsage
```

<details>
<summary>🔄 Mevcut Kurulumu Güncelle</summary>

```bash
pip install --upgrade ytsage
```

</details>

Ardından uygulamayı çalıştırın:

```bash
ytsage
```

### 📦 Hazır Çalıştırılabilir Dosyalar (Executable)

> [👉 En Son Sürümü İndir](https://github.com/oop7/YTSage/releases/latest)

#### 🪟 Windows

| Format | Açıklama |
|--------|-------------|
| ![Windows EXE](https://img.shields.io/badge/Windows-EXE-0078D6?style=for-the-badge&logo=windows&logoColor=white) | Standart Kurulum Dosyası |
| ![Windows FFmpeg](https://img.shields.io/badge/Windows-FFmpeg-0078D6?style=for-the-badge&logo=windows&logoColor=white) | FFmpeg Dahil |
| ![Windows Portable](https://img.shields.io/badge/Windows-Portable-0078D6?style=for-the-badge&logo=windows&logoColor=white) | Taşınabilir Sürüm, kuruluma gerek yok |
| ![Windows Portable FFmpeg](https://img.shields.io/badge/Windows-Portable%20FFmpeg-0078D6?style=for-the-badge&logo=windows&logoColor=white) | FFmpeg Dahil Taşınabilir, sıkıştırılmış (ZIP) |

<details>
<summary>🛠️ Kurulum Adımları</summary>

1. **EXE Yükleyici (`.exe`)**: Dosyaya çift tıklayın ve kurulum sihirbazını takip edin.
2. **Taşınabilir Sürüm (`.zip`)**: Dosyayı istediğiniz yere çıkarın ve `ytsage.exe` dosyasını çalıştırın.
3. **Dahili FFmpeg**: Sisteminizde FFmpeg kurulu değilse, FFmpeg dahil olan sürümleri seçin.
</details>

#### 🐧 Linux

| Format | Açıklama |
|--------|-------------|
| ![Linux DEB](https://img.shields.io/badge/Linux-DEB-FCC624?style=for-the-badge&logo=linux&logoColor=black) | Debian Paketi |
| ![Linux AppImage](https://img.shields.io/badge/Linux-AppImage-FCC624?style=for-the-badge&logo=linux&logoColor=black) | AppImage, Taşınabilir |
| ![Linux RPM](https://img.shields.io/badge/Linux-RPM-FCC624?style=for-the-badge&logo=linux&logoColor=black) | RPM Paketi |
| ![Flathub](https://img.shields.io/badge/Linux-Flatpak-FCC624?style=for-the-badge&logo=flathub&logoColor=black) | Flatpak Paketi |

<details>
<summary>🛠️ Kurulum Adımları</summary>

- **DEB (`.deb`)**:
  ```bash
  sudo dpkg -i ytsage_*.deb
  sudo apt-get install -f # Gerekirse eksik bağımlılıkları gidermek için
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
- **Flatpak**: Flathub üzerindeki talimatları izleyin veya şunu çalıştırın:
  ```bash
  flatpak install flathub io.github.oop7.ytsage
  ```
</details>

#### 🍎 macOS

| Format | Açıklama |
|--------|-------------|
| ![macOS ARM64 APP](https://img.shields.io/badge/macOS-ARM64%20APP-000000?style=for-the-badge&logo=apple&logoColor=white) | Apple Silicon için ZIP Uygulaması |
| ![macOS ARM64 DMG](https://img.shields.io/badge/macOS-ARM64%20DMG-000000?style=for-the-badge&logo=apple&logoColor=white) | Apple Silicon için Disk Image Kurulum Dosyası |

<details>
<summary>🛠️ Kurulum Adımları</summary>

- **DMG Yükleyici (`.dmg`)**: Bağlamak için çift tıklayın ve `YTSage.app` dosyasını Uygulamalar klasörünüze sürükleyin.
- **Uygulama Arşivi (`.zip`)**: ZIP dosyasını çıkarın ve `YTSage.app` dosyasını Uygulamalar klasörünüze taşıyın.

*Not: "Uygulama hasarlı" hatası alırsanız, aşağıdaki macOS Sorun Giderme bölümüne bakın.*
</details>

---

<details>
<summary>💻 Kaynak Kodundan Manuel Kurulum</summary>

### 1. Depoyu Klonlayın

```bash
git clone https://github.com/oop7/YTSage.git
cd YTSage
```

### 2. Bağımlılıkları Yükleyin

#### ⚡ uv ile

```bash
uv pip install .
```

#### 📦 Veya standart pip ile

```bash
pip install .
```

### 3. Uygulamayı Çalıştırın

```bash
python -m ytsage.main
```

</details>

<a id="ekran-görüntüleri"></a>
## 📸 Ekran Görüntüleri

<div align="center">
<table>
  <tr>
    <td><img src="../branding/screenshots/Download-Settings.png" alt="İndirme Ayarları" width="400"/></td>
    <td><img src="../branding/screenshots/playlist.png" alt="Oynatma Listesi İndirme" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><em>İndirme Ayarları</em></td>
    <td align="center"><em>Oynatma Listesi İndirme</em></td>
  </tr>
  <tr>
    <td><img src="../branding/screenshots/audio_format.png" alt="Ses Formatı Seçimi" width="400"/></td>
    <td><img src="../branding/screenshots/Custom-Option.png" alt="Özel Seçenekler" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><em>Ses Formatı</em></td>
    <td align="center"><em>Özel Seçenekler</em></td>
  </tr>
</table>
</div>

<a id="kullanım"></a>
## 📖 Kullanım

<details>
<summary>🎯 Temel Kullanım</summary>

1. **YTSage'i başlatın**
2. **Bir YouTube URL'si yapıştırın** (veya "Paste URL" düğmesini kullanın)
3. **"Analyze" düğmesine tıklayın**
4. **Formatı Seçin:**
   - Video indirmek için `Video`
   - Sadece ses çıkarmak için `Audio Only`
5. **Seçenekleri Belirleyin:**
   - Altyazıları etkinleştirin ve dili seçin
   - Altyazı birleştirmeyi (Merge subs) etkinleştirin
   - Küçük resmi kaydet (Save thumbnail)
   - Sponsor bölümlerini kaldır (SponsorBlock)
   - Açıklamayı kaydet (Save description)
   - Bölümleri göm (Embed chapters)
6. **Çıkış Dizinini Seçin**
7. **"Download" düğmesine tıklayın**

> 💡 Varsayılan indirme dizini kullanıcının "İndirmeler" klasörüdür.

</details>

<details>
<summary>📋 Oynatma Listesi İndirme</summary>

1. **Oynatma Listesi URL'sini yapıştırın**
2. **"Analyze" düğmesine tıklayın**
3. **Seçiciden videoları seçin (varsayılan olarak tümü seçilidir)**
4. **İstediğiniz formatı/kaliteyi seçin**
5. **"Download" düğmesine tıklayın**

> 💡 Uygulama indirme kuyruğunu otomatik olarak yönetir ve oynatma listesi girişlerini `.txt`, `.csv`, `.m3u` veya `.json` dosyaları olarak dışa aktarabilirsiniz.

</details>

<details>
<summary>🌍 YouTube Dışındaki Siteler İçin Genel Mod</summary>

YTSage'in Dailymotion, TikTok ve diğerleri gibi yt-dlp tarafından desteklenen sitelerden gelen URL'leri kabul etmesini istediğinizde Genel Modu kullanın.

Nasıl kullanılır:

1. `Download Settings` bölümünü açın.
2. `Generic Mode` seçeneğini etkinleştirin.
3. YouTube dışındaki desteklenen bir video veya oynatma listesi URL'sini yapıştırın.
4. `Analyze` düğmesine tıklayın.
5. Bir format seçin ve normal şekilde indirin.

Notlar:

- Genel Mod sadece YTSage içindeki URL doğrulamasını değiştirir. Hedef site hala yüklü yt-dlp sürümünüz tarafından desteklenmelidir.
- Bazı siteler, çıkarıcıya bağlı olarak çerezler, giriş, proxy veya ek yt-dlp argümanları gerektirebilir.
- Bir site hata verirse, sorun bildirmeden önce entegre güncelleme sekmesinden yt-dlp'yi güncelleyin.

</details>

<details>
<summary>🧰 Medya ve İndirme Seçenekleri</summary>

- **Altyazı Seçenekleri:** Dilleri filtreleyin ve altyazıları video dosyasına gömün.
- **Altyazı Birleştirme:** Altyazıları video dosyasına kalıcı olarak (hardcode) birleştirir.
- **Açıklamayı Kaydet:** Video açıklamasını bir metin dosyası olarak kaydeder.
- **Küçük Resmi Kaydet:** Video küçük resmini bir resim dosyası olarak kaydeder.
- **Bölümleri Göm:** Uyumlu video oynatıcılar için meta veri olarak bölüm işaretlerini ekler.
- **Sponsor Bölümlerini Kaldır:** Videodaki sponsorlu bölümleri kaldırmak için SponsorBlock kullanır.
- **Videoyu Kırp:** Zaman aralığını `SA:DA:SA` formatında belirterek videonun sadece belirli bölümlerini indirin.

</details>

<details>
<summary>⚙️ Çıkış ve Dosya Ayarları</summary>

- **Hız Sınırlayıcı:** İndirme hızını sınırlandırın, örneğin 500 KB/s için `500K`.
- **İndirme Yolunu Kaydet:** Gelecekteki indirmeler için varsayılan indirme yolunu kaydeder. **Download Settings → Download Path** bölümünde mevcuttur.
- **Varsayılan Video Çözünürlüğü:** Otomatik seçim için tercih ettiğiniz video çözünürlüğünü ayarlayın (örn: 1080p, 720p). **Download Settings → Default Video Resolution** bölümünde mevcuttur.
- **Varsayılan Altyazı Dilleri:** Otomatik seçim için varsayılan altyazı dillerini ayarlayın (virgülle ayrılmış, örn: `tr,en`). **Download Settings → Default Subtitle Languages** bölümünde mevcuttur.
- **Dosya Adı Formatı:** Çıkış dosyası adı formatını `%(title)s`, `%(uploader)s` gibi değişkenler kullanarak özelleştirin. **Download Settings → Filename Format** bölümünde mevcuttur.
- **Çıkış Formatını Zorla:** Videoyu `mp4`, `webm` veya `mkv` gibi belirli bir konteyner formatında indirmeye zorlar. **Download Settings → Output Format Settings** bölümünde mevcuttur.
- **Ses Formatı Dönüştürme:** Sadece ses indirmelerini `AAC`, `MP3`, `FLAC`, `WAV`, `Opus`, `M4A`, `Vorbis` veya `Best` gibi tercih edilen formatlara dönüştürün. **Download Settings → Audio Format Settings** bölümünde mevcuttur.
- **Ses Normalizasyonu:** EBU R128 kullanarak sadece ses indirmeleri için ses seviyesini standartlaştırır.
- **Eşzamanlı Bağlantılar:** Dosyaları aynı anda birden fazla parça halinde indirerek indirme hızını önemli ölçüde artırın. **Download Settings → General → Concurrent Connections** bölümünde mevcuttur (Varsayılan 1, IP engellemelerini önlemek için maksimum 8-10 önerilir).

</details>

<details>
<summary>🌐 Erişim ve Ağ</summary>

- **Çerez ile Giriş:** Özel içeriğe erişmek için çerezleri kullanarak YouTube'da oturum açın.
  Kullanım:
  1. **Önerilen:** Uygulamadaki entegre `Extract cookies from browser` seçeneğini kullanın, tarayıcıyı ve isteğe bağlı olarak profili seçin.
  2. İsteğe bağlı olarak çerezleri manuel olarak çıkarın:
     a. [cookie-editor](https://github.com/moustachauve/cookie-editor) gibi bir uzantı kullanarak tarayıcınızdan çerezleri dışa aktarın.
     b. Çerezleri Netscape formatında kopyalayın.
     c. `cookies.txt` adlı bir dosya oluşturun ve çerezleri yapıştırın.
     d. Uygulamada `cookies.txt` dosyasını seçin.
- **Proxy Desteği:** İndirmeler için bir proxy sunucusu kullanın, örn: `http://<proxy-server>:<port>`
- **Genel Mod:** YTSage'in yt-dlp tarafından desteklenen YouTube dışındaki siteleri analiz etmesine ve indirmesine olanak tanır. **Download Settings → Generic Mode** bölümünden etkinleştirin.

</details>

<details>
<summary>🛠️ Araçlar ve Bakım</summary>

- **Özel Komutlar:** Komut satırı argümanları aracılığıyla gelişmiş yt-dlp özelliklerine erişin.
- **Güncelleme Sekmesi:** Entegre güncelleme araçlarını Özel Seçenekler altındaki tek bir yerden yönetin:
  - **yt-dlp Güncelleme:** Güncellemeleri kontrol edin ve Stable ile Nightly yayın kanalları arasında geçiş yapın.
  - **FFmpeg Sürüm Kontrolü:** FFmpeg sürümünüzü kontrol edin ve kurulum kılavuzlarını açın.
  - **Deno Güncelleme:** Deno çalışma zamanını kontrol edin ve güncelleyin.
- **FFmpeg/yt-dlp/Deno Algılama:** Hakkında diyaloğunda FFmpeg, yt-dlp ve Deno yollarını ve sürümlerini otomatik olarak algılar.
- **İndirme Geçmişi:** **History** düğmesi aracılığıyla küçük resimler ve durumlarla birlikte geçmiş indirmeleri görün.

</details>

<details>
<summary>🌍 Yerelleştirme</summary>

YTSage, küresel erişim için **14 dili** destekler. Tercih ettiğiniz dili **Custom Options → Language** bölümünden seçin.

### Desteklenen Diller

| Dil | Kod | Dil | Kod |
|----------|------|----------|------|
| 🇺🇸 İngilizce | `en` | 🇪🇸 İspanyolca | `es` |
| 🇸🇦 Arapça | `ar` | 🇫🇷 Fransızca | `fr` |
| 🇩🇪 Almanca | `de` | 🇮🇳 Hintçe | `hi` |
| 🇮🇩 Endonezce | `id` | 🇮🇹 İtalyanca | `it` |
| 🇯🇵 Japonca | `ja` | 🇵🇱 Lehçe | `pl` |
| 🇧🇷 Portekizce | `pt` | 🇷🇺 Rusça | `ru` |
| 🇹🇷 Türkçe | `tr` | 🇨🇳 Çince | `zh` |

### README Çevirileri

| Dil | Dosya | Dil | Dosya |
|----------|------|----------|------|
| 🇺🇸 İngilizce | [README.md](../README.md) | 🇪🇸 İspanyolca | [README.es.md](README.es.md) |
| 🇸🇦 Arapça | [README.ar.md](README.ar.md) | 🇫🇷 Fransızca | [README.fr.md](README.fr.md) |
| 🇩🇪 Almanca | [README.de.md](README.de.md) | 🇮🇳 Hintçe | [README.hi.md](README.hi.md) |
| 🇮🇩 Endonezce | [README.id.md](README.id.md) | 🇮🇹 İtalyanca | [README.it.md](README.it.md) |
| 🇯🇵 Japonca | [README.ja.md](README.ja.md) | 🇵🇱 Lehçe | [README.pl.md](README.pl.md) |
| 🇧🇷 Portekizce | [README.pt.md](README.pt.md) | 🇷🇺 Rusça | [README.ru.md](README.ru.md) |
| 🇹🇷 Türkçe | [README.tr.md](README.tr.md) | 🇨🇳 Çince | [README.zh.md](README.zh.md) |

> 💡 **Çeviriye yardımcı olmak ister misiniz?** Daha fazla dil eklememize yardımcı olmak için [Katkıda Bulunma](#katkıda-bulunma) bölümüne bakın!

</details>

<a id="sorun-giderme"></a>
## 🛠️ Sorun Giderme

<details>
<summary>Yaygın sorunlar ve çözümler için tıklayın</summary>

- **Format tablosu görünmüyor:** yt-dlp'yi en son sürüme güncelleyin ve yt-dlp Nightly kanalına geçmeyi deneyin.
- **İndirme başarısız oldu:** İnternet bağlantınızı kontrol edin ve videonun erişilebilir olduğundan emin olun.
- **Belirli İndirme Hataları:**
  - **Özel Videolar:** Özel içeriğe erişmek için çerez kimlik doğrulamasını kullanın.
  - **Yaş Sınırlı İçerik:** Yaş sınırlı videoları görüntülemek için YouTube hesabınızda oturum açın.
  - **Coğrafi Engelli Videolar:** Bölgesel kısıtlamaları aşmak için bir VPN kullanmayı düşünün.
  - **Video Kaldırıldı:** Video artık YouTube'da mevcut değildir.
  - **Canlı Yayınlar:** Canlı yayınlar yayınlanırken indirilemez; yayın bitene kadar bekleyin.
  - **Ağ Hataları:** İnternet bağlantınızı kontrol edin ve tekrar deneyin.
  - **Geçersiz URL:** URL'nin doğru olduğundan ve desteklenen bir platforma ait olduğundan emin olun.
  - **Premium İçerik:** YouTube Premium aboneliği gerektirir.
  - **Telif Hakkı Engeli:** İçerik telif hakkı kısıtlamaları nedeniyle engellenmiştir.
- **İndirme sonrası video ve ses dosyaları ayrı:** Bu durum FFmpeg eksik olduğunda veya algılanmadığında olur. YTSage, yüksek kaliteli video ve ses akışlarını birleştirmek için FFmpeg gerektirir.
  - **Çözüm:** FFmpeg'in kurulu olduğundan ve sistem PATH'inizde erişilebilir olduğundan emin olun. Windows kullanıcıları için en kolay seçenek, FFmpeg ile birlikte gelen `YTSage-v<sürüm>-ffmpeg.exe` dosyasını indirmektir.

---

#### 🛡️ Windows Defender / Antivirüs Uyarısı

Bazı antivirüs yazılımları `.exe` dosyalarını yanlış pozitif olarak işaretleyebilir. Bu, paketlenmiş uygulamaların **bilinen bir sınırlamasıdır**.

**Neden olur:**
- Antivirüs sezgiselleri paketlenmiş yürütülebilir dosyaları hatalı bir şekilde şüpheli olarak tanımlayabilir.

**Güvenli Seçenekler:**
- ✅ **pip kurulumunu kullanın:** `pip install ytsage` (önerilir)
- ✅ **Kaynaktan derleyin**: Bu [kılavuzu](../.github/CI_CD_README.md) takip ederek
- ✅ **Uygulamayı antivirüs yazılımınızın beyaz listesine ekleyin**.

#### 🍎 macOS: "Uygulama hasarlı ve açılamıyor"
macOS Sonoma veya daha yeni sürümlerde bu hatayı görüyorsanız, karantina özniteliğini kaldırmanız gerekir.

1.  **Terminal'i açın** (Spotlight kullanarak bulabilirsiniz).
2.  **Aşağıdaki komutu yazın**, ancak henüz Enter tuşuna **BASMAYIN**. Sonundaki boşluğu eklediğinizden emin olun:
    ```bash
    xattr -d com.apple.quarantine 
    ```
3.  **`YTSage.app` dosyasını Finder penceresinden sürükleyin** ve doğrudan Terminal penceresine bırakın. Bu, doğru dosya yolunu otomatik olarak yapıştıracaktır.
4.  Komutu çalıştırmak için **Enter tuşuna basın**.
5.  **YTSage.app'i tekrar açmayı deneyin.** Artık düzgün bir şekilde çalışmalıdır.

---

#### **Yapılandırma Konumu (Gelişmiş)**
- **Windows:** `%LOCALAPPDATA%\YTSage`
- **macOS:** `~/Library/Application Support/YTSage`
- **Linux:** `~/.local/share/YTSage`

</details>

<a id="sponsor-olun"></a>
## 💖 Sponsor Olun

YTSage size zaman kazandırıyorsa, projeye sponsor olmayı düşünün. Sponsorluklar geliştirme süresini, tüm platformlarda test yapmayı ve gelecekteki iyileştirmeleri karşılamaya yardımcı olur.

- GitHub Sponsors: https://github.com/sponsors/oop7
- Sponsorluk bağlantısı uygulamadaki Hakkında diyaloğu üzerinden doğrudan mevcuttur.

[![Sponsor YTSage](https://img.shields.io/badge/Sponsor-YTSage-EA4AAA?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sponsors/oop7)

<a id="katkıda-bulunma"></a>
## 👥 Katkıda Bulunma

Katkılarınız bekliyoruz! İşte nasıl yardımcı olabileceğiniz:

1. 🍴 Depoyu Fork'layın
2. 🌿 Özellik dalınızı oluşturun:
  ```bash
  git checkout -b feature/AmazingFeature
  ```
3. 💾 Değişikliklerinizi commit'leyin:
  ```bash
  git commit -m ' AmazingFeature Ekle'
  ```
4. 📤 Dalı push'layın:
  ```bash
  git push origin feature/AmazingFeature
  ```
5. 🔄 Bir Pull Request açın

### 🌍 Çevirilerle Katkıda Bulunun

- İlgili yerelleştirilmiş README dosyasını güncelleyin (örn: `readme-translations/README.tr.md`)
- Uygulama dizelerini `ytsage/languages/<code>.json` dosyasını düzenleyerek senkronize tutun
- Diliniz eksikse, `README.md` dosyasından başlayın ve `README.<code>.md` dosyasını oluşturun

<details>
<summary>📂 Proje Yapısı</summary>

## YTSage - Proje Yapısı

Bu belge YTSage'in düzenli klasör yapısını detaylandırır.

### 📁 Proje Düzeni

```
YTSage/
├── 📁 .github/                   # GitHub konfigürasyonları
│   ├── 📁 ISSUE_TEMPLATE/         # Sorun şablonları
│   │   └── 🐛-bug-report.md       # Hata raporu şablonu
│   ├─── 📁 workflows/              # GitHub Actions iş akışları
│   │   ├── build-linux.yml        # Linux derleme akışı
│   │   ├── build-macos.yml        # macOS derleme akışı
│   │   │── build-windows.yml      # Windows derleme akışı
|   |   └── release-all.yml          # Ana yayın akışı
│   └── 📄 CI_CD_README.md        # CI/CD dökümantasyonu
├──  📁 branding/                 # Marka varlıkları (ekran görüntüleri, SVG'ler)
│   ├── 📁 icons/                 # Uygulama ikonları
│   ├── 📁 screenshots/           # Dökümantasyon için ekran görüntüleri
│   └── 📁 svg/                   # SVG varlıkları
├── 📄 LICENSE                    # Lisans dosyası
├── 📄 pyproject.toml             # Proje metadatası ve bağımlılıklar
├── 📄 README.md                  # Proje dökümantasyonu
├── 📄 requirements.txt           # Python bağımlılıkları (dev)
└── 📁 ytsage/                    # Kaynak kod paketi
    ├── 📁 assets/                # Çalışma zamanı varlıkları
    │   ├── 📁 Icon/              # Uygulama ikonları
    │   └── 📁 sound/             # Ses dosyaları
    ├── 📁 languages/             # Yerelleştirme dosyaları
    │   ├── 📄 ar.json            # Arapça çeviri
    │   ├── 📄 de.json            # Almanca çeviri
    │   ├── 📄 en.json            # İngilizce çeviri
    │   └── ...                   # Diğer diller
    ├── 📁 core/                  # Temel iş mantığı
    │   ├── 📄 __init__.py        
    │   ├── 📄 ytsage_deno.py     # Deno entegrasyonu
    │   ├── 📄 ytsage_downloader.py # İndirme işlevselliği
    │   ├── 📄 ytsage_ffmpeg.py   # FFmpeg entegrasyonu
    │   ├── 📄 ytsage_utils.py    # Yardımcı fonksiyonlar
    │   └── 📄 ytsage_yt_dlp.py   # yt-dlp entegrasyonu
    ├── 📁 gui/                   # Kullanıcı arayüzü bileşenleri
    │   ├── 📄 __init__.py        
    │   ├── 📄 ytsage_gui_main.py # Ana uygulama penceresi
    │   └── 📁 ytsage_gui_dialogs/ # Diyalog sınıfları
    ├── 📁 utils/                 # Yardımcı modüller
    │   ├── 📄 __init__.py        
    │   ├── 📄 ytsage_config_manager.py # Yapılandırma yönetimi
    │   └── 📄 ytsage_logger.py   # Günlük tutma araçları
    ├── 📄 __init__.py            # Paket giriş noktası
    └── 📄 main.py                # Ana yürütme scripti
```

</details>

## ⭐️ Yıldız Geçmişi

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

## 📜 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır - detaylar için [LICENSE](../LICENSE) dosyasına bakın.

## 🙏 Teşekkürler

<details>
<summary>Teşekkürleri Göster</summary>

<div align="center">

<p>İyileştirmeler önermek veya hataları bildirmek için sorunlar açarak bu projeye katkıda bulunan herkese çok teşekkürler.</p>

<table>
    <tr class="section"><th colspan="2">Temel Bileşenler</th></tr>
    <tr>
        <td width="35%"><a href="https://github.com/yt-dlp/yt-dlp">yt-dlp</a></td>
        <td>İndirme Motoru</td>
    </tr>
    <tr>
        <td><a href="https://ffmpeg.org/">FFmpeg</a></td>
        <td>Medya İşleme</td>
    </tr>
    <tr>
        <td><a href="https://deno.com/">Deno</a></td>
        <td>yt-dlp entegrasyonu için runtime</td>
    </tr>
    <tr class="section"><th colspan="2">Kütüphaneler ve Frameworkler</th></tr>
    <tr>
        <td><a href="https://wiki.qt.io/Qt_for_Python">PySide6</a></td>
        <td>GUI Framework</td>
    </tr>
    <tr>
        <td><a href="https://python-pillow.org/">Pillow</a></td>
        <td>Resim İşleme</td>
    </tr>
    <tr>
        <td><a href="https://requests.readthedocs.io/">requests</a></td>
        <td>HTTP İstekleri</td>
    </tr>
    <tr>
        <td><a href="https://packaging.python.org/">packaging</a></td>
        <td>Sürüm ve Paket Yönetimi</td>
    </tr>
    <tr>
        <td><a href="https://python-markdown.github.io/">markdown</a></td>
        <td>Markdown İşleme</td>
    </tr>
    <tr>
        <td><a href="https://github.com/Delgan/loguru">loguru</a></td>
        <td>Günlük Kaydı</td>
    </tr>
    <tr class="section"><th colspan="2">Varlıklar ve Katkıda Bulunanlar</th></tr>
    <tr>
        <td><a href="https://pixabay.com/sound-effects/new-notification-09-352705/">Universfield'dan New Notification 09</a></td>
        <td>Bildirim Sesi</td>
    </tr>
    <tr>
        <td><a href="https://github.com/viru185">viru185</a></td>
        <td>Kod Katkıda Bulunan</td>
    </tr>
</table>

</div>

</details>

## ⚠️ Feragatname

Bu araç sadece kişisel kullanım içindir. Lütfen YouTube'un Hizmet Şartlarına ve içerik oluşturucuların haklarına saygı gösterin.

---

<div align="center">

[oop7](https://github.com/oop7) tarafından ❤️ ile yapıldı

</div>
