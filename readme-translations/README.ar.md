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

**برنامج تحميل من يوتيوب عصري بواجهة PySide6 أنيقة.**  
قم بتحميل الفيديوهات بأي جودة، استخراج الصوت، جلب الترجمات، والمزيد.

### 🌍 لغات README

الإنجليزية: [EN](../README.md)
| العربية: [AR](README.ar.md)
| الألمانية: [DE](README.de.md)
| الإسبانية: [ES](README.es.md)
| الفرنسية: [FR](README.fr.md)
| الهندية: [HI](README.hi.md)
| الإندونيسية: [ID](README.id.md)
| الإيطالية: [IT](README.it.md)
| اليابانية: [JA](README.ja.md)
| البولندية: [PL](README.pl.md)
| البرتغالية: [PT](README.pt.md)
| الروسية: [RU](README.ru.md)
| التركية: [TR](README.tr.md)
| الصينية: [ZH](README.zh.md)

<p align="center">
  <a href="#installation">التثبيت</a> •
  <a href="#features">المميزات</a> •
  <a href="#usage">الاستخدام</a> •
  <a href="#screenshots">لقطات الشاشة</a> •
  <a href="#troubleshooting">استكشاف الأخطاء</a> •
  <a href="#sponsor">الدعم</a> •
  <a href="#contributing">المساهمة</a>
</p>

</div>

---

<a id="why-ytsage"></a>
## ❓ لماذا YTSage؟

تم تصميم YTSage للمستخدمين الذين يريدون **أداة تحميل يوتيوب بسيطة لكن قوية**. على عكس الأدوات الأخرى، فإنه يوفر:

- واجهة PySide6 عصرية ونظيفة
- تحميل بنقرة واحدة للفيديو والصوت والترجمات
- ميزات متقدمة مثل SponsorBlock، دمج الترجمات، واختيار قوائم التشغيل
- وضع عام (Generic Mode) اختياري للمواقع التي يدعمها yt-dlp بخلاف يوتيوب
- دعم منصات متعددة وتثبيت سهل

<a id="features"></a>
## ✨ المميزات

<div align="center">

| الميزات الأساسية | الميزات المتقدمة | ميزات إضافية |
|-----------------------------------|-----------------------------------------|------------------------------------|
| 🎥 جدول الصيغ | 🚫 تكامل SponsorBlock | 🎞️ عرض FPS/HDR |
| 🎵 استخراج الصوت | 📝 اختيار ودمج الترجمات | 🔄 تحديث تلقائي لـ yt-dlp |
| ✨ واجهة مستخدم بسيطة | 💾 حفظ الوصف والصورة المصغرة | 🛠️ اكتشاف FFmpeg/yt-dlp/Deno |
| 📋 دعم ومحدد قوائم التشغيل | 🚀 محدد السرعة | ⚙️ أوامر مخصصة |
| 📑 دمج الفصول | ✂️ قص أجزاء الفيديو | 🍪 تسجيل الدخول بالكوكيز |
| 📜 سجل التحميلات | 🔄 اختيار قناة الإصدار | 🌐 دعم البروكسي |
| 🎚️ تحويل صيغ الصوت | 🎬 إعدادات صيغ الفيديو | 🆙 تبويب تحديث مدمج |
| 🌍 الوضع العام | 🔊 تطبيع الصوت (EBU R128) | 🌍 دعم 14 لغة |
| 💾 تصدير قوائم التشغيل | ⚙️ الجودة والترجمات الافتراضية | |
</div>

<a id="installation"></a>
## 🚀 التثبيت

### ⚡ التثبيت السريع (موصى به)

تثبيت YTSage عبر PyPI:

```bash
pip install ytsage
```

<details>
<summary>🔄 تحديث نسخة مثبتة</summary>

```bash
pip install --upgrade ytsage
```

</details>

ثم قم بتشغيل التطبيق:

```bash
ytsage
```

### 📦 حزم جاهزة للتشغيل

