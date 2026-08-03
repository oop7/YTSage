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

**Un moderno descargador de YouTube con una interfaz PySide6 elegante.**  
Descarga videos en cualquier calidad, extrae audio, obtén subtítulos y más.

### 🌍 Idiomas del README

Inglés: [EN](../README.md)
| Árabe: [AR](README.ar.md)
| Alemán: [DE](README.de.md)
| Español: [ES](README.es.md)
| Francés: [FR](README.fr.md)
| Hindi: [HI](README.hi.md)
| Indonesio: [ID](README.id.md)
| Italiano: [IT](README.it.md)
| Japonés: [JA](README.ja.md)
| Polaco: [PL](README.pl.md)
| Portugués: [PT](README.pt.md)
| Ruso: [RU](README.ru.md)
| Turco: [TR](README.tr.md)
| Chino: [ZH](README.zh.md)

<p align="center">
  <a href="#installation">Instalación</a> •
  <a href="#features">Características</a> •
  <a href="#usage">Uso</a> •
  <a href="#screenshots">Capturas de pantalla</a> •
  <a href="#troubleshooting">Solución de problemas</a> •
  <a href="#sponsor">Patrocinar</a> •
  <a href="#contributing">Contribuir</a>
</p>

</div>

---

<a id="why-ytsage"></a>
## ❓ ¿Por qué YTSage?

YTSage está diseñado para usuarios que desean un **descargador de YouTube simple pero potente**. A diferencia de otras herramientas, ofrece:

- Interfaz PySide6 moderna y limpia
- Descarga con un solo clic para video, audio y subtítulos
- Funciones avanzadas como SponsorBlock, fusión de subtítulos y selección de listas de reproducción
- Modo genérico (Generic Mode) opcional para sitios compatibles con yt-dlp más allá de YouTube
- Soporte multiplataforma e instalación sencilla

<a id="features"></a>
## ✨ Características

<div align="center">

| Características básicas | Características avanzadas | Características adicionales |
|-----------------------------------|-----------------------------------------|------------------------------------|
| 🎥 Tabla de formatos | 🚫 Integración de SponsorBlock | 🎞️ Pantalla FPS/HDR |
| 🎵 Extracción de audio | 📝 Selección y fusión de subtítulos | 🔄 Actualización automática de yt-dlp |
| ✨ Interfaz de usuario simple | 💾 Guarda descripción y miniatura | 🛠️ Detección de FFmpeg/yt-dlp/Deno |
| 📋 Soporte y selector de listas de reproducción | 🚀 Limitador de velocidad | ⚙️ Comandos personalizados |
| 📑 Integración de capítulos | ✂️ Recorte de secciones de video | 🍪 Inicio de sesión con cookies |
| 📜 Historial de descargas | 🔄 Selección de canal de lanzamiento | 🌐 Soporte de proxy |
| 🎚️ Conversión de formato de audio | 🎬 Configuración de formato de video | 🆙 Pestaña de actualización integrada |
| 🌍 Modo genérico | 🔊 Normalización de audio (EBU R128) | 🌍 Localización en 14 idiomas |
| 💾 Exportación de listas de reproducción | ⚙️ Calidad y subtítulos predeterminados | |
</div>

<a id="installation"></a>
## 🚀 Instalación

### ⚡ Instalación rápida (Recomendado)

Instala YTSage vía PyPI:

```bash
pip install ytsage
```

<details>
<summary>🔄 Actualizar instalación existente</summary>

```bash
pip install --upgrade ytsage
```

</details>

Luego, ejecuta la aplicación:

```bash
ytsage
```

### 📦 Ejecutables precompilados

