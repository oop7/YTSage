# YTSage CI/CD Workflow

This repository uses GitHub Actions to automatically build and release YTSage for Windows when version tags are pushed.

## How It Works

### Trigger
The workflow is triggered when you push a git tag that starts with `v` (e.g., `v4.8.0`, `v4.9.1`).

### Build Process
1. **Setup**: Uses Python 3.12.10 on Windows
2. **Builds**: Creates both Standard and FFmpeg versions
3. **Packages**: Generates MSI installers and ZIP portable versions
4. **Release**: Creates a draft GitHub release with all artifacts

## Usage

### Creating a Release

1. **Update version** in your source code if needed
2. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Release v4.8.0"
   ```

3. **Create and push a tag**:
   ```bash
   git tag v4.8.0
   git push origin v4.8.0
   ```

4. **Watch the action**: Go to Actions tab in GitHub to monitor progress

5. **Review draft release**: Once complete, check the Releases section for the draft

### Release Artifacts

The workflow creates the following files:

- `YTSage-v<version>.msi` - Standard Windows installer
- `YTSage-v<version>.zip` - Standard portable version
- `YTSage-v<version>-ffmpeg.msi` - FFmpeg bundle installer
- `YTSage-v<version>-ffmpeg.zip` - FFmpeg bundle portable

### Release Notes

Automatic release notes are generated including:
- Download links and descriptions
- Installation instructions
- System requirements
- Feature highlights

## Workflow Features

### Automatic Version Detection
- Extracts version from git tag (removes 'v' prefix)
- Updates setup.py files with correct version
- Names all artifacts consistently

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
The workflow file is located at `.github/workflows/build-windows.yml`.

Key configuration options:
- `PYTHON_VERSION`: Python version to use
- Artifact naming patterns
- Release note templates

### Adding New Build Types
To add new build configurations:
1. Create new setup-*.py files
2. Add build steps to the workflow
3. Update artifact collection logic


## Notes

- The workflow only runs on Windows
- Requires Python 3.12.10 for MSI compatibility
- All builds use cx_Freeze for packaging
- FFmpeg binaries are expected in standard locations
- Draft releases allow for review before publication

## Example Tag Commands

```bash
# For a new release
git tag v4.8.0
git push origin v4.8.0

# For a patch release
git tag v4.8.1
git push origin v4.8.1

# To delete a tag (if needed)
git tag -d v4.8.0
git push origin :refs/tags/v4.8.0
```
