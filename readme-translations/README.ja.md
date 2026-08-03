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

**クリーンなPySide6インターフェースを備えたモダンなYouTubeダウンローダー。**  
あらゆる品質でのビデオダウンロード、オーディオ抽出、字幕取得などが可能です。

### 🌍 README 言語

英語: [EN](../README.md)
| アラビア語: [AR](README.ar.md)
| ドイツ語: [DE](README.de.md)
| スペイン語: [ES](README.es.md)
| フランス語: [FR](README.fr.md)
| ヒンディー語: [HI](README.hi.md)
| インドネシア語: [ID](README.id.md)
| イタリア語: [IT](README.it.md)
| 日本語: [JA](README.ja.md)
| ポーランド語: [PL](README.pl.md)
| ポルトガル語: [PT](README.pt.md)
| ロシア語: [RU](README.ru.md)
| トルコ語: [TR](README.tr.md)
| 中国語: [ZH](README.zh.md)

<p align="center">
  <a href="#インストール">インストール</a> •
  <a href="#機能">機能</a> •
  <a href="#使い方">使い方</a> •
  <a href="#スクリーンショット">スクリーンショット</a> •
  <a href="#トラブルシューティング">トラブルシューティング</a> •
  <a href="#スポンサー">スポンサー</a> •
  <a href="#貢献">貢献</a>
</p>

</div>

---

<a id="なぜytsageなのか"></a>
## ❓ なぜ YTSage なのか?

YTSageは、**シンプルでありながら強力なYouTubeダウンローダー**を求めるユーザーのために設計されています。他のツールとは異なり、以下の機能を提供します：

- モダンでクリーンなPySide6インターフェース
- ビデオ、オーディオ、字幕のワンクリックダウンロード
- SponsorBlock、字幕結合、プレイリスト選択などの高度な機能
- yt-dlpがサポートするYouTube以外のサイト向けのオプションのジェネリックモード
- クロスプラットフォーム対応と簡単なインストール

<a id="機能"></a>
## ✨ 機能

<div align="center">

| 基本機能 | 高度な機能 | 追加機能 |
|-----------------------------------|-----------------------------------------|------------------------------------|
| 🎥 フォーマットテーブル | 🚫 SponsorBlock統合 | 🎞️ FPS/HDR表示 |
| 🎵 オーディオ抽出 | 📝 字幕選択と結合 | 🔄 yt-dlp自動更新 |
| ✨ シンプルなユーザーインターフェース | 💾 説明とサムネイルの保存 | 🛠️ FFmpeg/yt-dlp/Deno検出 |
| 📋 プレイリストのサポートと選択 | 🚀 速度制限 | ⚙️ カスタムコマンド |
| 📑 チャプター統合 | ✂️ ビデオセクションのトリミング | 🍪 クッキーログイン |
| 📜 ダウンロード履歴 | 🔄 リリースチャネルの選択 | 🌐 プロキシサポート |
| 🎚️ オーディオフォーマット変換 | 🎬 ビデオフォーマット設定 | 🆙 統合アップデートタブ |
| 🌍 ジェネリックモード | 🔊 オーディオノーマライズ (EBU R128) | 🌍 14言語へのローカライズ |
| 💾 プレイリストのエクスポート | ⚙️ デフォルトの品質と字幕 | |
</div>

<a id="インストール"></a>
## 🚀 インストール

### ⚡ クイックインストール (推奨)

PyPI経由でYTSageをインストールします：

```bash
pip install ytsage
```

<details>
<summary>🔄 既存のインストールを更新する</summary>

```bash
pip install --upgrade ytsage
```

</details>

その後、アプリケーションを実行します：

```bash
ytsage
```

### 📦 ビルド済み実行ファイル (Executable)

