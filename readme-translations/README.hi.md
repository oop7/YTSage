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

**एक आधुनिक YouTube डाउनलोडर, एक स्वच्छ PySide6 इंटरफ़ेस के साथ।**  
किसी भी गुणवत्ता में वीडियो डाउनलोड करें, ऑडियो निकालें, उपशीर्षक प्राप्त करें, और बहुत कुछ।

### 🌍 README भाषाएँ

अंग्रेज़ी: [EN](../README.md)
| अरबी: [AR](README.ar.md)
| जर्मन: [DE](README.de.md)
| स्पेनिश: [ES](README.es.md)
| फ्रेंच: [FR](README.fr.md)
| हिंदी: [HI](README.hi.md)
| इंडोनेशियाई: [ID](README.id.md)
| इतालवी: [IT](README.it.md)
| जापानी: [JA](README.ja.md)
| पोलिश: [PL](README.pl.md)
| पुर्तगाली: [PT](README.pt.md)
| रूसी: [RU](README.ru.md)
| तुर्की: [TR](README.tr.md)
| चीनी: [ZH](README.zh.md)

<p align="center">
  <a href="#installation">स्थापना</a> •
  <a href="#features">विशेषताएँ</a> •
  <a href="#usage">उपयोग</a> •
  <a href="#screenshots">स्क्रीनशॉट</a> •
  <a href="#troubleshooting">समस्या निवारण</a> •
  <a href="#sponsor">प्रायोजक</a> •
  <a href="#contributing">योगदान</a>
</p>

</div>

---

<a id="why-ytsage"></a>
## ❓ YTSage क्यों?

YTSage उन उपयोगकर्ताओं के लिए डिज़ाइन किया गया है जो एक **सरल लेकिन शक्तिशाली YouTube डाउनलोडर** चाहते हैं। अन्य उपकरणों के विपरीत, यह प्रदान करता है:

- एक आधुनिक और स्वच्छ PySide6 इंटरफ़ेस
- वीडियो, ऑडियो और उपशीर्षक के लिए वन-क्लिक डाउनलोड
- SponsorBlock, उपशीर्षक मर्जिंग, और प्लेलिस्ट चयन जैसी उन्नत सुविधाएँ
- YouTube से इतर yt-dlp द्वारा समर्थित साइटों के लिए वैकल्पिक जेनेरिक मोड
- क्रॉस-प्लेटफ़ॉर्म समर्थन और आसान स्थापना

<a id="features"></a>
## ✨ विशेषताएँ

<div align="center">

| बुनियादी विशेषताएँ | उन्नत विशेषताएँ | अतिरिक्त विशेषताएँ |
|-----------------------------------|-----------------------------------------|------------------------------------|
| 🎥 प्रारूप तालिका | 🚫 SponsorBlock एकीकरण | 🎞️ FPS/HDR डिस्प्ले |
| 🎵 ऑडियो निष्कर्षण | 📝 उपशीर्षक चयन और मर्जिंग | 🔄 ऑटो yt-dlp अपडेट |
| ✨ सरल यूजर इंटरफेस | 💾 विवरण और थंबनेल सहेजें | 🛠️ FFmpeg/yt-dlp/Deno डिटेक्शन |
| 📋 प्लेलिस्ट समर्थन और चयनकर्ता | 🚀 गति सीमित करने वाला | ⚙️ कस्टम कमांड |
| 📑 अध्याय एकीकरण | ✂️ वीडियो अनुभाग ट्रिम करें | 🍪 कुकी लॉगिन |
| 📜 डाउनलोड इतिहास | 🔄 रिलीज़ चैनल चयन | 🌐 प्रॉक्सी समर्थन |
| 🎚️ ऑडियो प्रारूप रूपांतरण | 🎬 वीडियो प्रारूप सेटिंग्स | 🆙 एकीकृत अपडेट टैब |
| 🌍 जेनेरिक मोड | 🔊 ऑडियो सामान्यीकरण (EBU R128) | 🌍 14 भाषाओं में स्थानीयकरण |
| 💾 प्लेलिस्ट निर्यात | ⚙️ डिफ़ॉल्ट गुणवत्ता और उपशीर्षक | |
</div>

<a id="installation"></a>
## 🚀 स्थापना

### ⚡ त्वरित स्थापना (अनुशंसित)

PyPI के माध्यम से YTSage स्थापित करें:

```bash
pip install ytsage
```

<details>
<summary>🔄 मौजूदा स्थापना को अपडेट करें</summary>

```bash
pip install --upgrade ytsage
```

</details>

फिर एप्लिकेशन चलाएँ:

