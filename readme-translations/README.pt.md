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

**Um downloader de YouTube moderno com uma interface PySide6 limpa.**  
Baixe vídeos em qualquer qualidade, extraia áudio, obtenha legendas e muito mais.

### 🌍 Idiomas do README

Inglês: [EN](../README.md)
| Árabe: [AR](README.ar.md)
| Alemão: [DE](README.de.md)
| Espanhol: [ES](README.es.md)
| Francês: [FR](README.fr.md)
| Hindi: [HI](README.hi.md)
| Indonésio: [ID](README.id.md)
| Italiano: [IT](README.it.md)
| Japonês: [JA](README.ja.md)
| Polonês: [PL](README.pl.md)
| Português: [PT](README.pt.md)
| Russo: [RU](README.ru.md)
| Turco: [TR](README.tr.md)
| Chinês: [ZH](README.zh.md)

<p align="center">
  <a href="#instalação">Instalação</a> •
  <a href="#funcionalidades">Funcionalidades</a> •
  <a href="#uso">Uso</a> •
  <a href="#capturas-de-tela">Capturas de Tela</a> •
  <a href="#solução-de-problemas">Solução de Problemas</a> •
  <a href="#patrocinar">Patrocinar</a> •
  <a href="#contribuindo">Contribuindo</a>
</p>

</div>

---

<a id="por-que-ytsage"></a>
## ❓ Por que YTSage?

O YTSage foi projetado para usuários que desejam um **downloader de YouTube simples, mas poderoso**. Ao contrário de outras ferramentas, ele oferece:

- Uma interface PySide6 moderna e limpa
- Download de vídeo, áudio e legendas com um clique
- Recursos avançados como SponsorBlock, mesclagem de legendas e seleção de playlist
- Modo Genérico opcional para sites além do YouTube suportados pelo yt-dlp
- Suporte multiplataforma e instalação fácil

<a id="funcionalidades"></a>
## ✨ Funcionalidades

<div align="center">

| Recursos Básicos | Recursos Avançados | Recursos Extras |
|-----------------------------------|-----------------------------------------|------------------------------------|
| 🎥 Tabela de Formatos | 🚫 Integração SponsorBlock | 🎞️ Exibição de FPS/HDR |
| 🎵 Extração de Áudio | 📝 Seleção e Mesclagem de Legendas | 🔄 Atualização Automática do yt-dlp |
| ✨ Interface de Usuário Simples | 💾 Salvar Descrição e Miniatura | 🛠️ Detecção de FFmpeg/yt-dlp/Deno |
| 📋 Suporte e Seletor de Playlist | 🚀 Limitador de Velocidade | ⚙️ Comandos Personalizados |
| 📑 Integração de Capítulos | ✂️ Cortar Seções de Vídeo | 🍪 Login por Cookies |
| 📜 Histórico de Downloads | 🔄 Escolha do Canal de Lançamento | 🌐 Suporte a Proxy |
| 🎚️ Conversão de Formato de Áudio | 🎬 Configurações de Formato de Vídeo | 🆙 Aba de Atualização Integrada |
| 🌍 Modo Genérico | 🔊 Normalização de Áudio (EBU R128) | 🌍 Localização em 14 idiomas |
| 💾 Exportação de Playlist | ⚙️ Qualidade e Legendas Padrão | |
</div>

<a id="instalação"></a>
## 🚀 Instalação

### ⚡ Instalação Rápida (Recomendada)

Instale o YTSage via PyPI:

```bash
pip install ytsage
```

<details>
<summary>🔄 Atualizar Instalação Existente</summary>

```bash
pip install --upgrade ytsage
```

</details>

Em seguida, execute o aplicativo:

```bash
ytsage
```

### 📦 Executáveis Pré-compilados (Executable)

