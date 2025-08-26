#Requires -Version 5.1

<#
.SYNOPSIS
    YTSage Universal Build Script - Creates MSI Installers and ZIP Distributions
.DESCRIPTION
    This PowerShell script builds YTSage using cx_Freeze and creates:
    - MSI installer packages
    - ZIP file distributions (portable)
    - Both standard and FFmpeg versions
.NOTES
    Version: Auto-detected from setup.py
    Location: build/windows/windows-build-universal.ps1
    Usage: Run from project root directory (build-env/)
    
    IMPORTANT: This script must be executed from the project root directory!
    Example: .\build\windows\windows-build-universal.ps1 -Verbose
#>

param(
    [switch]$SkipVenv,
    [switch]$Verbose,
    [switch]$FFmpeg,
    [switch]$MSIOnly,
    [switch]$ZIPOnly,
    [string]$OutputDir = "releases",
    [string]$FFmpegPath = "$env:LOCALAPPDATA\ffmpeg\ffmpeg-7.1.1-full_build\bin"
)

# Set error handling
$ErrorActionPreference = "Stop"

# Script configuration - Auto-detect version from setup.py
$APP_NAME = "YTSage"
$RELEASE_DATE = Get-Date -Format "yyyy-MM-dd"

# Auto-detect version from setup.py
function Get-VersionFromSetup {
    try {
        $setupContent = Get-Content "build\windows\setup.py" -Raw
        if ($setupContent -match 'version\s*=\s*["\']([^"\']+)["\']') {
            $version = $matches[1]
            Write-Host "Detected version: $version" -ForegroundColor Gray
            return $version
        } else {
            Write-Warning-Custom "Could not extract version from setup.py, using 1.0.0"
            return "1.0.0"
        }
    } catch {
        Write-Warning-Custom "Could not read setup.py, using 1.0.0"
        return "1.0.0"
    }
}

$SCRIPT_VERSION = Get-VersionFromSetup

# Determine build type
$BUILD_TYPE = if ($FFmpeg) { "FFmpeg" } else { "Standard" }
$SETUP_FILE = if ($FFmpeg) { "build\windows\setup-ffmpeg.py" } else { "build\windows\setup.py" }
$OUTPUT_NAME_BASE = if ($FFmpeg) { "$APP_NAME-v$SCRIPT_VERSION-ffmpeg" } else { "$APP_NAME-v$SCRIPT_VERSION" }

# Banner
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "YTSage Universal Build Script v$SCRIPT_VERSION" -ForegroundColor Cyan
Write-Host "Build Type: $BUILD_TYPE" -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This script will create:" -ForegroundColor Yellow
if (-not $ZIPOnly) {
    Write-Host "- MSI installer package" -ForegroundColor White
}
if (-not $MSIOnly) {
    Write-Host "- ZIP portable distribution" -ForegroundColor White
}
Write-Host "- Professional packaging with metadata" -ForegroundColor White
Write-Host ""

function Write-Step {
    param($Message)
    Write-Host "[STEP] $Message" -ForegroundColor Green
}

