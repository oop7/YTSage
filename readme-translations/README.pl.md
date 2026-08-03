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

**Nowoczesny downloader YouTube z czystym interfejsem PySide6.**  
Pobieraj wideo w dowolnej jakości, wyodrębniaj audio, pobieraj napisy i wiele więcej.

### 🌍 Języki README

Angielski: [EN](../README.md)
| Arabski: [AR](README.ar.md)
| Niemiecki: [DE](README.de.md)
| Hiszpański: [ES](README.es.md)
| Francuski: [FR](README.fr.md)
| Hindi: [HI](README.hi.md)
| Indonezyjski: [ID](README.id.md)
| Włoski: [IT](README.it.md)
| Japoński: [JA](README.ja.md)
| Polski: [PL](README.pl.md)
| Portugalski: [PT](README.pt.md)
| Rosyjski: [RU](README.ru.md)
| Turecki: [TR](README.tr.md)
| Chiński: [ZH](README.zh.md)

<p align="center">
  <a href="#instalacja">Instalacja</a> •
  <a href="#funkcje">Funkcje</a> •
  <a href="#użycie">Użycie</a> •
  <a href="#zrzuty-ekranu">Zrzuty ekranu</a> •
  <a href="#rozwiązywanie-problemów">Rozwiązywanie problemów</a> •
  <a href="#sponsor">Sponsor</a> •
  <a href="#współpraca">Współpraca</a>
</p>

</div>

---

<a id="dlaczego-ytsage"></a>
## ❓ Dlaczego YTSage?

YTSage został zaprojektowany dla użytkowników, którzy chcą **prostego, ale potężnego downloadera YouTube**. W przeciwieństwie do innych narzędzi oferuje:

- Nowoczesny i czysty interfejs PySide6
- Pobieranie wideo, audio i napisów jednym kliknięciem
- Zaawansowane funkcje, takie jak SponsorBlock, scalanie napisów i wybór playlisty
- Opcjonalny tryb ogólny (Generic Mode) dla stron spoza YouTube obsługiwanych przez yt-dlp
- Obsługa wielu platform i łatwa instalacja

<a id="funkcje"></a>
## ✨ Funkcje

<div align="center">

| Funkcje podstawowe | Funkcje zaawansowane | Funkcje dodatkowe |
|-----------------------------------|-----------------------------------------|------------------------------------|
| 🎥 Tabela formatów | 🚫 Integracja SponsorBlock | 🎞️ Wyświetlanie FPS/HDR |
| 🎵 Wyodrębnianie audio | 📝 Wybór i scalanie napisów | 🔄 Auto-aktualizacja yt-dlp |
| ✨ Prosty interfejs użytkownika | 💾 Zapis opisu i miniatur | 🛠️ Wykrywanie FFmpeg/yt-dlp/Deno |
| 📋 Obsługa i wybór playlist | 🚀 Ogranicznik prędkości | ⚙️ Własne komendy |
| 📑 Integracja rozdziałów | ✂️ Przycinanie sekcji wideo | 🍪 Logowanie przez ciasteczka |
| 📜 Historia pobierania | 🔄 Wybór kanału wydań | 🌐 Obsługa proxy |
| 🎚️ Konwersja formatów audio | 🎬 Ustawienia formatu wideo | 🆙 Zintegrowana karta aktualizacji |
| 🌍 Tryb ogólny | 🔊 Normalizacja audio (EBU R128) | 🌍 Lokalizacja w 14 językach |
| 💾 Eksport playlisty | ⚙️ Domyślna jakość i napisy | |
</div>

<a id="instalacja"></a>
## 🚀 Instalacja

### ⚡ Szybka instalacja (zalecana)

Zainstaluj YTSage przez PyPI:

```bash
pip install ytsage
```

<details>
<summary>🔄 Aktualizacja istniejącej instalacji</summary>

```bash
pip install --upgrade ytsage
```

</details>

Następnie uruchom aplikację:

```bash
ytsage
```

### 📦 Gotowe pliki wykonywalne (Executable)