> [👉 تحميل أحدث إصدار](https://github.com/oop7/YTSage/releases/latest)

#### 🪟 Windows

| الصيغة | الوصف |
|--------|-------------|
| ![Windows EXE](https://img.shields.io/badge/Windows-EXE-0078D6?style=for-the-badge&logo=windows&logoColor=white) | مثبت قياسي |
| ![Windows FFmpeg](https://img.shields.io/badge/Windows-FFmpeg-0078D6?style=for-the-badge&logo=windows&logoColor=white) | مع FFmpeg مدمج |
| ![Windows Portable](https://img.shields.io/badge/Windows-Portable-0078D6?style=for-the-badge&logo=windows&logoColor=white) | نسخة محمولة، لا تحتاج لتثبيت |
| ![Windows Portable FFmpeg](https://img.shields.io/badge/Windows-Portable%20FFmpeg-0078D6?style=for-the-badge&logo=windows&logoColor=white) | محمولة مع FFmpeg، مضغوطة |

<details>
<summary>🛠️ خطوات التثبيت</summary>

1. **مثبت EXE (`.exe`)**: انقر نقرًا مزدوجًا على الملف واتبع معالج التثبيت.
2. **النسخة المحمولة (`.zip`)**: استخرج الملف في أي مكان وشغل `ytsage.exe`.
3. **FFmpeg المدمج**: اختر النسخة التي تحتوي على FFmpeg إذا لم يكن مثبتًا على نظامك.
</details>

#### 🐧 Linux

| الصيغة | الوصف |
|--------|-------------|
| ![Linux DEB](https://img.shields.io/badge/Linux-DEB-FCC624?style=for-the-badge&logo=linux&logoColor=black) | حزمة Debian |
| ![Linux AppImage](https://img.shields.io/badge/Linux-AppImage-FCC624?style=for-the-badge&logo=linux&logoColor=black) | AppImage، محمولة |
| ![Linux RPM](https://img.shields.io/badge/Linux-RPM-FCC624?style=for-the-badge&logo=linux&logoColor=black) | حزمة RPM |
| ![Flathub](https://img.shields.io/badge/Linux-Flatpak-FCC624?style=for-the-badge&logo=flathub&logoColor=black) | Flatpak Bundle |

<details>
<summary>🛠️ خطوات التثبيت</summary>

- **DEB (`.deb`)**:
  ```bash
  sudo dpkg -i ytsage_*.deb
  sudo apt-get install -f # لإصلاح الاعتمادات الناقصة إذا لزم الأمر
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
- **Flatpak**: اتبع التعليمات على Flathub أو شغل:
  ```bash
  flatpak install flathub io.github.oop7.ytsage
  ```
</details>

#### 🍎 macOS

| الصيغة | الوصف |
|--------|-------------|
| ![macOS ARM64 APP](https://img.shields.io/badge/macOS-ARM64%20APP-000000?style=for-the-badge&logo=apple&logoColor=white) | تطبيق مضغوط لـ Apple Silicon |
| ![macOS ARM64 DMG](https://img.shields.io/badge/macOS-ARM64%20DMG-000000?style=for-the-badge&logo=apple&logoColor=white) | صورة قرص لـ Apple Silicon |

<details>
<summary>🛠️ خطوات التثبيت</summary>

- **مثبت DMG (`.dmg`)**: انقر نقرًا مزدوجًا لفتح القرص، ثم اسحب `YTSage.app` إلى مجلد Applications.
- **تطبيق مضغوط (`.zip`)**: استخرج الملف وانقل `YTSage.app` إلى مجلد Applications.

*ملاحظة: إذا واجهت خطأ "التطبيق تالف"، راجع قسم استكشاف الأخطاء لنظام macOS أدناه.*
</details>

---

<details>
<summary>💻 التثبيت اليدوي من المصدر</summary>

### 1. نسخ المستودع

```bash
git clone https://github.com/oop7/YTSage.git
cd YTSage
```

### 2. تثبيت الاعتمادات

#### ⚡ باستخدام uv

```bash
uv pip install .
```

#### 📦 أو باستخدام pip العادي

```bash
pip install .
```

### 3. تشغيل التطبيق

```bash
python -m ytsage.main
```

</details>

<a id="screenshots"></a>
## 📸 لقطات الشاشة

<div align="center">
<table>
  <tr>
    <td><img src="../branding/screenshots/Download-Settings.png" alt="إعدادات التحميل" width="400"/></td>
    <td><img src="../branding/screenshots/playlist.png" alt="تحميل قوائم التشغيل" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><em>إعدادات التحميل</em></td>
    <td align="center"><em>تحميل قوائم التشغيل</em></td>
  </tr>
  <tr>
    <td><img src="../branding/screenshots/audio_format.png" alt="اختيار صيغة الصوت" width="400"/></td>
    <td><img src="../branding/screenshots/Custom-Option.png" alt="خيارات مخصصة" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><em>صيغة الصوت</em></td>
    <td align="center"><em>خيارات مخصصة</em></td>
  </tr>
</table>
</div>

<a id="usage"></a>
## 📖 الاستخدام

<details>
<summary>🎯 الاستخدام الأساسي</summary>

1. **شغل YTSage**
2. **الصق رابط يوتيوب** (أو استخدم زر "Paste URL")
3. **اضغط على "Analyze"**
4. **اختر الصيغة:**
   - `Video` للتحميلات المرئية
   - `Audio Only` لاستخراج الصوت فقط
5. **اختر الخيارات:**
   - تفعيل الترجمات واختيار اللغة
   - تفعيل دمج الترجمات
   - حفظ الصورة المصغرة
   - حذف المقاطع الإعلانية (Sponsor segments)
   - حفظ الوصف
   - دمج الفصول (Chapters)
6. **اختر مجلد الحفظ**
7. **اضغط على "Download"**

> 💡 مجلد التحميل الافتراضي هو مجلد "Downloads" للمستخدم.

</details>

<details>
<summary>📋 تحميل قائمة تشغيل (Playlist)</summary>

1. **الصق رابط قائمة التشغيل**
2. **اضغط على "Analyze"**
3. **اختر الفيديوهات من محدد القائمة (اختياري، يتم اختيار الكل تلقائيًا)**
4. **اختر الصيغة/الجودة المطلوبة**
5. **اضغط على "Download"**

> 💡 التطبيق يتعامل مع طابور التحميل تلقائيًا، ويمكنك تصدير مدخلات القائمة كملفات `.txt` أو `.csv` أو `.m3u` أو `.json`.

</details>

<details>
<summary>🌍 الوضع العام للمواقع غير يوتيوب</summary>

استخدم الوضع العام (Generic Mode) عندما تريد أن يقبل YTSage روابط من المواقع التي يدعمها yt-dlp، مثل Dailymotion و CBC Gem و TikTok وغيرها.

كيفية الاستخدام:

1. افتح `Download Settings`.
2. فعل `Generic Mode`.
3. الصق رابط فيديو أو قائمة تشغيل مدعومة غير يوتيوب.
4. اضغط على `Analyze`.
5. اختر الصيغة وحمل كالمعتاد.

ملاحظات:

- الوضع العام يغير فقط التحقق من الرابط داخل YTSage. يجب أن يكون الموقع مدعومًا من نسخة yt-dlp المثبتة لديك.
- بعض المواقع تتطلب كوكيز، تسجيل دخول، بروكسي أو وسائط yt-dlp إضافية حسب نوع الموقع.
- إذا فشل موقع ما، حدث yt-dlp أولاً من تبويب التحديث المدمج قبل الإبلاغ عن المشكلة.

</details>

<details>
<summary>🧰 خيارات الميديا والتحميل</summary>

- **خيارات الترجمة:** تصفية اللغات وتضمين الترجمات في ملف الفيديو.
- **دمج الترجمات:** دمج الترجمات داخل ملف الفيديو لتكون ترجمة مدمجة (Hardcoded).
- **حفظ الوصف:** حفظ وصف الفيديو كملف نصي.
- **حفظ الصورة المصغرة:** حفظ صورة الفيديو كملف صورة.
- **دمج الفصول:** تضمين علامات الفصول كبيانات وصفية لمشغلات الفيديو المتوافقة.
- **حذف مقاطع الرعاة:** حذف الأجزاء الإعلانية من الفيديو باستخدام SponsorBlock.
- **قص الفيديو:** تحميل أجزاء محددة فقط من الفيديو عن طريق تحديد أوقات البداية والنهاية بصيغة `HH:MM:SS`.

</details>

<details>
<summary>⚙️ إعدادات الإخراج والملفات</summary>

- **محدد السرعة:** تحديد سرعة التحميل، مثلاً `500K` لـ 500 كيلوبايت/ثانية.
- **حفظ مسار التحميل:** يحفظ مسار التحميل الافتراضي للتحميلات المستقبلية. متاح في **Download Settings → Download Path**.
- **دقة الفيديو الافتراضية:** حدد دقة الفيديو المفضلة للاختيار التلقائي (مثل 1080p أو 720p). متاح في **Download Settings → Default Video Resolution**.
- **لغات الترجمة الافتراضية:** حدد لغات الترجمة للاختيار التلقائي (مفصولة بفواصل، مثل `ar,en`). متاح في **Download Settings → Default Subtitle Languages**.
- **صيغة اسم الملف:** تخصيص صيغة اسم الملف باستخدام متغيرات مثل `%(title)s` و `%(uploader)s` و `%(playlist_index)s` و `%(resolution)s`. متاح في **Download Settings → Filename Format**.
- **فرض صيغة الإخراج:** فرض تحميل الفيديو بصيغة محددة مثل `mp4` أو `webm` أو `mkv`. متاح في **Download Settings → Output Format Settings**.
- **تحويل صيغ الصوت:** تحويل تحميلات الصوت فقط للصيغ المفضلة مثل `AAC` أو `MP3` أو `FLAC` أو `WAV` أو `Opus` أو `M4A` أو `Vorbis` أو `Best`. متاح في **Download Settings → Audio Format Settings**.
- **تطبيع الصوت:** توحيد مستوى الصوت لتحميلات الصوت فقط باستخدام EBU R128.
- **الاتصالات المتزامنة:** زيادة سرعة التحميل بشكل كبير عن طريق تحميل الملف في أجزاء متعددة في وقت واحد. متاح في **Download Settings → General → Concurrent Connections** (القيمة الافتراضية 1، الموصى به 8-10 لتجنب حظر IP).

</details>

<details>
<summary>🌐 الوصول والشبكة</summary>

- **تسجيل الدخول بالكوكيز:** سجل الدخول ليوتيوب باستخدام الكوكيز للوصول للمحتوى الخاص.
  كيفية الاستخدام:
  1. **موصى به:** استخدم خيار `Extract cookies from browser` المدمج في التطبيق، ثم اختر المتصفح والملف الشخصي.
  2. بدلاً من ذلك، استخرج الكوكيز يدويًا:
     أ. صدر الكوكيز من متصفحك باستخدام إضافة مثل [cookie-editor](https://github.com/moustachauve/cookie-editor)
     ب. انسخ الكوكيز بصيغة Netscape
     ج. أنشئ ملفًا باسم `cookies.txt` والصق الكوكيز فيه
     د. اختر ملف `cookies.txt` في التطبيق
- **دعم البروكسي:** استخدم خادم بروكسي للتحميلات، مثلاً `http://<proxy-server>:<port>`
- **الوضع العام:** يسمح لـ YTSage بتحليل والتحميل من المواقع غير يوتيوب التي يدعمها yt-dlp. فعله من **Download Settings → Generic Mode**.

</details>

<details>
<summary>🛠️ الأدوات والصيانة</summary>

- **أوامر مخصصة:** الوصول لميزات yt-dlp المتقدمة عبر وسائط موجه الأوامر.
- **تبويب التحديث:** إدارة أدوات التحديث من مكان واحد في الخيارات المخصصة:
  - **تحديثات yt-dlp:** التحقق من التحديثات والتبديل بين القناة المستقرة (Stable) والليلية (Nightly).
  - **فاحص نسخة FFmpeg:** التحقق من نسخة FFmpeg وعرض أدلة التثبيت.
  - **تحديثات Deno:** التحقق وتحديث محرك Deno.
- **اكتشاف FFmpeg/yt-dlp/Deno:** يكتشف تلقائيًا المسارات والنسخ لـ FFmpeg و yt-dlp و Deno من نافذة "About".
- **سجل التحميلات:** عرض التحميلات السابقة مع الصور المصغرة والحالة من زر **History**.

</details>

<details>
<summary>🌍 الترجمة</summary>

يدعم YTSage **14 لغة** للوصول العالمي. اختر لغتك المفضلة من **Custom Options → Language**.

### اللغات المدعومة

| اللغة | الرمز | اللغة | الرمز |
|----------|------|----------|------|
| 🇺🇸 الإنجليزية | `en` | 🇪🇸 الإسبانية | `es` |
| 🇸🇦 العربية | `ar` | 🇫🇷 الفرنسية | `fr` |
| 🇩🇪 الألمانية | `de` | 🇮🇳 الهندية | `hi` |
| 🇮🇩 الإندونيسية | `id` | 🇮🇹 الإيطالية | `it` |
| 🇯🇵 اليابانية | `ja` | 🇵🇱 البولندية | `pl` |
| 🇧🇷 البرتغالية | `pt` | 🇷🇺 الروسية | `ru` |
| 🇹🇷 التركية | `tr` | 🇨🇳 الصينية | `zh` |

### تراجم README

| اللغة | الملف | اللغة | الملف |
|----------|------|----------|------|
| 🇺🇸 الإنجليزية | [README.md](../README.md) | 🇪🇸 الإسبانية | [README.es.md](README.es.md) |
| 🇸🇦 العربية | [README.ar.md](README.ar.md) | 🇫🇷 الفرنسية | [README.fr.md](README.fr.md) |
| 🇩🇪 الألمانية | [README.de.md](README.de.md) | 🇮🇳 الهندية | [README.hi.md](README.hi.md) |
| 🇮🇩 الإندونيسية | [README.id.md](README.id.md) | 🇮🇹 الإيطالية | [README.it.md](README.it.md) |
| 🇯🇵 اليابانية | [README.ja.md](README.ja.md) | 🇵🇱 البولندية | [README.pl.md](README.pl.md) |
| 🇧🇷 البرتغالية | [README.pt.md](README.pt.md) | 🇷🇺 الروسية | [README.ru.md](README.ru.md) |
| 🇹🇷 التركية | [README.tr.md](README.tr.md) | 🇨🇳 الصينية | [README.zh.md](README.zh.md) |

> 💡 **هل تريد المساعدة في الترجمة؟** راجع قسم [المساهمة](#contributing) لمساعدتنا في إضافة المزيد من اللغات!

</details>

<a id="troubleshooting"></a>
## 🛠️ استكشاف الأخطاء

<details>
<summary>اضغط لعرض المشاكل الشائعة وحلولها</summary>

- **جدول الصيغ لا يظهر:** حدث yt-dlp لأحدث نسخة وانتقل للقناة الليلية (Nightly).
- **فشل التحميل:** تحقق من اتصال الإنترنت وتأكد أن الفيديو متاح.
- **أخطاء تحميل محددة:**
  - **فيديوهات خاصة:** استخدم الكوكيز للوصول للمحتوى الخاص.
  - **محتوى مقيد بالعمر:** سجل دخولك ليوتيوب لمشاهدة الفيديوهات المقيدة.
  - **فيديوهات محظورة جغرافيًا:** استخدم VPN لتجاوز القيود الإقليمية.
  - **فيديوهات محذوفة:** الفيديو لم يعد متاحًا على يوتيوب.
  - **البث المباشر (Live):** لا يمكن تحميل البث المباشر أثناء عرضه؛ انتظر حتى ينتهي.
  - **أخطاء الشبكة:** تحقق من اتصالك وحاول مرة أخرى.
  - **روابط غير صالحة:** تأكد من صحة الرابط وأنه من منصة مدعومة.
  - **محتوى Premium:** يتطلب اشتراك يوتيوب بريميوم.
  - **حظر حقوق الملكية:** المحتوى محظور بسبب قيود حقوق النشر.
- **ملفات الفيديو والصوت منفصلة بعد التحميل:** يحدث هذا عند فقدان FFmpeg أو عدم اكتشافه. يتطلب YTSage برنامج FFmpeg لدمج مسارات الفيديو والصوت عالية الجودة.
  - **الحل:** تأكد من تثبيت FFmpeg وإضافته لـ PATH النظام. لمستخدمي ويندوز، الخيار الأسهل هو تحميل ملف `YTSage-v<version>-ffmpeg.exe` الذي يأتي مع FFmpeg مدمجًا.

---

#### 🛡️ تنبيه Windows Defender / الأنتي فيروس

قد تصنف بعض برامج الحماية ملفات `.exe` كبرمجيات ضارة (False Positive). هذا **عيب معروف** في التطبيقات المحزمة.

**لماذا يحدث هذا:**
- أساليب الكشف في مضادات الفيروسات قد تعتبر الملفات المحزمة مشبوهة خطأً.

**البدائل الآمنة:**
- ✅ **استخدم تثبيت pip:** `pip install ytsage` (موصى به)
- ✅ **البناء من المصدر:** باتباع هذا [الدليل](../.github/CI_CD_README.md)
- ✅ **إضافة التطبيق للقائمة البيضاء** في برنامج الحماية لديك.

#### 🍎 macOS: "The app is damaged and can’t be opened"
إذا واجهت هذا الخطأ على macOS Sonoma أو أحدث، يجب عليك إزالة سمة الحجر الصحي.

1. **افتح الـ Terminal** (يمكنك البحث عنه عبر Spotlight).
2. **اكتب الأمر التالي** ولكن **لا تضغط** Enter بعد. تأكد من وجود مسافة في النهاية:
    ```bash
    xattr -d com.apple.quarantine 
    ```
3. **اسحب ملف `YTSage.app`** من نافذة Finder وأفلته في نافذة الـ Terminal. سيقوم بلصق المسار الصحيح تلقائيًا.
4. **اضغط Enter** لتنفيذ الأمر.
5. **حاول فتح YTSage.app مجددًا.** يجب أن يعمل الآن بشكل صحيح.

---

#### **مواقع الإعدادات (للمتقدمين)**
- **Windows:** `%LOCALAPPDATA%\YTSage`
- **macOS:** `~/Library/Application Support/YTSage`
- **Linux:** `~/.local/share/YTSage`

</details>

<a id="sponsor"></a>
## 💖 الدعم

إذا وفر لك YTSage الوقت، يرجى التفكير في دعم المشروع. يساعد الدعم في تغطية وقت التطوير، الاختبار على المنصات المختلفة، والتحسينات المستقبلية.

- GitHub Sponsors: https://github.com/sponsors/oop7
- رابط الدعم متاح أيضًا داخل التطبيق عبر نافذة "About".

[![Sponsor YTSage](https://img.shields.io/badge/Sponsor-YTSage-EA4AAA?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sponsors/oop7)

<a id="contributing"></a>
## 👥 المساهمة

نرحب بالمساهمات! إليك كيف يمكنك المساعدة:

1. 🍴 عمل Fork للمستودع
2. 🌿 إنشاء فرع جديد للميزة:
  ```bash
  git checkout -b feature/AmazingFeature
  ```
3. 💾 حفظ التغييرات:
  ```bash
  git commit -m 'Add some AmazingFeature'
  ```
4. 📤 رفع التغييرات:
  ```bash
  git push origin feature/AmazingFeature
  ```
5. 🔄 فتح Pull Request

### 🌍 المساهمة في الترجمة

- حدث ملف README المترجم (مثل `readme-translations/README.ar.md`)
- حافظ على تزامن نصوص التطبيق بتعديل `ytsage/languages/<code>.json`
- إذا كانت لغتك غير موجودة، ابدأ من `README.md` وأنشئ ملفًا جديدًا باسم `README.<code>.md`

<details>
<summary>📂 هيكل المشروع</summary>

## YTSage - هيكل المشروع

يوضح هذا المستند التنظيم الهيكلي لمجلدات YTSage.

### 📁 هيكل المشروع

```
YTSage/
├── 📁 .github/                   # إعدادات GitHub
│   ├── 📁 ISSUE_TEMPLATE/         # نماذج التذاكر
│   │   └── 🐛-bug-report.md       # نموذج تقرير الأخطاء
│   ├─── 📁 workflows/              # سير عمل GitHub Actions
│   │   ├── build-linux.yml        # بناء نسخة لينكس
│   │   ├── build-macos.yml        # بناء نسخة ماك
│   │   │── build-windows.yml      # بناء نسخة ويندوز
|   |   └── release-all.yml          # سير عمل الإصدارات
│   └── 📄 CI_CD_README.md        # توثيق CI/CD
├──  📁 branding/                 # أصول العلامة التجارية (لقطات شاشة، SVG)
│   ├── 📁 icons/                 # أيقونات التطبيق
│   ├── 📁 screenshots/           # لقطات شاشة للتوثيق
│   └── 📁 svg/                   # أصول بصيغة SVG
├── 📄 LICENSE                    # ملف الرخصة
├── 📄 pyproject.toml             # بيانات المشروع والاعتمادات
├── 📄 README.md                  # التوثيق الرئيسي
├── 📄 requirements.txt           # اعتمادات بايثون (للمطورين)
└── 📁 ytsage/                    # مجلد الأكواد المصدرية
    ├── 📁 assets/                # الأصول اللازمة للتشغيل
    │   ├── 📁 Icon/              # أيقونات التطبيق
    │   └── 📁 sound/             # ملفات صوتية
    ├── 📁 languages/             # ملفات الترجمة
    │   ├── 📄 ar.json            # الترجمة العربية
    │   ├── 📄 de.json            # الترجمة الألمانية
    │   ├── 📄 en.json            # الترجمة الإنجليزية
    │   └── ...                   # لغات أخرى
    ├── 📁 core/                  # المنطق البرمجي الأساسي
    │   ├── 📄 __init__.py        
    │   ├── 📄 ytsage_deno.py     # تكامل Deno
    │   ├── 📄 ytsage_downloader.py # وظائف التحميل
    │   ├── 📄 ytsage_ffmpeg.py   # تكامل FFmpeg
    │   ├── 📄 ytsage_utils.py    # وظائف مساعدة
    │   └── 📄 ytsage_yt_dlp.py   # تكامل yt-dlp
    ├── 📁 gui/                   # مكونات واجهة المستخدم
    │   ├── 📄 __init__.py        
    │   ├── 📄 ytsage_gui_main.py # نافذة التطبيق الرئيسية
    │   └── 📁 ytsage_gui_dialogs/ # كلاسات النوافذ الحوارية
    ├── 📁 utils/                 # موديلات مساعدة
    │   ├── 📄 __init__.py        
    │   ├── 📄 ytsage_config_manager.py # مدير الإعدادات
    │   └── 📄 ytsage_logger.py   # أداة تسجيل السجلات
    ├── 📄 __init__.py            # نقطة دخول الحزمة
    └── 📄 main.py                # سكربت التشغيل الرئيسي
```

</details>

## ⭐️ سجل النجوم

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

## 📜 الرخصة

هذا المشروع مرخص بموجب رخصة MIT - راجع ملف [LICENSE](../LICENSE) لمزيد من التفاصيل.

## 🙏 شكر وتقدير

<details>
<summary>عرض الشكر والتقدير</summary>

<div align="center">

<p>شكر كبير لكل من ساهم في هذا المشروع بفتح تذكرة لاقتراح تحسين أو الإبلاغ عن خطأ.</p>

<table>
    <tr class="section"><th colspan="2">المكونات الأساسية</th></tr>
    <tr>
        <td width="35%"><a href="https://github.com/yt-dlp/yt-dlp">yt-dlp</a></td>
        <td>محرك التحميل</td>
    </tr>
    <tr>
        <td><a href="https://ffmpeg.org/">FFmpeg</a></td>
        <td>معالجة الوسائط</td>
    </tr>
    <tr>
        <td><a href="https://deno.com/">Deno</a></td>
        <td>بيئة التشغيل لتكامل yt-dlp</td>
    </tr>
    <tr class="section"><th colspan="2">المكتبات وإطارات العمل</th></tr>
    <tr>
        <td><a href="https://wiki.qt.io/Qt_for_Python">PySide6</a></td>
        <td>إطار عمل الواجهة الرسومية</td>
    </tr>
    <tr>
        <td><a href="https://python-pillow.org/">Pillow</a></td>
        <td>معالجة الصور</td>
    </tr>
    <tr>
        <td><a href="https://requests.readthedocs.io/">requests</a></td>
        <td>طلبات HTTP</td>
    </tr>
    <tr>
        <td><a href="https://packaging.python.org/">packaging</a></td>
        <td>إدارة الإصدارات والحزم</td>
    </tr>
    <tr>
        <td><a href="https://python-markdown.github.io/">markdown</a></td>
        <td>معالجة Markdown</td>
    </tr>
    <tr>
        <td><a href="https://github.com/Delgan/loguru">loguru</a></td>
        <td>تسجيل السجلات</td>
    </tr>
    <tr class="section"><th colspan="2">الأصول والمساهمون</th></tr>
    <tr>
        <td><a href="https://pixabay.com/sound-effects/new-notification-09-352705/">New Notification 09 by Universfield</a></td>
        <td>صوت التنبيه</td>
    </tr>
    <tr>
        <td><a href="https://github.com/viru185">viru185</a></td>
        <td>مساهم بالكود</td>
    </tr>
</table>

</div>

</details>

## ⚠️ إخلاء مسؤولية

تُستخدم هذه الأداة للاستخدام الشخصي فقط. يرجى احترام شروط خدمة يوتيوب وحقوق منشئي المحتوى.

---

<div align="center">

صنع بـ ❤️ بواسطة [oop7](https://github.com/oop7)

</div>