```bash
ytsage
```

### 📦 प्री-बिल्ट एक्जीक्यूटेबल्स (एक्ज़ीक्यूटेबल्स)

> [👉 नवीनतम रिलीज़ डाउनलोड करें](https://github.com/oop7/YTSage/releases/latest)

#### 🪟 Windows

| प्रारूप | विवरण |
|--------|-------------|
| ![Windows EXE](https://img.shields.io/badge/Windows-EXE-0078D6?style=for-the-badge&logo=windows&logoColor=white) | मानक इंस्टॉलर |
| ![Windows FFmpeg](https://img.shields.io/badge/Windows-FFmpeg-0078D6?style=for-the-badge&logo=windows&logoColor=white) | FFmpeg के साथ |
| ![Windows Portable](https://img.shields.io/badge/Windows-Portable-0078D6?style=for-the-badge&logo=windows&logoColor=white) | पोर्टेबल संस्करण, स्थापना की आवश्यकता नहीं है |
| ![Windows Portable FFmpeg](https://img.shields.io/badge/Windows-Portable%20FFmpeg-0078D6?style=for-the-badge&logo=windows&logoColor=white) | FFmpeg के साथ पोर्टेबल, ज़िप्ड |

<details>
<summary>🛠️ स्थापना चरण</summary>

1. **EXE इंस्टॉलर (`.exe`)**: फ़ाइल पर डबल-क्लिक करें और सेटअप विज़ार्ड का पालन करें।
2. **पोर्टेबल संस्करण (`.zip`)**: संग्रह को इच्छित स्थान पर निकालें और `ytsage.exe` चलाएँ।
3. **बिल्ट-इन FFmpeg**: यदि आपके सिस्टम पर FFmpeg स्थापित नहीं है, तो बिल्ट-इन FFmpeg वाले संस्करण चुनें।
</details>

#### 🐧 Linux

| प्रारूप | विवरण |
|--------|-------------|
| ![Linux DEB](https://img.shields.io/badge/Linux-DEB-FCC624?style=for-the-badge&logo=linux&logoColor=black) | डेबियन पैकेज |
| ![Linux AppImage](https://img.shields.io/badge/Linux-AppImage-FCC624?style=for-the-badge&logo=linux&logoColor=black) | AppImage, पोर्टेबल |
| ![Linux RPM](https://img.shields.io/badge/Linux-RPM-FCC624?style=for-the-badge&logo=linux&logoColor=black) | RPM पैकेज |
| ![Flathub](https://img.shields.io/badge/Linux-Flatpak-FCC624?style=for-the-badge&logo=flathub&logoColor=black) | Flatpak बंडल |

<details>
<summary>🛠️ स्थापना चरण</summary>

- **DEB (`.deb`)**:
  ```bash
  sudo dpkg -i ytsage_*.deb
  sudo apt-get install -f # यदि आवश्यक हो तो गायब निर्भरताओं को ठीक करें
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
- **Flatpak**: Flathub पर निर्देशों का पालन करें या चलाएँ:
  ```bash
  flatpak install flathub io.github.oop7.ytsage
  ```
</details>

#### 🍎 macOS

| प्रारूप | विवरण |
|--------|-------------|
| ![macOS ARM64 APP](https://img.shields.io/badge/macOS-ARM64%20APP-000000?style=for-the-badge&logo=apple&logoColor=white) | Apple Silicon के लिए ज़िप्ड ऐप |
| ![macOS ARM64 DMG](https://img.shields.io/badge/macOS-ARM64%20DMG-000000?style=for-the-badge&logo=apple&logoColor=white) | Apple Silicon के लिए डिस्क इमेज इंस्टॉलर |

<details>
<summary>🛠️ स्थापना चरण</summary>

- **DMG इंस्टॉलर (`.dmg`)**: माउंट करने के लिए डबल-क्लिक करें, फिर `YTSage.app` को अपने एप्लिकेशन फ़ोल्डर में खींचें।
- **ऐप आर्काइव (`.zip`)**: ज़िप निकालें और `YTSage.app` को अपने एप्लिकेशन फ़ोल्डर में ले जाएँ।

*नोट: यदि आपको "ऐप क्षतिग्रस्त है" त्रुटि मिलती है, तो नीचे macOS समस्या निवारण अनुभाग देखें।*
</details>

---

<details>
<summary>💻 स्रोत से मैन्युअल स्थापना</summary>

### 1. रिपॉजिटरी क्लोन करें

```bash
git clone https://github.com/oop7/YTSage.git
cd YTSage
```

### 2. निर्भरताएँ स्थापित करें

#### ⚡ uv के साथ

```bash
uv pip install .
```

#### 📦 या मानक pip के साथ

```bash
pip install .
```

### 3. एप्लिकेशन चलाएँ

```bash
python -m ytsage.main
```

</details>

<a id="screenshots"></a>
## 📸 स्क्रीनशॉट

<div align="center">
<table>
  <tr>
    <td><img src="../branding/screenshots/Download-Settings.png" alt="डाउनलोड सेटिंग्स" width="400"/></td>
    <td><img src="../branding/screenshots/playlist.png" alt="प्लेलिस्ट डाउनलोड" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><em>डाउनलोड सेटिंग्स</em></td>
    <td align="center"><em>प्लेलिस्ट डाउनलोड</em></td>
  </tr>
  <tr>
    <td><img src="../branding/screenshots/audio_format.png" alt="ऑडियो प्रारूप चयन" width="400"/></td>
    <td><img src="../branding/screenshots/Custom-Option.png" alt="कस्टम विकल्प" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><em>ऑडियो प्रारूप</em></td>
    <td align="center"><em>कस्टम विकल्प</em></td>
  </tr>
</table>
</div>

<a id="usage"></a>
## 📖 उपयोग

<details>
<summary>🎯 बुनियादी उपयोग</summary>

1. **YTSage लॉन्च करें**
2. **YouTube URL पेस्ट करें** (या "Paste URL" बटन का उपयोग करें)
3. **"Analyze" पर क्लिक करें**
4. **प्रारूप चुनें:**
   - वीडियो डाउनलोड के लिए `Video`
   - ऑडियो निष्कर्षण के लिए `Audio Only`
5. **विकल्प चुनें:**
   - उपशीर्षक सक्षम करें और भाषा चुनें
   - उपशीर्षक मर्जिंग सक्षम करें
   - थंबनेल सहेजें
   - प्रायोजित अनुभाग हटाएँ
   - विवरण सहेजें
   - अध्याय एम्बेड करें
6. **आउटपुट निर्देशिका चुनें**
7. **"Download" पर क्लिक करें**

> 💡 डिफ़ॉल्ट डाउनलोड निर्देशिका उपयोगकर्ता का "Downloads" फ़ोल्डर है।

</details>

<details>
<summary>📋 प्लेलिस्ट डाउनलोड</summary>

1. **प्लेलिस्ट URL पेस्ट करें**
2. **"Analyze" पर क्लिक करें**
3. **प्लेलिस्ट चयनकर्ता से वीडियो चुनें (वैकल्पिक, डिफ़ॉल्ट रूप से सभी)**
4. **वांछित प्रारूप/गुणवत्ता चुनें**
5. **"Download" पर क्लिक करें**

> 💡 एप्लिकेशन डाउनलोड कतार को स्वचालित रूप से प्रबंधित करता है, और आप प्लेलिस्ट प्रविष्टियों को `.txt`, `.csv`, `.m3u`, या `.json` फ़ाइलों के रूप में निर्यात कर सकते हैं।

</details>

<details>
<summary>🌍 गैर-YouTube साइटों के लिए जेनेरिक मोड</summary>

जेनेरिक मोड (Generic Mode) का उपयोग तब करें जब आप चाहते हैं कि YTSage yt-dlp द्वारा समर्थित साइटों जैसे Dailymotion, CBC Gem, TikTok और अन्य से URL स्वीकार करे।

इसका उपयोग कैसे करें:

1. `Download Settings` खोलें।
2. `Generic Mode` सक्षम करें।
3. एक समर्थित वीडियो या प्लेलिस्ट URL पेस्ट करें जो YouTube नहीं है।
4. `Analyze` पर क्लिक करें।
5. एक प्रारूप चुनें और हमेशा की तरह डाउनलोड करें।

नोट्स:

- जेनेरिक मोड केवल YTSage के अंदर URL सत्यापन को बदलता है। लक्ष्य साइट अभी भी आपके स्थापित yt-dlp संस्करण द्वारा समर्थित होनी चाहिए।
- कुछ साइटों को एक्सट्रैक्टर के आधार पर कुकीज़, लॉगिन, प्रॉक्सी या अतिरिक्त yt-dlp तर्कों की आवश्यकता होती है।
- यदि कोई साइट विफल हो जाती है, तो समस्या की रिपोर्ट करने से पहले एकीकृत अपडेट टैब से yt-dlp को अपडेट करें।

</details>

<details>
<summary>🧰 मीडिया और डाउनलोड विकल्प</summary>

- **उपशीर्षक विकल्प:** भाषाओं को फ़िल्टर करें और उपशीर्षक को वीडियो फ़ाइल में एम्बेड करें।
- **उपशीर्षक मर्जिंग:** हार्डकोडेड उपशीर्षक के लिए वीडियो फ़ाइल में उपशीर्षक मर्ज करें।
- **विवरण सहेजें:** वीडियो विवरण को टेक्स्ट फ़ाइल के रूप में सहेजें।
- **थंबनेल सहेजें:** वीडियो थंबनेल को छवि फ़ाइल के रूप में सहेजें।
- **अध्याय एम्बेड करें:** संगत वीडियो प्लेयर के लिए मेटाडेटा के रूप में अध्याय मार्कर शामिल करें।
- **प्रायोजित अनुभाग हटाएँ:** SponsorBlock का उपयोग करके वीडियो से प्रायोजित अनुभाग हटाएँ।
- **वीडियो ट्रिम करें:** `HH:MM:SS` प्रारूप में समय सीमा निर्दिष्ट करके वीडियो के केवल विशिष्ट भागों को डाउनलोड करें।

</details>

<details>
<summary>⚙️ आउटपुट और फ़ाइल सेटिंग्स</summary>

- **गति सीमित करने वाला:** डाउनलोड गति को सीमित करें, उदाहरण के लिए `500K` 500 KB/s के लिए।
- **डाउनलोड पथ सहेजें:** भविष्य के डाउनलोड के लिए डिफ़ॉल्ट डाउनलोड पथ सहेजता है। **Download Settings → Download Path** में उपलब्ध है।
- **डिफ़ॉल्ट वीडियो रिज़ॉल्यूशन:** स्वचालित चयन के लिए अपना पसंदीदा वीडियो रिज़ॉल्यूशन सेट करें (जैसे 1080p, 720p)। **Download Settings → Default Video Resolution** में उपलब्ध है।
- **डिफ़ॉल्ट उपशीर्षक भाषाएँ:** स्वचालित चयन के लिए डिफ़ॉल्ट उपशीर्षक भाषाएँ सेट करें (अल्पविराम से अलग, जैसे `hi,en`)। **Download Settings → Default Subtitle Languages** में उपलब्ध है।
- **फ़ाइल नाम प्रारूप:** `%(title)s`, `%(uploader)s`, `%(playlist_index)s` और `%(resolution)s` जैसे चरों का उपयोग करके आउटपुट फ़ाइल नाम प्रारूप को अनुकूलित करें। **Download Settings → Filename Format** में उपलब्ध है।
- **आउटपुट प्रारूप बाध्य करें:** वीडियो डाउनलोड को `mp4`, `webm` या `mkv` जैसे विशिष्ट कंटेनर प्रारूप में बाध्य करें। **Download Settings → Output Format Settings** में उपलब्ध है।
- **ऑडियो प्रारूप रूपांतरण:** केवल ऑडियो डाउनलोड को `AAC`, `MP3`, `FLAC`, `WAV`, `Opus`, `M4A`, `Vorbis`, या `Best` जैसे पसंदीदा प्रारूपों में परिवर्तित करें। **Download Settings → Audio Format Settings** में उपलब्ध है।
- **ऑडियो सामान्यीकरण:** EBU R128 का उपयोग करके केवल ऑडियो डाउनलोड के लिए वॉल्यूम को मानकीकृत करें।
- **एक साथ कनेक्शन:** एक साथ कई टुकड़ों में फ़ाइलें डाउनलोड करके डाउनलोड गति को काफी बढ़ाएँ। **Download Settings → General → Concurrent Connections** (डिफ़ॉल्ट 1, IP ब्लॉक से बचने के लिए अधिकतम 8-10 अनुशंसित) में उपलब्ध है।

</details>

<details>
<summary>🌐 एक्सेस और नेटवर्क</summary>

- **कुकी लॉगिन:** निजी सामग्री तक पहुँचने के लिए कुकीज़ का उपयोग करके YouTube में लॉगिन करें।
  उपयोग:
  1. **अनुशंसित:** ऐप में बिल्ट-इन `Extract cookies from browser` विकल्प का उपयोग करें, फिर अपना ब्राउज़र और वैकल्पिक रूप से प्रोफ़ाइल चुनें।
  2. वैकल्पिक रूप से, कुकीज़ मैन्युअल रूप से निकालें:
     a. [cookie-editor](https://github.com/moustachauve/cookie-editor?tab=readme-ov-file) जैसे एक्सटेंशन का उपयोग करके अपने ब्राउज़र से कुकीज़ निर्यात करें
     b. नेटस्केप प्रारूप में कुकीज़ कॉपी करें
     c. `cookies.txt` नामक फ़ाइल बनाएँ और कुकीज़ पेस्ट करें
     d. ऐप में `cookies.txt` फ़ाइल चुनें
- **प्रॉक्सी समर्थन:** डाउनलोड के लिए प्रॉक्सी सर्वर का उपयोग करें, जैसे `http://<proxy-server>:<port>`
- **जेनेरिक मोड:** YTSage को yt-dlp द्वारा समर्थित गैर-YouTube साइटों से विश्लेषण और डाउनलोड करने की अनुमति देता है। इसे **Download Settings → Generic Mode** से सक्षम करें।

</details>

<details>
<summary>🛠️ उपकरण और रखरखाव</summary>

- **कस्टम कमांड:** कमांड-लाइन तर्कों के माध्यम से उन्नत yt-dlp सुविधाओं तक पहुँचें।
- **अपडेट टैब:** कस्टम विकल्पों में एक ही स्थान से बिल्ट-इन अपडेट टूल प्रबंधित करें:
  - **yt-dlp अपडेट:** अपडेट के लिए जाँच करें और स्टेबल और नाइटली रिलीज़ चैनलों के बीच स्विच करें।
  - **FFmpeg संस्करण जाँचकर्ता:** अपने FFmpeg संस्करण को सत्यापित करें और स्थापना मार्गदर्शिकाएँ खोलें।
  - **Deno अपडेट:** Deno रनटाइम की जाँच करें और अपडेट करें।
- **FFmpeg/yt-dlp/Deno डिटेक्शन:** अबाउट डायलॉग से FFmpeg, yt-dlp और Deno के पथ और संस्करण का स्वचालित रूप से पता लगाता है।
- **डाउनलोड इतिहास:** **History** बटन से थंबनेल और स्थितियों के साथ पिछले डाउनलोड देखें।

</details>

<details>
<summary>🌍 स्थानीयकरण</summary>

YTSage वैश्विक पहुँच के लिए **14 भाषाओं** का समर्थन करता है। **Custom Options → Language** में अपनी पसंदीदा भाषा चुनें।

### समर्थित भाषाएँ

| भाषा | कोड | भाषा | कोड |
|----------|------|----------|------|
| 🇺🇸 अंग्रेज़ी | `en` | 🇪🇸 स्पेनिश | `es` |
| 🇸🇦 अरबी | `ar` | 🇫🇷 फ्रेंच | `fr` |
| 🇩🇪 जर्मन | `de` | 🇮🇳 हिंदी | `hi` |
| 🇮🇩 इंडोनेशियाई | `id` | 🇮🇹 इतालवी | `it` |
| 🇯🇵 जापानी | `ja` | 🇵🇱 पोलिश | `pl` |
| 🇧🇷 पुर्तगाली | `pt` | 🇷🇺 रूसी | `ru` |
| 🇹🇷 तुर्की | `tr` | 🇨🇳 चीनी | `zh` |

### README अनुवाद

| भाषा | फ़ाइल | भाषा | फ़ाइल |
|----------|------|----------|------|
| 🇺🇸 अंग्रेज़ी | [README.md](../README.md) | 🇪🇸 स्पेनिश | [README.es.md](README.es.md) |
| 🇸🇦 अरबी | [README.ar.md](README.ar.md) | 🇫🇷 फ्रेंच | [README.fr.md](README.fr.md) |
| 🇩🇪 जर्मन | [README.de.md](README.de.md) | 🇮🇳 हिंदी | [README.hi.md](README.hi.md) |
| 🇮🇩 इंडोनेशियाई | [README.id.md](README.id.md) | 🇮🇹 इतालवी | [README.it.md](README.it.md) |
| 🇯🇵 जापानी | [README.ja.md](README.ja.md) | 🇵🇱 पोलिश | [README.pl.md](README.pl.md) |
| 🇧🇷 पुर्तगाली | [README.pt.md](README.pt.md) | 🇷🇺 रूसी | [README.ru.md](README.ru.md) |
| 🇹🇷 तुर्की | [README.tr.md](README.tr.md) | 🇨🇳 चीनी | [README.zh.md](README.zh.md) |

> 💡 **अनुवाद में मदद करना चाहते हैं?** अधिक भाषाओं को जोड़ने में हमारी सहायता करने के लिए [योगदान](#contributing) अनुभाग देखें!

</details>

<a id="troubleshooting"></a>
## 🛠️ समस्या निवारण

<details>
<summary>सामान्य समस्याओं और समाधानों को देखने के लिए क्लिक करें</summary>

- **प्रारूप तालिका दिखाई नहीं दे रही है:** yt-dlp को नवीनतम संस्करण में अपडेट करें और yt-dlp नाइटली पर स्विच करें।
- **डाउनलोड विफल:** अपना इंटरनेट कनेक्शन जाँचें और सुनिश्चित करें कि वीडियो उपलब्ध है।
- **विशिष्ट डाउनलोड त्रुटियाँ:**
  - **निजी वीडियो:** निजी सामग्री तक पहुँचने के लिए कुकी प्रमाणीकरण का उपयोग करें।
  - **आयु-प्रतिबंधित सामग्री:** आयु-प्रतिबंधित वीडियो देखने के लिए अपने YouTube खाते में लॉग इन करें।
  - **जियो-ब्लॉक किए गए वीडियो:** क्षेत्रीय प्रतिबंधों को दरकिनार करने के लिए VPN का उपयोग करने पर विचार करें।
  - **हटाए गए वीडियो:** वीडियो अब YouTube पर उपलब्ध नहीं है।
  - **लाइव स्ट्रीम:** प्रसारण के दौरान लाइव स्ट्रीम डाउनलोड नहीं की जा सकतीं; स्ट्रीम समाप्त होने तक प्रतीक्षा करें।
  - **नेटवर्क त्रुटियाँ:** अपना इंटरनेट कनेक्शन जाँचें और पुनः प्रयास करें।
  - **अमान्य URL:** सुनिश्चित करें कि URL सही है और समर्थित प्लेटफ़ॉर्म से है।
  - **प्रीमियम सामग्री:** YouTube प्रीमियम सदस्यता की आवश्यकता है।
  - **कॉपीराइट ब्लॉक:** कॉपीराइट प्रतिबंधों के कारण सामग्री अवरुद्ध है।
- **डाउनलोड के बाद वीडियो और ऑडियो फ़ाइलें अलग हैं:** यह तब होता है जब FFmpeg गायब होता है या पता नहीं चल पाता है। उच्च गुणवत्ता वाले वीडियो और ऑडियो स्ट्रीम को मर्ज करने के लिए YTSage को FFmpeg की आवश्यकता होती है।
  - **समाधान:** सुनिश्चित करें कि FFmpeg स्थापित है और आपके सिस्टम PATH में सुलभ है। विंडोज उपयोगकर्ताओं के लिए, सबसे आसान विकल्प `YTSage-v<version>-ffmpeg.exe` फ़ाइल डाउनलोड करना है, जो FFmpeg के साथ आती है।

---

#### 🛡️ Windows Defender / एंटीवायरस चेतावनी

कुछ एंटीवायरस सॉफ़्टवेयर `.exe` फ़ाइलों को गलत सकारात्मक (फॉल्स पॉजिटिव) के रूप में चिह्नित कर सकते हैं। यह पैक किए गए एप्लिकेशन की **ज्ञात सीमा** है।

**यह क्यों होता है:**
- एंटीवायरस हिउरिस्टिक्स पैक किए गए एक्जीक्यूटेबल्स को संदिग्ध के रूप में गलत तरीके से पहचान सकते हैं।

**सुरक्षित विकल्प:**
- ✅ **pip स्थापना का उपयोग करें:** `pip install ytsage` (अनुशंसित)
- ✅ **स्रोत से बिल्ड करें**: इस [गाइड](../.github/CI_CD_README.md) का पालन करते हुए
- ✅ **एप्लिकेशन को व्हाइटलिस्ट करें** अपने एंटीवायरस सॉफ़्टवेयर में।

#### 🍎 macOS: "ऐप क्षतिग्रस्त है और खोला नहीं जा सकता"
यदि आप macOS Sonoma या नए पर यह त्रुटि देखते हैं, तो आपको क्वारंटाइन एट्रिब्यूट को हटाने की आवश्यकता है।

1.  **टर्मिनल खोलें** (आप इसे Spotlight का उपयोग करके पा सकते हैं)।
2.  **निम्न कमांड टाइप करें** लेकिन अभी Enter **न दबाएँ**। सुनिश्चित करें कि अंत में स्थान शामिल है:
    ```bash
    xattr -d com.apple.quarantine 
    ```
3.  **अपनी फाइंडर विंडो से `YTSage.app` फ़ाइल खींचें** और इसे सीधे टर्मिनल विंडो में छोड़ें। यह स्वचालित रूप से सही फ़ाइल पथ पेस्ट कर देगा।
4.  **Enter दबाएँ** कमांड चलाने के लिए।
5.  **YTSage.app को फिर से खोलने का प्रयास करें।** इसे अब ठीक से लॉन्च होना चाहिए।

---

#### **कॉन्फ़िगरेशन स्थान (उन्नत)**
- **Windows:** `%LOCALAPPDATA%\YTSage`
- **macOS:** `~/Library/Application Support/YTSage`
- **Linux:** `~/.local/share/YTSage`

</details>

<a id="sponsor"></a>
## 💖 प्रायोजक

यदि YTSage आपका समय बचाता है, तो कृपया प्रोजेक्ट को प्रायोजित करने पर विचार करें। प्रायोजन विकास समय, सभी प्लेटफ़ॉर्म पर परीक्षण और भविष्य के सुधारों को कवर करने में मदद करता है।

- GitHub Sponsors: https://github.com/sponsors/oop7
- प्रायोजन लिंक ऐप में अबाउट डायलॉग के माध्यम से सीधे उपलब्ध है।

[![Sponsor YTSage](https://img.shields.io/badge/Sponsor-YTSage-EA4AAA?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sponsors/oop7)

<a id="contributing"></a>
## 👥 योगदान

हम योगदान का स्वागत करते हैं! यहाँ बताया गया है कि आप कैसे मदद कर सकते हैं:

1. 🍴 रिपॉजिटरी को फोर्क करें
2. 🌿 अपनी फीचर शाखा बनाएँ:
  ```bash
  git checkout -b feature/AmazingFeature
  ```
3. 💾 अपने बदलाव कमिट करें:
  ```bash
  git commit -m 'Add some AmazingFeature'
  ```
4. 📤 शाखा में पुश करें:
  ```bash
  git push origin feature/AmazingFeature
  ```
5. 🔄 एक पुल रिक्वेस्ट खोलें

### 🌍 अनुवाद में योगदान करें

- संबंधित स्थानीयकृत README फ़ाइल को अपडेट करें (जैसे `readme-translations/README.hi.md`)
- `ytsage/languages/<code>.json` को संपादित करके ऐप स्ट्रिंग्स को सिंक में रखें
- यदि आपकी भाषा गायब है, तो `README.md` से शुरू करें और `README.<code>.md` बनाएँ

<details>
<summary>📂 प्रोजेक्ट संरचना</summary>

## YTSage - प्रोजेक्ट संरचना

यह दस्तावेज़ YTSage की संगठित फ़ोल्डर संरचना का वर्णन करता है।

### 📁 प्रोजेक्ट संरचना

```
YTSage/
├── 📁 .github/                   # GitHub कॉन्फ़िगरेशन
│   ├── 📁 ISSUE_TEMPLATE/         # इश्यू टेम्पलेट
│   │   └── 🐛-bug-report.md       # बग रिपोर्ट टेम्पलेट
│   ├─── 📁 workflows/              # GitHub Actions वर्कफ़्लो
│   │   ├── build-linux.yml        # लिनक्स बिल्ड वर्कफ़्लो
│   │   ├── build-macos.yml        # macOS बिल्ड वर्कफ़्लो
│   │   │── build-windows.yml      # विंडोज बिल्ड वर्कफ़्लो
|   |   └── release-all.yml          # मास्टर रिलीज़ वर्कफ़्लो
│   └── 📄 CI_CD_README.md        # CI/CD दस्तावेज़ीकरण
├──  📁 branding/                 # ब्रांडिंग एसेट्स (स्क्रीनशॉट, SVGs)
│   ├── 📁 icons/                 # ऐप आइकन
│   ├── 📁 screenshots/           # दस्तावेज़ीकरण के लिए स्क्रीनशॉट
│   └── 📁 svg/                   # SVG एसेट्स
├── 📄 LICENSE                    # लाइसेंस फ़ाइल
├── 📄 pyproject.toml             # प्रोजेक्ट मेटाडेटा और निर्भरताएँ
├── 📄 README.md                  # प्रोजेक्ट दस्तावेज़ीकरण
├── 📄 requirements.txt           # पायथन निर्भरताएँ (dev)
└── 📁 ytsage/                    # स्रोत कोड पैकेज
    ├── 📁 assets/                # रनटाइम एसेट्स
    │   ├── 📁 Icon/              # ऐप आइकन
    │   └── 📁 sound/             # ऑडियो फ़ाइलें
    ├── 📁 languages/             # स्थानीयकरण फ़ाइलें
    │   ├── 📄 ar.json            # अरबी अनुवाद
    │   ├── 📄 de.json            # जर्मन अनुवाद
    │   ├── 📄 en.json            # अंग्रेज़ी अनुवाद
    │   └── ...                   # अन्य भाषाएँ
    ├── 📁 core/                  # मुख्य व्यावसायिक तर्क
    │   ├── 📄 __init__.py        
    │   ├── 📄 ytsage_deno.py     # Deno एकीकरण
    │   ├── 📄 ytsage_downloader.py # डाउनलोड कार्यक्षमता
    │   ├── 📄 ytsage_ffmpeg.py   # FFmpeg एकीकरण
    │   ├── 📄 ytsage_utils.py    # उपयोगिता कार्य
    │   └── 📄 ytsage_yt_dlp.py   # yt-dlp एकीकरण
    ├── 📁 gui/                   # यूजर इंटरफेस घटक
    │   ├── 📄 __init__.py        
    │   ├── 📄 ytsage_gui_main.py # ऐप की मुख्य विंडो
    │   └── 📁 ytsage_gui_dialogs/ # संवाद वर्ग
    ├── 📁 utils/                 # उपयोगिता मॉड्यूल
    │   ├── 📄 __init__.py        
    │   ├── 📄 ytsage_config_manager.py # कॉन्फ़िगरेशन प्रबंधन
    │   └── 📄 ytsage_logger.py   # लॉगिंग टूल
    ├── 📄 __init__.py            # पैकेज प्रविष्टि बिंदु
    └── 📄 main.py                # मुख्य निष्पादन स्क्रिप्ट
```

</details>

## ⭐️ स्टार इतिहास

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

## 📜 लाइसेंस

यह प्रोजेक्ट MIT लाइसेंस के तहत है - विवरण के लिए [LICENSE](../LICENSE) फ़ाइल देखें।

## 🙏 धन्यवाद

<details>
<summary>धन्यवाद प्रदर्शित करें</summary>

<div align="center">

<p>उन सभी को बहुत-बहुत धन्यवाद जिन्होंने सुधार का सुझाव देने या बग की रिपोर्ट करने के लिए इश्यू खोलकर इस प्रोजेक्ट में योगदान दिया है।</p>

<table>
    <tr class="section"><th colspan="2">मुख्य घटक</th></tr>
    <tr>
        <td width="35%"><a href="https://github.com/yt-dlp/yt-dlp">yt-dlp</a></td>
        <td>डाउनलोड इंजन</td>
    </tr>
    <tr>
        <td><a href="https://ffmpeg.org/">FFmpeg</a></td>
        <td>मीडिया प्रसंस्करण</td>
    </tr>
    <tr>
        <td><a href="https://deno.com/">Deno</a></td>
        <td>yt-dlp एकीकरण के लिए रनटाइम</td>
    </tr>
    <tr class="section"><th colspan="2">पुस्तकालय और फ्रेमवर्क</th></tr>
    <tr>
        <td><a href="https://wiki.qt.io/Qt_for_Python">PySide6</a></td>
        <td>GUI फ्रेमवर्क</td>
    </tr>
    <tr>
        <td><a href="https://python-pillow.org/">Pillow</a></td>
        <td>छवि प्रसंस्करण</td>
    </tr>
    <tr>
        <td><a href="https://requests.readthedocs.io/">requests</a></td>
        <td>HTTP अनुरोध</td>
    </tr>
    <tr>
        <td><a href="https://packaging.python.org/">packaging</a></td>
        <td>संस्करण प्रबंधन और पैकेजिंग</td>
    </tr>
    <tr>
        <td><a href="https://python-markdown.github.io/">markdown</a></td>
        <td>Markdown रेंडरिंग</td>
    </tr>
    <tr>
        <td><a href="https://github.com/Delgan/loguru">loguru</a></td>
        <td>लॉगिंग</td>
    </tr>
    <tr class="section"><th colspan="2">एसेट्स और योगदानकर्ता</th></tr>
    <tr>
        <td><a href="https://pixabay.com/sound-effects/new-notification-09-352705/">New Notification 09 by Universfield</a></td>
        <td>अधिसूचना ध्वनि</td>
    </tr>
    <tr>
        <td><a href="https://github.com/viru185">viru185</a></td>
        <td>कोड योगदानकर्ता</td>
    </tr>
</table>

</div>

</details>

## ⚠️ अस्वीकरण

यह उपकरण केवल व्यक्तिगत उपयोग के लिए है। कृपया YouTube की सेवा की शर्तों और सामग्री रचनाकारों के अधिकारों का सम्मान करें।

---

<div align="center">

[oop7](https://github.com/oop7) द्वारा ❤️ के साथ बनाया गया

</div>