> [👉 最新リリースをダウンロード](https://github.com/oop7/YTSage/releases/latest)

#### 🪟 Windows

| フォーマット | 説明 |
|--------|-------------|
| ![Windows EXE](https://img.shields.io/badge/Windows-EXE-0078D6?style=for-the-badge&logo=windows&logoColor=white) | 標準インストーラー |
| ![Windows FFmpeg](https://img.shields.io/badge/Windows-FFmpeg-0078D6?style=for-the-badge&logo=windows&logoColor=white) | FFmpeg同梱 |
| ![Windows Portable](https://img.shields.io/badge/Windows-Portable-0078D6?style=for-the-badge&logo=windows&logoColor=white) | ポータブル版、インストール不要 |
| ![Windows Portable FFmpeg](https://img.shields.io/badge/Windows-Portable%20FFmpeg-0078D6?style=for-the-badge&logo=windows&logoColor=white) | FFmpeg同梱、ポータブル版 (ZIP縮小) |

<details>
<summary>🛠️ インストール手順</summary>

1. **EXE インストーラー (`.exe`)**: ファイルをダブルクリックし、セットアップウィザードに従います。
2. **ポータブル版 (`.zip`)**: アーカイブを任意の場所に展開し、`ytsage.exe` を実行します。
3. **内蔵 FFmpeg**: システムに FFmpeg がインストールされていない場合は、FFmpeg 同梱版を選択してください。
</details>

#### 🐧 Linux

| フォーマット | 説明 |
|--------|-------------|
| ![Linux DEB](https://img.shields.io/badge/Linux-DEB-FCC624?style=for-the-badge&logo=linux&logoColor=black) | Debian パッケージ |
| ![Linux AppImage](https://img.shields.io/badge/Linux-AppImage-FCC624?style=for-the-badge&logo=linux&logoColor=black) | AppImage、ポータブル |
| ![Linux RPM](https://img.shields.io/badge/Linux-RPM-FCC624?style=for-the-badge&logo=linux&logoColor=black) | RPM パッケージ |
| ![Flathub](https://img.shields.io/badge/Linux-Flatpak-FCC624?style=for-the-badge&logo=flathub&logoColor=black) | Flatpak バンドル |

<details>
<summary>🛠️ インストール手順</summary>

- **DEB (`.deb`)**:
  ```bash
  sudo dpkg -i ytsage_*.deb
  sudo apt-get install -f # 必要に応じて不足している依存関係を修正
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
- **Flatpak**: Flathub の指示に従うか、以下を実行します：
  ```bash
  flatpak install flathub io.github.oop7.ytsage
  ```
</details>

#### 🍎 macOS

| フォーマット | 説明 |
|--------|-------------|
| ![macOS ARM64 APP](https://img.shields.io/badge/macOS-ARM64%20APP-000000?style=for-the-badge&logo=apple&logoColor=white) | Apple Silicon 用 ZIP アプリ |
| ![macOS ARM64 DMG](https://img.shields.io/badge/macOS-ARM64%20DMG-000000?style=for-the-badge&logo=apple&logoColor=white) | Apple Silicon 用ディスクイメージインストーラー |

<details>
<summary>🛠️ インストール手順</summary>

- **DMG インストーラー (`.dmg`)**: ダブルクリックしてマウントし、`YTSage.app` をアプリケーションフォルダにドラッグします。
- **App アーカイブ (`.zip`)**: ZIP を展開し、`YTSage.app` をアプリケーションフォルダに移動します。

*注意: 「アプリが破損しています」というエラーが表示される場合は、以下の macOS トラブルシューティング セクションを参照してください。*
</details>

---

<details>
<summary>💻 ソースからの手動インストール</summary>

### 1. リポジトリをクローンする

```bash
git clone https://github.com/oop7/YTSage.git
cd YTSage
```

### 2. 依存関係をインストールする

#### ⚡ uv を使用する場合

```bash
uv pip install .
```

#### 📦 または標準の pip を使用する場合

```bash
pip install .
```

### 3. アプリケーションを実行する

```bash
python -m ytsage.main
```

</details>

<a id="スクリーンショット"></a>
## 📸 スクリーンショット

<div align="center">
<table>
  <tr>
    <td><img src="../branding/screenshots/Download-Settings.png" alt="ダウンロード設定" width="400"/></td>
    <td><img src="../branding/screenshots/playlist.png" alt="プレイリストダウンロード" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><em>ダウンロード設定</em></td>
    <td align="center"><em>プレイリストダウンロード</em></td>
  </tr>
  <tr>
    <td><img src="../branding/screenshots/audio_format.png" alt="オーディオフォーマット選択" width="400"/></td>
    <td><img src="../branding/screenshots/Custom-Option.png" alt="カスタムオプション" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><em>オーディオフォーマット</em></td>
    <td align="center"><em>カスタムオプション</em></td>
  </tr>
</table>
</div>

<a id="使い方"></a>
## 📖 使い方

<details>
<summary>🎯 基本的な使い方</summary>

1. **YTSage を起動する**
2. **YouTube の URL を貼り付ける** (または「URL を貼り付け」ボタンを使用)
3. **「分析」をクリックする**
4. **フォーマットを選択する：**
   - ビデオダウンロードの場合は `Video`
   - オーディオ抽出の場合は `Audio Only`
5. **オプションを選択する：**
   - 字幕を有効にして言語を選択
   - 字幕結合を有効化
   - サムネイルを保存
   - スポンサーセクションを削除
   - 説明を保存
   - チャプターを埋め込む
6. **出力ディレクトリを選択する**
7. **「ダウンロード」をクリックする**

> 💡 デフォルトのダウンロードディレクトリは、ユーザーの「ダウンロード」フォルダです。

</details>

<details>
<summary>📋 プレイリストのダウンロード</summary>

1. **プレイリストの URL を貼り付ける**
2. **「分析」をクリックする**
3. **プレイリストセレクターからビデオを選択する (任意、デフォルトはすべて)**
4. **希望のフォーマット/品質を選択する**
5. **「ダウンロード」をクリックする**

> 💡 アプリケーションはダウンロードキューを自動的に管理し、プレイリストのエントリを `.txt`, `.csv`, `.m3u`, または `.json` ファイルとしてエクスポートできます。

</details>

<details>
<summary>🌍 YouTube 以外のサイト向けのジェネリックモード</summary>

Dailymotion、CBC Gem、TikTok など、yt-dlp がサポートするサイトからの URL を YTSage に受け入れさせたい場合は、ジェネリックモードを使用します。

使用方法：

1. `Download Settings` を開きます。
2. `Generic Mode` を有効にします。
3. YouTube 以外のサポートされているビデオまたはプレイリストの URL を貼り付けます。
4. `Analyze` をクリックします。
5. フォーマットを選択し、通常通りダウンロードします。

注意：

- ジェネリックモードは、YTSage 内部の URL バリデーションのみを変更します。対象サイトは、インストールされている yt-dlp バージョンでサポートされている必要があります。
- サイトによっては、エクストラクターに応じてクッキー、ログイン、プロキシ、または追加の yt-dlp 引数が必要になる場合があります。
- サイトが失敗する場合は、問題を報告する前に統合アップデートタブから yt-dlp を更新してください。

</details>

<details>
<summary>🧰 メディアとダウンロードのオプション</summary>

- **字幕オプション:** 言語をフィルタリングし、字幕をビデオファイルに埋め込みます。
- **字幕結合:** 字幕をビデオファイルにマージして、焼き付け字幕（ハードコード）にします。
- **説明の保存:** ビデオの説明をテキストファイルとして保存します。
- **サムネイルの保存:** ビデオのサムネイルを画像ファイルとして保存します。
- **チャプターの埋め込み:** 対応しているビデオプレーヤー用に、チャプターマーカーをメタデータとして含めます。
- **スポンサーセクションを削除:** SponsorBlock を使用して、ビデオからスポンサーセグメントを削除します。
- **ビデオのトリミング:** `HH:MM:SS` 形式で時間範囲を指定して、ビデオの特定のセクションのみをダウンロードします。

</details>

<details>
<summary>⚙️ 出力とファイルの設定</summary>

- **速度制限:** ダウンロード速度を制限します（例：500 KB/s の場合は `500K`）。
- **ダウンロードパスの保存:** 将来のダウンロードのためにデフォルトのダウンロードパスを保存します。**Download Settings → Download Path** で設定可能です。
- **デフォルトのビデオ解像度:** 自動選択のために好みのビデオ解像度を設定します（例：1080p, 720p）。**Download Settings → Default Video Resolution** で設定可能です。
- **デフォルトの字幕言語:** 自動選択のためにデフォルトの字幕言語を設定します（カンマ区切り、例：`ja,en`）。**Download Settings → Default Subtitle Languages** で設定可能です。
- **ファイル名形式:** `%(title)s`, `%(uploader)s`, `%(playlist_index)s`, `%(resolution)s` などの変数を使用して出力ファイル名の形式をカスタマイズします。**Download Settings → Filename Format** で設定可能です。
- **出力形式の強制:** ビデオダウンロードを `mp4`, `webm`, `mkv` などの特定のコンテナ形式に強制します。**Download Settings → Output Format Settings** で設定可能です。
- **オーディオ形式の変換:** オーディオのみのダウンロードを `AAC`, `MP3`, `FLAC`, `WAV`, `Opus`, `M4A`, `Vorbis`, または `Best` などの好みの形式に変換します。**Download Settings → Audio Format Settings** で設定可能です。
- **オーディオノーマライズ:** EBU R128 を使用して、オーディオのみのダウンロードの音量を標準化します。
- **同時接続数:** ファイルを複数のパーツで同時にダウンロードすることで、ダウンロード速度を大幅に向上させます。**Download Settings → General → Concurrent Connections** で設定可能です（デフォルトは 1。IP ブロックを避けるため最大 8-10 を推奨）。

</details>

<details>
<summary>🌐 アクセスとネットワーク</summary>

- **クッキーログイン:** クッキーを使用して YouTube にログインし、非公開コンテンツにアクセスします。
  使用方法：
  1. **推奨:** アプリ内蔵の `Extract cookies from browser` オプションを使用し、ブラウザと（必要に応じて）プロフィールを選択します。
  2. あるいは、クッキーを手動で抽出します：
     a. [cookie-editor](https://github.com/moustachauve/cookie-editor?tab=readme-ov-file) などの拡張機能を使用して、ブラウザからクッキーをエクスポートします。
     b. Netscape 形式でクッキーをコピーします。
     c. `cookies.txt` という名前のファイルを作成し、クッキーを貼り付けます。
     d. アプリで `cookies.txt` ファイルを選択します。
- **プロキシサポート:** ダウンロードにプロキシサーバーを使用します（例：`http://<proxy-server>:<port>`）。
- **ジェネリックモード:** YTSage が yt-dlp でサポートされている YouTube 以外のサイトから分析およびダウンロードできるようにします。**Download Settings → Generic Mode** から有効にします。

</details>

<details>
<summary>🛠️ ツールとメンテナンス</summary>

- **カスタムコマンド:** コマンドライン引数を介して高度な yt-dlp 機能にアクセスします。
- **アップデートタブ:** カスタムオプション内の一箇所で内蔵のアップデートツールを管理します：
  - **yt-dlp アップデート:** アップデートを確認し、Stable と Nightly リリースチャネルを切り替えます。
  - **FFmpeg バージョンチェッカー:** FFmpeg のバージョンを確認し、インストールガイドを開きます。
  - **Deno アップデート:** Deno ランタイムを確認し、アップデートします。
- **FFmpeg/yt-dlp/Deno 検出:** About ダイアログから FFmpeg、yt-dlp、Deno のパスとバージョンを自動的に検出します。
- **ダウンロード履歴:** **History** ボタンから、サムネイルとステータス付きで過去のダウンロードを表示します。

</details>

<details>
<summary>🌍 ローカライズ</summary>

YTSage はグローバルに対応するため、**14 言語**をサポートしています。**Custom Options → Language** で好みの言語を選択してください。

### サポートされている言語

| 言語 | コード | 言語 | コード |
|----------|------|----------|------|
| 🇺🇸 英語 | `en` | 🇪🇸 スペイン語 | `es` |
| 🇸🇦 アラビア語 | `ar` | 🇫🇷 フランス語 | `fr` |
| 🇩🇪 ドイツ語 | `de` | 🇮🇳 ヒンディー語 | `hi` |
| 🇮🇩 インドネシア語 | `id` | 🇮🇹 イタリア語 | `it` |
| 🇯🇵 日本語 | `ja` | 🇵🇱 ポーランド語 | `pl` |
| 🇧🇷 ポルトガル語 | `pt` | 🇷🇺 ロシア語 | `ru` |
| 🇹🇷 トルコ語 | `tr` | 🇨🇳 中国語 | `zh` |

### README 翻訳

| 言語 | ファイル | 言語 | ファイル |
|----------|------|----------|------|
| 🇺🇸 英語 | [README.md](../README.md) | 🇪🇸 スペイン語 | [README.es.md](README.es.md) |
| 🇸🇦 アラビア語 | [README.ar.md](README.ar.md) | 🇫🇷 フランス語 | [README.fr.md](README.fr.md) |
| 🇩🇪 ドイツ語 | [README.de.md](README.de.md) | 🇮🇳 ヒンディー語 | [README.hi.md](README.hi.md) |
| 🇮🇩 インドネシア語 | [README.id.md](README.id.md) | 🇮🇹 イタリア語 | [README.it.md](README.it.md) |
| 🇯🇵 日本語 | [README.ja.md](README.ja.md) | 🇵🇱 ポーランド語 | [README.pl.md](README.pl.md) |
| 🇧🇷 ポルトガル語 | [README.pt.md](README.pt.md) | 🇷🇺 ロシア語 | [README.ru.md](README.ru.md) |
| 🇹🇷 トルコ語 | [README.tr.md](README.tr.md) | 🇨🇳 中国語 | [README.zh.md](README.zh.md) |

> 💡 **翻訳を手伝いたいですか？** [貢献](#貢献) セクションを参照して、さらに多くの言語を追加するのを手伝ってください！

</details>

<a id="トラブルシューティング"></a>
## 🛠️ トラブルシューティング

<details>
<summary>クリックして一般的な問題と解決策を表示</summary>

- **フォーマットテーブルが表示されない:** yt-dlp を最新バージョンに更新し、yt-dlp Nightly への切り替えを試してください。
- **ダウンロードが失敗する:** インターネット接続を確認し、ビデオが利用可能であることを確認してください。
- **特定のダウンロードエラー：**
  - **非公開ビデオ:** 非公開コンテンツにアクセスするには、クッキー認証を使用してください。
  - **年齢制限のあるコンテンツ:** YouTube アカウントにログインして、年齢制限のあるビデオを表示してください。
  - **ジオブロックされたビデオ:** 地域制限を回避するために VPN の使用を検討してください。
  - **削除されたビデオ:** ビデオは YouTube で利用できなくなっています。
  - **ライブストリーム:** ライブストリームは放送中にダウンロードできません。ストリームが終了するまで待ってください。
  - **ネットワークエラー:** インターネット接続を確認して再試行してください。
  - **無効な URL:** URL が正しく、サポートされているプラットフォームのものであることを確認してください。
  - **プレミアムコンテンツ:** YouTube Premium のサブスクリプションが必要です。
  - **著作権ブロック:** 著作権制限のため、コンテンツがブロックされています。
- **ダウンロード後にビデオとオーディオファイルが分かれている:** これは FFmpeg が不足しているか、検出されない場合に発生します。YTSage は、高品質のビデオとオーディオストリームを結合するために FFmpeg を必要とします。
  - **解決策:** FFmpeg がインストールされており、システムの PATH でアクセス可能であることを確認してください。Windows ユーザーにとって最も簡単なオプションは、FFmpeg が同梱されている `YTSage-v<version>-ffmpeg.exe` ファイルをダウンロードすることです。

---

#### 🛡️ Windows Defender / アンチウイルス警告

一部のアンチウイルスソフトウェアは、`.exe` ファイルを誤検知（False Positive）としてフラグを立てる場合があります。これは、パッケージ化されたアプリケーションの**既知の制限**です。

**なぜ発生するのか：**
- アンチウイルスのヒューリスティック機能が、パッケージ化された実行ファイルを疑わしいものとして誤認することがあります。

**安全な選択肢：**
- ✅ **pip インストールを使用する:** `pip install ytsage` (推奨)
- ✅ **ソースからビルドする**: この[ガイド](../.github/CI_CD_README.md)に従ってください。
- ✅ **アプリケーションをホワイトリストに追加する** (アンチウイルスソフトウェアの設定)。

#### 🍎 macOS: 「アプリが破損しているため開けません」
macOS Sonoma 以降でこのエラーが表示される場合は、 quarantine（隔離）属性を削除する必要があります。

1.  **ターミナルを開きます** (Spotlight で検索できます)。
2.  **次のコマンドを入力します** が、まだ Enter は押さないでください。最後にスペースを含めるようにしてください：
    ```bash
    xattr -d com.apple.quarantine 
    ```
3.  **Finder ウィンドウから `YTSage.app` ファイルをドラッグし**、ターミナルウィンドウに直接ドロップします。これにより、正しいファイルパスが自動的に貼り付けられます。
4.  **Enter を押して** コマンドを実行します。
5.  **YTSage.app を再度開いてみてください。** 正しく起動するはずです。

---

#### **設定ファイルの場所 (上級者向け)**
- **Windows:** `%LOCALAPPDATA%\YTSage`
- **macOS:** `~/Library/Application Support/YTSage`
- **Linux:** `~/.local/share/YTSage`

</details>

<a id="スポンサー"></a>
## 💖 スポンサー

YTSage があなたの時間を節約できたなら、プロジェクトのスポンサーになることを検討してください。スポンサーシップは、開発時間、全プラットフォームでのテスト、および将来の改善に役立てられます。

- GitHub Sponsors: https://github.com/sponsors/oop7
- スポンサーリンクは、アプリ内の About ダイアログから直接利用可能です。

[![Sponsor YTSage](https://img.shields.io/badge/Sponsor-YTSage-EA4AAA?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sponsors/oop7)

<a id="貢献"></a>
## 👥 貢献

貢献を歓迎します！以下のように手助けができます：

1. 🍴 リポジトリをフォークする
2. 🌿 フィーチャーブランチを作成する：
  ```bash
  git checkout -b feature/AmazingFeature
  ```
3. 💾 変更をコミットする：
  ```bash
  git commit -m 'Add some AmazingFeature'
  ```
4. 📤 ブランチにプッシュする：
  ```bash
  git push origin feature/AmazingFeature
  ```
5. 🔄 プルリクエストを作成する

### 🌍 翻訳に貢献する

- 関連するローカライズ版 README ファイルを更新する (例: `readme-translations/README.ja.md`)
- `ytsage/languages/<code>.json` を編集して、アプリの文字列を同期させる
- お使いの言語がない場合は、 `README.md` をベースに `README.<code>.md` を作成してください。

<details>
<summary>📂 プロジェクト構造</summary>

## YTSage - プロジェクト構造

このドキュメントでは、YTSage の整理されたフォルダ構造について説明します。

### 📁 プロジェクト構造

```
YTSage/
├── 📁 .github/                   # GitHub 設定
│   ├── 📁 ISSUE_TEMPLATE/         # イシューテンプレート
│   │   └── 🐛-bug-report.md       # バグレポートテンプレート
│   ├─── 📁 workflows/              # GitHub Actions ワークフロー
│   │   ├── build-linux.yml        # Linux ビルドワークフロー
│   │   ├── build-macos.yml        # macOS ビルドワークフロー
│   │   │── build-windows.yml      # Windows ビルドワークフロー
|   |   └── release-all.yml          # マスターリリースワークフロー
│   └── 📄 CI_CD_README.md        # CI/CD ドキュメント
├──  📁 branding/                 # ブランディングアセット (スクリーンショット, SVG)
│   ├── 📁 icons/                 # アプリアイコン
│   ├── 📁 screenshots/           # ドキュメント用スクリーンショット
│   └── 📁 svg/                   # SVG アセット
├── 📄 LICENSE                    # ライセンスファイル
├── 📄 pyproject.toml             # プロジェクトメタデータと依存関係
├── 📄 README.md                  # プロジェクトドキュメント
├── 📄 requirements.txt           # Python 依存関係 (dev)
└── 📁 ytsage/                    # ソースコードパッケージ
    ├── 📁 assets/                # ランタイムアセット
    │   ├── 📁 Icon/              # アプリアイコン
    │   └── 📁 sound/             # オーディオファイル
    ├── 📁 languages/             # ローカライズファイル
    │   ├── 📄 ar.json            # アラビア語翻訳
    │   ├── 📄 de.json            # ドイツ語翻訳
    │   ├── 📄 en.json            # 英語翻訳
    │   └── ...                   # その他の言語
    ├── 📁 core/                  # コアビジネスロジック
    │   ├── 📄 __init__.py        
    │   ├── 📄 ytsage_deno.py     # Deno 統合
    │   ├── 📄 ytsage_downloader.py # ダウンロード機能
    │   ├── 📄 ytsage_ffmpeg.py   # FFmpeg 統合
    │   ├── 📄 ytsage_utils.py    # ユーティリティ関数
    │   └── 📄 ytsage_yt_dlp.py   # yt-dlp 統合
    ├── 📁 gui/                   # ユーザーインターフェースコンポーネント
    │   ├── 📄 __init__.py        
    │   ├── 📄 ytsage_gui_main.py # アプリメインウィンドウ
    │   └── 📁 ytsage_gui_dialogs/ # ダイアログクラス
    ├── 📁 utils/                 # ユーティリティモジュール
    │   ├── 📄 __init__.py        
    │   ├── 📄 ytsage_config_manager.py # 設定管理
    │   └── 📄 ytsage_logger.py   # ロギングツール
    ├── 📄 __init__.py            # パッケージエントリポイント
    └── 📄 main.py                # メイン実行スクリプト
```

</details>

## ⭐️ スター履歴

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

## 📜 ライセンス

このプロジェクトは MIT ライセンスの下でライセンスされています。詳細は [LICENSE](../LICENSE) ファイルを参照してください。

## 🙏 謝辞

<details>
<summary>謝辞を表示</summary>

<div align="center">

<p>改善の提案やバグの報告のためにイシューを開いてこのプロジェクトに貢献してくださったすべての方々に感謝いたします。</p>

<table>
    <tr class="section"><th colspan="2">主要コンポーネント</th></tr>
    <tr>
        <td width="35%"><a href="https://github.com/yt-dlp/yt-dlp">yt-dlp</a></td>
        <td>ダウンロードエンジン</td>
    </tr>
    <tr>
        <td><a href="https://ffmpeg.org/">FFmpeg</a></td>
        <td>メディア処理</td>
    </tr>
    <tr>
        <td><a href="https://deno.com/">Deno</a></td>
        <td>yt-dlp 統合用ランタイム</td>
    </tr>
    <tr class="section"><th colspan="2">ライブラリとフレームワーク</th></tr>
    <tr>
        <td><a href="https://wiki.qt.io/Qt_for_Python">PySide6</a></td>
        <td>GUI フレームワーク</td>
    </tr>
    <tr>
        <td><a href="https://python-pillow.org/">Pillow</a></td>
        <td>画像処理</td>
    </tr>
    <tr>
        <td><a href="https://requests.readthedocs.io/">requests</a></td>
        <td>HTTP リクエスト</td>
    </tr>
    <tr>
        <td><a href="https://packaging.python.org/">packaging</a></td>
        <td>バージョン管理とパッケージ化</td>
    </tr>
    <tr>
        <td><a href="https://python-markdown.github.io/">markdown</a></td>
        <td>Markdown レンダリング</td>
    </tr>
    <tr>
        <td><a href="https://github.com/Delgan/loguru">loguru</a></td>
        <td>ロギング</td>
    </tr>
    <tr class="section"><th colspan="2">アセットと貢献者</th></tr>
    <tr>
        <td><a href="https://pixabay.com/sound-effects/new-notification-09-352705/">New Notification 09 by Universfield</a></td>
        <td>通知音</td>
    </tr>
    <tr>
        <td><a href="https://github.com/viru185">viru185</a></td>
        <td>コード貢献者</td>
    </tr>
</table>

</div>

</details>

## ⚠️ 免責事項

このツールは個人利用のみを目的としています。YouTube の利用規約およびコンテンツ制作者の権利を尊重してください。

---

<div align="center">

Created with ❤️ by [oop7](https://github.com/oop7)

</div>
