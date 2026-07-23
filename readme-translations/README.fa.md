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

**یک دانلودکننده مدرن یوتیوب با رابط کاربری تمیز PySide6.**  
ویدیوها را با هر کیفیتی دانلود کنید، صدا را استخراج کنید، زیرنویس‌ها را دریافت کنید و موارد دیگر.

### 🌍 زبان‌های README

انگلیسی: [EN](../README.md)
| عربی: [AR](README.ar.md)
| آلمانی: [DE](README.de.md)
| اسپانیایی: [ES](README.es.md)
| فرانسوی: [FR](README.fr.md)
| هندی: [HI](README.hi.md)
| اندونزیایی: [ID](README.id.md)
| ایتالیایی: [IT](README.it.md)
| ژاپنی: [JA](README.ja.md)
| لهستانی: [PL](README.pl.md)
| پرتغالی: [PT](README.pt.md)
| روسی: [RU](README.ru.md)
| ترکی: [TR](README.tr.md)
| چینی: [ZH](README.zh.md)
| فارسی: [FA](README.fa.md)


<p align="center">
  <a href="#installation">نصب</a> •
  <a href="#features">امکانات</a> •
  <a href="#usage">استفاده</a> •
  <a href="#screenshots">تصاویر</a> •
  <a href="#troubleshooting">عیب‌یابی</a> •
  <a href="#sponsor">حمایت مالی</a> •
  <a href="#contributing">مشارکت</a>
</p>

</div>

---

<a id="why-ytsage"></a>
## ❓ چرا YTSage؟

YTSage برای کاربرانی طراحی شده که به دنبال یک **دانلودکننده یوتیوب ساده اما قدرتمند** هستند. برخلاف سایر ابزارها، این برنامه موارد زیر را ارائه می‌دهد:

- رابط کاربری مدرن و تمیز PySide6
- دانلود با یک کلیک برای ویدیو، صدا و زیرنویس
- امکانات پیشرفته مانند SponsorBlock، ادغام زیرنویس و انتخاب پلی‌لیست
- حالت عمومی (Generic Mode) اختیاری برای سایت‌های پشتیبانی‌شده توسط yt-dlp فراتر از یوتیوب
- پشتیبانی چندسکویی و نصب آسان

<a id="features"></a>
## ✨ امکانات

<div align="center">

| امکانات پایه | امکانات پیشرفته | امکانات تکمیلی |
|-----------------------------------|-----------------------------------------|------------------------------------|
| 🎥 جدول فرمت‌ها | 🚫 یکپارچه‌سازی SponsorBlock | 🎞️ نمایش FPS/HDR |
| 🎵 استخراج صدا | 📝 انتخاب و ادغام زیرنویس | 🔄 به‌روزرسانی خودکار yt-dlp |
| ✨ رابط کاربری ساده | 💾 ذخیره توضیحات و تصویر بندانگشتی | 🛠️ شناسایی FFmpeg/yt-dlp/Deno |
| 📋 پشتیبانی و انتخابگر پلی‌لیست | 🚀 محدودکننده سرعت | ⚙️ دستورات سفارشی |
| 📑 یکپارچه‌سازی فصل‌ها | ✂️ برش بخش‌های ویدیو | 🍪 ورود با کوکی |
| 📜 تاریخچه دانلود | 🔄 انتخاب کانال نسخه | 🌐 پشتیبانی پروکسی |
| 🎚️ تبدیل فرمت صدا | 🎬 تنظیمات فرمت ویدیو | 🆙 تب به‌روزرسانی یکپارچه |
| 🌍 حالت عمومی | 🔊 نرمال‌سازی صدا (EBU R128) | 🌍 محلی‌سازی به ۱۴ زبان |
| 💾 خروجی گرفتن پلی‌لیست | ⚙️ کیفیت و زیرنویس پیش‌فرض | |
</div>

<a id="installation"></a>
## 🚀 نصب

### ⚡ نصب سریع (پیشنهادی)

YTSage را از طریق PyPI نصب کنید:

```bash
pip install ytsage
```

<details>
<summary>🔄 به‌روزرسانی یک نصب موجود</summary>

```bash
pip install --upgrade ytsage
```

</details>

سپس برنامه را اجرا کنید:

```bash
ytsage
```

### 📦 فایل‌های اجرایی از پیش ساخته‌شده

