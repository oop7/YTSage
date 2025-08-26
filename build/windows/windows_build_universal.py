#!/usr/bin/env python3
"""
YTSage Universal Build Script - Python Version
Creates MSI Installers and ZIP Distributions

This Python script builds YTSage using cx_Freeze and creates:
- MSI installer packages  
- ZIP file distributions (portable)
- Both standard and FFmpeg versions

Usage: python windows_build_universal.py [options]
Example: python windows_build_universal.py --verbose --ffmpeg
"""

import os
import sys
import subprocess
import shutil
import argparse
import zipfile
import re
from pathlib import Path
from datetime import datetime
import json

class YTSageBuildScript:
    def __init__(self, args):
        self.args = args
        self.app_name = "YTSage"
        self.release_date = datetime.now().strftime("%Y-%m-%d")
        self.script_version = self.get_version_from_setup()
        self.build_type = "FFmpeg" if args.ffmpeg else "Standard"
        self.setup_file = "build/windows/setup-ffmpeg.py" if args.ffmpeg else "build/windows/setup.py"
        self.output_dir = Path(args.output_dir)
        self.output_name_base = f"{self.app_name}-v{self.script_version}" + ("-ffmpeg" if args.ffmpeg else "")
        
    def get_version_from_setup(self):
        """Extract version from setup.py file"""
        try:
            setup_path = Path("build/windows/setup.py")
            if not setup_path.exists():
                self.print_warning("Setup file not found, using 1.0.0")
                return "1.0.0"
                
            content = setup_path.read_text(encoding='utf-8')
            match = re.search(r'version="([^"]*)"', content)
            if match:
                version = match.group(1)
                self.print_info(f"Detected version: {version}")
                return version
            else:
                self.print_warning("Could not extract version from setup.py, using 1.0.0")
                return "1.0.0"
        except Exception as e:
            self.print_warning(f"Could not read setup.py: {e}, using 1.0.0")
            return "1.0.0"
    
    def print_step(self, message):
        """Print step message"""
        print(f"[STEP] {message}")
    
    def print_info(self, message):
        """Print info message"""
        print(f"[INFO] {message}")
    
    def print_success(self, message):
        """Print success message"""
        print(f"[SUCCESS] {message}")
    
    def print_warning(self, message):
        """Print warning message"""
        print(f"[WARNING] {message}")
    
    def print_error(self, message):
        """Print error message"""
        print(f"[ERROR] {message}")
    
    def run_command(self, cmd, check=True, shell=True):
        """Run a command and return the result"""
        if self.args.verbose:
            self.print_info(f"Running: {cmd}")
        
        try:
            result = subprocess.run(cmd, shell=shell, check=check, 
                                  capture_output=True, text=True)
            if self.args.verbose and result.stdout:
                print(result.stdout)
            return result
        except subprocess.CalledProcessError as e:
            self.print_error(f"Command failed: {cmd}")
            if e.stdout:
                print(f"STDOUT: {e.stdout}")
            if e.stderr:
                print(f"STDERR: {e.stderr}")
            raise
    
    def test_command(self, cmd):
        """Test if a command exists"""
        try:
            subprocess.run(cmd, shell=True, check=True, 
                          capture_output=True, text=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def check_prerequisites(self):
        """Check system prerequisites"""
        self.print_step("Checking prerequisites...")
        
        # Check Python
        if not self.test_command("python --version"):
            raise Exception("Python is not installed or not in PATH")
        
        # Check setup file
        if not Path(self.setup_file).exists():
            raise Exception(f"Setup file not found: {self.setup_file}")
        
        # Get Python version
        result = self.run_command("python --version")
        self.print_success(f"Found: {result.stdout.strip()}")
        
        # Check for Python 3.13 MSI limitation
        version_result = self.run_command('python -c "import sys; print(f\'{sys.version_info.major}.{sys.version_info.minor}\')"')
        python_version = version_result.stdout.strip()
        
        if python_version == "3.13" and not self.args.zip_only:
            self.print_warning("Python 3.13 detected. MSI building is not supported yet by cx_Freeze.")
            self.print_info("See: https://github.com/marcelotduarte/cx_Freeze/issues/2837")
            self.print_info("Switching to ZIP-only mode. Use Python 3.12 for MSI support.")
            self.args.zip_only = True
            self.args.msi_only = False
    
    def setup_virtual_environment(self):
        """Set up and activate virtual environment"""
        if self.args.skip_venv:
            return
            
        if not Path("venv").exists():
            self.print_step("Creating virtual environment...")
            self.run_command("python -m venv venv")
        else:
            self.print_step("Using existing virtual environment...")
        
        self.print_step("Activating virtual environment...")
        # Note: We'll use venv/Scripts/python.exe directly instead of activation
    
    def get_python_exe(self):
        """Get the Python executable path (venv or system)"""
        if self.args.skip_venv:
            return "python"
        else:
            venv_python = Path("venv/Scripts/python.exe")
            if venv_python.exists():
                return str(venv_python)
            else:
                return "python"
    
    def install_dependencies(self):
        """Install Python dependencies"""
        self.print_step("Installing dependencies...")
        python_exe = self.get_python_exe()
        
        # Upgrade pip
        self.run_command(f'"{python_exe}" -m pip install --upgrade pip')
        
        # Install requirements
        if Path("requirements.txt").exists():
            self.run_command(f'"{python_exe}" -m pip install --no-cache-dir -r requirements.txt')
        
        # Install build dependencies
        self.run_command(f'"{python_exe}" -m pip install --no-cache-dir cx_Freeze')
        self.run_command(f'"{python_exe}" -m pip install --no-cache-dir yt-dlp')
        
        self.print_success("Dependencies installed successfully")
    
    def remove_build_artifacts(self):
        """Remove existing build artifacts"""
        self.print_step("Cleaning build artifacts...")
        
        for path in ["build", "dist"]:
            if Path(path).exists():
                shutil.rmtree(path)
                if self.args.verbose:
                    self.print_info(f"Removed {path} directory")
        
        self.print_success("Build artifacts cleaned")
    
    def build_executable(self):
        """Build executable using cx_Freeze"""
        self.print_step("Building executable...")
        python_exe = self.get_python_exe()
        
        try:
            self.run_command(f'"{python_exe}" {self.setup_file} build')
            self.print_success("Executable built successfully")
        except subprocess.CalledProcessError:
            raise Exception("Failed to build executable")
    
    def build_msi(self):
        """Build MSI installer"""
        if self.args.zip_only:
            return
            
        self.print_step("Building MSI installer...")
        python_exe = self.get_python_exe()
        
        try:
            self.run_command(f'"{python_exe}" {self.setup_file} bdist_msi')
            self.print_success("MSI installer built successfully")
        except subprocess.CalledProcessError:
            raise Exception("Failed to build MSI installer")
    
    def create_zip_distribution(self):
        """Create ZIP distribution"""
        if self.args.msi_only:
            return
            
        self.print_step("Creating ZIP distribution...")
        
        # Find the built executable directory
        build_dirs = list(Path("build").glob("exe.*"))
        if not build_dirs:
            raise Exception("No executable build directory found")
        
        exe_dir = build_dirs[0]
        zip_name = f"{self.output_name_base}.zip"
        zip_path = self.output_dir / zip_name
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create ZIP file
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in exe_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(exe_dir)
                    zipf.write(file_path, arcname)
        
        # Get file size
        zip_size_mb = zip_path.stat().st_size / (1024 * 1024)
        self.print_success(f"ZIP created: {zip_path}")
        self.print_info(f"ZIP size: {zip_size_mb:.2f} MB")
    
    def move_msi_files(self):
        """Move MSI files to output directory"""
        if self.args.zip_only:
            return
            
        self.print_step("Organizing MSI files...")
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Find and move MSI files
        msi_files = list(Path("dist").glob("*.msi"))
        
        for msi_file in msi_files:
            new_name = f"{self.output_name_base}.msi"
            destination = self.output_dir / new_name
            
            shutil.move(str(msi_file), str(destination))
            
            # Get file size
            msi_size_mb = destination.stat().st_size / (1024 * 1024)
            self.print_success(f"MSI moved to: {destination}")
            self.print_info(f"MSI size: {msi_size_mb:.2f} MB")
    
    def create_release_notes(self):
        """Create release notes"""
        self.print_step("Creating release notes...")
        
        release_notes = f"""# YTSage v{self.script_version} Release

**Release Date:** {self.release_date}
**Build Type:** {self.build_type}

## Installation Options

### MSI Installer (Recommended)
- **File:** {self.output_name_base}.msi
- **Installation:** Double-click to install system-wide
- **Updates:** Automatic update notifications  
- **Uninstall:** Via Windows Programs and Features

### Portable ZIP
- **File:** {self.output_name_base}.zip
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
*Built with cx_Freeze*
"""
        
        try:
            release_notes_path = self.output_dir / "RELEASE_NOTES.md"
            release_notes_path.write_text(release_notes, encoding='utf-8')
            self.print_success(f"Release notes created: {release_notes_path}")
        except Exception as e:
            self.print_warning(f"Failed to create release notes: {e}")
    
    def cleanup_post_build(self):
        """Clean up post-build artifacts"""
        self.print_step("Cleaning up post-build artifacts...")
        
        try:
            if Path("build").exists():
                shutil.rmtree("build")
                self.print_info("Removed build folder")
            
            self.print_success("Post-build cleanup completed")
        except Exception as e:
            self.print_warning(f"Some cleanup operations failed: {e}")
    
    def show_build_summary(self):
        """Show build summary"""
        print("\n" + "="*50)
        print("Build completed successfully!")
        print("="*50)
        print(f"Build Type: {self.build_type}")
        print(f"Version: {self.script_version}")
        print(f"Output Directory: {self.output_dir}")
        print()
        
        if self.output_dir.exists():
            print("Created files:")
            for file_path in self.output_dir.iterdir():
                if file_path.is_file():
                    size_mb = file_path.stat().st_size / (1024 * 1024)
                    print(f"  + {file_path.name} ({size_mb:.2f} MB)")
                else:
                    print(f"  + {file_path.name} (Folder)")
        
        print()
        print("Distribution ready for release!")
        print()
    
    def run(self):
        """Main build process"""
        try:
            # Print banner
            print("="*50)
            print(f"YTSage Universal Build Script v{self.script_version}")
            print(f"Build Type: {self.build_type}")
            print("="*50)
            print()
            print("This script will create:")
            if not self.args.zip_only:
                print("- MSI installer package")
            if not self.args.msi_only:
                print("- ZIP portable distribution")
            print("- Professional packaging with metadata")
            print()
            
            # Main build process
            self.check_prerequisites()
            self.setup_virtual_environment()
            self.install_dependencies()
            self.remove_build_artifacts()
            self.build_executable()
            
            # Create distributions
            if not self.args.zip_only:
                self.build_msi()
                self.move_msi_files()
            
            if not self.args.msi_only:
                self.create_zip_distribution()
            
            self.create_release_notes()
            self.cleanup_post_build()
            self.show_build_summary()
            
        except Exception as e:
            self.print_error(f"Build failed: {e}")
            if self.args.verbose:
                import traceback
                traceback.print_exc()
            sys.exit(1)
        
        print("Press Enter to continue...")
        input()

def main():
    parser = argparse.ArgumentParser(description="YTSage Universal Build Script")
    parser.add_argument("--skip-venv", action="store_true", help="Skip virtual environment setup")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--ffmpeg", action="store_true", help="Build FFmpeg version")
    parser.add_argument("--msi-only", action="store_true", help="Build MSI only")
    parser.add_argument("--zip-only", action="store_true", help="Build ZIP only")
    parser.add_argument("--output-dir", default="releases", help="Output directory")
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.msi_only and args.zip_only:
        print("Error: Cannot specify both --msi-only and --zip-only")
        sys.exit(1)
    
    # Run build script
    build_script = YTSageBuildScript(args)
    build_script.run()

if __name__ == "__main__":
    main()
