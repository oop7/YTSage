# YTSage CI/CD Workflow

This repository uses GitHub Actions to automatically build and release YTSage for multiple platforms when version tags are pushed.

## How It Works

### Trigger
The workflow is triggered when you push a git tag that starts with `v` (e.g., `v4.9.0`, `v4.9.1`).

### Build Process
1. **Setup**: Uses Python 3.13.6 on all platforms
2. **Builds**: Creates platform-specific executables using cx_Freeze
3. **Packages**: Generates native package formats for each platform
4. **Release**: Creates a draft GitHub release with all artifacts

## Usage

### Creating a Release

1. **Update version** in your source code if needed
2. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Release v4.9.0"
   ```

3. **Create and push a tag**:
   ```bash
   git tag v4.9.0
   git push origin v4.9.0
   ```

4. **Watch the action**: Go to Actions tab in GitHub to monitor progress

5. **Review draft release**: Once complete, check the Releases section for the draft

### Release Artifacts

The workflow creates the following files based on the platform:

#### Windows
- `YTSage-v{version}-portable.zip` - Standard portable version
- `YTSage-v{version}-ffmpeg-portable.zip` - FFmpeg bundle portable

#### Linux
- `YTSage-v{version}-{arch}.AppImage` - AppImage portable
- `YTSage-v{version}-{arch}.rpm` - RPM package
- `YTSage-v{version}-{arch}.deb` - Debian package

#### macOS
- `YTSage-v{version}-{arch}.app.zip` - Zipped application bundle
- `YTSage-v{version}-{arch}.dmg` - Disk image installer

## Workflow Features

### Multi-Platform Support
- **Windows**: Uses PowerShell scripts with cx_Freeze
- **Linux**: Uses Bash scripts with cx_Freeze, creates AppImage, RPM, and DEB
- **macOS**: Matrix build for both Intel (x64) and Apple Silicon (arm64)

### Automatic Version Detection
- Extracts version from git tag (removes 'v' prefix)
- Names all artifacts consistently across platforms

### Caching
- Python dependencies are cached to speed up builds
- Virtual environment is cached between runs

### Error Handling
- Comprehensive error checking at each step
- Detailed logging for troubleshooting
- Artifact verification before upload

### Security
- Uses official GitHub Actions
- No external dependencies
- Secure token handling

## Manual Intervention

### After Workflow Completion
1. **Review the draft release** in GitHub
2. **Test the artifacts** if needed
3. **Edit release notes** if desired
4. **Publish the release** when ready

### Troubleshooting
If the workflow fails:
1. Check the Actions logs for error details
2. Ensure all required files are present
3. Verify the tag format is correct (`v*`)
4. Check that dependencies are properly listed

## Configuration

### Modifying the Workflow
The workflow files are located in `.github/workflows/`:
- `build-windows.yml` - Windows builds
- `build-linux.yml` - Linux builds
- `build-macos.yml` - macOS builds

### Key Configuration Options
- `PYTHON_VERSION`: Python version (currently 3.13.6)
- Artifact naming patterns
- Release note templates
- Build optimization settings

### Adding New Build Types
To add new platform packages:
1. Create or modify workflow files in `.github/workflows/`
2. Target the appropriate OS runner (windows-latest, ubuntu-latest, macos-latest)
3. Use cx_Freeze or PyInstaller for packaging
4. Package the build output in platform-native formats
5. Upload the artifacts and include them in the release


## Notes

- All builds use cx_Freeze for packaging
- FFmpeg binaries are bundled where needed
- Screenshots are removed from builds to reduce size
- Draft releases allow for review before publication
- macOS builds run on both Intel and Apple Silicon runners

## Example Tag Commands

```bash
# For a new release
git tag v4.8.1
git push origin v4.8.1

# For a patch release
git tag v4.8.1
git push origin v4.8.1

# To delete a tag (if needed)
git tag -d v4.8.1
git push origin :refs/tags/v4.8.1
```