> [👉 دانلود آخرین نسخه](https://github.com/oop7/YTSage/releases/latest)

#### 🪟 ویندوز

| فرمت | توضیحات |
|--------|-------------|
| ![Windows EXE](https://img.shields.io/badge/Windows-EXE-0078D6?style=for-the-badge&logo=windows&logoColor=white) | نصب‌کننده استاندارد |
| ![Windows FFmpeg](https://img.shields.io/badge/Windows-FFmpeg-0078D6?style=for-the-badge&logo=windows&logoColor=white) | همراه با FFmpeg |
| ![Windows Portable](https://img.shields.io/badge/Windows-Portable-0078D6?style=for-the-badge&logo=windows&logoColor=white) | نسخه پرتابل، بدون نیاز به نصب |
| ![Windows Portable FFmpeg](https://img.shields.io/badge/Windows-Portable%20FFmpeg-0078D6?style=for-the-badge&logo=windows&logoColor=white) | پرتابل همراه با FFmpeg، فشرده‌شده |

<details>
<summary>🛠️ مراحل نصب</summary>

1. **نصب‌کننده EXE (`.exe`)**: روی فایل دوبار کلیک کرده و مراحل نصب را دنبال کنید.
2. **نسخه پرتابل (`.zip`)**: آرشیو را در مکان دلخواه استخراج کرده و `ytsage.exe` را اجرا کنید.
3. **همراه با FFmpeg**: در صورتی که FFmpeg روی سیستم شما نصب نیست، نسخه‌های همراه با FFmpeg را انتخاب کنید.
</details>

#### 🐧 لینوکس

| فرمت | توضیحات |
|--------|-------------|
| ![Linux DEB](https://img.shields.io/badge/Linux-DEB-FCC624?style=for-the-badge&logo=linux&logoColor=black) | بسته دبیان |
| ![Linux AppImage](https://img.shields.io/badge/Linux-AppImage-FCC624?style=for-the-badge&logo=linux&logoColor=black) | AppImage، پرتابل |
| ![Linux RPM](https://img.shields.io/badge/Linux-RPM-FCC624?style=for-the-badge&logo=linux&logoColor=black) | بسته RPM |
| ![Flathub](https://img.shields.io/badge/Linux-Flatpak-FCC624?style=for-the-badge&logo=flathub&logoColor=black) | بسته Flatpak |

<details>
<summary>🛠️ مراحل نصب</summary>

- **DEB (`.deb`)**:
  ```bash
  sudo dpkg -i ytsage_*.deb
  sudo apt-get install -f # در صورت نیاز، وابستگی‌های ناقص را رفع می‌کند
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
- **Flatpak**: دستورالعمل‌های موجود در Flathub را دنبال کنید یا اجرا کنید:
  ```bash
  flatpak install flathub io.github.oop7.ytsage
  ```
</details>

#### 🍎 macOS

| فرمت | توضیحات |
|--------|-------------|
| ![macOS ARM64 APP](https://img.shields.io/badge/macOS-ARM64%20APP-000000?style=for-the-badge&logo=apple&logoColor=white) | برنامه فشرده‌شده برای Apple Silicon |
| ![macOS ARM64 DMG](https://img.shields.io/badge/macOS-ARM64%20DMG-000000?style=for-the-badge&logo=apple&logoColor=white) | نصب‌کننده تصویر دیسک برای Apple Silicon |

<details>
<summary>🛠️ مراحل نصب</summary>

- **نصب‌کننده DMG (`.dmg`)**: برای مانت کردن دوبار کلیک کنید، سپس `YTSage.app` را به پوشه Applications بکشید.
- **آرشیو برنامه (`.zip`)**: فایل zip را استخراج کرده و `YTSage.app` را به پوشه Applications منتقل کنید.

*توجه: اگر با خطای "برنامه آسیب دیده است" مواجه شدید، به بخش عیب‌یابی macOS در پایین مراجعه کنید.*
</details>

---

<details>
<summary>💻 نصب دستی از کد منبع</summary>

### ۱. کلون کردن مخزن

```bash
git clone https://github.com/oop7/YTSage.git
cd YTSage
```

### ۲. نصب وابستگی‌ها

#### ⚡ با uv

```bash
uv pip install .
```

#### 📦 یا با pip استاندارد

```bash
pip install .
```

### ۳. اجرای برنامه

```bash
python -m ytsage.main
```

</details>

<a id="screenshots"></a>
## 📸 تصاویر

<div align="center">
<table>
  <tr>
    <td><img src="../branding/screenshots/Download-Settings.png" alt="تنظیمات دانلود" width="400"/></td>
    <td><img src="../branding/screenshots/playlist.png" alt="دانلود پلی‌لیست" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><em>تنظیمات دانلود</em></td>
    <td align="center"><em>دانلود پلی‌لیست</em></td>
  </tr>
  <tr>
    <td><img src="../branding/screenshots/audio_format.png" alt="انتخاب فرمت صدا" width="400"/></td>
    <td><img src="../branding/screenshots/Custom-Option.png" alt="گزینه‌های سفارشی" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><em>فرمت صدا</em></td>
    <td align="center"><em>گزینه‌های سفارشی</em></td>
  </tr>
</table>
</div>

<a id="usage"></a>
## 📖 استفاده

<details>
<summary>🎯 استفاده پایه</summary>

1. **YTSage را اجرا کنید**
2. **لینک یوتیوب را بچسبانید** (یا از دکمه "Paste URL" استفاده کنید)
3. **روی "Analyze" کلیک کنید**
4. **فرمت را انتخاب کنید:**
   - `Video` برای دانلود ویدیو
   - `Audio Only` برای استخراج صدا
5. **گزینه‌ها را انتخاب کنید:**
   - فعال‌سازی زیرنویس و انتخاب زبان
   - فعال‌سازی ادغام زیرنویس
   - ذخیره تصویر بندانگشتی
   - حذف بخش‌های اسپانسری
   - ذخیره توضیحات
   - یکپارچه‌سازی فصل‌ها
6. **پوشه خروجی را انتخاب کنید**
7. **روی "Download" کلیک کنید**

> 💡 پوشه دانلود پیش‌فرض، پوشه "Downloads" کاربر است.

</details>

<details>
<summary>📋 دانلود پلی‌لیست</summary>

1. **لینک پلی‌لیست را بچسبانید**
2. **روی "Analyze" کلیک کنید**
3. **ویدیوها را از انتخابگر پلی‌لیست انتخاب کنید (اختیاری، به‌طور پیش‌فرض همه انتخاب می‌شوند)**
4. **فرمت/کیفیت مورد نظر را انتخاب کنید**
5. **روی "Download" کلیک کنید**

> 💡 برنامه به‌طور خودکار صف دانلود را مدیریت می‌کند، و می‌توانید ورودی‌های پلی‌لیست را به فرمت `.txt`، `.csv`، `.m3u` یا `.json` خروجی بگیرید.

</details>

<details>
<summary>🌍 حالت عمومی برای سایت‌های غیر یوتیوبی</summary>

از حالت عمومی (Generic Mode) زمانی استفاده کنید که می‌خواهید YTSage لینک‌هایی از سایت‌های پشتیبانی‌شده توسط yt-dlp، مانند Dailymotion، CBC Gem، TikTok و سایرین را بپذیرد.

نحوه استفاده:

1. `Download Settings` را باز کنید.
2. `Generic Mode` را فعال کنید.
3. لینک ویدیو یا پلی‌لیست پشتیبانی‌شده‌ای که یوتیوب نیست را بچسبانید.
4. روی `Analyze` کلیک کنید.
5. یک فرمت انتخاب کرده و مانند همیشه دانلود کنید.

نکات:

- حالت عمومی فقط اعتبارسنجی لینک را در داخل YTSage تغییر می‌دهد. سایت مقصد همچنان باید توسط نسخه نصب‌شده yt-dlp شما پشتیبانی شود.
- برخی سایت‌ها بسته به استخراج‌کننده، نیاز به کوکی، نشست ورود، پروکسی یا آرگومان‌های اضافی yt-dlp دارند.
- اگر سایتی با شکست مواجه شد، ابتدا yt-dlp را از تب به‌روزرسانی یکپارچه به‌روز کنید و سپس مشکل را گزارش دهید.

</details>

<details>
<summary>🧰 گزینه‌های رسانه و دانلود</summary>

- **گزینه‌های زیرنویس:** فیلتر زبان‌ها و یکپارچه‌سازی زیرنویس در فایل ویدیو.
- **ادغام زیرنویس:** ادغام زیرنویس در فایل ویدیو برای زیرنویس‌های چسبیده (hardcoded).
- **ذخیره توضیحات:** ذخیره توضیحات ویدیو به‌صورت فایل متنی.
- **ذخیره تصویر بندانگشتی:** ذخیره تصویر بندانگشتی ویدیو به‌صورت فایل تصویری.
- **یکپارچه‌سازی فصل‌ها:** یکپارچه‌سازی نشانگرهای فصل به‌عنوان فراداده برای پخش‌کننده‌های ویدیوی سازگار.
- **حذف بخش‌های اسپانسری:** حذف بخش‌های اسپانسری از ویدیو با استفاده از SponsorBlock.
- **برش ویدیو:** فقط بخش‌های خاصی از یک ویدیو را با مشخص کردن بازه‌های زمانی به فرمت `HH:MM:SS` دانلود کنید.

</details>

<details>
<summary>⚙️ تنظیمات خروجی و فایل</summary>

- **محدودکننده سرعت:** محدود کردن سرعت دانلود، برای مثال `500K` برای ۵۰۰ کیلوبایت بر ثانیه.
- **ذخیره مسیر دانلود:** مسیر دانلود پیش‌فرض را برای دانلودهای آینده ذخیره می‌کند. در **Download Settings → Download Path** موجود است.
- **وضوح تصویر پیش‌فرض ویدیو:** وضوح تصویر ترجیحی خود را برای انتخاب خودکار به‌طور پیش‌فرض تنظیم کنید (مثلاً 1080p، 720p). در **Download Settings → Default Video Resolution** موجود است.
- **زبان‌های زیرنویس پیش‌فرض:** زبان‌های زیرنویس پیش‌فرض را برای انتخاب خودکار تنظیم کنید (با کاما جدا شوند، مثلاً `fr,en`). در **Download Settings → Default Subtitle Languages** موجود است.
- **فرمت نام فایل خروجی:** فرمت نام فایل خروجی را با استفاده از متغیرهایی مانند `%(title)s`، `%(uploader)s`، `%(playlist_index)s` و `%(resolution)s` سفارشی‌سازی کنید. در **Download Settings → Filename Format** موجود است.
- **اجبار فرمت خروجی:** دانلودهای ویدیو را به فرمت کانتینر خاصی مانند `mp4`، `webm` یا `mkv` اجبار کنید. در **Download Settings → Output Format Settings** موجود است.
- **تبدیل فرمت صدا:** دانلودهای فقط صوتی را به فرمت‌های ترجیحی مانند `AAC`، `MP3`، `FLAC`، `WAV`، `Opus`، `M4A`، `Vorbis` یا `Best` تبدیل کنید. در **Download Settings → Audio Format Settings** موجود است.
- **نرمال‌سازی صدا:** استانداردسازی حجم صدا برای دانلودهای فقط صوتی با استفاده از EBU R128.
- **اتصالات همزمان:** سرعت دانلود را با دانلود فایل‌ها در چندین قطعه به‌صورت همزمان به‌طور قابل توجهی افزایش دهید. در **Download Settings → General → Concurrent Connections** موجود است (پیش‌فرض ۱، حداکثر پیشنهادی ۸ تا ۱۰ برای جلوگیری از محدودیت IP).

</details>

<details>
<summary>🌐 دسترسی و شبکه</summary>

- **ورود با کوکی:** با استفاده از کوکی‌ها به یوتیوب وارد شوید تا به محتوای خصوصی دسترسی داشته باشید.
  نحوه استفاده:
  1. **پیشنهادی:** از گزینه یکپارچه `Extract cookies from browser` در برنامه استفاده کرده، سپس مرورگر و در صورت لزوم یک پروفایل را انتخاب کنید.
  2. یا به‌طور جایگزین، کوکی‌ها را به‌صورت دستی استخراج کنید:
     الف. کوکی‌های مرورگر خود را با استفاده از افزونه‌ای مانند [cookie-editor](https://github.com/moustachauve/cookie-editor?tab=readme-ov-file) خروجی بگیرید
     ب. کوکی‌ها را به فرمت Netscape کپی کنید
     ج. فایلی با نام `cookies.txt` ایجاد کرده و کوکی‌ها را در آن بچسبانید
     د. فایل `cookies.txt` را در برنامه انتخاب کنید
- **پشتیبانی پروکسی:** از یک سرور پروکسی برای دانلودها استفاده کنید، برای مثال `http://<proxy-server>:<port>`
- **حالت عمومی:** به YTSage اجازه می‌دهد از سایت‌های غیر یوتیوبی پشتیبانی‌شده توسط yt-dlp تحلیل و دانلود کند. آن را از **Download Settings → Generic Mode** فعال کنید.

</details>

<details>
<summary>🛠️ ابزارها و نگهداری</summary>

- **دستورات سفارشی:** به امکانات پیشرفته yt-dlp از طریق آرگومان‌های خط فرمان دسترسی پیدا کنید.
- **تب به‌روزرسانی:** ابزارهای به‌روزرسانی یکپارچه را از یک مکان در تنظیمات سفارشی مدیریت کنید:
  - **به‌روزرسانی‌های yt-dlp:** بررسی به‌روزرسانی‌ها و جابه‌جایی بین کانال‌های نسخه پایدار و شبانه.
  - **بررسی‌کننده نسخه FFmpeg:** نسخه FFmpeg خود را بررسی کرده و راهنماهای نصب را باز کنید.
  - **به‌روزرسانی‌های Deno:** بررسی و به‌روزرسانی موتور اجرای Deno.
- **شناسایی FFmpeg/yt-dlp/Deno:** مسیرها و نسخه‌های FFmpeg، yt-dlp و Deno را به‌طور خودکار از پنجره درباره شناسایی می‌کند.
- **تاریخچه دانلود:** دانلودهای گذشته را همراه با تصاویر بندانگشتی و وضعیت آن‌ها از دکمه **History** مشاهده کنید.

</details>

<details>
<summary>🌍 محلی‌سازی</summary>

YTSage از **۱۴ زبان** برای دسترسی‌پذیری جهانی پشتیبانی می‌کند. زبان ترجیحی خود را از **Custom Options → Language** انتخاب کنید.

### زبان‌های پشتیبانی‌شده

| زبان | کد | زبان | کد |
|----------|------|----------|------|
| 🇺🇸 انگلیسی | `en` | 🇪🇸 اسپانیایی | `es` |
| 🇸🇦 عربی | `ar` | 🇫🇷 فرانسوی | `fr` |
| 🇩🇪 آلمانی | `de` | 🇮🇳 هندی | `hi` |
| 🇮🇩 اندونزیایی | `id` | 🇮🇹 ایتالیایی | `it` |
| 🇯🇵 ژاپنی | `ja` | 🇵🇱 لهستانی | `pl` |
| 🇧🇷 پرتغالی | `pt` | 🇷🇺 روسی | `ru` |
| 🇹🇷 ترکی | `tr` | 🇨🇳 چینی | `zh` |
| 🇮🇷 فارسی | `fa` |

### ترجمه‌های READMEترکی

| زبان | فایل | زبان | فایل |
|----------|------|----------|------|
| 🇺🇸 انگلیسی | [README.md](../README.md) | 🇪🇸 اسپانیایی | [README.es.md](README.es.md) |
| 🇸🇦 عربی | [README.ar.md](README.ar.md) | 🇫🇷 فرانسوی | [README.fr.md](README.fr.md) |
| 🇩🇪 آلمانی | [README.de.md](README.de.md) | 🇮🇳 هندی | [README.hi.md](README.hi.md) |
| 🇮🇩 اندونزیایی | [README.id.md](README.id.md) | 🇮🇹 ایتالیایی | [README.it.md](README.it.md) |
| 🇯🇵 ژاپنی | [README.ja.md](README.ja.md) | 🇵🇱 لهستانی | [README.pl.md](README.pl.md) |
| 🇧🇷 پرتغالی | [README.pt.md](README.pt.md) | 🇷🇺 روسی | [README.ru.md](README.ru.md) |
| 🇹🇷 ترکی | [README.tr.md](README.tr.md) | 🇨🇳 چینی | [README.zh.md](README.zh.md) |
| 🇮🇷 فارسی | [README.fa.md](README.fa.md) |

> 💡 **می‌خواهید در یک ترجمه مشارکت کنید؟** بخش [مشارکت](#contributing) را ببینید تا به ما در افزودن زبان‌های بیشتر کمک کنید!

</details>

<a id="troubleshooting"></a>
## 🛠️ عیب‌یابی

<details>
<summary>برای مشاهده مشکلات رایج و راه‌حل‌ها کلیک کنید</summary>

- **جدول فرمت‌ها نمایش داده نمی‌شود:** yt-dlp را به آخرین نسخه به‌روزرسانی کرده و به کانال شبانه yt-dlp تغییر دهید.
- **دانلود ناموفق است:** اتصال اینترنت خود را بررسی کرده و مطمئن شوید ویدیو در دسترس است.
- **خطاهای خاص دانلود:**
  - **ویدیوهای خصوصی:** برای دسترسی به محتوای خصوصی از احراز هویت با کوکی استفاده کنید.
  - **محتوای دارای محدودیت سنی:** برای مشاهده ویدیوهای دارای محدودیت سنی به حساب یوتیوب خود وارد شوید.
  - **ویدیوهای دارای محدودیت جغرافیایی:** برای دور زدن محدودیت‌های منطقه‌ای استفاده از VPN را در نظر بگیرید.
  - **ویدیوهای حذف‌شده:** ویدیو دیگر در یوتیوب موجود نیست.
  - **پخش‌های زنده (Live streams):** پخش‌های زنده قابل دانلود نیستند؛ منتظر پایان پخش بمانید.
  - **خطاهای شبکه:** اتصال اینترنت خود را بررسی کرده و دوباره تلاش کنید.
  - **لینک‌های نامعتبر:** مطمئن شوید لینک صحیح بوده و از یک پلتفرم پشتیبانی‌شده است.
  - **محتوای پرمیوم:** نیازمند اشتراک یوتیوب پرمیوم است.
  - **مسدودیت‌های کپی‌رایت:** محتوا به دلیل محدودیت‌های کپی‌رایت مسدود شده است.
- **فایل‌های ویدیو و صدای جداگانه پس از دانلود:** این اتفاق زمانی رخ می‌دهد که FFmpeg موجود نباشد یا شناسایی نشود. YTSage برای ادغام جریان‌های ویدیو و صدای با کیفیت بالا نیاز به FFmpeg دارد.
  - **راه‌حل:** مطمئن شوید FFmpeg نصب شده و در PATH سیستم شما قابل دسترسی است. برای کاربران ویندوز، ساده‌ترین گزینه دانلود فایل `YTSage-v<version>-ffmpeg.exe` است که همراه با FFmpeg ارائه می‌شود.

---

#### 🛡️ هشدار Windows Defender / آنتی‌ویروس

برخی نرم‌افزارهای آنتی‌ویروس ممکن است فایل‌های `.exe` را به‌عنوان مثبت کاذب علامت‌گذاری کنند. این یک **محدودیت شناخته‌شده** برنامه‌های بسته‌بندی‌شده است.

**چرا این اتفاق می‌افتد:**
- الگوریتم‌های اکتشافی آنتی‌ویروس ممکن است به اشتباه فایل‌های اجرایی بسته‌بندی‌شده را مشکوک تشخیص دهند.

**جایگزین‌های امن:**
- ✅ **استفاده از نصب pip:** `pip install ytsage` (پیشنهادی)
- ✅ **کامپایل از کد منبع**: با دنبال کردن این [راهنما](../.github/CI_CD_README.md)
- ✅ **افزودن برنامه به لیست سفید** در نرم‌افزار آنتی‌ویروس خود.

#### 🍎 macOS: "برنامه آسیب دیده است و نمی‌توان آن را باز کرد"
اگر این خطا را در macOS Sonoma یا نسخه جدیدتر مشاهده کردید، باید ویژگی قرنطینه (quarantine) را حذف کنید.

1.  **ترمینال را باز کنید** (می‌توانید آن را با استفاده از Spotlight پیدا کنید).
2.  **دستور زیر را تایپ کنید** اما هنوز **Enter را نزنید**. مطمئن شوید فاصله انتهایی را نیز وارد کرده‌اید:
    ```bash
    xattr -d com.apple.quarantine 
    ```
3.  **فایل `YTSage.app`** را از پنجره Finder بکشید و مستقیماً در پنجره ترمینال رها کنید. این کار مسیر صحیح فایل را به‌طور خودکار می‌چسباند.
4.  **Enter را بزنید** تا دستور اجرا شود.
5.  **دوباره سعی کنید YTSage.app را باز کنید.** اکنون باید به‌درستی اجرا شود.

---

#### **مکان‌های پیکربندی (پیشرفته)**
- **ویندوز:** `%LOCALAPPDATA%\YTSage`
- **macOS:** `~/Library/Application Support/YTSage`
- **لینوکس:** `~/.local/share/YTSage`

</details>

<a id="sponsor"></a>
## 💖 حمایت مالی

اگر YTSage در وقت شما صرفه‌جویی می‌کند، حمایت مالی از این پروژه را در نظر بگیرید. حمایت مالی به پوشش زمان توسعه، آزمایش روی همه پلتفرم‌ها و بهبودهای آینده کمک می‌کند.

- حامیان مالی گیت‌هاب: https://github.com/sponsors/oop7
- لینک حمایت مالی همچنین مستقیماً از طریق پنجره درباره در داخل برنامه در دسترس است.

[![Sponsor YTSage](https://img.shields.io/badge/Sponsor-YTSage-EA4AAA?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sponsors/oop7)

<a id="contributing"></a>
## 👥 مشارکت

ما با کمال میل از مشارکت‌ها استقبال می‌کنیم! در اینجا نحوه کمک شما آمده است:

۱. 🍴 مخزن را فورک کنید
۲. 🌿 شاخه فیچر خود را ایجاد کنید:
  ```bash
  git checkout -b feature/AmazingFeature
  ```
۳. 💾 تغییرات خود را کامیت کنید:
  ```bash
  git commit -m 'Add some AmazingFeature'
  ```
۴. 📤 به شاخه پوش کنید:
  ```bash
  git push origin feature/AmazingFeature
  ```
۵. 🔄 یک Pull Request باز کنید

### 🌍 مشارکت در ترجمه‌ها

- فایل README محلی‌شده مربوطه را به‌روزرسانی کنید (مثلاً `readme-translations/README.fr.md`)
- با ویرایش `ytsage/languages/<code>.json` رشته‌های برنامه را همگام نگه دارید
- اگر زبان شما موجود نیست، از `README.md` شروع کرده و `README.<code>.md` را ایجاد کنید

<details>
<summary>📂 ساختار پروژه</summary>

## YTSage - ساختار پروژه

این سند ساختار سازمان‌یافته پوشه‌های YTSage را شرح می‌دهد.

### 📁 ساختار پروژه

```
YTSage/
├── 📁 .github/                   # پیکربندی گیت‌هاب
│   ├── 📁 ISSUE_TEMPLATE/         # قالب‌های تیکت
│   │   └── 🐛-bug-report.md       # قالب گزارش باگ
│   ├─── 📁 workflows/              # جریان‌های کاری GitHub Actions
│   │   ├── build-linux.yml        # جریان کاری بیلد لینوکس
│   │   ├── build-macos.yml        # جریان کاری بیلد macOS
│   │   │── build-windows.yml      # جریان کاری بیلد ویندوز
|   |   └── release-all.yml          # جریان کاری انتشار master
│   └── 📄 CI_CD_README.md        # مستندات CI/CD
├──  📁 branding/                 # منابع برند (تصاویر، SVGها)
│   ├── 📁 icons/                 # آیکون‌های برنامه
│   ├── 📁 screenshots/           # تصاویر برای مستندات
│   └── 📁 svg/                   # منابع SVG
├── 📄 LICENSE                    # فایل مجوز
├── 📄 pyproject.toml             # فراداده و وابستگی‌های پروژه
├── 📄 README.md                  # مستندات پروژه
├── 📄 requirements.txt           # وابستگی‌های پایتون (توسعه)
└── 📁 ytsage/                    # بسته کد منبع
    ├── 📁 assets/                # منابع زمان اجرا
    │   ├── 📁 Icon/              # آیکون‌های برنامه
    │   └── 📁 sound/             # فایل‌های صوتی
    ├── 📁 languages/             # فایل‌های محلی‌سازی
    │   ├── 📄 ar.json            # ترجمه عربی
    │   ├── 📄 de.json            # ترجمه آلمانی
    │   ├── 📄 en.json            # ترجمه انگلیسی
    │   └── ...                   # سایر زبان‌ها
    ├── 📁 core/                  # منطق اصلی کسب‌وکار
    │   ├── 📄 __init__.py        # مقداردهی اولیه بسته core
    │   ├── 📄 ytsage_deno.py     # یکپارچه‌سازی Deno
    │   ├── 📄 ytsage_downloader.py # قابلیت دانلود
    │   ├── 📄 ytsage_ffmpeg.py   # یکپارچه‌سازی FFmpeg
    │   ├── 📄 ytsage_utils.py    # توابع کمکی
    │   └── 📄 ytsage_yt_dlp.py   # یکپارچه‌سازی yt-dlp
    ├── 📁 gui/                   # اجزای رابط کاربری
    │   ├── 📄 __init__.py        # مقداردهی اولیه بسته GUI
    │   ├── 📄 ytsage_gui_main.py # پنجره اصلی برنامه
    │   └── 📁 ytsage_gui_dialogs/ # کلاس‌های پنجره‌های دیالوگ
    ├── 📁 utils/                 # ماژول‌های کمکی
    │   ├── 📄 __init__.py        # مقداردهی اولیه بسته utils
    │   ├── 📄 ytsage_config_manager.py # مدیریت پیکربندی
    │   └── 📄 ytsage_logger.py   # ابزارهای گزارش‌گیری
    ├── 📄 __init__.py            # نقطه ورود بسته
    └── 📄 main.py                # اسکریپت اجرای اصلی
```

</details>

## ⭐️ تاریخچه ستاره‌ها

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

## 📜 مجوز

این پروژه تحت مجوز MIT منتشر شده است - برای جزئیات بیشتر فایل [LICENSE](../LICENSE) را ببینید.

## 🙏 قدردانی

<details>
<summary>نمایش قدردانی</summary>

<div align="center">

<p>تشکر فراوان از همه کسانی که با باز کردن یک تیکت برای پیشنهاد بهبود یا گزارش باگ، در این پروژه مشارکت کرده‌اند.</p>

<table>
    <tr class="section"><th colspan="2">اجزای اصلی</th></tr>
    <tr>
        <td width="35%"><a href="https://github.com/yt-dlp/yt-dlp">yt-dlp</a></td>
        <td>موتور دانلود</td>
    </tr>
    <tr>
        <td><a href="https://ffmpeg.org/">FFmpeg</a></td>
        <td>پردازش رسانه</td>
    </tr>
    <tr>
        <td><a href="https://deno.com/">Deno</a></td>
        <td>موتور اجرا برای یکپارچه‌سازی با yt-dlp</td>
    </tr>
    <tr class="section"><th colspan="2">کتابخانه‌ها و فریم‌ورک‌ها</th></tr>
    <tr>
        <td><a href="https://wiki.qt.io/Qt_for_Python">PySide6</a></td>
        <td>فریم‌ورک رابط کاربری</td>
    </tr>
    <tr>
        <td><a href="https://python-pillow.org/">Pillow</a></td>
        <td>پردازش تصویر</td>
    </tr>
    <tr>
        <td><a href="https://requests.readthedocs.io/">requests</a></td>
        <td>درخواست‌های HTTP</td>
    </tr>
    <tr>
        <td><a href="https://packaging.python.org/">packaging</a></td>
        <td>مدیریت نسخه‌ها و بسته‌ها</td>
    </tr>
    <tr>
        <td><a href="https://python-markdown.github.io/">markdown</a></td>
        <td>رندر Markdown</td>
    </tr>
    <tr>
        <td><a href="https://github.com/Delgan/loguru">loguru</a></td>
        <td>گزارش‌گیری</td>
    </tr>
    <tr class="section"><th colspan="2">منابع و مشارکت‌کنندگان</th></tr>
    <tr>
        <td><a href="https://pixabay.com/sound-effects/new-notification-09-352705/">New Notification 09 by Universfield</a></td>
        <td>صدای اعلان</td>
    </tr>
    <tr>
        <td><a href="https://github.com/viru185">viru185</a></td>
        <td>مشارکت‌کننده کد</td>
    </tr>
</table>

</div>

</details>

## ⚠️ سلب مسئولیت

این ابزار فقط برای استفاده شخصی در نظر گرفته شده است. لطفاً شرایط استفاده یوتیوب و حقوق سازندگان محتوا را رعایت کنید.

---

<div align="center">

ساخته شده با ❤️ توسط [oop7](https://github.com/oop7)

</div>