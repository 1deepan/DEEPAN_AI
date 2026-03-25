import os
import sys
import subprocess

def build():
    print("Building Ironman Executable (Background Mode)...")
    try:
        import PyInstaller.__main__
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        import PyInstaller.__main__

    # Define paths
    script = "app.py"
    icon = "static/favicon.ico"
    name = "Ironman"

    # PyInstaller command
    # --onefile: Create a single executable
    # --noconsole: Don't show the terminal window (Background mode)
    # --add-data: Include templates, static files, and modules
    # --hidden-import: Ensure dynamic imports are bundled
    args = [
        script,
        "--onefile",
        "--noconsole",
        "--name=" + name,
        "--add-data=templates;templates",
        "--add-data=static;static",
        "--add-data=assistant;assistant",
        "--hidden-import=flask",
        "--hidden-import=pystray",
        "--hidden-import=PIL",
        "--hidden-import=PIL._imagingtk",
        "--hidden-import=PIL._tkinter_finder",
        "--hidden-import=psutil",
        "--hidden-import=pyttsx3",
        "--hidden-import=pyautogui",
        "--hidden-import=requests"
    ]

    if os.path.exists(icon):
        args.append("--icon=" + icon)

    PyInstaller.__main__.run(args)
    print("\n[SUCCESS] Executable created in the 'dist' folder.")
    print("[INFO] You can now closed the terminal and JARVIS will run in your system tray.")

if __name__ == "__main__":
    build()