> [👉 Pobierz najnowsze wydanie](https://github.com/oop7/YTSage/releases/latest)

#### 🪟 Windows

| Format | Opis |
|--------|-------------|
| ![Windows EXE](https://img.shields.io/badge/Windows-EXE-0078D6?style=for-the-badge&logo=windows&logoColor=white) | Standardowy instalator |
| ![Windows FFmpeg](https://img.shields.io/badge/Windows-FFmpeg-0078D6?style=for-the-badge&logo=windows&logoColor=white) | Z dołączonym FFmpeg |
| ![Windows Portable](https://img.shields.io/badge/Windows-Portable-0078D6?style=for-the-badge&logo=windows&logoColor=white) | Wersja przenośna, nie wymaga instalacji |
| ![Windows Portable FFmpeg](https://img.shields.io/badge/Windows-Portable%20FFmpeg-0078D6?style=for-the-badge&logo=windows&logoColor=white) | Przenośna z FFmpeg, skompresowana (ZIP) |

<details>
<summary>🛠️ Kroki instalacji</summary>

1. **Instalator EXE (`.exe`)**: Kliknij dwukrotnie plik i postępuj zgodnie z instrukcjami kreatora.
2. **Wersja przenośna (`.zip`)**: Rozpakuj archiwum w wybranym miejscu i uruchom `ytsage.exe`.
3. **Wbudowany FFmpeg**: Jeśli nie masz zainstalowanego FFmpeg w systemie, wybierz wersję z dołączonym FFmpeg.
</details>

#### 🐧 Linux

| Format | Opis |
|--------|-------------|
| ![Linux DEB](https://img.shields.io/badge/Linux-DEB-FCC624?style=for-the-badge&logo=linux&logoColor=black) | Pakiet Debian |
| ![Linux AppImage](https://img.shields.io/badge/Linux-AppImage-FCC624?style=for-the-badge&logo=linux&logoColor=black) | AppImage, przenośny |
| ![Linux RPM](https://img.shields.io/badge/Linux-RPM-FCC624?style=for-the-badge&logo=linux&logoColor=black) | Pakiet RPM |
| ![Flathub](https://img.shields.io/badge/Linux-Flatpak-FCC624?style=for-the-badge&logo=flathub&logoColor=black) | Pakiet Flatpak |

<details>
<summary>🛠️ Kroki instalacji</summary>

- **DEB (`.deb`)**:
  ```bash
  sudo dpkg -i ytsage_*.deb
  sudo apt-get install -f # Jeśli trzeba naprawić brakujące zależności
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
- **Flatpak**: Postępuj zgodnie z instrukcjami na Flathub lub uruchom:
  ```bash
  flatpak install flathub io.github.oop7.ytsage
  ```
</details>

#### 🍎 macOS

| Format | Opis |
|--------|-------------|
| ![macOS ARM64 APP](https://img.shields.io/badge/macOS-ARM64%20APP-000000?style=for-the-badge&logo=apple&logoColor=white) | Aplikacja ZIP dla Apple Silicon |
| ![macOS ARM64 DMG](https://img.shields.io/badge/macOS-ARM64%20DMG-000000?style=for-the-badge&logo=apple&logoColor=white) | Instalator Disk Image dla Apple Silicon |

<details>
<summary>🛠️ Kroki instalacji</summary>

- **Instalator DMG (`.dmg`)**: Kliknij dwukrotnie, aby zamontować, a następnie przeciągnij `YTSage.app` do folderu Aplikacje.
- **Archiwum aplikacji (`.zip`)**: Rozpakuj ZIP i przenieś `YTSage.app` do folderu Aplikacje.

*Uwaga: Jeśli otrzymasz błąd "Aplikacja jest uszkodzona", zapoznaj się z sekcją rozwiązywania problemów macOS poniżej.*
</details>

---

<details>
<summary>💻 Ręczna instalacja ze źródeł</summary>

### 1. Sklonuj repozytorium

```bash
git clone https://github.com/oop7/YTSage.git
cd YTSage
```

### 2. Zainstaluj zależności

#### ⚡ Z użyciem uv

```bash
uv pip install .
```

#### 📦 Lub ze standardowym pip

```bash
pip install .
```

### 3. Uruchom aplikację

```bash
python -m ytsage.main
```

</details>

<a id="zrzuty-ekranu"></a>
## 📸 Zrzuty ekranu

<div align="center">
<table>
  <tr>
    <td><img src="../branding/screenshots/Download-Settings.png" alt="Ustawienia pobierania" width="400"/></td>
    <td><img src="../branding/screenshots/playlist.png" alt="Pobieranie playlisty" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><em>Ustawienia pobierania</em></td>
    <td align="center"><em>Pobieranie playlisty</em></td>
  </tr>
  <tr>
    <td><img src="../branding/screenshots/audio_format.png" alt="Wybór formatu audio" width="400"/></td>
    <td><img src="../branding/screenshots/Custom-Option.png" alt="Opcje niestandardowe" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><em>Format audio</em></td>
    <td align="center"><em>Opcje niestandardowe</em></td>
  </tr>
</table>
</div>

<a id="użycie"></a>
## 📖 Użycie

<details>
<summary>🎯 Podstawowe użycie</summary>

1. **Uruchom YTSage**
2. **Wklej URL z YouTube** (lub użyj przycisku "Wklej URL")
3. **Kliknij "Analizuj"**
4. **Wybierz format:**
   - `Wideo` dla pobierania wideo
   - `Tylko audio` dla wyodrębniania dźwięku
5. **Wybierz opcje:**
   - Włącz napisy i wybierz język
   - Włącz scalanie napisów
   - Zapisz miniaturę
   - Usuń sekcje sponsorowane
   - Zapisz opis
   - Osadź rozdziały
6. **Wybierz folder wyjściowy**
7. **Kliknij "Pobierz"**

> 💡 Domyślny folder pobierania to folder "Pobrane" użytkownika.

</details>

<details>
<summary>📋 Pobieranie playlisty</summary>

1. **Wklej URL playlisty**
2. **Kliknij "Analizuj"**
3. **Wybierz filmy z selektora (opcjonalnie, domyślnie wszystkie)**
4. **Wybierz żądany format/jakość**
5. **Kliknij "Pobierz"**

> 💡 Aplikacja automatycznie zarządza kolejką pobierania, a wpisy playlisty możesz eksportować do plików `.txt`, `.csv`, `.m3u` lub `.json`.

</details>

<details>
<summary>🌍 Tryb ogólny dla stron innych niż YouTube</summary>

Użyj trybu ogólnego (Generic Mode), gdy chcesz, aby YTSage akceptował adresy URL ze stron obsługiwanych przez yt-dlp, takich jak Dailymotion, CBC Gem, TikTok i inne.

Jak go użyć:

1. Otwórz `Download Settings`.
2. Włącz `Generic Mode`.
3. Wklej obsługiwany URL wideo lub playlisty spoza YouTube.
4. Kliknij `Analyze`.
5. Wybierz format i pobierz jak zwykle.

Uwagi:

- Tryb ogólny zmienia tylko walidację adresu URL wewnątrz YTSage. Strona docelowa musi być nadal obsługiwana przez zainstalowaną wersję yt-dlp.
- Niektóre strony wymagają ciasteczek, logowania, proxy lub dodatkowych argumentów yt-dlp w zależności od ekstraktora.
- Jeśli strona nie działa, zaktualizuj yt-dlp ze zintegrowanej karty aktualizacji przed zgłoszeniem problemu.

</details>

<details>
<summary>🧰 Opcje mediów i pobierania</summary>

- **Opcje napisów:** Filtruj języki i osadzaj napisy w pliku wideo.
- **Scalanie napisów:** Scala napisy z plikiem wideo (hardcoded).
- **Zapis opisu:** Zapisuje opis wideo jako plik tekstowy.
- **Zapis miniatury:** Zapisuje miniaturę wideo jako plik graficzny.
- **Osadź rozdziały:** Dołącza znaczniki rozdziałów jako metadane dla kompatybilnych odtwarzaczy.
- **Usuń sekcje sponsorowane:** Używa SponsorBlock do usuwania segmentów sponsorowanych z filmu.
- **Przycinanie wideo:** Pobieraj tylko określone części filmu, określając zakres czasu w formacie `GG:MM:SS`.

</details>

<details>
<summary>⚙️ Ustawienia wyjściowe i plików</summary>

- **Ogranicznik prędkości:** Ogranicz prędkość pobierania, np. `500K` dla 500 KB/s.
- **Zapisz ścieżkę pobierania:** Zapisuje domyślną ścieżkę dla przyszłych pobrań. Dostępne w **Download Settings → Download Path**.
- **Domyślna rozdzielczość wideo:** Ustaw preferowaną rozdzielczość dla automatycznego wyboru (np. 1080p, 720p). Dostępne w **Download Settings → Default Video Resolution**.
- **Domyślne języki napisów:** Ustaw domyślne języki dla automatycznego wyboru (rozdzielone przecinkami, np. `pl,en`). Dostępne w **Download Settings → Default Subtitle Languages**.
- **Format nazwy pliku:** Dostosuj format nazwy pliku wyjściowego, używając zmiennych takich jak `%(title)s`, `%(uploader)s`, `%(playlist_index)s` i `%(resolution)s`. Dostępne w **Download Settings → Filename Format**.
- **Wymuś format wyjściowy:** Wymuś pobieranie wideo do konkretnego formatu kontenera, jak `mp4`, `webm` lub `mkv`. Dostępne w **Download Settings → Output Format Settings**.
- **Konwersja formatów audio:** Konwertuj pobierany dźwięk do preferowanego formatu, takiego jak `AAC`, `MP3`, `FLAC`, `WAV`, `Opus`, `M4A`, `Vorbis` lub `Best`. Dostępne w **Download Settings → Audio Format Settings**.
- **Normalizacja audio:** Ujednolica głośność pobieranego dźwięku przy użyciu EBU R128.
- **Jednoczesne połączenia:** Znacznie zwiększa prędkość pobierania, pobierając pliki w kilku częściach naraz. Dostępne w **Download Settings → General → Concurrent Connections** (domyślnie 1, zalecane maks. 8-10, aby uniknąć blokad IP).

</details>

<details>
<summary>🌐 Dostęp i sieć</summary>

- **Logowanie przez ciasteczka:** Zaloguj się do YouTube, używając ciasteczek, aby uzyskać dostęp do prywatnych treści.
  Użycie:
  1. **Zalecane:** Użyj wbudowanej opcji `Eksportuj ciasteczka z przeglądarki`, a następnie wybierz przeglądarkę i opcjonalnie profil.
  2. Alternatywnie, wyeksportuj ciasteczka ręcznie:
     a. Eksportuj ciasteczka z przeglądarki, używając rozszerzenia typu [cookie-editor](https://github.com/moustachauve/cookie-editor?tab=readme-ov-file)
     b. Skopiuj ciasteczka w formacie Netscape
     c. Utwórz plik o nazwie `cookies.txt` i wklej ciasteczka
     d. Wybierz plik `cookies.txt` w aplikacji
- **Obsługa proxy:** Użyj serwera proxy do pobierania, np. `http://<serwer-proxy>:<port>`
- **Tryb ogólny:** Pozwala YTSage na analizę i pobieranie z witryn innych niż YouTube obsługiwanych przez yt-dlp. Włącz w **Download Settings → Generic Mode**.

</details>

<details>
<summary>🛠️ Narzędzia i konserwacja</summary>

- **Własne komendy:** Dostęp do zaawansowanych funkcji yt-dlp poprzez argumenty wiersza poleceń.
- **Karta aktualizacji:** Zarządzaj wbudowanymi narzędziami aktualizacji z jednego miejsca w opcjach niestandardowych:
  - **Aktualizacja yt-dlp:** Sprawdzaj aktualizacje i przełączaj się między kanałami Stable i Nightly.
  - **Sprawdzanie wersji FFmpeg:** Weryfikuj wersję FFmpeg i otwieraj przewodniki instalacji.
  - **Aktualizacja Deno:** Sprawdzaj i aktualizuj środowisko uruchomieniowe Deno.
- **Wykrywanie FFmpeg/yt-dlp/Deno:** Automatycznie wykrywa ścieżki i wersje FFmpeg, yt-dlp i Deno w oknie "O programie".
- **Historia pobierania:** Przeglądaj poprzednie pobrania z miniaturami i statusami za pomocą przycisku **History**.

</details>

<details>
<summary>🌍 Lokalizacja</summary>

YTSage obsługuje **14 języków**. Wybierz preferowany język w **Custom Options → Language**.

### Obsługiwane języki

| Język | Kod | Język | Kod |
|----------|------|----------|------|
| 🇺🇸 Angielski | `en` | 🇪🇸 Hiszpański | `es` |
| 🇸🇦 Arabski | `ar` | 🇫🇷 Francuski | `fr` |
| 🇩🇪 Niemiecki | `de` | 🇮🇳 Hindi | `hi` |
| 🇮🇩 Indonezyjski | `id` | 🇮🇹 Włoski | `it` |
| 🇯🇵 Japoński | `ja` | 🇵🇱 Polski | `pl` |
| 🇧🇷 Portugalski | `pt` | 🇷🇺 Rosyjski | `ru` |
| 🇹🇷 Turecki | `tr` | 🇨🇳 Chiński | `zh` |

### Tłumaczenia README

| Język | Plik | Język | Plik |
|----------|------|----------|------|
| 🇺🇸 Angielski | [README.md](../README.md) | 🇪🇸 Hiszpański | [README.es.md](README.es.md) |
| 🇸🇦 Arabski | [README.ar.md](README.ar.md) | 🇫🇷 Francuski | [README.fr.md](README.fr.md) |
| 🇩🇪 Niemiecki | [README.de.md](README.de.md) | 🇮🇳 Hindi | [README.hi.md](README.hi.md) |
| 🇮🇩 Indonezyjski | [README.id.md](README.id.md) | 🇮🇹 Włoski | [README.it.md](README.it.md) |
| 🇯🇵 Japoński | [README.ja.md](README.ja.md) | 🇵🇱 Polski | [README.pl.md](README.pl.md) |
| 🇧🇷 Portugalski | [README.pt.md](README.pt.md) | 🇷🇺 Rosyjski | [README.ru.md](README.ru.md) |
| 🇹🇷 Turecki | [README.tr.md](README.tr.md) | 🇨🇳 Chiński | [README.zh.md](README.zh.md) |

> 💡 **Chcesz pomóc w tłumaczeniu?** Sprawdź sekcję [Współpraca](#współpraca), aby pomóc nam dodać więcej języków!

</details>

<a id="rozwiązywanie-problemów"></a>
## 🛠️ Rozwiązywanie problemów

<details>
<summary>Kliknij, aby zobaczyć typowe problemy i rozwiązania</summary>

- **Tabela formatów nie pojawia się:** Zaktualizuj yt-dlp do najnowszej wersji i spróbuj przełączyć się na kanał yt-dlp Nightly.
- **Pobieranie nie powiodło się:** Sprawdź połączenie z internetem i upewnij się, że wideo jest dostępne.
- **Konkretne błędy pobierania:**
  - **Prywatne wideo:** Użyj uwierzytelniania przez ciasteczka, aby uzyskać dostęp do prywatnych treści.
  - **Treści z ograniczeniem wiekowym:** Zaloguj się na swoje konto YouTube, aby wyświetlić filmy z ograniczeniem wiekowym.
  - **Wideo z blokadą regionalną:** Rozważ użycie VPN, aby obejść ograniczenia regionalne.
  - **Usunięte wideo:** Film nie jest już dostępny na YouTube.
  - **Transmisje na żywo:** Transmisji na żywo nie można pobierać w trakcie ich trwania; poczekaj, aż transmisja się zakończy.
  - **Błędy sieciowe:** Sprawdź połączenie z internetem i spróbuj ponownie.
  - **Nieprawidłowy URL:** Upewnij się, że adres URL jest poprawny i pochodzi z obsługiwanej platformy.
  - **Treść Premium:** Wymaga subskrypcji YouTube Premium.
  - **Blokada praw autorskich:** Treść jest zablokowana z powodu ograniczeń praw autorskich.
- **Pliki wideo i audio są oddzielne po pobraniu:** Dzieje się tak, gdy brakuje FFmpeg lub nie został on wykryty. YTSage wymaga FFmpeg do scalania strumieni wideo i audio wysokiej jakości.
  - **Rozwiązanie:** Upewnij się, że FFmpeg jest zainstalowany i dostępny w zmiennej PATH systemu. Dla użytkowników Windows najprostszą opcją jest pobranie pliku `YTSage-v<wersja>-ffmpeg.exe`, który zawiera FFmpeg.

---

#### 🛡️ Ostrzeżenie Windows Defender / Antywirus

Niektóre programy antywirusowe mogą oznaczać pliki `.exe` jako fałszywe alarmy (false positive). Jest to **znane ograniczenie** pakowanych aplikacji.

**Dlaczego tak się dzieje:**
- Heurystyka antywirusa może błędnie zidentyfikować spakowane pliki wykonywalne jako podejrzane.

**Bezpieczne alternatywy:**
- ✅ **Użyj instalacji przez pip:** `pip install ytsage` (zalecane)
- ✅ **Zbuduj ze źródeł**: Postępując zgodnie z tym [przewodnikiem](../.github/CI_CD_README.md)
- ✅ **Dodaj aplikację do wyjątków** w swoim programie antywirusowym.

#### 🍎 macOS: "Aplikacja jest uszkodzona i nie można jej otworzyć"
Jeśli widzisz ten błąd w systemie macOS Sonoma lub nowszym, musisz usunąć atrybut kwarantanny.

1.  **Otwórz Terminal** (możesz go znaleźć przez Spotlight).
2.  **Wpisz następującą komendę**, ale jeszcze **NIE** naciskaj Enter. Pamiętaj o spacjach na końcu:
    ```bash
    xattr -d com.apple.quarantine 
    ```
3.  **Przeciągnij plik `YTSage.app` z okna Findera** i upuść go bezpośrednio w oknie Terminala. To automatycznie wklei poprawną ścieżkę do pliku.
4.  **Naciśnij Enter**, aby uruchomić komendę.
5.  **Spróbuj ponownie otworzyć YTSage.app.** Powinien uruchomić się poprawnie.

---

#### **Lokalizacja konfiguracji (zaawansowane)**
- **Windows:** `%LOCALAPPDATA%\YTSage`
- **macOS:** `~/Library/Application Support/YTSage`
- **Linux:** `~/.local/share/YTSage`

</details>

<a id="sponsor"></a>
## 💖 Sponsor

Jeśli YTSage oszczędza Twój czas, rozważ wsparcie projektu. Sponsoring pomaga pokryć czas programistyczny, testy na wszystkich platformach i przyszłe ulepszenia.

- GitHub Sponsors: https://github.com/sponsors/oop7
- Link do wsparcia jest dostępny bezpośrednio przez okno "O programie" w aplikacji.

[![Sponsor YTSage](https://img.shields.io/badge/Sponsor-YTSage-EA4AAA?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sponsors/oop7)

<a id="współpraca"></a>
## 👥 Współpraca

Zapraszamy do współpracy! Oto jak możesz pomóc:

1. 🍴 Skonfiguruj fork repozytorium
2. 🌿 Utwórz gałąź (branch) dla swojej funkcji:
  ```bash
  git checkout -b feature/NiesamowitaFunkcja
  ```
3. 💾 Zatwierdź zmiany (commit):
  ```bash
  git commit -m 'Dodaj NiesamowitaFunkcja'
  ```
4. 📤 Wyślij zmiany do gałęzi (push):
  ```bash
  git push origin feature/NiesamowitaFunkcja
  ```
5. 🔄 Otwórz Pull Request

### 🌍 Pomóż w tłumaczeniach

- Zaktualizuj odpowiedni lokalny plik README (np. `readme-translations/README.pl.md`)
- Dbaj o synchronizację komunikatów aplikacji, edytując `ytsage/languages/<code>.json`
- Jeśli brakuje Twojego języka, zacznij od `README.md` i stwórz `README.<code>.md`

<details>
<summary>📂 Struktura projektu</summary>

## YTSage - Struktura projektu

Ten dokument opisuje zorganizowaną strukturę folderów projektu YTSage.

### 📁 Struktura projektu

```
YTSage/
├── 📁 .github/                   # Konfiguracja GitHub
│   ├── 📁 ISSUE_TEMPLATE/         # Szablony zgłoszeń
│   │   └── 🐛-bug-report.md       # Szablon zgłoszenia błędu
│   ├─── 📁 workflows/              # Procesy GitHub Actions
│   │   ├── build-linux.yml        # Proces budowania dla Linux
│   │   ├── build-macos.yml        # Proces budowania dla macOS
│   │   │── build-windows.yml      # Proces budowania dla Windows
|   |   └── release-all.yml          # Proces głównego wydania
│   └── 📄 CI_CD_README.md        # Dokumentacja CI/CD
├──  📁 branding/                 # Materiały graficzne (zrzuty ekranu, SVG)
│   ├── 📁 icons/                 # Ikony aplikacji
│   ├── 📁 screenshots/           # Zrzuty ekranu do dokumentacji
│   └── 📁 svg/                   # Zasoby SVG
├── 📄 LICENSE                    # Plik licencji
├── 📄 pyproject.toml             # Metadane projektu i zależności
├── 📄 README.md                  # Dokumentacja projektu
├── 📄 requirements.txt           # Zależności Python (dev)
└── 📁 ytsage/                    # Pakiet kodu źródłowego
    ├── 📁 assets/                # Zasoby czasu wykonywania
    │   ├── 📁 Icon/              # Ikony aplikacji
    │   └── 📁 sound/             # Pliki dźwiękowe
    ├── 📁 languages/             # Pliki lokalizacji
    │   ├── 📄 ar.json            # Tłumaczenie arabskie
    │   ├── 📄 de.json            # Tłumaczenie niemieckie
    │   ├── 📄 en.json            # Tłumaczenie angielskie
    │   └── ...                   # Inne języki
    ├── 📁 core/                  # Główna logika biznesowa
    │   ├── 📄 __init__.py        
    │   ├── 📄 ytsage_deno.py     # Integracja Deno
    │   ├── 📄 ytsage_downloader.py # Funkcjonalność pobierania
    │   ├── 📄 ytsage_ffmpeg.py   # Integracja FFmpeg
    │   ├── 📄 ytsage_utils.py    # Funkcje pomocnicze
    │   └── 📄 ytsage_yt_dlp.py   # Integrasi yt-dlp
    ├── 📁 gui/                   # Komponenty interfejsu użytkownika
    │   ├── 📄 __init__.py        
    │   ├── 📄 ytsage_gui_main.py # Główne okno aplikacji
    │   └── 📁 ytsage_gui_dialogs/ # Klasy okien dialogowych
    ├── 📁 utils/                 # Moduły pomocnicze
    │   ├── 📄 __init__.py        
    │   ├── 📄 ytsage_config_manager.py # Zarządzanie konfiguracją
    │   └── 📄 ytsage_logger.py   # Narzędzia logowania
    ├── 📄 __init__.py            # Punkt wejścia pakietu
    └── 📄 main.py                # Główny skrypt wykonawczy
```

</details>

## ⭐️ Historia gwiazdek

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

## 📜 Licencja

Ten projekt jest udostępniany na licencji MIT - zobacz plik [LICENSE](../LICENSE), aby poznać szczegóły.

## 🙏 Podziękowania

<details>
<summary>Pokaż podziękowania</summary>

<div align="center">

<p>Wielkie podziękowania dla wszystkich, którzy przyczynili się do rozwoju projektu poprzez zgłaszanie sugestii i błędów.</p>

<table>
    <tr class="section"><th colspan="2">Główne komponenty</th></tr>
    <tr>
        <td width="35%"><a href="https://github.com/yt-dlp/yt-dlp">yt-dlp</a></td>
        <td>Silnik pobierania</td>
    </tr>
    <tr>
        <td><a href="https://ffmpeg.org/">FFmpeg</a></td>
        <td>Przetwarzanie mediów</td>
    </tr>
    <tr>
        <td><a href="https://deno.com/">Deno</a></td>
        <td>Środowisko dla integracji yt-dlp</td>
    </tr>
    <tr class="section"><th colspan="2">Biblioteki i frameworki</th></tr>
    <tr>
        <td><a href="https://wiki.qt.io/Qt_for_Python">PySide6</a></td>
        <td>Framework GUI</td>
    </tr>
    <tr>
        <td><a href="https://python-pillow.org/">Pillow</a></td>
        <td>Przetwarzanie obrazów</td>
    </tr>
    <tr>
        <td><a href="https://requests.readthedocs.io/">requests</a></td>
        <td>Żądania HTTP</td>
    </tr>
    <tr>
        <td><a href="https://packaging.python.org/">packaging</a></td>
        <td>Zarządzanie wersjami i pakowanie</td>
    </tr>
    <tr>
        <td><a href="https://python-markdown.github.io/">markdown</a></td>
        <td>Renderowanie Markdown</td>
    </tr>
    <tr>
        <td><a href="https://github.com/Delgan/loguru">loguru</a></td>
        <td>Logowanie</td>
    </tr>
    <tr class="section"><th colspan="2">Zasoby i współpracownicy</th></tr>
    <tr>
        <td><a href="https://pixabay.com/sound-effects/new-notification-09-352705/">New Notification 09 by Universfield</a></td>
        <td>Dźwięk powiadomienia</td>
    </tr>
    <tr>
        <td><a href="https://github.com/viru185">viru185</a></td>
        <td>Współpracownik kodu</td>
    </tr>
</table>

</div>

</details>

## ⚠️ Zastrzeżenie

To narzędzie służy wyłącznie do użytku osobistego. Prosimy o przestrzeganie Warunków świadczenia usług YouTube i praw twórców treści.

---

<div align="center">

Stworzone z ❤️ przez [oop7](https://github.com/oop7)

</div>