> [👉 Descargar el último lanzamiento](https://github.com/oop7/YTSage/releases/latest)

#### 🪟 Windows

| Formato | Descripción |
|--------|-------------|
| ![Windows EXE](https://img.shields.io/badge/Windows-EXE-0078D6?style=for-the-badge&logo=windows&logoColor=white) | Instalador estándar |
| ![Windows FFmpeg](https://img.shields.io/badge/Windows-FFmpeg-0078D6?style=for-the-badge&logo=windows&logoColor=white) | Con FFmpeg incorporado |
| ![Windows Portable](https://img.shields.io/badge/Windows-Portable-0078D6?style=for-the-badge&logo=windows&logoColor=white) | Versión portable, no requiere instalación |
| ![Windows Portable FFmpeg](https://img.shields.io/badge/Windows-Portable%20FFmpeg-0078D6?style=for-the-badge&logo=windows&logoColor=white) | Portable con FFmpeg, comprimido |

<details>
<summary>🛠️ Pasos de instalación</summary>

1. **Instalador EXE (`.exe`)**: Haz doble clic en el archivo y sigue el asistente de configuración.
2. **Versión portable (`.zip`)**: Extrae el archivo en el lugar deseado y ejecuta `ytsage.exe`.
3. **FFmpeg incorporado**: Elige las versiones con FFmpeg incorporado si no tienes FFmpeg instalado en tu sistema.
</details>

#### 🐧 Linux

| Formato | Descripción |
|--------|-------------|
| ![Linux DEB](https://img.shields.io/badge/Linux-DEB-FCC624?style=for-the-badge&logo=linux&logoColor=black) | Paquete Debian |
| ![Linux AppImage](https://img.shields.io/badge/Linux-AppImage-FCC624?style=for-the-badge&logo=linux&logoColor=black) | AppImage, portable |
| ![Linux RPM](https://img.shields.io/badge/Linux-RPM-FCC624?style=for-the-badge&logo=linux&logoColor=black) | Paquete RPM |
| ![Flathub](https://img.shields.io/badge/Linux-Flatpak-FCC624?style=for-the-badge&logo=flathub&logoColor=black) | Flatpak Bundle |

<details>
<summary>🛠️ Pasos de instalación</summary>

- **DEB (`.deb`)**:
  ```bash
  sudo dpkg -i ytsage_*.deb
  sudo apt-get install -f # Repara dependencias faltantes si es necesario
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
- **Flatpak**: Sigue las instrucciones en Flathub o ejecuta:
  ```bash
  flatpak install flathub io.github.oop7.ytsage
  ```
</details>

#### 🍎 macOS

| Formato | Descripción |
|--------|-------------|
| ![macOS ARM64 APP](https://img.shields.io/badge/macOS-ARM64%20APP-000000?style=for-the-badge&logo=apple&logoColor=white) | Aplicación comprimida para Apple Silicon |
| ![macOS ARM64 DMG](https://img.shields.io/badge/macOS-ARM64%20DMG-000000?style=for-the-badge&logo=apple&logoColor=white) | Instalador de imagen de disco para Apple Silicon |

<details>
<summary>🛠️ Pasos de instalación</summary>

- **Instalador DMG (`.dmg`)**: Haz doble clic para montar, luego arrastra `YTSage.app` a tu carpeta de Aplicaciones.
- **Archivo de aplicación (`.zip`)**: Extrae el zip y mueve `YTSage.app` a tu carpeta de Aplicaciones.

*Nota: Si encuentras el error "La aplicación está dañada", consulta la sección de solución de problemas de macOS a continuación.*
</details>

---

<details>
<summary>💻 Instalación manual desde el código fuente</summary>

### 1. Clonar el repositorio

```bash
git clone https://github.com/oop7/YTSage.git
cd YTSage
```

### 2. Instalar dependencias

#### ⚡ Con uv

```bash
uv pip install .
```

#### 📦 O con pip estándar

```bash
pip install .
```

### 3. Ejecutar la aplicación

```bash
python -m ytsage.main
```

</details>

<a id="screenshots"></a>
## 📸 Capturas de pantalla

<div align="center">
<table>
  <tr>
    <td><img src="../branding/screenshots/Download-Settings.png" alt="Ajustes de descarga" width="400"/></td>
    <td><img src="../branding/screenshots/playlist.png" alt="Descarga de lista de reproducción" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><em>Ajustes de descarga</em></td>
    <td align="center"><em>Descarga de lista de reproducción</em></td>
  </tr>
  <tr>
    <td><img src="../branding/screenshots/audio_format.png" alt="Selección de formato de audio" width="400"/></td>
    <td><img src="../branding/screenshots/Custom-Option.png" alt="Opción personalizada" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><em>Formato de audio</em></td>
    <td align="center"><em>Opción personalizada</em></td>
  </tr>
</table>
</div>

<a id="usage"></a>
## 📖 Uso

<details>
<summary>🎯 Uso básico</summary>

1. **Lanza YTSage**
2. **Pega la URL de YouTube** (o usa el botón "Paste URL")
3. **Haz clic en "Analyze"**
4. **Selecciona el formato:**
   - `Video` para descargas de video
   - `Audio Only` para extracción de audio
5. **Elige opciones:**
   - Activar subtítulos y elegir idioma
   - Activar fusión de subtítulos
   - Guardar miniatura
   - Eliminar segmentos patrocinados
   - Guardar descripción
   - Integrar capítulos
6. **Selecciona directorio de salida**
7. **Haz clic en "Download"**

> 💡 El directorio de descarga predeterminado es la carpeta "Downloads" del usuario.

</details>

<details>
<summary>📋 Descarga de listas de reproducción</summary>

1. **Pega la URL de la lista de reproducción**
2. **Haz clic en "Analyze"**
3. **Selecciona videos del selector de listas (opcional, todos por defecto)**
4. **Elige formato/calidad deseada**
5. **Haz clic en "Download"**

> 💡 La aplicación gestiona las colas de descarga automáticamente, y puedes exportar entradas de la lista como archivos `.txt`, `.csv`, `.m3u` o `.json`.

</details>

<details>
<summary>🌍 Modo genérico para sitios que no son YouTube</summary>

Usa el modo genérico (Generic Mode) cuando desees que YTSage acepte URLs de sitios compatibles con yt-dlp, como Dailymotion, CBC Gem, TikTok y otros.

Cómo usarlo:

1. Abre `Download Settings`.
2. Activa `Generic Mode`.
3. Pega una URL de video o lista de reproducción compatible que no sea de YouTube.
4. Haz clic en `Analyze`.
5. Elige el formato y descarga como de costumbre.

Notas:

- El modo genérico solo cambia la validación de la URL dentro de YTSage. El sitio debe ser compatible con tu versión instalada de yt-dlp.
- Algunos sitios requieren cookies, inicio de sesión, proxy o argumentos adicionales de yt-dlp dependiendo del extractor.
- Si un sitio falla, actualiza primero yt-dlp desde la pestaña de actualización integrada antes de informar del problema.

</details>

<details>
<summary>🧰 Opciones de medios y descarga</summary>

- **Opciones de subtítulos:** Filtra idiomas e incrusta subtítulos en el archivo de video.
- **Fusión de subtítulos:** Fusiona subtítulos en el archivo de video para subtítulos fijos (hardcoded).
- **Guardar descripción:** Guarda la descripción del video como un archivo de texto.
- **Guardar miniatura:** Guarda la miniatura del video como un archivo de imagen.
- **Integrar capítulos:** Incluye marcas de capítulo como metadatos para reproductores de video compatibles.
- **Eliminar segmentos patrocinados:** Elimina segmentos patrocinados del video usando SponsorBlock.
- **Recortar video:** Descarga solo partes específicas de un video especificando rangos de tiempo en formato `HH:MM:SS`.

</details>

<details>
<summary>⚙️ Ajustes de salida y archivos</summary>

- **Limitador de velocidad:** Limita la velocidad de descarga, p. ej., `500K` para 500 KB/s.
- **Guardar ruta de descarga:** Guarda la ruta de descarga predeterminada para futuras descargas. Disponible en **Download Settings → Download Path**.
- **Resolución de video predeterminada:** Establece tu resolución de video preferida para selección automática (p. ej., 1080p, 720p). Disponible en **Download Settings → Default Video Resolution**.
- **Idiomas de subtítulos predeterminados:** Establece idiomas de subtítulos para selección automática (separados por comas, p. ej., `es,en`). Disponible en **Download Settings → Default Subtitle Languages**.
- **Formato de nombre de archivo:** Personaliza el formato del nombre de archivo usando variables como `%(title)s`, `%(uploader)s`, `%(playlist_index)s` y `%(resolution)s`. Disponible en **Download Settings → Filename Format**.
- **Forzar formato de salida:** Fuerza las descargas de video a un formato de contenedor específico como `mp4`, `webm` o `mkv`. Disponible en **Download Settings → Output Format Settings**.
- **Conversión de formato de audio:** Convierte descargas de solo audio a formatos preferidos como `AAC`, `MP3`, `FLAC`, `WAV`, `Opus`, `M4A`, `Vorbis` o `Best`. Disponible en **Download Settings → Audio Format Settings**.
- **Normalización de audio:** Estandariza el volumen para descargas de solo audio usando EBU R128.
- **Conexiones simultáneas:** Aumenta drásticamente la velocidad de descarga descargando archivos en múltiples fragmentos a la vez. Disponible en **Download Settings → General → Concurrent Connections** (1 por defecto, máximo recomendado 8-10 para evitar bloqueos por IP).

</details>

<details>
<summary>🌐 Acceso y red</summary>

- **Inicio de sesión con cookies:** Inicia sesión en YouTube usando cookies para acceder a contenido privado.
  Cómo usarlo:
  1. **Recomendado:** Usa la opción integrada `Extract cookies from browser` en la aplicación, luego selecciona tu navegador y opcionalmente un perfil.
  2. Alternativamente, extrae las cookies manualmente:
     a. Exporta cookies de tu navegador usando una extensión como [cookie-editor](https://github.com/moustachauve/cookie-editor?tab=readme-ov-file)
     b. Copia las cookies en formato Netscape
     c. Crea un archivo llamado `cookies.txt` y pega las cookies
     d. Selecciona el archivo `cookies.txt` en la aplicación
- **Soporte de proxy:** Usa un servidor proxy para las descargas, p. ej., `http://<servidor-proxy>:<puerto>`
- **Modo genérico:** Permite a YTSage analizar y descargar desde sitios que no son YouTube compatibles con yt-dlp. Actívalo en **Download Settings → Generic Mode**.

</details>

<details>
<summary>🛠️ Herramientas y mantenimiento</summary>

- **Comandos personalizados:** Accede a funciones avanzadas de yt-dlp mediante argumentos de línea de comandos.
- **Pestaña de actualización:** Gestiona herramientas de actualización desde un solo lugar en Opciones personalizadas:
  - **Actualizaciones de yt-dlp:** Busca actualizaciones y cambia entre canales estable y nightly.
  - **Verificador de versión de FFmpeg:** Verifica tu versión de FFmpeg y abre guías de instalación.
  - **Actualizaciones de Deno:** Verifica y actualiza el motor de ejecución Deno.
- **Detección de FFmpeg/yt-dlp/Deno:** Detecta automáticamente rutas y versiones de FFmpeg, yt-dlp y Deno desde el diálogo Acerca de.
- **Historial de descargas:** Visualiza descargas pasadas con miniaturas y estados desde el botón **History**.

</details>

<details>
<summary>🌍 Localización</summary>

YTSage soporta **14 idiomas** para accesibilidad global. Selecciona tu idioma preferido en **Custom Options → Language**.

### Idiomas soportados

| Idioma | Código | Idioma | Código |
|----------|------|----------|------|
| 🇺🇸 Inglés | `en` | 🇪🇸 Español | `es` |
| 🇸🇦 Árabe | `ar` | 🇫🇷 Francés | `fr` |
| 🇩🇪 Alemán | `de` | 🇮🇳 Hindi | `hi` |
| 🇮🇩 Indonesio | `id` | 🇮🇹 Italiano | `it` |
| 🇯🇵 Japonés | `ja` | 🇵🇱 Polaco | `pl` |
| 🇧🇷 Portugués | `pt` | 🇷🇺 Ruso | `ru` |
| 🇹🇷 Turco | `tr` | 🇨🇳 Chino | `zh` |

### Traducciones del README

| Idioma | Archivo | Idioma | Archivo |
|----------|------|----------|------|
| 🇺🇸 Inglés | [README.md](../README.md) | 🇪🇸 Español | [README.es.md](README.es.md) |
| 🇸🇦 Árabe | [README.ar.md](README.ar.md) | 🇫🇷 Francés | [README.fr.md](README.fr.md) |
| 🇩🇪 Alemán | [README.de.md](README.de.md) | 🇮🇳 Hindi | [README.hi.md](README.hi.md) |
| 🇮🇩 Indonesio | [README.id.md](README.id.md) | 🇮🇹 Italiano | [README.it.md](README.it.md) |
| 🇯🇵 Japonés | [README.ja.md](README.ja.md) | 🇵🇱 Polaco | [README.pl.md](README.pl.md) |
| 🇧🇷 Portugués | [README.pt.md](README.pt.md) | 🇷🇺 Ruso | [README.ru.md](README.ru.md) |
| 🇹🇷 Turco | [README.tr.md](README.tr.md) | 🇨🇳 Chino | [README.zh.md](README.zh.md) |

> 💡 **¿Quieres contribuir con una traducción?** ¡Consulta la sección de [Contribución](#contributing) para ayudarnos a añadir más idiomas!

</details>

<a id="troubleshooting"></a>
## 🛠️ Solución de problemas

<details>
<summary>Haz clic para ver problemas comunes y soluciones</summary>

- **La tabla de formatos no aparece:** Actualiza yt-dlp a la última versión y cambia a yt-dlp nightly.
- **Fallo de descarga:** Verifica tu conexión a internet y asegúrate de que el video esté disponible.
- **Errores de descarga específicos:**
  - **Videos privados:** Usa autenticación por cookies para acceder a contenido privado.
  - **Contenido con restricción de edad:** Inicia sesión en tu cuenta de YouTube para ver videos restringidos.
  - **Videos bloqueados geográficamente:** Considera usar una VPN para saltar restricciones regionales.
  - **Videos eliminados:** El video ya no está disponible en YouTube.
  - **Transmisiones en vivo:** Los directos no se pueden descargar; espera a que la transmisión termine.
  - **Errores de red:** Verifica tu conexión a internet e inténtalo de nuevo.
  - **URLs no válidas:** Asegúrate de que la URL sea correcta y de una plataforma compatible.
  - **Contenido Premium:** Requiere suscripción a YouTube Premium.
  - **Bloqueos por copyright:** El contenido está bloqueado por restricciones de derechos de autor.
- **Archivos de video y audio separados tras descarga:** Esto sucede cuando falta FFmpeg o no se detecta. YTSage requiere FFmpeg para fusionar flujos de video y audio de alta calidad.
  - **Solución:** Asegúrate de que FFmpeg esté instalado y accesible en el PATH de tu sistema. Para usuarios de Windows, la opción más fácil es descargar el archivo `YTSage-v<version>-ffmpeg.exe`, que incluye FFmpeg.

---

#### 🛡️ Advertencia de Windows Defender / Antivirus

Algunos programas antivirus pueden marcar archivos `.exe` como falsos positivos. Esta es una **limitación conocida** de las aplicaciones empaquetadas.

**Por qué sucede esto:**
- La heurística de los antivirus puede identificar erróneamente ejecutables empaquetados como sospechosos.

**Alternativas seguras:**
- ✅ **Usa la instalación de pip:** `pip install ytsage` (Recomendado)
- ✅ **Construye desde el código fuente**: siguiendo esta [guía](../.github/CI_CD_README.md)
- ✅ **Añade la aplicación a la lista blanca** en tu software antivirus.

#### 🍎 macOS: "La aplicación está dañada y no se puede abrir"
Si ves este error en macOS Sonoma o más reciente, necesitas eliminar el atributo de cuarentena.

1.  **Abre el Terminal** (puedes encontrarlo usando Spotlight).
2.  **Escribe el siguiente comando** pero **no presiones** Enter todavía. Asegúrate de incluir el espacio al final:
    ```bash
    xattr -d com.apple.quarantine 
    ```
3.  **Arrastra el archivo `YTSage.app`** desde tu ventana de Finder y suéltalo directamente en la ventana del Terminal. Esto pegará automáticamente la ruta correcta del archivo.
4.  **Presiona Enter** para ejecutar el comando.
5.  **Intenta abrir YTSage.app de nuevo.** Ahora debería lanzarse correctamente.

---

#### **Ubicaciones de configuración (Avanzado)**
- **Windows:** `%LOCALAPPDATA%\YTSage`
- **macOS:** `~/Library/Application Support/YTSage`
- **Linux:** `~/.local/share/YTSage`

</details>

<a id="sponsor"></a>
## 💖 Patrocinar

Si YTSage te ahorra tiempo, considera patrocinar el proyecto. El patrocinio ayuda a cubrir tiempo de desarrollo, pruebas en todas las plataformas y futuras mejoras.

- GitHub Sponsors: https://github.com/sponsors/oop7
- El enlace de patrocinio también está disponible directamente en la aplicación a través del diálogo Acerca de.

[![Sponsor YTSage](https://img.shields.io/badge/Sponsor-YTSage-EA4AAA?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sponsors/oop7)

<a id="contributing"></a>
## 👥 Contribuir

¡Agradecemos las contribuciones! Aquí tienes cómo puedes ayudar:

1. 🍴 Haz un Fork del repositorio
2. 🌿 Crea tu rama de características:
  ```bash
  git checkout -b feature/AmazingFeature
  ```
3. 💾 Haz commit de tus cambios:
  ```bash
  git commit -m 'Add some AmazingFeature'
  ```
4. 📤 Haz Push a la rama:
  ```bash
  git push origin feature/AmazingFeature
  ```
5. 🔄 Abre un Pull Request

### 🌍 Contribuir con traducciones

- Actualiza el archivo README localizado correspondiente (p. ej., `readme-translations/README.es.md`)
- Mantén las cadenas de la aplicación sincronizadas editando `ytsage/languages/<code>.json`
- Si falta tu idioma, comienza desde `README.md` y crea `README.<code>.md`

<details>
<summary>📂 Estructura del proyecto</summary>

## YTSage - Estructura del proyecto

Este documento describe la estructura de carpetas organizada de YTSage.

### 📁 Estructura del proyecto

```
YTSage/
├── 📁 .github/                   # Configuración de GitHub
│   ├── 📁 ISSUE_TEMPLATE/         # Plantillas de problemas
│   │   └── 🐛-bug-report.md       # Plantilla de informe de errores
│   ├─── 📁 workflows/              # Flujos de trabajo de GitHub Actions
│   │   ├── build-linux.yml        # Flujo de construcción para Linux
│   │   ├── build-macos.yml        # Flujo de construcción para macOS
│   │   │── build-windows.yml      # Flujo de construcción para Windows
|   |   └── release-all.yml          # Flujo de liberación maestra
│   └── 📄 CI_CD_README.md        # Documentación de CI/CD
├──  📁 branding/                 # Activos de marca (Capturas de pantalla, SVGs)
│   ├── 📁 icons/                 # Iconos de la aplicación
│   ├── 📁 screenshots/           # Capturas de pantalla para documentación
│   └── 📁 svg/                   # Activos SVG
├── 📄 LICENSE                    # Archivo de licencia
├── 📄 pyproject.toml             # Metadatos del proyecto y dependencias
├── 📄 README.md                  # Documentación del proyecto
├── 📄 requirements.txt           # Dependencias de Python (dev)
└── 📁 ytsage/                    # Paquete de código fuente
    ├── 📁 assets/                # Activos en tiempo de ejecución
    │   ├── 📁 Icon/              # Iconos de la aplicación
    │   └── 📁 sound/             # Archivos de audio
    ├── 📁 languages/             # Archivos de localización
    │   ├── 📄 ar.json            # Traducción al árabe
    │   ├── 📄 de.json            # Traducción al alemán
    │   ├── 📄 en.json            # Traducción al inglés
    │   └── ...                   # Otros idiomas
    ├── 📁 core/                  # Lógica de negocio principal
    │   ├── 📄 __init__.py        # Init del paquete core
    │   ├── 📄 ytsage_deno.py     # Integración con Deno
    │   ├── 📄 ytsage_downloader.py # Funcionalidad de descarga
    │   ├── 📄 ytsage_ffmpeg.py   # Integración con FFmpeg
    │   ├── 📄 ytsage_utils.py    # Funciones de utilidad
    │   └── 📄 ytsage_yt_dlp.py   # Integración con yt-dlp
    ├── 📁 gui/                   # Componentes de interfaz de usuario
    │   ├── 📄 __init__.py        # Init del paquete GUI
    │   ├── 📄 ytsage_gui_main.py # Ventana principal de la aplicación
    │   └── 📁 ytsage_gui_dialogs/ # Clases de diálogos
    ├── 📁 utils/                 # Módulos de utilidad
    │   ├── 📄 __init__.py        # Init del paquete utils
    │   ├── 📄 ytsage_config_manager.py # Gestión de configuración
    │   └── 📄 ytsage_logger.py   # Utilidad de registro
    ├── 📄 __init__.py            # Punto de entrada del paquete
    └── 📄 main.py                # Script de ejecución principal
```

</details>

## ⭐️ Historial de estrellas

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

## 📜 Licencia

Este proyecto está bajo la Licencia MIT - mira el archivo [LICENSE](../LICENSE) para más detalles.

## 🙏 Agradecimientos

<details>
<summary>Ver agradecimientos</summary>

<div align="center">

<p>Muchas gracias a todos los que han contribuido a este proyecto abriendo un problema para sugerir una mejora o informar de un error.</p>

<table>
    <tr class="section"><th colspan="2">Componentes principales</th></tr>
    <tr>
        <td width="35%"><a href="https://github.com/yt-dlp/yt-dlp">yt-dlp</a></td>
        <td>Motor de descarga</td>
    </tr>
    <tr>
        <td><a href="https://ffmpeg.org/">FFmpeg</a></td>
        <td>Procesamiento de medios</td>
    </tr>
    <tr>
        <td><a href="https://deno.com/">Deno</a></td>
        <td>Runtime para integración con yt-dlp</td>
    </tr>
    <tr class="section"><th colspan="2">Librerías y Frameworks</th></tr>
    <tr>
        <td><a href="https://wiki.qt.io/Qt_for_Python">PySide6</a></td>
        <td>Framework de GUI</td>
    </tr>
    <tr>
        <td><a href="https://python-pillow.org/">Pillow</a></td>
        <td>Procesamiento de imágenes</td>
    </tr>
    <tr>
        <td><a href="https://requests.readthedocs.io/">requests</a></td>
        <td>Solicitudes HTTP</td>
    </tr>
    <tr>
        <td><a href="https://packaging.python.org/">packaging</a></td>
        <td>Gestión de versiones y empaquetado</td>
    </tr>
    <tr>
        <td><a href="https://python-markdown.github.io/">markdown</a></td>
        <td>Renderizado de Markdown</td>
    </tr>
    <tr>
        <td><a href="https://github.com/Delgan/loguru">loguru</a></td>
        <td>Logging</td>
    </tr>
    <tr class="section"><th colspan="2">Activos y Colaboradores</th></tr>
    <tr>
        <td><a href="https://pixabay.com/sound-effects/new-notification-09-352705/">New Notification 09 by Universfield</a></td>
        <td>Sonido de notificación</td>
    </tr>
    <tr>
        <td><a href="https://github.com/viru185">viru185</a></td>
        <td>Colaborador de código</td>
    </tr>
</table>

</div>

</details>

## ⚠️ Descargo de responsabilidad

Esta herramienta es solo para uso personal. Por favor, respeta los términos de servicio de YouTube y los derechos de los creadores de contenido.

---

<div align="center">

Hecho con ❤️ por [oop7](https://github.com/oop7)

</div>
