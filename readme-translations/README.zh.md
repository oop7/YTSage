<div align="center">

<img src="../branding/svg/ytsage-wordmark.svg" width="400" alt="ytsage-wordmark">
<img src="../branding/screenshots/main.png" width="800" alt="YTSage 界面"/>

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-1f2937?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![PyPI 下载量](https://img.shields.io/pepy/dt/ytsage?color=1f2937&style=for-the-badge&label=downloads&logo=python&logoColor=white)](https://pepy.tech/project/ytsage)
[![GitHub 下载量](https://img.shields.io/github/downloads/oop7/YTSage/total?color=1f2937&style=for-the-badge&label=downloads&logo=github&logoColor=white)](https://github.com/oop7/YTSage/releases)
[![许可证: MIT](https://img.shields.io/badge/License-MIT-1f2937?style=for-the-badge&logo=opensource&logoColor=white)](https://opensource.org/licenses/MIT)
[![支持平台](https://img.shields.io/badge/platform-cross--platform-1f2937?style=for-the-badge&logo=github&logoColor=white)](https://github.com/oop7/YTSage/releases)
[![GitHub Stars](https://img.shields.io/github/stars/oop7/YTSage?color=c90000&style=for-the-badge&logo=github&logoColor=white)](https://github.com/oop7/YTSage/stargazers)
[![PyPI 版本](https://img.shields.io/pypi/v/ytsage?color=c90000&style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/ytsage/)
[![GitHub 赞助](https://img.shields.io/github/sponsors/oop7?color=c90000&style=for-the-badge&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/oop7)

**一款现代、整洁、基于 PySide6 的 YouTube 下载器。**  
支持下载任意质量的视频、提取音频、获取字幕等更多功能。

### 🌍 README 语言

英语: [EN](../README.md)
| 阿拉伯语: [AR](README.ar.md)
| 德语: [DE](README.de.md)
| 西班牙语: [ES](README.es.md)
| 法语: [FR](README.fr.md)
| 印地语: [HI](README.hi.md)
| 印尼语: [ID](README.id.md)
| 意大利语: [IT](README.it.md)
| 日语: [JA](README.ja.md)
| 波兰语: [PL](README.pl.md)
| 葡萄牙语: [PT](README.pt.md)
| 俄语: [RU](README.ru.md)
| 土耳其语: [TR](README.tr.md)
| 中文: [ZH](README.zh.md)

<p align="center">
  <a href="#安装">安装</a> •
  <a href="#功能">功能</a> •
  <a href="#使用说明">使用说明</a> •
  <a href="#屏幕截图">屏幕截图</a> •
  <a href="#故障排除">故障排除</a> •
  <a href="#赞助支持">赞助支持</a> •
  <a href="#贡献">贡献</a>
</p>

</div>

---

<a id="为什么选择-ytsage"></a>
## ❓ 为什么选择 YTSage?

YTSage 专为寻找 **简单但强大** 的 YouTube 下载器的用户而设计。与其他工具不同，它提供：

- 现代、整洁的 PySide6 用户界面
- 一键下载视频、音频和字幕
- 支持 SponsorBlock、字幕合并和播放列表选择等高级功能
- 可选的“通用模式”，支持 yt-dlp 兼容的其他非 YouTube 网站
- 跨平台支持，安装简单

<a id="功能"></a>
## ✨ 功能

<div align="center">

| 核心功能 | 高级功能 | 更多功能 |
|-----------------------------------|-----------------------------------------|------------------------------------|
| 🎥 格式选择列表 | 🚫 集成 SponsorBlock | 🎞️ FPS / HDR 显示 |
| 🎵 音频提取 | 📝 字幕选择与合并 | 🔄 yt-dlp 自动更新 |
| ✨ 现代 UI 体验 | 💾 保存描述与缩略图 | 🛠️ FFmpeg/yt-dlp/Deno 检测 |
| 📋 播放列表支持与选择 | 🚀 下载限速 | ⚙️ 自定义参数支持 |
| 📑 视频列表集成 | ✂️ 视频剪辑 | 🍪 Cookie 登录集成 |
| 📜 下载历史记录 | 🔄 更新版本分支选择 | 🌐 代理支持 |
| 🎚️ 音频格式转换 | 🎬 视频格式设置 | 🆙 内置更新页签 |
| 🌍 通用模式 | 🔊 音频归一化 (EBU R128) | 🌍 支持 14 种语言 |
| 💾 播放列表导出 | ⚙️ 默认质量与字幕设置 | |
</div>

<a id="安装"></a>
## 🚀 安装

### ⚡ 快速安装 (推荐)

通过 PyPI 安装 YTSage：

```bash
pip install ytsage
```

<details>
<summary>🔄 更新现有安装</summary>

```bash
pip install --upgrade ytsage
```

</details>

然后通过以下命令运行：

```bash
ytsage
```

### 📦 独立可执行文件

> [👉 下载最新版本](https://github.com/oop7/YTSage/releases/latest)

#### 🪟 Windows

| 格式 | 说明 |
|--------|-------------|
| ![Windows EXE](https://img.shields.io/badge/Windows-EXE-0078D6?style=for-the-badge&logo=windows&logoColor=white) | 标准安装程序 |
| ![Windows FFmpeg](https://img.shields.io/badge/Windows-FFmpeg-0078D6?style=for-the-badge&logo=windows&logoColor=white) | 包含 FFmpeg 的安装程序 |
| ![Windows Portable](https://img.shields.io/badge/Windows-Portable-0078D6?style=for-the-badge&logo=windows&logoColor=white) | 便携版 (无需安装) |
| ![Windows Portable FFmpeg](https://img.shields.io/badge/Windows-Portable%20FFmpeg-0078D6?style=for-the-badge&logo=windows&logoColor=white) | 包含 FFmpeg 的便携版 (ZIP) |

<details>
<summary>🛠️ 安装步骤</summary>

1. **EXE 安装程序 (`.exe`)**: 双击并按照安装向导进行操作。
2. **便携版 (`.zip`)**: 解压到所需位置并运行 `ytsage.exe`。
3. **内置 FFmpeg**: 如果系统没有安装 FFmpeg，请选择带 `-ffmpeg` 的版本。
</details>

#### 🐧 Linux

| 格式 | 说明 |
|--------|-------------|
| ![Linux DEB](https://img.shields.io/badge/Linux-DEB-FCC624?style=for-the-badge&logo=linux&logoColor=black) | Debian 软件包 |
| ![Linux AppImage](https://img.shields.io/badge/Linux-AppImage-FCC624?style=for-the-badge&logo=linux&logoColor=black) | 便携 AppImage |
| ![Linux RPM](https://img.shields.io/badge/Linux-RPM-FCC624?style=for-the-badge&logo=linux&logoColor=black) | RPM 软件包 |
| ![Flathub](https://img.shields.io/badge/Linux-Flatpak-FCC624?style=for-the-badge&logo=flathub&logoColor=black) | Flatpak 软件包 |

<details>
<summary>🛠️ 安装步骤</summary>

- **DEB (`.deb`)**:
  ```bash
  sudo dpkg -i ytsage_*.deb
  sudo apt-get install -f # 如有依赖问题请运行
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
- **Flatpak**: 按照 Flathub 的说明或运行：
  ```bash
  flatpak install flathub io.github.oop7.ytsage
  ```
</details>

#### 🍎 macOS

| 格式 | 说明 |
|--------|-------------|
| ![macOS ARM64 APP](https://img.shields.io/badge/macOS-ARM64%20APP-000000?style=for-the-badge&logo=apple&logoColor=white) | Apple Silicon 专用 ZIP 压缩包 |
| ![macOS ARM64 DMG](https://img.shields.io/badge/macOS-ARM64%20DMG-000000?style=for-the-badge&logo=apple&logoColor=white) | Apple Silicon 专用 DMG 安装程序 |

<details>
<summary>🛠️ 安装步骤</summary>

- **DMG 安装程序 (`.dmg`)**: 双击挂载，然后将 `YTSage.app` 拖入 Applications 文件夹。
- **ZIP 应用包 (`.zip`)**: 解压并移动 `YTSage.app` 到 Applications 文件夹。

*注意：如果遇到“应用已损坏”的提示，请参阅下方的 macOS 解决办法。*
</details>

---

<details>
<summary>💻 从源码手动安装</summary>

### 1. 克隆仓库

```bash
git clone https://github.com/oop7/YTSage.git
cd YTSage
```

### 2. 安装依赖

#### ⚡ 使用 uv

```bash
uv pip install .
```

#### 📦 或使用标准 pip

```bash
pip install .
```

### 3. 运行程序

```bash
python -m ytsage.main
```

</details>

<a id="屏幕截图"></a>
## 📸 屏幕截图

<div align="center">
<table>
  <tr>
    <td><img src="../branding/screenshots/Download-Settings.png" alt="下载设置" width="400"/></td>
    <td><img src="../branding/screenshots/playlist.png" alt="播放列表下载" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><em>下载设置</em></td>
    <td align="center"><em>播放列表列表</em></td>
  </tr>
  <tr>
    <td><img src="../branding/screenshots/audio_format.png" alt="音频格式选择" width="400"/></td>
    <td><img src="../branding/screenshots/Custom-Option.png" alt="自定义选项" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><em>音频格式设置</em></td>
    <td align="center"><em>自定义选项</em></td>
  </tr>
</table>
</div>

<a id="使用说明"></a>
## 📖 使用说明

<details>
<summary>🎯 基本使用方法</summary>

1. **运行 YTSage**
2. **粘贴 YouTube 地址** (或点击 "Paste URL")
3. **点击 "Analyze" (分析)**
4. **选择下载模式:**
   - `Video` 下载视频
   - `Audio Only` 仅提取音频
5. **配置下载项:**
   - 启用字幕并选择语言
   - 启用字幕合并 (Merge)
   - 保存缩略图 (Save Thumbnail)
   - 启用赞助内容跳过 (SponsorBlock)
   - 下载描述文本 (Save Description)
   - 嵌入视频章节 (Embed Chapters)
6. **选择路径**
7. **点击 "Download" (下载)**

> 💡 默认下载到系统的“下载”文件夹。

</details>

<details>
<summary>📋 下载播放列表</summary>

1. **粘贴播放列表地址**
2. **添加并分析**
3. **在弹出窗口中选择视频 (默认全选)**
4. **设置质量方案**
5. **开始下载**

> 💡 程序会自动管理下载队列。您可以将列表导出为 `.txt`, `.csv`, `.m3u` 或 `.json` 格式。

</details>

<details>
<summary>🌍 非 YouTube 网站 (通用模式)</summary>

当您想从被 yt-dlp 支持的其他网站（如 TikTok、Dailymotion 等）下载时，请开启通用模式。

如何使用：

1. 打开 `Download Settings` (下载设置)。
2. 启用 `Generic Mode` (通用模式)。
3. 输入非 YouTube 的支持网站链接。
4. 点击 `Analyze` (分析)。
5. 正常下载。

说明：

- 通用模式仅关闭了 YTSage 内部的 URL 类型检查。网站支持程度仍取决于您安装的 yt-dlp。
- 有些站点可能需要特定的 Cookie 或代理配置。
- 如果某个网站无法分析，请先在内置更新程序中更新 yt-dlp。

</details>

<details>
<summary>🧰 媒体与下载选项</summary>

- **字幕选项:** 过滤特定语言并支持嵌入到视频中。
- **字幕合并:** 将字幕“烧录”到视频中（硬字幕）。
- **保存描述:** 将视频描述保存为独立的文本文档。
- **保存缩略图:** 下载视频的高清封面。
- **嵌入章节:** 允许将视频章节标记写入媒体元数据。
- **赞助商跳过:** 配合 SponsorBlock 自动跳过或剪辑掉广告段落。
- **视频剪裁:** 输入 `HH:MM:SS` 时间点来实现部分下载。

</details>

<details>
<summary>⚙️ 文件与输出设置</summary>

- **下载限速:** 输入如 `500K` 表示限制为 500 KB/s。
- **保存路径:** 在 **Download Settings → Download Path** 中保存您的默认位置。
- **默认分辨率:** 设置您首选的清晰度（如 1080p, 720p）。
- **默认字幕语言:** 输入语言代码（如 `zh,en`）来自动选择默认字幕。
- **文件命名模板:** 通过 `%(title)s` 等变量自定义文件名格式。
- **强制输出格式:** 强制转换输出容器，如 `mp4`, `webm` 或 `mkv`。
- **音频转换:** 将音频转换为 `AAC`, `MP3`, `FLAC` 等格式。
- **音量归一化:** 使用 EBU R128 标准使下载的音量均衡。
- **多线程连接:** 设置 **Concurrent Connections** 为 8-10 以最大化下载速度。

</details>

<details>
<summary>🌐 进阶访问与网络</summary>

- **Cookie 登录:** 允许通过 Cookie 下载私人内容或绕过限制。
  推荐方法：
  1. 在设置中点击 `Extract cookies from browser`，选择您的浏览器。
  2. 或：导出 Netscape 格式的 `cookies.txt` 文件并手动载入。
- **代理支持:** 支持设置 HTTP 代理，例如 `http://127.0.0.1:8080`。

</details>

<details>
<summary>🛠️ 系统工具与维护</summary>

- **自定义参数:** 为 yt-dlp 传递特定的命令行参数。
- **内置更新器:** (在 Custom Options 中)
  - **yt-dlp 更新:** 在稳定版和测试版之间切换。
  - **FFmpeg 检测:** 验证安装路劲。
  - **Deno 更新:** 维护相关的集成环境。
- **下载历史:** 管理您的所有下载历史记录，包含缩略图和状态。

</details>

<details>
<summary>🌍 语言支持</summary>

YTSage 支持 **14 种语言**。您可以在 **Custom Options → Language** 中更改。

### 支持的界面语言

| 语言 | 代码 | 语言 | 代码 |
|----------|------|----------|------|
| 🇺🇸 英语 | `en` | 🇪🇸 西班牙语 | `es` |
| 🇸🇦 阿拉伯语 | `ar` | 🇫🇷 法语 | `fr` |
| 🇩🇪 德语 | `de` | 🇮🇳 印地语 | `hi` |
| 🇮🇩 印尼语 | `id` | 🇮🇹 意大利语 | `it` |
| 🇯🇵 日语 | `ja` | 🇵🇱 波兰语 | `pl` |
| 🇧🇷 葡萄牙语 | `pt` | 🇷🇺 俄语 | `ru` |
| 🇹🇷 土耳其语 | `tr` | 🇨🇳 中文 | `zh` |

### README 翻译版

| 语言 | 文件 | 语言 | 文件 |
|----------|------|----------|------|
| 🇺🇸 英语 | [README.md](../README.md) | 🇪🇸 西班牙语 | [README.es.md](README.es.md) |
| 🇸🇦 阿拉伯语 | [README.ar.md](README.ar.md) | 🇫🇷 法语 | [README.fr.md](README.fr.md) |
| 🇩🇪 德语 | [README.de.md](README.de.md) | 🇮🇳 印地语 | [README.hi.md](README.hi.md) |
| 🇮🇩 印尼语 | [README.id.md](README.id.md) | 🇮🇹 意大利语 | [README.it.md](README.it.md) |
| 🇯🇵 日语 | [README.ja.md](README.ja.md) | 🇵🇱 波兰语 | [README.pl.md](README.pl.md) |
| 🇧🇷 葡萄牙语 | [README.pt.md](README.pt.md) | 🇷🇺 俄语 | [README.ru.md](README.ru.md) |
| 🇹🇷 土耳其语 | [README.tr.md](README.tr.md) | 🇨🇳 中文 | [README.zh.md](README.zh.md) |

> 💡 **想要贡献翻译?** 欢迎查看 [贡献指南](#贡献) 部分！

</details>

<a id="故障排除"></a>
## 🛠️ 故障排除

<details>
<summary>常见问题解答</summary>

- **没有显示格式表格:** 请更新 yt-dlp。如果仍无效，请尝试切换到测试版 (Nightly) 分支。
- **下载失败:** 请检查网络连接或该地区视频是否可用。
- **常见特定的错误提示:**
  - **私有视频:** 需提供 Cookie 登录。
  - **内容受限:** 部分视频需登录账号。
  - **地理锁定:** 需使用代理或 VPN。
  - **视频已删除:** 视频已不存在。
  - **直播内容:** YTSage 目前不支持实时直播下载，请等直播结束后再试。
- **下载后画面和声音分离:** 意味着系统中未安装或未检测到 FFmpeg。
  - **解决方法:** 确保 FFmpeg 已安装并加入 PATH，或下载带 `-ffmpeg` 版本的 Windows 程序。

---

#### 🛡️ Windows Defender / 杀毒软件警告

某些杀毒软件可能会误报。这是打包程序的常见现象。

**原因:**
- 启发式查杀可能会误认为打包的可执行文件是恶意软件。

**安全建议:**
- ✅ **通过 pip 安装:** `pip install ytsage`（推荐）
- ✅ **自行构建**: 参照 [CI_CD 指南](../.github/CI_CD_README.md)
- ✅ **添加排除项**。

#### 🍎 macOS: "应用已损坏，无法打开"
在 macOS Sonoma 及以后版本：

1. 打开 **终端 (Terminal)**。
2. 输入命令 (结尾有一个空格):
   ```bash
   xattr -d com.apple.quarantine 
   ```
3. 从 Finder 中将 **YTSage.app** 拖入终端窗口。
4. 按回车。
5. 再次打开应用。

---

#### **配置存放路径**
- **Windows:** `%LOCALAPPDATA%\YTSage`
- **macOS:** `~/Library/Application Support/YTSage`
- **Linux:** `~/.local/share/YTSage`

</details>

<a id="赞助支持"></a>
## 💖 赞助支持

如果 YTSage 节省了您的时间，请考虑资助本项目。赞助收入将用于多平台测试环境的维护和新功能开发。

- GitHub Sponsors: https://github.com/sponsors/oop7
- 您也可以通过应用内的“About (关于)”窗口找到捐赠链接。

[![赞助 YTSage](https://img.shields.io/badge/Sponsor-YTSage-EA4AAA?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sponsors/oop7)

<a id="贡献"></a>
## 👥 贡献

感谢所有帮助！

1. 🍴 Fork 仓库
2. 🌿 创建特性分支: `git checkout -b feature/NewFeature`
3. 💾 提交更改: `git commit -m 'Add NewFeature'`
4. 📤 推送分支: `git push origin feature/NewFeature`
5. 🔄 开启 Pull Request

### 🌍 翻译贡献

- 您可以更新各语种 README (例如 `readme-translations/README.zh.md`)。
- 也可以翻译界面词条：`ytsage/languages/<语言代码>.json`。

<details>
<summary>📂 项目结构</summary>

## YTSage - 项目结构

### 📁 目录概览

```
YTSage/
├── 📁 .github/                   # GitHub 设置
│   ├── 📁 ISSUE_TEMPLATE/         # 问题模板
│   ├─── 📁 workflows/              # GitHub Actions 流程
├──  📁 branding/                 # 品牌资源 (截图, SVG)
│   ├── 📁 icons/                 # 图标
│   ├── 📁 screenshots/           # 截图说明
│   └── 📁 svg/                   # SVG 素材
├── 📄 LICENSE                    # 许可证
├── 📄 pyproject.toml             # 项目元数据与依赖
├── 📄 README.md                  # 英语 README
├── 📄 requirements.txt           # 开发依赖
└── 📁 ytsage/                    # 源代码
    ├── 📁 assets/                # 运行时资源 (音频, 图标)
    ├── 📁 languages/             # 多语言 JSON 文件
    ├── 📁 core/                  # 下载与集成核心逻辑
    ├── 📁 gui/                   # UI 组件
    ├── 📁 utils/                 # 工具类
    ├── 📄 __init__.py            
    └── 📄 main.py                # 程序入口
```

</details>

## ⭐️ 关注趋势

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

## 📜 许可证

本项目基于 MIT 许可证分发 - 详情请参阅 [LICENSE](../LICENSE) 文件。

## 🙏 鸣谢

<details>
<summary>查看致谢名单</summary>

<div align="center">

<p>特别鸣谢所有通过反馈、建议或代码合并来完善此工具的贡献者。</p>

<table>
    <tr class="section"><th colspan="2">核心组件</th></tr>
    <tr>
        <td width="35%"><a href="https://github.com/yt-dlp/yt-dlp">yt-dlp</a></td>
        <td>核心下载引擎</td>
    </tr>
    <tr>
        <td><a href="https://ffmpeg.org/">FFmpeg</a></td>
        <td>媒体流处理</td>
    </tr>
    <tr>
        <td><a href="https://deno.com/">Deno</a></td>
        <td>集成运行环境</td>
    </tr>
    <tr class="section"><th colspan="2">库与框架</th></tr>
    <tr>
        <td><a href="https://wiki.qt.io/Qt_for_Python">PySide6</a></td>
        <td>GUI 框架</td>
    </tr>
    <tr>
        <td><a href="https://python-pillow.org/">Pillow</a></td>
        <td>图片处理</td>
    </tr>
    <tr>
        <td><a href="https://requests.readthedocs.io/">requests</a></td>
        <td>网络请求</td>
    </tr>
    <tr>
        <td><a href="https://packaging.python.org/">packaging</a></td>
        <td>版本管理</td>
    </tr>
    <tr>
        <td><a href="https://python-markdown.github.io/">markdown</a></td>
        <td>Markdown 渲染</td>
    </tr>
    <tr>
        <td><a href="https://github.com/Delgan/loguru">loguru</a></td>
        <td>日志记录</td>
    </tr>
    <tr class="section"><th colspan="2">内容与贡献</th></tr>
    <tr>
        <td><a href="https://pixabay.com/sound-effects/new-notification-09-352705/">Universfield 的通知音效</a></td>
        <td>通知声音</td>
    </tr>
    <tr>
        <td><a href="https://github.com/viru185">viru185</a></td>
        <td>代码贡献</td>
    </tr>
</table>

</div>

</details>

## ⚠️ 免责声明

本工具仅供个人学习与研究使用。请尊重 YouTube 服务条款及创作者版权。

---

<div align="center">
由 [oop7](https://github.com/oop7) 倾力协作 ❤️
</div>
