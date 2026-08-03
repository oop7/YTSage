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

**Un downloader YouTube moderno con un'interfaccia PySide6 pulita.**  
Scarica video in qualsiasi qualità, estrai audio, ottieni sottotitoli e molto altro.

### 🌍 Lingue del README

Inglese: [EN](../README.md)
| Arabo: [AR](README.ar.md)
| Tedesco: [DE](README.de.md)
| Spagnolo: [ES](README.es.md)
| Francese: [FR](README.fr.md)
| Hindi: [HI](README.hi.md)
| Indonesiano: [ID](README.id.md)
| Italiano: [IT](README.it.md)
| Giapponese: [JA](README.ja.md)
| Polacco: [PL](README.pl.md)
| Portoghese: [PT](README.pt.md)
| Russo: [RU](README.ru.md)
| Turco: [TR](README.tr.md)
| Cinese: [ZH](README.zh.md)

<p align="center">
  <a href="#installazione">Installazione</a> •
  <a href="#caratteristiche">Caratteristiche</a> •
  <a href="#utilizzo">Utilizzo</a> •
  <a href="#screenshot">Screenshot</a> •
  <a href="#risoluzione-dei-problemi">Risoluzione dei problemi</a> •
  <a href="#sponsor">Sponsor</a> •
  <a href="#contribuire">Contribuire</a>
</p>

</div>

---

<a id="perché-ytsage"></a>
## ❓ Perché YTSage?

YTSage è progettato per gli utenti che desiderano un **downloader YouTube semplice ma potente**. A differenza di altri strumenti, offre:

- Un'interfaccia PySide6 moderna e pulita
- Download di video, audio e sottotitoli con un solo clic
- Funzioni avanzate come SponsorBlock, fusione dei sottotitoli e selezione della playlist
- Modalità Generica opzionale per siti diversi da YouTube supportati da yt-dlp
- Supporto multipiattaforma e installazione semplice

<a id="caratteristiche"></a>
## ✨ Caratteristiche

<div align="center">

| Funzioni Base | Funzioni Avanzate | Funzioni Extra |
|-----------------------------------|-----------------------------------------|------------------------------------|
| 🎥 Tabella Formati | 🚫 Integrazione SponsorBlock | 🎞️ Visualizzazione FPS/HDR |
| 🎵 Estrazione Audio | 📝 Selezione e Fusione Sottotitoli | 🔄 Aggiornamento automatico yt-dlp |
| ✨ Interfaccia Utente Semplice | 💾 Salva Descrizione e Anteprima | 🛠️ Rilevamento FFmpeg/yt-dlp/Deno |
| 📋 Supporto e Selettore Playlist | 🚀 Limitatore di Velocità | ⚙️ Comandi Personalizzati |
| 📑 Integrazione Capitoli | ✂️ Ritaglio Sezioni Video | 🍪 Login tramite Cookie |
| 📜 Cronologia Download | 🔄 Scelta del Canale di Rilascio | 🌐 Supporto Proxy |
| 🎚️ Conversione Formato Audio | 🎬 Impostazioni Formato Video | 🆙 Tab Aggiornamento Integrato |
| 🌍 Modalità Generica | 🔊 Normalizzazione Audio (EBU R128) | 🌍 Localizzazione in 14 lingue |
| 💾 Esportazione Playlist | ⚙️ Qualità e Sottotitoli Predefiniti | |
</div>

<a id="installazione"></a>
## 🚀 Installazione

### ⚡ Installazione Rapida (Consigliata)

Installa YTSage tramite PyPI:

```bash
pip install ytsage
```

<details>
<summary>🔄 Aggiornare un'installazione esistente</summary>

```bash
pip install --upgrade ytsage
```

</details>

Quindi esegui l'applicazione:

```bash
ytsage
```

### 📦 Eseguibili Pre-compilati (Executable)

