param(
    [Parameter(Mandatory = $true)]
    [string]$DistDir
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $DistDir -PathType Container)) {
    throw "Build directory not found: $DistDir"
}

$libDir = Join-Path $DistDir "lib"

if (Test-Path "$libDir\assets\branding\screenshots") {
    Remove-Item "$libDir\assets\branding\screenshots" -Recurse -Force
    Write-Host "Removed screenshots folder"
}

Get-ChildItem -Path $DistDir -Recurse -Filter "*.pdb" | Remove-Item -Force
Write-Host "Removed PDB debug files"

if (Test-Path "$libDir\PySide6\translations") {
    Remove-Item "$libDir\PySide6\translations" -Recurse -Force
    Write-Host "Removed Qt translations"
}

$unusedPlugins = @(
    "designer", "pdf", "svg", "sql", "help", "qml", "quick",
    "webengine", "bluetooth", "opengl", "printsupport", "test", "xml"
)
foreach ($plugin in $unusedPlugins) {
    if (Test-Path "$libDir\PySide6\plugins\$plugin") {
        Remove-Item "$libDir\PySide6\plugins\$plugin" -Recurse -Force
        Write-Host "Removed unused plugin folder: $plugin"
    }
}

if (Test-Path "$libDir\PySide6\plugins\platforminputcontexts") {
    Remove-Item "$libDir\PySide6\plugins\platforminputcontexts" -Recurse -Force
    Write-Host "Removed plugin: platforminputcontexts"
}

foreach ($format in @("qpdf.dll", "qsvg.dll")) {
    $formatPath = "$libDir\PySide6\plugins\imageformats\$format"
    if (Test-Path $formatPath) {
        Remove-Item $formatPath -Force
        Write-Host "Removed plugin: $format"
    }
}

$svgIconPath = "$libDir\PySide6\plugins\iconengines\qsvgicon.dll"
if (Test-Path $svgIconPath) {
    Remove-Item $svgIconPath -Force
    Write-Host "Removed plugin: qsvgicon.dll"
}

$bloatDlls = @(
    "Qt6Web*", "Qt6Pdf*", "Qt6Qml*", "Qt6Quick*",
    "Qt6VirtualKeyboard*", "Qt6OpenGL*"
)
foreach ($pattern in $bloatDlls) {
    Get-ChildItem -Path $libDir -Filter $pattern -ErrorAction SilentlyContinue |
        Remove-Item -Force
    if (Test-Path "$libDir\PySide6") {
        Get-ChildItem -Path "$libDir\PySide6" -Filter $pattern -ErrorAction SilentlyContinue |
            Remove-Item -Force
    }
}
Write-Host "Removed unnecessary Qt DLLs"

$uselessFolders = @(
    "setuptools", "wheel", "pkg_resources", "_distutils_hack", "curses", "_pyrepl"
)
foreach ($folder in $uselessFolders) {
    $folderPath = "$libDir\$folder"
    if (Test-Path $folderPath) {
        Remove-Item $folderPath -Recurse -Force
        Write-Host "Removed unused module: $folder"
    }
}
