# YTSage CI/CD Workflow

This repository uses GitHub Actions to automatically build and release YTSage for multiple platforms. The workflow is designed to be manually triggered, allowing for flexibility in building specific versions or platforms on demand.

## How It Works

### Trigger
The workflows are triggered manually via the GitHub Actions "Workflow Dispatch" interface. This allows you to specify the version number explicitly (e.g., `1.0.0`) at runtime.

### Workflows
- **Create All Releases** (`release-all.yml`): The master workflow. Triggering this will automatically run the Windows, Linux, and macOS builds in parallel with the version you provide.
- **Platform Specific**: You can also trigger `Build Windows Release`, `Build Linux Release`, or `Build macOS Release` individually if you only need updates for one OS.

### Build Process
1. **Setup**: Uses Python 3.13 on all platforms
2. **Builds**: Creates platform-specific executables using cx_Freeze
3. **Packages**: Generates native package formats for each platform
4. **Release**: Creates or updates a draft GitHub release with the artifacts

## Usage

### Creating a Full Release (Recommended)

1. Go to the **Actions** tab in the GitHub repository.
2. Select **"Create All Releases"** from the left sidebar.
3. Click **Run workflow**.
4. Enter the **Version name** (e.g., `1.0.0`).
   > *Note: Do not include the 'v' prefix in the input field unless you want your filenames to be `v1.0.0`.*
5. Click the green **Run workflow** button.
6. The system will trigger the Windows, Linux, and macOS jobs. Once complete, a draft release will be available in the Releases section.

### Creating a Single Platform Build

1. Go to the **Actions** tab.
2. Select the specific workflow (e.g., **"Build Windows Release"**).
3. Click **Run workflow** and enter the version.
4. Only that specific platform's artifacts will be built and added to the release.

### Release Artifacts

The workflow creates the following files based on the platform:

#### Windows
- `YTSage-v{version}-portable.zip` - Standard portable version
- `YTSage-v{version}-ffmpeg-portable.zip` - FFmpeg bundle portable

#### Linux
- `YTSage-v{version}-{arch}.AppImage` - AppImage portable (x86_64, aarch64)
- `YTSage-v{version}-{arch}.rpm` - RPM package
- `YTSage-v{version}-{arch}.deb` - Debian package

#### macOS
- `YTSage-v{version}-{arch}.app.zip` - Zipped application bundle (x64, arm64)
- `YTSage-v{version}-{arch}.dmg` - Disk image installer

## Workflow Features

### Multi-Platform Support
- **Windows**: Uses PowerShell scripts with cx_Freeze
- **Linux**: Uses Bash scripts with cx_Freeze, creates AppImage, RPM, and DEB
- **macOS**: Matrix build for both Intel (x64) and Apple Silicon (arm64)

### Manual Versioning
- Version is strictly controlled by the input you provide at runtime.
- No longer dependent on git tags, reducing accidental releases.

### Caching
- Python dependencies and virtual environments are cached to speed up builds.

### Error Handling
- Comprehensive error checking at each step.
- Artifact verification before upload.

### Security
- Uses official GitHub Actions.
- Secure token handling via `secrets: inherit` for the master workflow.

## Manual Intervention

### After Workflow Completion
1. **Review the draft release** in GitHub.
2. **Test the artifacts** if needed.
3. **Edit release notes** to add changelogs or descriptions.
4. **Publish the release** when ready (change from Draft to Published).

## Configuration

### Modifying the Workflow
The workflow files are located in `.github/workflows/`:
- `release-all.yml` - Master workflow that orchestrates the others
- `build-windows.yml` - Windows builds logic
- `build-linux.yml` - Linux builds logic
- `build-macos.yml` - macOS builds logic

### Key Configuration Options
- `PYTHON_VERSION`: Python version (currently 3.13)
- `version` input: Defined as a required string in all workflows.

## Notes

- All builds use cx_Freeze for packaging.
- FFmpeg binaries are bundled where needed (Windows).
- Screenshots are removed from builds to reduce size.
- Draft releases allow for review before publication.
