import os
import subprocess
from pathlib import Path

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def setup_git():
    commands = [
        'git init',
        'git add .',
        'git commit -m "Initial commit: QGIS CoordToGeom plugin"'
    ]
    
    for cmd in commands:
        if not run_command(cmd):
            print(f"Error executing: {cmd}")
            return False
    return True

def main():
    # Change to the project directory
    os.chdir(Path(__file__).parent)
    
    # Create .gitignore
    gitignore_content = """
*.pyc
__pycache__/
.idea/
.vscode/
*.zip
    """
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content.strip())
    
    # Initialize and setup git
    if not setup_git():
        print("Failed to initialize git repository")
        return
    
    # Get GitHub repository URL
    repo_url = input("Enter your GitHub repository URL: ")
    if not repo_url:
        print("No repository URL provided")
        return
    
    # Add remote and push
    commands = [
        f'git remote add origin {repo_url}',
        'git push -u origin main'
    ]
    
    for cmd in commands:
        if not run_command(cmd):
            print(f"Error executing: {cmd}")
            return
    
    print("Successfully pushed code to GitHub!")

if __name__ == "__main__":
    main()