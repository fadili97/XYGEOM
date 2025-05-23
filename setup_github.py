import os
import subprocess
from pathlib import Path

def run_git_command(command):
    try:
        process = subprocess.run(command, shell=True, capture_output=True, text=True)
        if process.returncode != 0:
            print(f"Error: {process.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Exception: {str(e)}")
        return False

def setup_github():
    # Set working directory
    os.chdir(Path(__file__).parent)
    
    # Create .gitignore
    gitignore_content = """
*.pyc
__pycache__/
.idea/
.vscode/
*.zip
.qt_for_python/
*.bak
    """
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content.strip())

    # Initialize repository
    commands = [
        "git init",
        "git add .",
        'git config --global user.email "elfadily.igt@gmail.com"',
        'git config --global user.name "fadili97"',
        'git commit -m "Initial commit: QGIS CoordToGeom plugin"',
        "git branch -M main",
        "git remote add origin https://github.com/fadili97/XYGEOM.git",
        "git pull origin main --allow-unrelated-histories --no-rebase",
        "git add .",
        'git commit -m "Merge remote changes and add plugin code"',
        "git push -u origin main --force"
    ]

    for cmd in commands:
        print(f"Executing: {cmd}")
        if not run_git_command(cmd):
            print(f"Failed at command: {cmd}")
            return False
        
    print("Successfully pushed code to GitHub!")
    return True

if __name__ == "__main__":
    setup_github()