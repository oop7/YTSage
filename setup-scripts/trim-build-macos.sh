#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <app-path>" >&2
    exit 2
fi

app_path="$1"
if [ ! -d "$app_path" ]; then
    echo "App bundle not found: $app_path" >&2
    exit 1
fi

contents_dir="$app_path/Contents"
lib_dirs=()
while IFS= read -r -d '' lib_dir; do
    lib_dirs+=("$lib_dir")
done < <(find "$contents_dir" -type d -name "lib" -print0)
if [ "${#lib_dirs[@]}" -eq 0 ]; then
    echo "No library directory found in app bundle: $app_path" >&2
    exit 1
fi

trimmed_lib=false
for lib_dir in "${lib_dirs[@]}"; do
    if [ ! -d "$lib_dir/asyncio" ] &&
       [ ! -d "$lib_dir/PySide6" ] &&
       [ ! -d "$lib_dir/ytsage" ]; then
        continue
    fi

    trimmed_lib=true
    echo "Cleaning library directory: $lib_dir"

    rm -rf "$lib_dir/assets/branding/screenshots"

    while IFS= read -r -d '' translations_dir; do
        rm -rf "$translations_dir"
    done < <(find "$lib_dir" -type d \( \
        -path "*/PySide6/*/translations" -o \
        -path "*/PySide6/translations" \
    \) -print0)

    plugins_path=""
    if [ -d "$lib_dir/PySide6/plugins" ]; then
        plugins_path="$lib_dir/PySide6/plugins"
    elif [ -d "$lib_dir/PySide6/Qt/plugins" ]; then
        plugins_path="$lib_dir/PySide6/Qt/plugins"
    fi

    if [ -n "$plugins_path" ]; then
        echo "Cleaning Qt plugins: $plugins_path"
        for plugin in designer pdf svg sql help qml quick webengine bluetooth opengl printsupport test xml; do
            rm -rf "$plugins_path/$plugin"
        done
        find "$plugins_path" -type f -name "libqpdf.*" -delete
    fi

    for bloat in \
        QtQml QtQmlMeta QtQmlModels QtQmlWorkerScript \
        QtQuick QtQuickControls2 QtQuickTemplates2 \
        QtWebEngine QtWebEngineCore QtVirtualKeyboard QtVirtualKeyboardQml \
        QtOpenGL QtOpenGLWidgets QtPdf QtPdfWidgets; do
        find "$lib_dir" -maxdepth 2 -type f \( \
            -name "$bloat" -o \
            -name "${bloat}.*" -o \
            -name "*$bloat*" \
        \) -delete
    done

    for tool in setuptools wheel pkg_resources _distutils_hack curses _pyrepl; do
        rm -rf "$lib_dir/$tool"
    done
done

if [ "$trimmed_lib" != true ]; then
    echo "No Python library directory found in app bundle: $app_path" >&2
    exit 1
fi

echo "Trim complete. Remaining library directories:"
printf '%s\n' "${lib_dirs[@]}"
