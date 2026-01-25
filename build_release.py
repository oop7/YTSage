import os
import shutil
import re
import subprocess
import sys

def build_release():
    print("Starting Production Build...")

    # 1. Backup local README
    if os.path.exists("README.md"):
        shutil.copy2("README.md", "README.md.bak")
        print("Backed up README.md")

    try:
        # 2. Prepare PyPI README
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()

        # Base URL for assets
        base_url = "https://github.com/oop7/YTSage/raw/main/branding/"
        
        # Function to fix paths matches by regex
        def path_fixer(match):
            full_match = match.group(0)
            # Convert backslashes to forward slashes for URL compatibility
            fixed = full_match.replace("\\", "/")
            # Prepend the absolute URL
            return fixed.replace("branding/", base_url)

        # Regex: matches "branding" followed by backslash or slash, then characters until quote, closing paren, or space
        # This captures paths like: branding\screenshots\main.png
        pattern = r"branding[\\/][^\"')\s]+"
        new_content = re.sub(pattern, path_fixer, content)

        with open("README.md", "w", encoding="utf-8") as f:
            f.write(new_content)
        
        print("Modified README.md for PyPI (Absolute URLs)")

        # 3. Clean previous builds
        for folder in ["dist", "build", "ytsage.egg-info"]:
            if os.path.exists(folder):
                shutil.rmtree(folder)

        # 4. Run Build
        print("Building Wheel...")
        subprocess.check_call([sys.executable, "-m", "build"])

    except Exception as e:
        print(f"Error during build: {e}")
        sys.exit(1)
        
    finally:
        # 5. Restore README
        if os.path.exists("README.md.bak"):
            # Force move back, overwriting the modified one
            shutil.move("README.md.bak", "README.md")
            print("Restored original README.md")

    print("Build Complete. Artifacts are in the /dist folder.")

if __name__ == "__main__":
    build_release()