> [👉 Scarica l'ultima versione](https://github.com/oop7/YTSage/releases/latest)

#### 🪟 Windows

| Formato | Descrizione |
|--------|-------------|
| ![Windows EXE](https://img.shields.io/badge/Windows-EXE-0078D6?style=for-the-badge&logo=windows&logoColor=white) | Installer Standard |
| ![Windows FFmpeg](https://img.shields.io/badge/Windows-FFmpeg-0078D6?style=for-the-badge&logo=windows&logoColor=white) | Include FFmpeg |
| ![Windows Portable](https://img.shields.io/badge/Windows-Portable-0078D6?style=for-the-badge&logo=windows&logoColor=white) | Versione Portable, nessuna installazione richiesta |
| ![Windows Portable FFmpeg](https://img.shields.io/badge/Windows-Portable%20FFmpeg-0078D6?style=for-the-badge&logo=windows&logoColor=white) | Portable con FFmpeg, compresso (ZIP) |

<details>
<summary>🛠️ Passaggi per l'installazione</summary>

1. **Installer EXE (`.exe`)**: Fare doppio clic sul file e seguire la procedura guidata.
2. **Versione Portable (`.zip`)**: Estrarre l'archivio nella posizione desiderata ed eseguire `ytsage.exe`.
3. **FFmpeg integrato**: Se non hai FFmpeg sul tuo sistema, scegli le versioni con FFmpeg integrato.
</details>

#### 🐧 Linux

| Formato | Descrizione |
|--------|-------------|
| ![Linux DEB](https://img.shields.io/badge/Linux-DEB-FCC624?style=for-the-badge&logo=linux&logoColor=black) | Pacchetto Debian |
| ![Linux AppImage](https://img.shields.io/badge/Linux-AppImage-FCC624?style=for-the-badge&logo=linux&logoColor=black) | AppImage, Portable |
| ![Linux RPM](https://img.shields.io/badge/Linux-RPM-FCC624?style=for-the-badge&logo=linux&logoColor=black) | Pacchetto RPM |
| ![Flathub](https://img.shields.io/badge/Linux-Flatpak-FCC624?style=for-the-badge&logo=flathub&logoColor=black) | Bundle Flatpak |

<details>
<summary>🛠️ Passaggi per l'installazione</summary>

- **DEB (`.deb`)**:
  ```bash
  sudo dpkg -i ytsage_*.deb
  sudo apt-get install -f # Se necessario per correggere le dipendenze mancanti
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
- **Flatpak**: Seguire le istruzioni su Flathub o eseguire:
  ```bash
  flatpak install flathub io.github.oop7.ytsage
  ```
</details>

#### 🍎 macOS

| Formato | Descrizione |
|--------|-------------|
| ![macOS ARM64 APP](https://img.shields.io/badge/macOS-ARM64%20APP-000000?style=for-the-badge&logo=apple&logoColor=white) | App ZIP per Apple Silicon |
| ![macOS ARM64 DMG](https://img.shields.io/badge/macOS-ARM64%20DMG-000000?style=for-the-badge&logo=apple&logoColor=white) | Installer Disk Image per Apple Silicon |

<details>
<summary>🛠️ Passaggi per l'installazione</summary>

- **Installer DMG (`.dmg`)**: Fare doppio clic per montare, quindi trascinare `YTSage.app` nella cartella Applicazioni.
- **Archivio App (`.zip`)**: Estrarre lo ZIP e spostare `YTSage.app` nella cartella Applicazioni.

*Nota: Se ricevi l'errore "L'app è danneggiata", consulta la sezione Risoluzione dei problemi macOS di seguito.*
</details>

---

<details>
<summary>💻 Installazione manuale dai sorgenti</summary>

### 1. Clonare il repository

```bash
git clone https://github.com/oop7/YTSage.git
cd YTSage
```

### 2. Installare le dipendenze

#### ⚡ Con uv

```bash
uv pip install .
```

#### 📦 O con pip standard

```bash
pip install .
```

### 3. Eseguire l'applicazione

```bash
python -m ytsage.main
```

</details>

<a id="screenshot"></a>
## 📸 Screenshot

<div align="center">
<table>
  <tr>
    <td><img src="../branding/screenshots/Download-Settings.png" alt="Impostazioni Download" width="400"/></td>
    <td><img src="../branding/screenshots/playlist.png" alt="Download Playlist" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><em>Impostazioni Download</em></td>
    <td align="center"><em>Download Playlist</em></td>
  </tr>
  <tr>
    <td><img src="../branding/screenshots/audio_format.png" alt="Selezione Formato Audio" width="400"/></td>
    <td><img src="../branding/screenshots/Custom-Option.png" alt="Opzioni Personalizzate" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><em>Formato Audio</em></td>
    <td align="center"><em>Opzioni Personalizzate</em></td>
  </tr>
</table>
</div>

<a id="utilizzo"></a>
## 📖 Utilizzo

<details>
<summary>🎯 Utilizzo Base</summary>

1. **Avvia YTSage**
2. **Incolla un URL di YouTube** (o usa il pulsante "Incolla URL")
3. **Clicca su "Analizza"**
4. **Scegli il formato:**
   - `Video` per il download del video
   - `Solo Audio` per l'estrazione dell'audio
5. **Seleziona le opzioni:**
   - Abilita i sottotitoli e scegli la lingua
   - Abilita la fusione dei sottotitoli
   - Salva l'anteprima (thumbnail)
   - Rimuovi sezioni sponsor
   - Salva la descrizione
   - Incorpora i capitoli
6. **Scegli la directory di destinazione**
7. **Clicca su "Download"**

> 💡 La directory di download predefinita è la cartella "Download" dell'utente.

</details>

<details>
<summary>📋 Download Playlist</summary>

1. **Incolla l'URL della playlist**
2. **Clicca su "Analizza"**
3. **Seleziona i video dal selettore (opzionale, tutti per impostazione predefinita)**
4. **Scegli il formato/qualità desiderati**
5. **Clicca su "Download"**

> 💡 L'applicazione gestisce automaticamente la coda di download e puoi esportare le voci della playlist come file `.txt`, `.csv`, `.m3u` o `.json`.

</details>

<details>
<summary>🌍 Modalità Generica per siti non YouTube</summary>

Usa la Modalità Generica quando vuoi che YTSage accetti URL da siti supportati da yt-dlp come Dailymotion, CBC Gem, TikTok e altri.

Come usarla:

1. Apri `Impostazioni Download`.
2. Abilita `Modalità Generica`.
3. Incolla un URL di un video o di una playlist supportata che non sia YouTube.
4. Clicca su `Analizza`.
5. Scegli un formato e scarica normalmente.

Note:

- La Modalità Generica cambia solo la validazione dell'URL all'interno di YTSage. Il sito di destinazione deve essere comunque supportato dalla versione di yt-dlp installata.
- Alcuni siti richiedono cookie, login, proxy o argomenti yt-dlp aggiuntivi a seconda dell'estrattore.
- Se un sito fallisce, aggiorna yt-dlp dal tab di aggiornamento integrato prima di segnalare il problema.

</details>

<details>
<summary>🧰 Opzioni Media e Download</summary>

- **Opzioni Sottotitoli:** Filtra le lingue e incorpora i sottotitoli nel file video.
- **Fusione Sottotitoli:** Fonde i sottotitoli nel file video per sottotitoli permanenti (hardcoded).
- **Salva Descrizione:** Salva la descrizione del video come file di testo.
- **Salva Anteprima:** Salva l'anteprima (thumbnail) del video come file immagine.
- **Incorpora Capitoli:** Include i segnaposti dei capitoli come metadati per i lettori video compatibili.
- **Rimuovi Sezioni Sponsor:** Usa SponsorBlock per rimuovere i segmenti sponsorizzati dal video.
- **Ritaglia Video:** Scarica solo parti specifiche del video specificando un intervallo di tempo nel formato `HH:MM:SS`.

</details>

<details>
<summary>⚙️ Impostazioni Output e File</summary>

- **Limitatore di Velocità:** Limita la velocità di download, ad esempio `500K` per 500 KB/s.
- **Salva Percorso Download:** Salva il percorso di download predefinito per i download futuri. Disponibile in **Impostazioni Download → Percorso Download**.
- **Risoluzione Video Predefinita:** Imposta la risoluzione video preferita per la selezione automatica (es. 1080p, 720p). Disponibile in **Impostazioni Download → Risoluzione Video Predefinita**.
- **Lingue Sottotitoli Predefinite:** Imposta le lingue dei sottotitoli predefinite per la selezione automatica (separate da virgola, es. `it,en`). Disponibile in **Impostazioni Download → Lingue Sottotitoli Predefinite**.
- **Formato Nome File:** Personalizza il formato del nome del file di output utilizzando variabili come `%(title)s`, `%(uploader)s`, `%(playlist_index)s` e `%(resolution)s`. Disponibile in **Impostazioni Download → Formato Nome File**.
- **Forza Formato Output:** Forza il download del video in un formato contenitore specifico come `mp4`, `webm` o `mkv`. Disponibile in **Impostazioni Download → Impostazioni Formato Output**.
- **Conversione Formato Audio:** Converte i download di solo audio nel formato preferito come `AAC`, `MP3`, `FLAC`, `WAV`, `Opus`, `M4A`, `Vorbis`, o `Best`. Disponibile in **Impostazioni Download → Impostazioni Formato Audio**.
- **Normalizzazione Audio:** Standardizza il volume per i download di solo audio utilizzando EBU R128.
- **Connessioni Simultanee:** Aumenta significativamente la velocità di download scaricando i file in più parti contemporaneamente. Disponibile in **Impostazioni Download → Generali → Connessioni Simultanee** (predefinito 1, massimo 8-10 consigliato per evitare blocchi IP).

</details>

<details>
<summary>🌐 Accesso e Rete</summary>

- **Login tramite Cookie:** Accedi a YouTube utilizzando i cookie per accedere ai contenuti privati.
  Utilizzo:
  1. **Consigliato:** Usa l'opzione integrata nell'app `Estrai cookie dal browser`, quindi scegli il browser e opzionalmente il profilo.
  2. In alternativa, estrai i cookie manualmente:
     a. Esporta i cookie dal tuo browser utilizzando un'estensione come [cookie-editor](https://github.com/moustachauve/cookie-editor?tab=readme-ov-file)
     b. Copia i cookie nel formato Netscape
     c. Crea un file chiamato `cookies.txt` e incolla i cookie
     d. Seleziona il file `cookies.txt` nell'app
- **Supporto Proxy:** Usa un server proxy per i download, ad esempio `http://<server-proxy>:<porta>`
- **Modalità Generica:** Consente a YTSage di analizzare e scaricare da siti non YouTube supportati da yt-dlp. Abilitalo da **Impostazioni Download → Modalità Generica**.

</details>

<details>
<summary>🛠️ Strumenti e Manutenzione</summary>

- **Comandi Personalizzati:** Accedi alle funzioni avanzate di yt-dlp tramite argomenti della riga di comando.
- **Tab Aggiornamento:** Gestisci gli strumenti di aggiornamento integrati da un unico posto nelle Opzioni Personalizzate:
  - **Aggiornamento yt-dlp:** Controlla gli aggiornamenti e passa tra i canali di rilascio Stabile e Nightly.
  - **Controllo Versione FFmpeg:** Verifica la tua versione di FFmpeg e apri le guide all'installazione.
  - **Aggiornamento Deno:** Controlla e aggiorna il runtime Deno.
- **Rilevamento FFmpeg/yt-dlp/Deno:** Rileva automaticamente i percorsi e le versioni di FFmpeg, yt-dlp e Deno dal dialogo Informazioni.
- **Cronologia Download:** Visualizza i download passati con anteprime e stati dal pulsante **Cronologia**.

</details>

<details>
<summary>🌍 Localizzazione</summary>

YTSage supporta **14 lingue** per una portata globale. Scegli la tua lingua preferita in **Opzioni Personalizzate → Lingua**.

### Lingue Supportate

| Lingua | Codice | Lingua | Codice |
|----------|------|----------|------|
| 🇺🇸 Inglese | `en` | 🇪🇸 Spagnolo | `es` |
| 🇸🇦 Arabo | `ar` | 🇫🇷 Francese | `fr` |
| 🇩🇪 Tedesco | `de` | 🇮🇳 Hindi | `hi` |
| 🇮🇩 Indonesiano | `id` | 🇮🇹 Italiano | `it` |
| 🇯🇵 Giapponese | `ja` | 🇵🇱 Polacco | `pl` |
| 🇧🇷 Portoghese | `pt` | 🇷🇺 Russo | `ru` |
| 🇹🇷 Turco | `tr` | 🇨🇳 Cinese | `zh` |

### Traduzioni del README

| Lingua | File | Lingua | File |
|----------|------|----------|------|
| 🇺🇸 Inglese | [README.md](../README.md) | 🇪🇸 Spagnolo | [README.es.md](README.es.md) |
| 🇸🇦 Arabo | [README.ar.md](README.ar.md) | 🇫🇷 Francese | [README.fr.md](README.fr.md) |
| 🇩🇪 Tedesco | [README.de.md](README.de.md) | 🇮🇳 Hindi | [README.hi.md](README.hi.md) |
| 🇮🇩 Indonesiano | [README.id.md](README.id.md) | 🇮🇹 Italiano | [README.it.md](README.it.md) |
| 🇯🇵 Giapponese | [README.ja.md](README.ja.md) | 🇵🇱 Polacco | [README.pl.md](README.pl.md) |
| 🇧🇷 Portoghese | [README.pt.md](README.pt.md) | 🇷🇺 Russo | [README.ru.md](README.ru.md) |
| 🇹🇷 Turco | [README.tr.md](README.tr.md) | Cinese | [README.zh.md](README.zh.md) |

> 💡 **Vuoi aiutare con la traduzione?** Consulta la sezione [Contribuire](#contribuire) per aiutarci ad aggiungere altre lingue!

</details>

<a id="risoluzione-dei-problemi"></a>
## 🛠️ Risoluzione dei problemi

<details>
<summary>Clicca per visualizzare i problemi comuni e le soluzioni</summary>

- **La tabella dei formati non appare:** Aggiorna yt-dlp all'ultima versione e prova a passare a yt-dlp Nightly.
- **Download fallito:** Controlla la tua connessione internet e assicurati che il video sia disponibile.
- **Errori di download specifici:**
  - **Video Privati:** Usa l'autenticazione tramite cookie per accedere ai contenuti privati.
  - **Contenuti con limiti di età:** Accedi al tuo account YouTube per visualizzare i video con limiti di età.
  - **Video bloccati geograficamente:** Considera l'uso di una VPN per aggirare le restrizioni regionali.
  - **Video rimosso:** Il video non è più disponibile su YouTube.
  - **Live Stream:** I live stream non possono essere scaricati durante la trasmissione; attendi la fine dello stream.
  - **Errori di rete:** Controlla la tua connessione internet e riprova.
  - **URL non valido:** Assicurati che l'URL sia corretto e provenga da una piattaforma supportata.
  - **Contenuti Premium:** Richiede un abbonamento YouTube Premium.
  - **Blocco Copyright:** Il contenuto è bloccato a causa di restrizioni sul copyright.
- **I file video e audio sono separati dopo il download:** Questo accade quando FFmpeg manca o non viene rilevato. YTSage richiede FFmpeg per unire i flussi video e audio di alta qualità.
  - **Soluzione:** Assicurati che FFmpeg sia installato e accessibile nel PATH del tuo sistema. Per gli utenti Windows, l'opzione più semplice è scaricare il file `YTSage-v<versione>-ffmpeg.exe`, che include FFmpeg.

---

#### 🛡️ Avviso Windows Defender / Antivirus

Alcuni software antivirus potrebbero contrassegnare i file `.exe` come falsi positivi. Questa è una **limitazione nota** delle applicazioni pacchettizzate.

**Perché succede:**
- Le euristiche dell'antivirus potrebbero identificare erroneamente gli eseguibili pacchettizzati come sospetti.

**Opzioni sicure:**
- ✅ **Usa l'installazione tramite pip:** `pip install ytsage` (consigliato)
- ✅ **Compila dai sorgenti**: Seguendo questa [guida](../.github/CI_CD_README.md)
- ✅ **Aggiungi l'applicazione alla whitelist** nel tuo software antivirus.

#### 🍎 macOS: "L’app è danneggiata e non può essere aperta"
Se visualizzi questo errore su macOS Sonoma o versioni successive, devi rimuovere l'attributo di quarantena.

1.  **Apri il Terminale** (puoi trovarlo usando Spotlight).
2.  **Digita il seguente comando** ma **NON** premere ancora Invio. Assicurati di includere lo spazio alla fine:
    ```bash
    xattr -d com.apple.quarantine 
    ```
3.  **Trascina il file `YTSage.app` dalla finestra del Finder** e rilascialo direttamente nella finestra del Terminale. Questo incollerà automaticamente il percorso corretto del file.
4.  **Premi Invio** per eseguire il comando.
5.  **Prova a riaprire YTSage.app.** Ora dovrebbe avviarsi correttamente.

---

#### **Percorsi di configurazione (Avanzato)**
- **Windows:** `%LOCALAPPDATA%\YTSage`
- **macOS:** `~/Library/Application Support/YTSage`
- **Linux:** `~/.local/share/YTSage`

</details>

<a id="sponsor"></a>
## 💖 Sponsor

Se YTSage ti fa risparmiare tempo, considera di sponsorizzare il progetto. Le sponsorizzazioni aiutano a coprire il tempo di sviluppo, i test su tutte le piattaforme e i miglioramenti futuri.

- GitHub Sponsors: https://github.com/sponsors/oop7
- Il link per la sponsorizzazione è disponibile direttamente tramite il dialogo Informazioni all'interno dell'app.

[![Sponsor YTSage](https://img.shields.io/badge/Sponsor-YTSage-EA4AAA?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sponsors/oop7)

<a id="contribuire"></a>
## 👥 Contribuire

I contributi sono benvenuti! Ecco come puoi aiutare:

1. 🍴 Fork del repository
2. 🌿 Crea il tuo ramo per la funzione:
  ```bash
  git checkout -b feature/FunzioneIncredibile
  ```
3. 💾 Fai il commit delle tue modifiche:
  ```bash
  git commit -m 'Aggiungi FunzioneIncredibile'
  ```
4. 📤 Fai il push sul ramo:
  ```bash
  git push origin feature/FunzioneIncredibile
  ```
5. 🔄 Apri una Pull Request

### 🌍 Contribuire alle traduzioni

- Aggiorna il file README localizzato pertinente (es. `readme-translations/README.it.md`)
- Mantieni sincronizzate le stringhe dell'app modificando `ytsage/languages/<code>.json`
- Se la tua lingua manca, parti da `README.md` e crea `README.<code>.md`

<details>
<summary>📂 Struttura del Progetto</summary>

## YTSage - Struttura del Progetto

Questo documento descrive la struttura organizzata delle cartelle di YTSage.

### 📁 Struttura del Progetto

```
YTSage/
├── 📁 .github/                   # Configurazioni GitHub
│   ├── 📁 ISSUE_TEMPLATE/         # Modelli per segnalazioni
│   │   └── 🐛-bug-report.md       # Modello per segnalazione bug
│   ├─── 📁 workflows/              # Workflow GitHub Actions
│   │   ├── build-linux.yml        # Workflow build Linux
│   │   ├── build-macos.yml        # Workflow build macOS
│   │   │── build-windows.yml      # Workflow build Windows
|   |   └── release-all.yml          # Workflow release master
│   └── 📄 CI_CD_README.md        # Documentazione CI/CD
├──  📁 branding/                 # Asset di branding (screenshot, SVG)
│   ├── 📁 icons/                 # Icone dell'app
│   ├── 📁 screenshots/           # Screenshot per la documentazione
│   └── 📁 svg/                   # Asset SVG
├── 📄 LICENSE                    # File della licenza
├── 📄 pyproject.toml             # Metadati del progetto e dipendenze
├── 📄 README.md                  # Documentazione del progetto
├── 📄 requirements.txt           # Dipendenze Python (dev)
└── 📁 ytsage/                    # Pacchetto del codice sorgente
    ├── 📁 assets/                # Asset runtime
    │   ├── 📁 Icon/              # Icone dell'app
    │   └── 📁 sound/             # File audio
    ├── 📁 languages/             # File di localizzazione
    │   ├── 📄 ar.json            # Traduzione araba
    │   ├── 📄 de.json            # Traduzione tedesca
    │   ├── 📄 en.json            # Traduzione inglese
    │   └── ...                   # Altre lingue
    ├── 📁 core/                  # Logica di business principale
    │   ├── 📄 __init__.py        
    │   ├── 📄 ytsage_deno.py     # Integrazione Deno
    │   ├── 📄 ytsage_downloader.py # Funzionalità di download
    │   ├── 📄 ytsage_ffmpeg.py   # Integrazione FFmpeg
    │   ├── 📄 ytsage_utils.py    # Funzioni di utilità
    │   └── 📄 ytsage_yt_dlp.py   # Integrazione yt-dlp
    ├── 📁 gui/                   # Componenti dell'interfaccia utente
    │   ├── 📄 __init__.py        
    │   ├── 📄 ytsage_gui_main.py # Finestra principale dell'app
    │   └── 📁 ytsage_gui_dialogs/ # Classi per i dialoghi
    ├── 📁 utils/                 # Moduli di utilità
    │   ├── 📄 __init__.py        
    │   ├── 📄 ytsage_config_manager.py # Gestione configurazione
    │   └── 📄 ytsage_logger.py   # Strumenti di logging
    ├── 📄 __init__.py            # Punto di ingresso del pacchetto
    └── 📄 main.py                # Script di esecuzione principale
```

</details>

## ⭐️ Cronologia Stelle

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

## 📜 Licenza

Questo progetto è rilasciato sotto Licenza MIT - vedi il file [LICENSE](../LICENSE) per i dettagli.

## 🙏 Ringraziamenti

<details>
<summary>Mostra Ringraziamenti</summary>

<div align="center">

<p>Un grande ringraziamento a tutti coloro che hanno contribuito a questo progetto aprendo segnalazioni per suggerire miglioramenti o segnalare bug.</p>

<table>
    <tr class="section"><th colspan="2">Componenti Principali</th></tr>
    <tr>
        <td width="35%"><a href="https://github.com/yt-dlp/yt-dlp">yt-dlp</a></td>
        <td>Motore di Download</td>
    </tr>
    <tr>
        <td><a href="https://ffmpeg.org/">FFmpeg</a></td>
        <td>Elaborazione Media</td>
    </tr>
    <tr>
        <td><a href="https://deno.com/">Deno</a></td>
        <td>Runtime per l'integrazione di yt-dlp</td>
    </tr>
    <tr class="section"><th colspan="2">Librerie e Framework</th></tr>
    <tr>
        <td><a href="https://wiki.qt.io/Qt_for_Python">PySide6</a></td>
        <td>Framework GUI</td>
    </tr>
    <tr>
        <td><a href="https://python-pillow.org/">Pillow</a></td>
        <td>Elaborazione Immagini</td>
    </tr>
    <tr>
        <td><a href="https://requests.readthedocs.io/">requests</a></td>
        <td>Richieste HTTP</td>
    </tr>
    <tr>
        <td><a href="https://packaging.python.org/">packaging</a></td>
        <td>Gestione Versioni e Packaging</td>
    </tr>
    <tr>
        <td><a href="https://python-markdown.github.io/">markdown</a></td>
        <td>Rendering Markdown</td>
    </tr>
    <tr>
        <td><a href="https://github.com/Delgan/loguru">loguru</a></td>
        <td>Logging</td>
    </tr>
    <tr class="section"><th colspan="2">Asset e Collaboratori</th></tr>
    <tr>
        <td><a href="https://pixabay.com/sound-effects/new-notification-09-352705/">New Notification 09 di Universfield</a></td>
        <td>Suono di Notifica</td>
    </tr>
    <tr>
        <td><a href="https://github.com/viru185">viru185</a></td>
        <td>Collaboratore al Codice</td>
    </tr>
</table>

</div>

</details>

## ⚠️ Disclaimer

Questo strumento è solo per uso personale. Rispettate i Termini di Servizio di YouTube e i diritti dei produttori di contenuti.

---

<div align="center">

Creato con ❤️ da [oop7](https://github.com/oop7)

</div>