function Write-Error-Custom {
    param($Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Write-Warning-Custom {
    param($Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Test-Command {
    param($Command)
    try {
        & $Command --version | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

function Test-FFmpegBinaries {
    if (-not $FFmpeg) { return $null }
    
    Write-Step "Checking FFmpeg binaries..."
    
    $ffmpegExe = Join-Path $FFmpegPath "ffmpeg.exe"
    $ffprobeExe = Join-Path $FFmpegPath "ffprobe.exe" 
    $ffplayExe = Join-Path $FFmpegPath "ffplay.exe"
    
    $missingFiles = @()
    
    if (-not (Test-Path $ffmpegExe)) { $missingFiles += "ffmpeg.exe" }
    if (-not (Test-Path $ffprobeExe)) { $missingFiles += "ffprobe.exe" }
    if (-not (Test-Path $ffplayExe)) { $missingFiles += "ffplay.exe" }
    
    if ($missingFiles.Count -gt 0) {
        Write-Error-Custom "Missing FFmpeg binaries: $($missingFiles -join ', ')"
        Write-Host "Expected FFmpeg path: $FFmpegPath" -ForegroundColor Yellow
        throw "FFmpeg binaries not found"
    }
    
    Write-Host "✓ Found all FFmpeg binaries" -ForegroundColor Green
    return @{
        ffmpeg = $ffmpegExe
        ffprobe = $ffprobeExe
        ffplay = $ffplayExe
    }
}

function New-VirtualEnvironment {
    Write-Step "Creating virtual environment..."
    try {
        python -m venv venv
        Write-Host "Virtual environment created successfully." -ForegroundColor Green
    }
    catch {
        Write-Error-Custom "Failed to create virtual environment: $($_.Exception.Message)"
        throw
    }
}

function Start-VirtualEnvironment {
    Write-Step "Activating virtual environment..."
    
    $venvScript = ".\venv\Scripts\Activate.ps1"
    if (-not (Test-Path $venvScript)) {
        Write-Error-Custom "Virtual environment activation script not found at: $venvScript"
        throw "Virtual environment not properly created"
    }
    
    try {
        & $venvScript
        Write-Host "Virtual environment activated successfully." -ForegroundColor Green
    }
    catch {
        Write-Error-Custom "Failed to activate virtual environment: $($_.Exception.Message)"
        throw
    }
}

function Install-Dependencies {
    Write-Step "Installing/Upgrading required packages..."
    
    try {
        Write-Host "Upgrading pip..." -ForegroundColor White
        python -m pip install --upgrade pip | Out-Null
        
        Write-Host "Installing requirements..." -ForegroundColor White
        pip install --no-cache-dir -r requirements.txt | Out-Null
        
        Write-Host "Installing cx_Freeze..." -ForegroundColor White
        pip install --no-cache-dir cx_Freeze | Out-Null
        
        Write-Host "Installing yt-dlp (temporary for build)..." -ForegroundColor White
        pip install --no-cache-dir yt-dlp | Out-Null
        
        Write-Host "All packages installed successfully." -ForegroundColor Green
    }
    catch {
        Write-Error-Custom "Failed to install required packages: $($_.Exception.Message)"
        throw
    }
}

function Remove-BuildArtifacts {
    Write-Step "Cleaning previous build artifacts..."
    
    $itemsToRemove = @("build", "dist", $OutputDir)
    
    foreach ($item in $itemsToRemove) {
        if (Test-Path $item) {
            Remove-Item $item -Recurse -Force
            Write-Host "Removed: $item" -ForegroundColor Gray
        }
    }
    
    Write-Host "Build artifacts cleaned." -ForegroundColor Green
}

function Build-Executable {
    param($FFmpegBinaries)
    
    Write-Step "Building executable with cx_Freeze..."
    
    try {
        if ($FFmpegBinaries) {
            $env:FFMPEG_PATH = $FFmpegBinaries.ffmpeg | Split-Path
        }
        
        # Build the executable
        python $SETUP_FILE build
        
        if ($LASTEXITCODE -ne 0) {
            throw "cx_Freeze build failed with exit code $LASTEXITCODE"
        }
        
        Write-Host "Executable built successfully." -ForegroundColor Green
    }
    catch {
        Write-Error-Custom "Failed to build executable: $($_.Exception.Message)"
        throw
    }
}

function Build-MSI {
    Write-Step "Creating MSI installer..."
    
    try {
        # Build MSI package
        python $SETUP_FILE bdist_msi
        
        if ($LASTEXITCODE -ne 0) {
            throw "MSI build failed with exit code $LASTEXITCODE"
        }
        
        Write-Host "MSI installer created successfully." -ForegroundColor Green
    }
    catch {
        Write-Error-Custom "Failed to build MSI: $($_.Exception.Message)"
        throw
    }
}

function New-ZIPDistribution {
    Write-Step "Creating ZIP distribution..."
    
    try {
        # Ensure output directory exists
        if (-not (Test-Path $OutputDir)) {
            New-Item -ItemType Directory -Path $OutputDir | Out-Null
        }
        
        # Find the built executable directory
        $executableDir = if ($FFmpeg) { "dist\YTSage-FFmpeg" } else { "dist\YTSage" }
        
        if (-not (Test-Path $executableDir)) {
            throw "Executable directory not found: $executableDir"
        }
        
        # Create ZIP file
        $zipPath = Join-Path $OutputDir "$OUTPUT_NAME_BASE.zip"
        Compress-Archive -Path "$executableDir\*" -DestinationPath $zipPath -Force
        
        Write-Host "ZIP distribution created: $zipPath" -ForegroundColor Green
        
        # Get ZIP file size
        $zipSize = (Get-Item $zipPath).Length
        $zipSizeMB = [math]::Round($zipSize / 1MB, 2)
        Write-Host "ZIP size: $zipSizeMB MB" -ForegroundColor Gray
        
    }
    catch {
        Write-Error-Custom "Failed to create ZIP distribution: $($_.Exception.Message)"
        throw
    }
}

function Move-MSIFiles {
    Write-Step "Organizing MSI files..."
    
    try {
        # Ensure output directory exists
        if (-not (Test-Path $OutputDir)) {
            New-Item -ItemType Directory -Path $OutputDir | Out-Null
        }
        
        # Find and move MSI files
        $msiFiles = Get-ChildItem -Path "dist" -Filter "*.msi" -Recurse
        
        foreach ($msiFile in $msiFiles) {
            $newName = "$OUTPUT_NAME_BASE.msi"
            $destination = Join-Path $OutputDir $newName
            
            Move-Item $msiFile.FullName $destination -Force
            Write-Host "MSI installer moved to: $destination" -ForegroundColor Green
            
            # Get MSI file size
            $msiSize = (Get-Item $destination).Length
            $msiSizeMB = [math]::Round($msiSize / 1MB, 2)
            Write-Host "MSI size: $msiSizeMB MB" -ForegroundColor Gray
        }
    }
    catch {
        Write-Error-Custom "Failed to organize MSI files: $($_.Exception.Message)"
        throw
    }
}

function New-ReleaseNotes {
    Write-Step "Creating release notes..."
    
    $releaseNotes = @"
# YTSage v$SCRIPT_VERSION Release

**Release Date:** $RELEASE_DATE  
**Build Type:** $BUILD_TYPE

## Installation Options

### MSI Installer (Recommended)
- **File:** $OUTPUT_NAME_BASE.msi
- **Installation:** Double-click to install system-wide
- **Updates:** Automatic update notifications
- **Uninstall:** Via Windows Programs & Features

### Portable ZIP
- **File:** $OUTPUT_NAME_BASE.zip
- **Installation:** Extract and run - no installation required
- **Updates:** Manual download and replacement
- **Uninstall:** Simply delete the folder

## System Requirements
- Windows 10/11 (64-bit)
- .NET Framework 4.7.2 or later
- Internet connection for yt-dlp updates

## Support
For issues or questions, please visit the project repository.

---
*Built with cx_Freeze v$(pip show cx_Freeze | Select-String "Version" | ForEach-Object { ($_ -split ":")[1].Trim() })*
"@

    try {
        $releaseNotesPath = Join-Path $OutputDir "RELEASE_NOTES.md"
        $releaseNotes | Out-File -FilePath $releaseNotesPath -Encoding UTF8
        Write-Host "Release notes created: $releaseNotesPath" -ForegroundColor Green
    }
    catch {
        Write-Warning-Custom "Failed to create release notes: $($_.Exception.Message)"
    }
}

function Remove-PostBuildArtifacts {
    Write-Step "Cleaning up post-build artifacts..."
    
    try {
        if (Test-Path "build") {
            Remove-Item "build" -Recurse -Force
            Write-Host "Removed build folder." -ForegroundColor Gray
        }
        
        Write-Host "Post-build cleanup completed." -ForegroundColor Green
    }
    catch {
        Write-Warning-Custom "Some cleanup operations failed: $($_.Exception.Message)"
    }
}

function Stop-VirtualEnvironment {
    try {
        deactivate
        Write-Host "Virtual environment deactivated." -ForegroundColor Green
    }
    catch {
        Write-Warning-Custom "Failed to deactivate virtual environment (this might be normal)"
    }
}

function Show-BuildSummary {
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host "Build completed successfully!" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Build Type: $BUILD_TYPE" -ForegroundColor Yellow
    Write-Host "Version: $SCRIPT_VERSION" -ForegroundColor Yellow
    Write-Host "Output Directory: $OutputDir" -ForegroundColor Yellow
    Write-Host ""
    
    if (Test-Path $OutputDir) {
        Write-Host "Created files:" -ForegroundColor Green
        Get-ChildItem $OutputDir | ForEach-Object {
            $size = if ($_.PSIsContainer) { "Folder" } else { "$([math]::Round($_.Length / 1MB, 2)) MB" }
            Write-Host "  ✓ $($_.Name) ($size)" -ForegroundColor White
        }
    }
    
    Write-Host ""
    Write-Host "Distribution ready for release!" -ForegroundColor Green
    Write-Host ""
}

# Main execution
try {
    # Validation
    Write-Step "Checking prerequisites..."
    
    if (-not (Test-Command "python")) {
        Write-Error-Custom "Python is not installed or not in PATH"
        exit 1
    }
    
    if (-not (Test-Path $SETUP_FILE)) {
        Write-Error-Custom "Setup file not found: $SETUP_FILE"
        exit 1
    }
    
    $pythonVersion = python --version
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
    
    # Check for Python 3.13 MSI limitation
    $pythonVersionInfo = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
    $isPython313 = $pythonVersionInfo -eq "3.13"
    
    if ($isPython313 -and -not $ZIPOnly) {
        Write-Warning-Custom "Python 3.13 detected. MSI building is not supported yet by cx_Freeze."
        Write-Host "See: https://github.com/marcelotduarte/cx_Freeze/issues/2837" -ForegroundColor Yellow
        Write-Host "Switching to ZIP-only mode. Use Python 3.12 for MSI support." -ForegroundColor Yellow
        $ZIPOnly = $true
        $MSIOnly = $false
    }
    
    # Check FFmpeg if needed
    $ffmpegBinaries = Test-FFmpegBinaries
    
    # Virtual environment
    if (-not $SkipVenv) {
        if (-not (Test-Path "venv")) {
            New-VirtualEnvironment
        } else {
            Write-Step "Using existing virtual environment..."
        }
        Start-VirtualEnvironment
    }
    
    # Build process
    Install-Dependencies
    Remove-BuildArtifacts
    Build-Executable -FFmpegBinaries $ffmpegBinaries
    
    # Create distributions
    if (-not $ZIPOnly) {
        Build-MSI
        Move-MSIFiles
    }
    
    if (-not $MSIOnly) {
        New-ZIPDistribution
    }
    
    New-ReleaseNotes
    Remove-PostBuildArtifacts
    Show-BuildSummary
}
catch {
    Write-Error-Custom "Build failed: $($_.Exception.Message)"
    if ($Verbose) {
        Write-Host $_.Exception.StackTrace -ForegroundColor Red
    }
    exit 1
}
finally {
    if (-not $SkipVenv) {
        Stop-VirtualEnvironment
    }
}

Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