> [👉 Baixar Lançamento Mais Recente](https://github.com/oop7/YTSage/releases/latest)

#### 🪟 Windows

| Formato | Descrição |
|--------|-------------|
| ![Windows EXE](https://img.shields.io/badge/Windows-EXE-0078D6?style=for-the-badge&logo=windows&logoColor=white) | Instalador Padrão |
| ![Windows FFmpeg](https://img.shields.io/badge/Windows-FFmpeg-0078D6?style=for-the-badge&logo=windows&logoColor=white) | Com FFmpeg incluído |
| ![Windows Portable](https://img.shields.io/badge/Windows-Portable-0078D6?style=for-the-badge&logo=windows&logoColor=white) | Versão Portátil, sem necessidade de instalação |
| ![Windows Portable FFmpeg](https://img.shields.io/badge/Windows-Portable%20FFmpeg-0078D6?style=for-the-badge&logo=windows&logoColor=white) | Portátil com FFmpeg, compactado (ZIP) |

<details>
<summary>🛠️ Passos para Instalação</summary>

1. **Instalador EXE (`.exe`)**: Clique duas vezes no arquivo e siga o assistente de configuração.
2. **Versão Portátil (`.zip`)**: Extraia o arquivo para o local desejado e execute `ytsage.exe`.
3. **FFmpeg Integrado**: Se você não possui o FFmpeg instalado no sistema, escolha as versões com FFmpeg integrado.
</details>

#### 🐧 Linux

| Formato | Descrição |
|--------|-------------|
| ![Linux DEB](https://img.shields.io/badge/Linux-DEB-FCC624?style=for-the-badge&logo=linux&logoColor=black) | Pacote Debian |
| ![Linux AppImage](https://img.shields.io/badge/Linux-AppImage-FCC624?style=for-the-badge&logo=linux&logoColor=black) | AppImage, Portátil |
| ![Linux RPM](https://img.shields.io/badge/Linux-RPM-FCC624?style=for-the-badge&logo=linux&logoColor=black) | Pacote RPM |
| ![Flathub](https://img.shields.io/badge/Linux-Flatpak-FCC624?style=for-the-badge&logo=flathub&logoColor=black) | Pacote Flatpak |

<details>
<summary>🛠️ Passos para Instalação</summary>

- **DEB (`.deb`)**:
  ```bash
  sudo dpkg -i ytsage_*.deb
  sudo apt-get install -f # Se necessário para corrigir dependências ausentes
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
- **Flatpak**: Siga as instruções no Flathub ou execute:
  ```bash
  flatpak install flathub io.github.oop7.ytsage
  ```
</details>

#### 🍎 macOS

| Formato | Descrição |
|--------|-------------|
| ![macOS ARM64 APP](https://img.shields.io/badge/macOS-ARM64%20APP-000000?style=for-the-badge&logo=apple&logoColor=white) | Aplicativo ZIP para Apple Silicon |
| ![macOS ARM64 DMG](https://img.shields.io/badge/macOS-ARM64%20DMG-000000?style=for-the-badge&logo=apple&logoColor=white) | Instalador Disk Image para Apple Silicon |

<details>
<summary>🛠️ Passos para Instalação</summary>

- **Instalador DMG (`.dmg`)**: Clique duas vezes para montar e arraste `YTSage.app` para a sua pasta Aplicativos.
- **Arquivo do Aplicativo (`.zip`)**: Extraia o ZIP e mova `YTSage.app` para a sua pasta Aplicativos.

*Nota: Se você receber o erro "App está danificado", veja a seção de Problemos no macOS abaixo.*
</details>

---

<details>
<summary>💻 Instalação Manual a partir do Código-Fonte</summary>

### 1. Clonar o Repositório

```bash
git clone https://github.com/oop7/YTSage.git
cd YTSage
```

### 2. Instalar Dependências

#### ⚡ Com uv

```bash
uv pip install .
```

#### 📦 Ou com pip padrão

```bash
pip install .
```

### 3. Executar o Aplicativo

```bash
python -m ytsage.main
```

</details>

<a id="capturas-de-tela"></a>
## 📸 Capturas de Tela

<div align="center">
<table>
  <tr>
    <td><img src="../branding/screenshots/Download-Settings.png" alt="Configurações de Download" width="400"/></td>
    <td><img src="../branding/screenshots/playlist.png" alt="Download de Playlist" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><em>Configurações de Download</em></td>
    <td align="center"><em>Download de Playlist</em></td>
  </tr>
  <tr>
    <td><img src="../branding/screenshots/audio_format.png" alt="Seleção de Formato de Áudio" width="400"/></td>
    <td><img src="../branding/screenshots/Custom-Option.png" alt="Opções Personalizadas" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><em>Formato de Áudio</em></td>
    <td align="center"><em>Opções Personalizadas</em></td>
  </tr>
</table>
</div>

<a id="uso"></a>
## 📖 Uso

<details>
<summary>🎯 Uso Básico</summary>

1. **Inicie o YTSage**
2. **Cole uma URL do YouTube** (ou use o botão "Paste URL")
3. **Clique em "Analyze"**
4. **Escolha o Formato:**
   - `Video` para download de vídeo
   - `Audio Only` para extração de áudio
5. **Selecione Opções:**
   - Habilite legendas e escolha o idioma
   - Habilite a mesclagem de legendas
   - Salvar miniatura
   - Remover seções de patrocinadores
   - Salvar descrição
   - Incorporar capítulos
6. **Escolha o Diretório de Saída**
7. **Clique em "Download"**

> 💡 O diretório de download padrão é a pasta "Downloads" do usuário.

</details>

<details>
<summary>📋 Download de Playlist</summary>

1. **Cole a URL da Playlist**
2. **Clique em "Analyze"**
3. **Selecione vídeos do seletor (opcional, padrão todos)**
4. **Escolha o formato/qualidade desejado**
5. **Clique em "Download"**

> 💡 O aplicativo gerencia automaticamente a fila de download, e você pode exportar as entradas da playlist como arquivos `.txt`, `.csv`, `.m3u` ou `.json`.

</details>

<details>
<summary>🌍 Modo Genérico para Sites além do YouTube</summary>

Use o Modo Genérico quando quiser que o YTSage aceite URLs de sites suportados pelo yt-dlp, como Dailymotion, CBC Gem, TikTok e outros.

Como usar:

1. Abra `Download Settings`.
2. Habilite `Generic Mode`.
3. Cole uma URL de vídeo ou playlist suportada que não seja do YouTube.
4. Clique em `Analyze`.
5. Escolha um formato e baixe normalmente.

Notas:

- O Modo Genérico apenas altera a validação da URL dentro do YTSage. O site de destino ainda deve ser suportado pela sua versão instalada do yt-dlp.
- Alguns sites exigem cookies, login, proxy ou argumentos adicionais do yt-dlp, dependendo do extrator.
- Se um site falhar, atualize o yt-dlp na aba de atualização integrada antes de relatar o problema.

</details>

<details>
<summary>🧰 Opções de Mídia e Download</summary>

- **Opções de Legendas:** Filtre idiomas e incorpore legendas no arquivo de vídeo.
- **Mesclagem de Legendas:** Mescla legendas no arquivo de vídeo para legendas fixas (hardcoded).
- **Salvar Descrição:** Salva a descrição do vídeo como um arquivo de texto.
- **Salvar Miniatura:** Salva a miniatura do vídeo como um arquivo de imagem.
- **Incorporar Capítulos:** Inclui marcadores de capítulo como metadados para players de vídeo compatíveis.
- **Remover Seções de Patrocinadores:** Usa o SponsorBlock para remover segmentos patrocinados do vídeo.
- **Cortar Vídeo:** Baixe apenas partes específicas do vídeo, especificando o intervalo de tempo no formato `HH:MM:SS`.

</details>

<details>
<summary>⚙️ Configurações de Saída e Arquivos</summary>

- **Limitador de Velocidade:** Limite a velocidade de download, por exemplo, `500K` para 500 KB/s.
- **Salvar Caminho de Download:** Salva o caminho de download padrão para downloads futuros. Disponível em **Download Settings → Download Path**.
- **Resolução de Vídeo Padrão:** Defina sua resolução de vídeo preferida para seleção automática (ex: 1080p, 720p). Disponível em **Download Settings → Default Video Resolution**.
- **Idiomas de Legendas Padrão:** Defina idiomas de legendas padrão para seleção automática (separados por vírgula, ex: `pt,en`). Disponível em **Download Settings → Default Subtitle Languages**.
- **Formato de Nome de Arquivo:** Personalize o formato do nome do arquivo de saída usando variáveis como `%(title)s`, `%(uploader)s`, `%(playlist_index)s` e `%(resolution)s`. Disponível em **Download Settings → Filename Format**.
- **Forçar Formato de Saída:** Força o download do vídeo em um formato de contêiner específico, como `mp4`, `webm` ou `mkv`. Disponível em **Download Settings → Output Format Settings**.
- **Conversão de Formato de Áudio:** Converta downloads de apenas áudio para formatos preferidos como `AAC`, `MP3`, `FLAC`, `WAV`, `Opus`, `M4A`, `Vorbis`, ou `Best`. Disponível em **Download Settings → Audio Format Settings**.
- **Normalização de Áudio:** Padroniza o volume para downloads de apenas áudio usando EBU R128.
- **Conexões Simultâneas:** Aumente significativamente a velocidade de download baixando arquivos em várias partes ao mesmo tempo. Disponível em **Download Settings → General → Concurrent Connections** (padrão 1, máximo 8-10 recomendado para evitar bloqueios de IP).

</details>

<details>
<summary>🌐 Acesso e Rede</summary>

- **Login por Cookies:** Faça login no YouTube usando cookies para acessar conteúdo privado.
  Uso:
  1. **Recomendado:** Use a opção integrada `Extract cookies from browser` no aplicativo, selecione o navegador e, opcionalmente, o perfil.
  2. Opcionalmente, extraia cookies manualmente:
     a. Exporte cookies do seu navegador usando uma extensão como [cookie-editor](https://github.com/moustachauve/cookie-editor?tab=readme-ov-file)
     b. Copie os cookies no formato Netscape
     c. Crie um arquivo chamado `cookies.txt` e cole os cookies
     d. Selecione o arquivo `cookies.txt` no aplicativo
- **Suporte a Proxy:** Use um servidor proxy para downloads, ex: `http://<proxy-server>:<port>`
- **Modo Genérico:** Permite que o YTSage analise e baixe de sites além do YouTube suportados pelo yt-dlp. Habilite em **Download Settings → Generic Mode**.

</details>

<details>
<summary>🛠️ Ferramentas e Manutenção</summary>

- **Comandos Personalizados:** Acesse recursos avançados do yt-dlp via argumentos de linha de comando.
- **Aba de Atualização:** Gerencie as ferramentas de atualização integradas em um só lugar nas Opções Personalizadas:
  - **Atualização do yt-dlp:** Verifique atualizações e alterne entre os canais de lançamento Stable e Nightly.
  - **Verificador de Versão do FFmpeg:** Verifique sua versão do FFmpeg e abra guias de instalação.
  - **Atualização do Deno:** Verifique e atualize o runtime do Deno.
- **Detecção de FFmpeg/yt-dlp/Deno:** Detecta automaticamente caminhos e versões de FFmpeg, yt-dlp e Deno no diálogo Sobre.
- **Histórico de Downloads:** Veja downloads anteriores com miniaturas e status no botão **History**.

</details>

<details>
<summary>🌍 Localização</summary>

O YTSage suporta **14 idiomas** para alcance global. Escolha o seu idioma preferido em **Custom Options → Language**.

### Idiomas Suportados

| Idioma | Código | Idioma | Código |
|----------|------|----------|------|
| 🇺🇸 Inglês | `en` | 🇪🇸 Espanhol | `es` |
| 🇸🇦 Árabe | `ar` | 🇫🇷 Francês | `fr` |
| 🇩🇪 Alemão | `de` | 🇮🇳 Hindi | `hi` |
| 🇮🇩 Indonésio | `id` | 🇮🇹 Italiano | `it` |
| 🇯🇵 Japonês | `ja` | 🇵🇱 Polonês | `pl` |
| 🇧🇷 Português | `pt` | 🇷🇺 Russo | `ru` |
| 🇹🇷 Turco | `tr` | 🇨🇳 Chinês | `zh` |

### Traduções do README

| Idioma | Arquivo | Idioma | Arquivo |
|----------|------|----------|------|
| 🇺🇸 Inglês | [README.md](../README.md) | 🇪🇸 Espanhol | [README.es.md](README.es.md) |
| 🇸🇦 Árabe | [README.ar.md](README.ar.md) | 🇫🇷 Francês | [README.fr.md](README.fr.md) |
| 🇩🇪 Alemão | [README.de.md](README.de.md) | 🇮🇳 Hindi | [README.hi.md](README.hi.md) |
| 🇮🇩 Indonésio | [README.id.md](README.id.md) | 🇮🇹 Italiano | [README.it.md](README.it.md) |
| 🇯🇵 Japonês | [README.ja.md](README.ja.md) | 🇵🇱 Polonês | [README.pl.md](README.pl.md) |
| 🇧🇷 Português | [README.pt.md](README.pt.md) | 🇷🇺 Russo | [README.ru.md](README.ru.md) |
| 🇹🇷 Turco | [README.tr.md](README.tr.md) | 🇨🇳 Chinês | [README.zh.md](README.zh.md) |

> 💡 **Quer ajudar na tradução?** Veja a seção [Contribuindo](#contribuindo) para nos ajudar a adicionar mais idiomas!

</details>

<a id="solução-de-problemas"></a>
## 🛠️ Solução de Problemas

<details>
<summary>Clique para ver problemas comuns e soluções</summary>

- **Tabela de formatos não aparece:** Atualize o yt-dlp para a versão mais recente e tente alternar para o yt-dlp Nightly.
- **Download falhou:** Verifique sua conexão com a internet e certifique-se de que o vídeo está disponível.
- **Erros de Download Específicos:**
  - **Vídeos Privados:** Use a autenticação por cookies para acessar conteúdo privado.
  - **Conteúdo com Restrição de Idade:** Faça login na sua conta do YouTube para visualizar vídeos com restrição de idade.
  - **Vídeos com Bloqueio Geográfico:** Considere usar uma VPN para contornar restrições regionais.
  - **Vídeo Removido:** O vídeo não está mais disponível no YouTube.
  - **Live Streams:** Transmissões ao vivo não podem ser baixadas enquanto estão sendo transmitidas; aguarde até que a transmissão termine.
  - **Erros de Rede:** Verifique sua conexão com a internet e tente novamente.
  - **URL Inválida:** Certifique-se de que a URL está correta e pertence a uma plataforma suportada.
  - **Conteúdo Premium:** Requer uma assinatura do YouTube Premium.
  - **Bloqueio por Direitos Autorais:** O conteúdo está bloqueado devido a restrições de direitos autorais.
- **Arquivos de vídeo e áudio estão separados após o download:** Isso acontece quando o FFmpeg está ausente ou não foi detectado. O YTSage requer o FFmpeg para mesclar streams de vídeo e áudio de alta qualidade.
  - **Solução:** Certifique-se de que o FFmpeg está instalado e acessível no PATH do seu sistema. Para usuários do Windows, a opção mais fácil é baixar o arquivo `YTSage-v<versão>-ffmpeg.exe`, que já vem com o FFmpeg.

---

#### 🛡️ Aviso do Windows Defender / Antivírus

Alguns softwares antivírus podem sinalizar arquivos `.exe` como falsos positivos. Esta é uma **limitação conhecida** de aplicativos empacotados.

**Por que isso acontece:**
- As heurísticas do antivírus podem identificar incorretamente executáveis empacotados como suspeitos.

**Opções Seguras:**
- ✅ **Use a instalação via pip:** `pip install ytsage` (recomendado)
- ✅ **Compile a partir do código-fonte**: Seguindo este [guia](../.github/CI_CD_README.md)
- ✅ **Adicione o aplicativo à lista de permissões** do seu software antivírus.

#### 🍎 macOS: "App está danificado e não pode ser aberto"
Se você vir este erro no macOS Sonoma ou mais recente, você precisa remover o atributo de quarentena.

1.  **Abra o Terminal** (você pode encontrá-lo usando o Spotlight).
2.  **Digite o seguinte comando**, mas ainda **NÃO** pressione Enter. Certifique-se de incluir o espaço no final:
    ```bash
    xattr -d com.apple.quarantine 
    ```
3.  **Arraste o arquivo `YTSage.app` da janela do Finder** e solte-o diretamente na janela do Terminal. Isso colará automaticamente o caminho correto do arquivo.
4.  **Pressione Enter** para executar o comando.
5.  **Tente abrir o YTSage.app novamente.** Ele agora deve iniciar corretamente.

---

#### **Localização da Configuração (Avançado)**
- **Windows:** `%LOCALAPPDATA%\YTSage`
- **macOS:** `~/Library/Application Support/YTSage`
- **Linux:** `~/.local/share/YTSage`

</details>

<a id="patrocinar"></a>
## 💖 Patrocinar

Se o YTSage economiza seu tempo, considere patrocinar o projeto. Os patrocínios ajudam a cobrir o tempo de desenvolvimento, testes em todas as plataformas e melhorias futuras.

- GitHub Sponsors: https://github.com/sponsors/oop7
- O link de patrocínio está disponível diretamente através do diálogo Sobre no aplicativo.

[![Sponsor YTSage](https://img.shields.io/badge/Sponsor-YTSage-EA4AAA?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sponsors/oop7)

<a id="contribuindo"></a>
## 👥 Contribuindo

Contribuições são bem-vindas! Veja como você pode ajudar:

1. 🍴 Faça um Fork do repositório
2. 🌿 Crie sua branch de recurso:
  ```bash
  git checkout -b feature/RecursoIncrivel
  ```
3. 💾 Faça o commit de suas alterações:
  ```bash
  git commit -m 'Adicionar RecursoIncrivel'
  ```
4. 📤 Faça o push para a branch:
  ```bash
  git push origin feature/RecursoIncrivel
  ```
5. 🔄 Abra um Pull Request

### 🌍 Contribua com Traduções

- Atualize o arquivo README localizado relevante (ex: `readme-translations/README.pt.md`)
- Mantenha as strings do aplicativo em sincronia editando `ytsage/languages/<code>.json`
- Se o seu idioma estiver ausente, comece pelo `README.md` e crie `README.<code>.md`

<details>
<summary>📂 Estrutura do Projeto</summary>

## YTSage - Estrutura do Projeto

Este documento descreve a estrutura de pastas organizada do YTSage.

### 📁 Estrutura do Projeto

```
YTSage/
├── 📁 .github/                   # Configurações do GitHub
│   ├── 📁 ISSUE_TEMPLATE/         # Modelos de problemas
│   │   └── 🐛-bug-report.md       # Modelo de relatório de erro
│   ├─── 📁 workflows/              # Fluxos de trabalho do GitHub Actions
│   │   ├── build-linux.yml        # Fluxo de build para Linux
│   │   ├── build-macos.yml        # Fluxo de build para macOS
│   │   │── build-windows.yml      # Fluxo de build para Windows
|   |   └── release-all.yml          # Fluxo de lançamento principal
│   └── 📄 CI_CD_README.md        # Documentação CI/CD
├──  📁 branding/                 # Ativos de marca (capturas de tela, SVGs)
│   ├── 📁 icons/                 # Ícones do aplicativo
│   ├── 📁 screenshots/           # Capturas de tela para documentação
│   └── 📁 svg/                   # Ativos SVG
├── 📄 LICENSE                    # Arquivo de licença
├── 📄 pyproject.toml             # Metadados do projeto e dependências
├── 📄 README.md                  # Documentação do projeto
├── 📄 requirements.txt           # Dependências Python (dev)
└── 📁 ytsage/                    # Pacote de código-fonte
    ├── 📁 assets/                # Ativos de tempo de execução
    │   ├── 📁 Icon/              # Ícones do aplicativo
    │   └── 📁 sound/             # Arquivos de áudio
    ├── 📁 languages/             # Arquivos de localização
    │   ├── 📄 ar.json            # Tradução em árabe
    │   ├── 📄 de.json            # Tradução em alemão
    │   ├── 📄 en.json            # Tradução em inglês
    │   └── ...                   # Outros idiomas
    ├── 📁 core/                  # Lógica de negócios principal
    │   ├── 📄 __init__.py        
    │   ├── 📄 ytsage_deno.py     # Integração Deno
    │   ├── 📄 ytsage_downloader.py # Funcionalidade de download
    │   ├── 📄 ytsage_ffmpeg.py   # Integração FFmpeg
    │   ├── 📄 ytsage_utils.py    # Funções utilitárias
    │   └── 📄 ytsage_yt_dlp.py   # Integração yt-dlp
    ├── 📁 gui/                   # Componentes de interface do usuário
    │   ├── 📄 __init__.py        
    │   ├── 📄 ytsage_gui_main.py # Janela principal do aplicativo
    │   └── 📁 ytsage_gui_dialogs/ # Classes de diálogo
    ├── 📁 utils/                 # Módulos utilitários
    │   ├── 📄 __init__.py        
    │   ├── 📄 ytsage_config_manager.py # Gerenciamento de configuração
    │   └── 📄 ytsage_logger.py   # Ferramentas de registro
    ├── 📄 __init__.py            # Ponto de entrada do pacote
    └── 📄 main.py                # Script de execução principal
```

</details>

## ⭐️ Histórico de Estrelas

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

## 📜 Licença

Este projeto é licenciado sob a Licença MIT - consulte o arquivo [LICENSE](../LICENSE) para mais detalhes.

## 🙏 Agradecimentos

<details>
<summary>Mostrar Agradecimentos</summary>

<div align="center">

<p>Muito obrigado a todos que contribuíram para este projeto abrindo problemas para sugerir melhorias ou relatar erros.</p>

<table>
    <tr class="section"><th colspan="2">Componentes Principais</th></tr>
    <tr>
        <td width="35%"><a href="https://github.com/yt-dlp/yt-dlp">yt-dlp</a></td>
        <td>Mecanismo de Download</td>
    </tr>
    <tr>
        <td><a href="https://ffmpeg.org/">FFmpeg</a></td>
        <td>Processamento de Mídia</td>
    </tr>
    <tr>
        <td><a href="https://deno.com/">Deno</a></td>
        <td>Runtime para integração do yt-dlp</td>
    </tr>
    <tr class="section"><th colspan="2">Bibliotecas e Frameworks</th></tr>
    <tr>
        <td><a href="https://wiki.qt.io/Qt_for_Python">PySide6</a></td>
        <td>Framework GUI</td>
    </tr>
    <tr>
        <td><a href="https://python-pillow.org/">Pillow</a></td>
        <td>Processamento de Imagens</td>
    </tr>
    <tr>
        <td><a href="https://requests.readthedocs.io/">requests</a></td>
        <td>Requisições HTTP</td>
    </tr>
    <tr>
        <td><a href="https://packaging.python.org/">packaging</a></td>
        <td>Gerenciamento de Versão e Empacotamento</td>
    </tr>
    <tr>
        <td><a href="https://python-markdown.github.io/">markdown</a></td>
        <td>Renderização de Markdown</td>
    </tr>
    <tr>
        <td><a href="https://github.com/Delgan/loguru">loguru</a></td>
        <td>Registro de Logs</td>
    </tr>
    <tr class="section"><th colspan="2">Ativos e Contribuidores</th></tr>
    <tr>
        <td><a href="https://pixabay.com/sound-effects/new-notification-09-352705/">New Notification 09 de Universfield</a></td>
        <td>Som de Notificação</td>
    </tr>
    <tr>
        <td><a href="https://github.com/viru185">viru185</a></td>
        <td>Contribuidor de Código</td>
    </tr>
</table>

</div>

</details>

## ⚠️ Isenção de Responsabilidade

Esta ferramenta é apenas para uso pessoal. Respeite os Termos de Serviço do YouTube e os direitos dos produtores de conteúdo.

---

<div align="center">

Criado com ❤️ por [oop7](https://github.com/oop7)

</div>
