<div align="center">

<img src="../branding/svg/ytsage-wordmark.svg" width="400" alt="ytsage-wordmark">
<img src="../branding/screenshots/main.png" width="800" alt="Интерфейс YTSage"/>

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-1f2937?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![PyPI Downloads](https://img.shields.io/pepy/dt/ytsage?color=1f2937&style=for-the-badge&label=downloads&logo=python&logoColor=white)](https://pepy.tech/project/ytsage)
[![GitHub Downloads](https://img.shields.io/github/downloads/oop7/YTSage/total?color=1f2937&style=for-the-badge&label=downloads&logo=github&logoColor=white)](https://github.com/oop7/YTSage/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-1f2937?style=for-the-badge&logo=opensource&logoColor=white)](https://opensource.org/licenses/MIT)
[![Supported Platforms](https://img.shields.io/badge/platform-cross--platform-1f2937?style=for-the-badge&logo=github&logoColor=white)](https://github.com/oop7/YTSage/releases)
[![GitHub Stars](https://img.shields.io/github/stars/oop7/YTSage?color=c90000&style=for-the-badge&logo=github&logoColor=white)](https://github.com/oop7/YTSage/stargazers)
[![PyPI version](https://img.shields.io/pypi/v/ytsage?color=c90000&style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/ytsage/)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/oop7?color=c90000&style=for-the-badge&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/oop7)

**Современный загрузчик с YouTube с чистым интерфейсом на PySide6.**  
Загружайте видео в любом качестве, извлекайте аудио, получайте субтитры и многое другое.

### 🌍 Языки README

Английский: [EN](../README.md)
| Арабский: [AR](README.ar.md)
| Немецкий: [DE](README.de.md)
| Испанский: [ES](README.es.md)
| Французский: [FR](README.fr.md)
| Хинди: [HI](README.hi.md)
| Индонезийский: [ID](README.id.md)
| Итальянский: [IT](README.it.md)
| Японский: [JA](README.ja.md)
| Польский: [PL](README.pl.md)
| Португальский: [PT](README.pt.md)
| Русский: [RU](README.ru.md)
| Турецкий: [TR](README.tr.md)
| Китайский: [ZH](README.zh.md)

<p align="center">
  <a href="#установка">Установка</a> •
  <a href="#функции">Функции</a> •
  <a href="#использование">Использование</a> •
  <a href="#скриншоты">Скриншоты</a> •
  <a href="#решение-проблем">Решение проблем</a> •
  <a href="#спонсорство">Спонсорство</a> •
  <a href="#участие-в-проекте">Участие в проекте</a>
</p>

</div>

---

<a id="почему-ytsage"></a>
## ❓ Почему YTSage?

YTSage создан для пользователей, которым нужен **простой, но мощный загрузчик с YouTube**. В отличие от других инструментов, он предлагает:

- Современный и чистый интерфейс PySide6
- Загрузку видео, аудио и субтитров одним щелчком мыши
- Дополнительные функции, такие как SponsorBlock, объединение субтитров и выбор плейлиста
- Опциональный "Общий режим" (Generic Mode) для сайтов помимо YouTube, поддерживаемых yt-dlp
- Кроссплатформенную поддержку и простую установку

<a id="функции"></a>
## ✨ Функции

<div align="center">

| Основные функции | Продвинутые функции | Дополнительные возможности |
|-----------------------------------|-----------------------------------------|------------------------------------|
| 🎥 Таблица форматов | 🚫 Интеграция SponsorBlock | 🎞️ Отображение FPS/HDR |
| 🎵 Извлечение аудио | 📝 Выбор и объединение субтитров | 🔄 Автообновление yt-dlp |
| ✨ Простой пользовательский интерфейс | 💾 Сохранение описания и обложки | 🛠️ Обнаружение FFmpeg/yt-dlp/Deno |
| 📋 Поддержка и выбор плейлиста | 🚀 Ограничение скорости | ⚙️ Пользовательские команды |
| 📑 Интеграция разделов | ✂️ Обрезка видео | 🍪 Вход через Cookies |
| 📜 История загрузок | 🔄 Выбор канала выпуска | 🌐 Поддержка прокси |
| 🎚️ Конвертация аудиоформатов | 🎬 Настройки видеоформата | 🆙 Встроенная вкладка обновления |
| 🌍 Общий режим | 🔊 Нормализация звука (EBU R128) | 🌍 Локализация на 14 языков |
| 💾 Экспорт плейлиста | ⚙️ Качество и субтитры по умолчанию | |
</div>

<a id="установка"></a>
## 🚀 Установка

### ⚡ Быстрая установка (Рекомендуется)

Установите YTSage через PyPI:

```bash
pip install ytsage
```

<details>
<summary>🔄 Обновить существующую установку</summary>

```bash
pip install --upgrade ytsage
```

</details>

Затем запустите приложение:

```bash
ytsage
```

### 📦 Готовые исполняемые файлы (Executable)

> [👉 Скачать последний релиз](https://github.com/oop7/YTSage/releases/latest)

#### 🪟 Windows

| Формат | Описание |
|--------|-------------|
| ![Windows EXE](https://img.shields.io/badge/Windows-EXE-0078D6?style=for-the-badge&logo=windows&logoColor=white) | Стандартный установщик |
| ![Windows FFmpeg](https://img.shields.io/badge/Windows-FFmpeg-0078D6?style=for-the-badge&logo=windows&logoColor=white) | С включенным FFmpeg |
| ![Windows Portable](https://img.shields.io/badge/Windows-Portable-0078D6?style=for-the-badge&logo=windows&logoColor=white) | Портативная версия (не требует установки) |
| ![Windows Portable FFmpeg](https://img.shields.io/badge/Windows-Portable%20FFmpeg-0078D6?style=for-the-badge&logo=windows&logoColor=white) | Портативная с FFmpeg, сжатая (ZIP) |

<details>
<summary>🛠️ Шаги по установке</summary>

1. **EXE установщик (`.exe`)**: Дважды щелкните файл и следуйте инструкциям мастера установки.
2. **Портативная версия (`.zip`)**: Распакуйте файл в нужное место и запустите `ytsage.exe`.
3. **Встроенный FFmpeg**: Если в вашей системе не установлен FFmpeg, выбирайте версии со встроенным FFmpeg.
</details>

#### 🐧 Linux

| Формат | Описание |
|--------|-------------|
| ![Linux DEB](https://img.shields.io/badge/Linux-DEB-FCC624?style=for-the-badge&logo=linux&logoColor=black) | Пакет Debian |
| ![Linux AppImage](https://img.shields.io/badge/Linux-AppImage-FCC624?style=for-the-badge&logo=linux&logoColor=black) | AppImage, Портативный |
| ![Linux RPM](https://img.shields.io/badge/Linux-RPM-FCC624?style=for-the-badge&logo=linux&logoColor=black) | Пакет RPM |
| ![Flathub](https://img.shields.io/badge/Linux-Flatpak-FCC624?style=for-the-badge&logo=flathub&logoColor=black) | Пакет Flatpak |

<details>
<summary>🛠️ Шаги по установке</summary>

- **DEB (`.deb`)**:
  ```bash
  sudo dpkg -i ytsage_*.deb
  sudo apt-get install -f # Если нужно исправить зависимости
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
- **Flatpak**: Следуйте инструкциям на Flathub или выполните:
  ```bash
  flatpak install flathub io.github.oop7.ytsage
  ```
</details>

#### 🍎 macOS

| Формат | Описание |
|--------|-------------|
| ![macOS ARM64 APP](https://img.shields.io/badge/macOS-ARM64%20APP-000000?style=for-the-badge&logo=apple&logoColor=white) | Приложение ZIP для Apple Silicon |
| ![macOS ARM64 DMG](https://img.shields.io/badge/macOS-ARM64%20DMG-000000?style=for-the-badge&logo=apple&logoColor=white) | Установщик DMG для Apple Silicon |

<details>
<summary>🛠️ Шаги по установке</summary>

- **DMG установщик (`.dmg`)**: Дважды щелкните, чтобы смонтировать, и перетащите `YTSage.app` в папку Applications (Программы).
- **Приложение в архиве (`.zip`)**: Распакуйте ZIP и переместите `YTSage.app` в папку Applications.

*Примечание: Если вы получили ошибку "App is damaged", см. раздел по macOS ниже.*
</details>

---

<details>
<summary>💻 Ручная установка из исходного кода</summary>

### 1. Клонировать репозиторий

```bash
git clone https://github.com/oop7/YTSage.git
cd YTSage
```

### 2. Установить зависимости

#### ⚡ С помощью uv

```bash
uv pip install .
```

#### 📦 Или через стандартный pip

```bash
pip install .
```

### 3. Запустить приложение

```bash
python -m ytsage.main
```

</details>

<a id="скриншоты"></a>
## 📸 Скриншоты

<div align="center">
<table>
  <tr>
    <td><img src="../branding/screenshots/Download-Settings.png" alt="Настройки загрузки" width="400"/></td>
    <td><img src="../branding/screenshots/playlist.png" alt="Загрузка плейлиста" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><em>Настройки загрузки</em></td>
    <td align="center"><em>Загрузка плейлиста</em></td>
  </tr>
  <tr>
    <td><img src="../branding/screenshots/audio_format.png" alt="Выбор аудиоформата" width="400"/></td>
    <td><img src="../branding/screenshots/Custom-Option.png" alt="Пользовательские опции" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><em>Аудиоформат</em></td>
    <td align="center"><em>Пользовательские опции</em></td>
  </tr>
</table>
</div>

<a id="использование"></a>
## 📖 Использование

<details>
<summary>🎯 Базовое использование</summary>

1. **Запустите YTSage**
2. **Вставьте ссылку на YouTube** (или используйте кнопку "Paste URL")
3. **Нажмите "Analyze"**
4. **Выберите формат:**
   - `Video` для загрузки видео
   - `Audio Only` для извлечения аудио
5. **Выберите опции:**
   - Включите субтитры и выберите язык
   - Включите объединение субтитров (Merge)
   - Сохранить обложку (Save Thumbnail)
   - Удалить спонсорские вставки (SponsorBlock)
   - Сохранить описание (Save Description)
   - Внедрить главы (Embed Chapters)
6. **Выберите папку для сохранения**
7. **Нажмите "Download"**

> 💡 Папка загрузок по умолчанию — папка "Загрузки" текущего пользователя.

</details>

<details>
<summary>📋 Загрузка плейлиста</summary>

1. **Вставьте ссылку на плейлист**
2. **Нажмите "Analyze"**
3. **Выберите видео в селекторе (по умолчанию выбраны все)**
4. **Выберите нужный формат/качество**
5. **Нажмите "Download"**

> 💡 Приложение автоматически управляет очередью загрузки, и вы можете экспортировать записи плейлиста в файлы `.txt`, `.csv`, `.m3u` или `.json`.

</details>

<details>
<summary>🌍 Общий режим для сайтов помимо YouTube</summary>

Используйте Общий режим (Generic Mode), когда хотите, чтобы YTSage принимал ссылки с других сайтов, поддерживаемых yt-dlp, таких как Dailymotion, TikTok и другие.

Как использовать:

1. Откройте `Download Settings`.
2. Включите `Generic Mode`.
3. Вставьте ссылку на видео или плейлист с поддерживаемого сайта (не YouTube).
4. Нажмите `Analyze`.
5. Выберите формат и скачайте как обычно.

Примечания:

- Общий режим только отключает строгую проверку URL внутри YTSage. Сайт все равно должен поддерживаться установленной версией yt-dlp.
- Некоторым сайтам требуются cookies, вход, прокси или дополнительные аргументы yt-dlp.
- Если сайт перестал работать, обновите yt-dlp во встроенной вкладке обновления, прежде чем сообщать о проблеме.

</details>

<details>
<summary>🧰 Опции медиа и загрузки</summary>

- **Опции субтитров:** Фильтруйте языки и внедряйте субтитры в видеофайл.
- **Объединение субтитров:** "Вшивает" субтитры в видеофайл (hardcode).
- **Сохранить описание:** Сохраняет описание видео в текстовый файл.
- **Сохранить обложку:** Сохраняет превью видео как изображение.
- **Внедрить главы:** Добавляет маркеры глав в метаданные для совместимых медиаплееров.
- **Удалить спонсорские вставки:** Использует SponsorBlock для удаления рекламных сегментов из видео.
- **Обрезать видео:** Загружайте только части видео, указав временной интервал в формате `HH:MM:SS`.

</details>

<details>
<summary>⚙️ Настройки вывода и файлов</summary>

- **Ограничение скорости:** Ограничьте скорость загрузки, например, `500K` для 500 КБ/с.
- **Путь загрузки:** Сохраните путь по умолчанию для будущих загрузок. Доступно в **Download Settings → Download Path**.
- **Разрешение по умолчанию:** Установите предпочитаемое разрешение для автовыбора (например, 1080p, 720p). Доступно в **Download Settings → Default Video Resolution**.
- **Языки субтитров по умолчанию:** Установите языки по умолчанию для автовыбора (через запятую, например, `ru,en`). Доступно в **Download Settings → Default Subtitle Languages**.
- **Формат имени файла:** Настройте формат имени выходного файла, используя переменные типа `%(title)s`, `%(uploader)s` и др. Доступно в **Download Settings → Filename Format**.
- **Принудительный формат вывода:** Принудительно скачивайте видео в определенном контейнере, например `mp4`, `webm` или `mkv`. Доступно в **Download Settings → Output Format Settings**.
- **Конвертация аудио:** Конвертируйте аудио в форматы `AAC`, `MP3`, `FLAC`, `WAV`, `Opus`, `M4A`, `Vorbis`, или `Best`. Доступно в **Download Settings → Audio Format Settings**.
- **Нормализация звука:** Выравнивает громкость аудио загрузок согласно EBU R128.
- **Одновременные соединения:** Значительно увеличивает скорость за счет загрузки в несколько потоков. Доступно в **Download Settings → General → Concurrent Connections** (рекомендуется 8-10).

</details>

<details>
<summary>🌐 Доступ и сеть</summary>

- **Вход через Cookies:** Войдите в YouTube через куки для доступа к приватному контенту.
  Как использовать:
  1. **Рекомендуется:** Используйте встроенную опцию `Extract cookies from browser`, выберите браузер и профиль.
  2. Или вручную:
     a. Экспортируйте куки через расширение [cookie-editor](https://github.com/moustachauve/cookie-editor).
     b. Скопируйте куки в формате Netscape.
     c. Создайте файл `cookies.txt` и вставьте их туда.
     d. Выберите этот файл в приложении.
- **Поддержка прокси:** Используйте прокси-сервер для загрузок, например: `http://<proxy-server>:<port>`
- **Общий режим:** Позволяет скачивать с сайтов помимо YouTube. Включите в **Download Settings → Generic Mode**.

</details>

<details>
<summary>🛠️ Инструменты и обслуживание</summary>

- **Пользовательские команды:** Доступ к продвинутым функциям yt-dlp через аргументы командной строки.
- **Вкладка обновления:** Управляйте инструментами в одном месте (Custom Options):
  - **Обновление yt-dlp:** Проверка обновлений, переключение между Stable и Nightly ветками.
  - **Версия FFmpeg:** Проверка версии и инструкции по установке.
  - **Обновление Deno:** Проверка и обновление Deno.
- **Обнаружение FFmpeg/yt-dlp/Deno:** Автоматически находит пути и версии в окне "About".
- **История загрузок:** Просматривайте историю с обложками и статусом через кнопку **History**.

</details>

<details>
<summary>🌍 Локализация</summary>

YTSage поддерживает **14 языков**. Выберите нужный в **Custom Options → Language**.

### Поддерживаемые языки

| Язык | Код | Язык | Код |
|----------|------|----------|------|
| 🇺🇸 Английский | `en` | 🇪🇸 Испанский | `es` |
| 🇸🇦 Арабский | `ar` | 🇫🇷 Французский | `fr` |
| 🇩🇪 Немецкий | `de` | 🇮🇳 Хинди | `hi` |
| 🇮🇩 Индонезийский | `id` | 🇮🇹 Итальянский | `it` |
| 🇯🇵 Японский | `ja` | 🇵🇱 Польский | `pl` |
| 🇧🇷 Португальский | `pt` | 🇷🇺 Русский | `ru` |
| 🇹🇷 Турецкий | `tr` | 🇨🇳 Китайский | `zh` |

### Переводы README

| Язык | Файл | Язык | Файл |
|----------|------|----------|------|
| 🇺🇸 Английский | [README.md](../README.md) | 🇪🇸 Испанский | [README.es.md](README.es.md) |
| 🇸🇦 Арабский | [README.ar.md](README.ar.md) | 🇫🇷 Французский | [README.fr.md](README.fr.md) |
| 🇩🇪 Немецкий | [README.de.md](README.de.md) | 🇮🇳 Хинди | [README.hi.md](README.hi.md) |
| 🇮🇩 Индонезийский | [README.id.md](README.id.md) | 🇮🇹 Итальянский | [README.it.md](README.it.md) |
| 🇯🇵 Японский | [README.ja.md](README.ja.md) | 🇵🇱 Польский | [README.pl.md](README.pl.md) |
| 🇧🇷 Португальский | [README.pt.md](README.pt.md) | 🇷🇺 Русский | [README.ru.md](README.ru.md) |
| 🇹🇷 Турецкий | [README.tr.md](README.tr.md) | 🇨🇳 Китайский | [README.zh.md](README.zh.md) |

> 💡 **Хотите помочь с переводом?** Ознакомьтесь с разделом [Участие в проекте](#участие-в-проекте), чтобы помочь нам добавить новые языки!

</details>

<a id="решение-проблем"></a>
## 🛠️ Решение проблем

<details>
<summary>Нажмите, чтобы увидеть частые вопросы</summary>

- **Не появляется таблица форматов:** Обновите yt-dlp до последней версии и попробуйте переключиться на канал Nightly.
- **Загрузка не удалась:** Проверьте интернет-соединение и доступность видео.
- **Специфические ошибки:**
  - **Приватные видео:** Используйте вход через Cookies.
  - **Ограничение по возрасту:** Войдите в аккаунт YouTube.
  - **Геоблокировка:** Используйте VPN.
  - **Видео удалено:** Видео больше недоступно на YouTube.
  - **Прямые трансляции:** Стримы нельзя скачать, пока они идут; дождитесь завершения.
  - **Сетевые ошибки:** Проверьте подключение к интернету и повторите попытку.
  - **Неверный URL:** Убедитесь, что URL указан правильно и принадлежит поддерживаемой платформе.
  - **Премиум-контент:** Требуется подписка YouTube Premium.
  - **Блокировка авторских прав:** Контент заблокирован из-за ограничений авторского права.
- **Видео и аудио разделены после загрузки:** Это происходит, если FFmpeg отсутствует или не обнаружен. YTSage нужен FFmpeg для объединения потоков.
  - **Решение:** Убедитесь, что FFmpeg установлен и добавлен в PATH. Пользователям Windows проще всего скачать версию с `-ffmpeg.exe`.

---

#### 🛡️ Предупреждение Windows Defender / Антивируса

Некоторые антивирусы могут помечать `.exe` файлы как ложные срабатывания. Это **известная особенность** упакованных приложений.

**Причины:**
- Эвристические алгоритмы антивирусов могут ошибочно идентифицировать упакованные исполняемые файлы как подозрительные.

**Безопасные варианты:**
- ✅ **Установка через pip:** `pip install ytsage` (рекомендуется)
- ✅ **Сборка из исходников**: Инструкция [здесь](../.github/CI_CD_README.md)
- ✅ **Добавить в исключения** антивируса.

#### 🍎 macOS: "App is damaged and cannot be opened"
Если вы видите эту ошибку на macOS Sonoma или новее:

1.  **Откройте Терминал**.
2.  **Введите команду** (с пробелом в конце):
    ```bash
    xattr -d com.apple.quarantine 
    ```
3.  **Перетащите `YTSage.app`** из Finder в окно Терминала.
4.  **Нажмите Enter**.
5.  Попробуйте открыть программу снова.

---

#### **Пути конфигурации (Продвинутым)**
- **Windows:** `%LOCALAPPDATA%\YTSage`
- **macOS:** `~/Library/Application Support/YTSage`
- **Linux:** `~/.local/share/YTSage`

</details>

<a id="спонсорство"></a>
## 💖 Спонсорство

Если YTSage экономит ваше время, поддержите разработку проекта. Спонсорство помогает поддерживать тестирование на всех платформах и внедрять новые функции.

- GitHub Sponsors: https://github.com/sponsors/oop7
- Ссылка на спонсорство также есть в окне "About" в приложении.

[![Sponsor YTSage](https://img.shields.io/badge/Sponsor-YTSage-EA4AAA?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sponsors/oop7)

<a id="участие-в-проекте"></a>
## 👥 Участие в проекте

Мы рады любой помощи!

1. 🍴 Сделайте Fork репозитория
2. 🌿 Создайте ветку: `git checkout -b feature/NewFeature`
3. 💾 Сделайте коммит: `git commit -m 'Add NewFeature'`
4. 📤 Отправите изменения: `git push origin feature/NewFeature`
5. 🔄 Создайте Pull Request

### 🌍 Помощь с переводами

- Обновите файл README (например, `readme-translations/README.ru.md`)
- Обновите строки интерфейса в `ytsage/languages/<code>.json`
- Если ваш язык отсутствует, начните с `README.md` и создайте `README.<code>.md`

<details>
<summary>📂 Структура проекта</summary>

## YTSage - Структура проекта

Этот документ описывает организованную структуру папок YTSage.

### 📁 Схема проекта

```
YTSage/
├── 📁 .github/                   # Настройки GitHub
│   ├── 📁 ISSUE_TEMPLATE/         # Шаблоны проблем
│   │   └── 🐛-bug-report.md       # Шаблон отчета об ошибке
│   ├─── 📁 workflows/              # Рабочие процессы GitHub Actions
│   │   ├── build-linux.yml        # Сборка для Linux
│   │   ├── build-macos.yml        # Сборка для macOS
│   │   │── build-windows.yml      # Сборка для Windows
|   |   └── release-all.yml          # Основной процесс выпуска
│   └── 📄 CI_CD_README.md        # Документация CI/CD
├──  📁 branding/                 # Брендинг (скриншоты, SVG)
│   ├── 📁 icons/                 # Иконки приложения
│   ├── 📁 screenshots/           # Скриншоты для документации
│   └── 📁 svg/                   # SVG ассеты
├── 📄 LICENSE                    # Файл лицензии
├── 📄 pyproject.toml             # Метаданные проекта и зависимости
├── 📄 README.md                  # Документация проекта
├── 📄 requirements.txt           # Зависимости Python (разработка)
└── 📁 ytsage/                    # Исходный код
    ├── 📁 assets/                # Ресурсы времени выполнения
    │   ├── 📁 Icon/              # Иконки приложения
    │   └── 📁 sound/             # Звуковые файлы
    ├── 📁 languages/             # Файлы локализации
    │   ├── 📄 ar.json            # Перевод на арабский
    │   ├── 📄 de.json            # Перевод на немецкий
    │   ├── 📄 en.json            # Перевод на английский
    │   └── ...                   # Другие языки
    ├── 📁 core/                  # Основная бизнес-логика
    │   ├── 📄 __init__.py        
    │   ├── 📄 ytsage_deno.py     # Интеграция Deno
    │   ├── 📄 ytsage_downloader.py # Функционал загрузки
    │   ├── 📄 ytsage_ffmpeg.py   # Интеграция FFmpeg
    │   ├── 📄 ytsage_utils.py    # Вспомогательные функции
    │   └── 📄 ytsage_yt_dlp.py   # Интеграция yt-dlp
    ├── 📁 gui/                   # Компоненты интерфейса
    │   ├── 📄 __init__.py        
    │   ├── 📄 ytsage_gui_main.py # Главное окно приложения
    │   └── 📁 ytsage_gui_dialogs/ # Классы диалогов
    ├── 📁 utils/                 # Утилиты
    │   ├── 📄 __init__.py        
    │   ├── 📄 ytsage_config_manager.py # Управление конфигурацией
    │   └── 📄 ytsage_logger.py   # Логирование
    ├── 📄 __init__.py            # Точка входа в пакет
    └── 📄 main.py                # Основной скрипт запуска
```

</details>

## ⭐️ История звезд

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

## 📜 Лицензия

Проект распространяется под лицензией MIT — подробности в файле [LICENSE](../LICENSE).

## 🙏 Благодарности

<details>
<summary>Показать благодарности</summary>

<div align="center">

<p>Большое спасибо всем, кто внес свой вклад в этот проект, открывая проблемы с предложениями по улучшению или отчетами об ошибках.</p>

<table>
    <tr class="section"><th colspan="2">Основные компоненты</th></tr>
    <tr>
        <td width="35%"><a href="https://github.com/yt-dlp/yt-dlp">yt-dlp</a></td>
        <td>Движок загрузки</td>
    </tr>
    <tr>
        <td><a href="https://ffmpeg.org/">FFmpeg</a></td>
        <td>Обработка медиа</td>
    </tr>
    <tr>
        <td><a href="https://deno.com/">Deno</a></td>
        <td>Среда для интеграции yt-dlp</td>
    </tr>
    <tr class="section"><th colspan="2">Библиотеки и фреймворки</th></tr>
    <tr>
        <td><a href="https://wiki.qt.io/Qt_for_Python">PySide6</a></td>
        <td>GUI фреймворк</td>
    </tr>
    <tr>
        <td><a href="https://python-pillow.org/">Pillow</a></td>
        <td>Обработка изображений</td>
    </tr>
    <tr>
        <td><a href="https://requests.readthedocs.io/">requests</a></td>
        <td>HTTP запросы</td>
    </tr>
    <tr>
        <td><a href="https://packaging.python.org/">packaging</a></td>
        <td>Управление версиями</td>
    </tr>
    <tr>
        <td><a href="https://python-markdown.github.io/">markdown</a></td>
        <td>Рендеринг Markdown</td>
    </tr>
    <tr>
        <td><a href="https://github.com/Delgan/loguru">loguru</a></td>
        <td>Логирование</td>
    </tr>
    <tr class="section"><th colspan="2">Контент и участники</th></tr>
    <tr>
        <td><a href="https://pixabay.com/sound-effects/new-notification-09-352705/">New Notification 09 от Universfield</a></td>
        <td>Звук уведомления</td>
    </tr>
    <tr>
        <td><a href="https://github.com/viru185">viru185</a></td>
        <td>Участник разработки</td>
    </tr>
</table>

</div>

</details>

## ⚠️ Отказ от ответственности

Этот инструмент предназначен только для личного использования. Пожалуйста, соблюдайте Условия использования YouTube и права создателей контента.

---

<div align="center">
Сделано с ❤️ от [oop7](https://github.com/oop7)
</div>
