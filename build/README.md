# YTSage Build System

This directory contains all build-related files and configurations for creating YTSage distributions.

## 🏗️ Build Architecture

### Automated Builds (CI/CD)
- **GitHub Actions**: Fully automated releases triggered by git tags
- **Location**: `.github/workflows/build-windows.yml`
- **Triggers**: Version tags (e.g., `v4.8.0`, `v4.9.1`)
- **Output**: MSI installers + ZIP portable versions (Standard & FFmpeg)

### Local Development Builds
- **Script**: `build/windows/windows-build-universal.ps1`
- **Purpose**: Local testing and development
- **Flexibility**: Manual control over build options

## 📁 Directory Structure

```
build/
├── windows/
│   ├── setup.py                      # Standard cx_Freeze configuration
│   ├── setup-ffmpeg.py               # FFmpeg bundle cx_Freeze configuration
│   ├── windows-build-universal.ps1   # Local development build script
│   └── README.md                     # This file
└── (future platforms)
```

## 🚀 Quick Start

### For Releases (Recommended)
```bash
# Create and push a version tag
git tag v4.8.1
git push origin v4.8.1

# GitHub Actions will automatically:
# 1. Build both versions
# 2. Create MSI installers
# 3. Create ZIP portable versions
# 4. Generate draft release with artifacts
```

### For Local Development
```powershell
# Navigate to project root
cd c:\path\to\YTSage\build-env

# Run the universal build script
.\build\windows\windows-build-universal.ps1 -Verbose

# Build only FFmpeg version
.\build\windows\windows-build-universal.ps1 -FFmpeg -Verbose

# Build only MSI (no ZIP)
.\build\windows\windows-build-universal.ps1 -MSIOnly

# Build only ZIP (no MSI)
.\build\windows\windows-build-universal.ps1 -ZIPOnly
```

## 📋 Build Configurations

### Standard Version (`setup.py`)
- **Target**: General users
- **Size**: Smaller download
- **FFmpeg**: Downloaded automatically when needed

### FFmpeg Bundle (`setup-ffmpeg.py`)
- **Target**: Users without internet or restricted environments
- **Size**: Larger download (~100MB+)
- **FFmpeg**: Included in installer

## 🔧 Build Script Options

### windows-build-universal.ps1 Parameters
```powershell
-SkipVenv          # Skip virtual environment creation
-Verbose           # Enable detailed output
-FFmpeg            # Build FFmpeg bundle version
-MSIOnly           # Create only MSI installer
-ZIPOnly           # Create only ZIP distribution
-OutputDir         # Custom output directory (default: "releases")
-FFmpegPath        # Custom FFmpeg binaries path
```

### Examples
```powershell
# Full build with verbose output
.\build\windows\windows-build-universal.ps1 -Verbose

# Quick standard version build
.\build\windows\windows-build-universal.ps1 -MSIOnly

# FFmpeg version to custom directory
.\build\windows\windows-build-universal.ps1 -FFmpeg -OutputDir "custom-builds"
```

## 📦 Output Artifacts

### CI/CD Builds (GitHub Actions)
```
releases/
├── YTSage-v4.8.1.msi              # Standard installer
├── YTSage-v4.8.1.zip              # Standard portable
├── YTSage-v4.8.1-ffmpeg.msi       # FFmpeg installer
└── YTSage-v4.8.1-ffmpeg.zip       # FFmpeg portable
```

### Local Builds
```
releases/
├── YTSage-4.8.1.msi               # Standard installer
├── YTSage-4.8.1.zip               # Standard portable
├── YTSage-4.8.1-ffmpeg.msi        # FFmpeg installer (if built)
└── YTSage-4.8.1-ffmpeg.zip        # FFmpeg portable (if built)
```

## 🛠️ Build Requirements

### System Requirements
- **OS**: Windows 10/11
- **PowerShell**: 5.1 or later
- **Python**: 3.12+ (3.12.10 recommended for MSI compatibility)
- **Memory**: 4GB+ RAM recommended
- **Storage**: 2GB+ free space

### Python Dependencies
- **cx_Freeze**: 6.x for MSI creation
- **playsound3**: Audio notification system
- **All project dependencies**: Listed in `requirements.txt`

### Optional Components
- **FFmpeg**: For bundled builds (auto-downloaded if not present)
- **Code Signing**: Certificate for signed installers (optional)

## 🔍 Troubleshooting

### Common Issues

#### Build Fails with Import Errors
```powershell
# Recreate virtual environment
Remove-Item venv -Recurse -Force
.\build\windows\windows-build-universal.ps1 -Verbose
```

#### MSI Creation Fails
- Ensure Python 3.12.x (required for MSI compatibility)
- Check cx_Freeze version (should be 6.x)
- Verify all dependencies are installed

#### FFmpeg Not Found
```powershell
# Specify custom FFmpeg path
.\build\windows\windows-build-universal.ps1 -FFmpeg -FFmpegPath "C:\ffmpeg\bin"
```

#### CI/CD Build Fails
- Check GitHub Actions logs
- Verify tag format (`v*`)
- Ensure all required files are present
- Check file paths in workflow

### Debug Mode
```powershell
# Enable maximum verbosity
.\build\windows\windows-build-universal.ps1 -Verbose -Debug
```

## 📈 Version Management

### Automatic Version Detection
- **CI/CD**: Extracts version from git tag
- **Local**: Uses version from setup.py files
- **Format**: Semantic versioning (e.g., 4.8.1)

### Manual Version Update
```powershell
# Update version in setup files
(Get-Content build\windows\setup.py) -replace 'version="[^"]*"', 'version="4.8.2"' | Set-Content build\windows\setup.py
(Get-Content build\windows\setup-ffmpeg.py) -replace 'version="[^"]*"', 'version="4.8.2"' | Set-Content build\windows\setup-ffmpeg.py
```

## 🔮 Future Enhancements

### Planned Features
- **Linux builds**: Future cross-platform support
- **macOS builds**: Apple platform support
- **Auto-updater**: Built-in update mechanism
- **Digital signing**: Code signing for Windows

### Contributing
- Build improvements welcome
- Cross-platform configurations
- Performance optimizations
- Documentation enhancements

## 📚 Related Documentation

- **CI/CD Guide**: `.github/CI_CD_README.md`
- **Project README**: `../README.md`
- **Release Notes**: GitHub Releases
- **Issue Tracking**: GitHub Issues

---

**Last Updated**: August 2025  
**Build System Version**: 4.8.x  
**Supported Platforms**: Windows (primary)  
