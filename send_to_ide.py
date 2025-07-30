import subprocess
import time
import sys
import tempfile
import os
import platform
import ctypes

# ------------------------------
# Get arguments
# ------------------------------
message = sys.argv[1] if len(sys.argv) > 1 else "hello world"
ide = sys.argv[2] if len(sys.argv) > 2 else "Visual Studio Code"
os_type = sys.argv[3] if len(sys.argv) > 3 else platform.system()  # "Darwin" for Mac, "Windows" for Windows

print(f"🧠 Selected IDE: {ide} | OS: {os_type}")

# ------------------------------
# Create temporary message file
# ------------------------------
with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
    f.write(message)
    temp_path = f.name

try:
    # ------------------------------
    # macOS Implementation
    # ------------------------------
    if os_type == "Mac":
        applescript = f'''
            set messageFile to POSIX file "{temp_path}"
            set messageText to (read messageFile)
            set the clipboard to messageText
        '''
        subprocess.run(['osascript', '-e', applescript])

        if ide == "Cursor":
            subprocess.run(['osascript', '-e', 'tell application "Cursor" to activate'])
        if ide == "Visual Studio Code":
            subprocess.run(['osascript', '-e', 'tell application "Visual Studio Code" to activate'])

        time.sleep(1)

        if ide == "Cursor":
            subprocess.run(['osascript', '-e', 'tell application "System Events" to keystroke "y" using command down'])
        if ide == "Visual Studio Code":
            subprocess.run(['osascript', '-e', 'tell application "System Events" to key code 34 using {command down, control down}'])

        time.sleep(1)

        subprocess.run(['osascript', '-e', '''
            tell application "System Events"
                keystroke "v" using command down
                delay 0.5
                key code 36
            end tell
        '''])

    # ------------------------------
    # Windows Implementation
    # ------------------------------
    elif os_type == "Windows":
        def is_admin():
            try:
                return ctypes.windll.shell32.IsUserAnAdmin()
            except:
                return False

        if not is_admin():
            print("⚠️ Please run as Administrator for best results (window focus, key send).")
            time.sleep(2)

        # Set clipboard
        subprocess.run([
            'powershell',
            '-Command',
            f'Get-Content -Path "{temp_path}" | Set-Clipboard'
        ], shell=True)

        # Activate IDE window
        subprocess.run([
            'powershell',
            '-Command',
            f'(New-Object -ComObject WScript.Shell).AppActivate("{ide}")'
        ], shell=True)

        time.sleep(1)

        # Send shortcut to open chat
        shortcut = "^y" if ide == "Cursor" else "^%i"
        subprocess.run([
            'powershell',
            '-Command',
            f'''
            Add-Type -AssemblyName System.Windows.Forms;
            [System.Windows.Forms.SendKeys]::SendWait("{shortcut}")
            '''
        ], shell=True)

        time.sleep(1)

        # Paste and press Enter
        subprocess.run([
            'powershell',
            '-Command',
            '''
            Add-Type -AssemblyName System.Windows.Forms;
            [System.Windows.Forms.SendKeys]::SendWait("^v");
            Start-Sleep -Milliseconds 500;
            [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
            '''
        ], shell=True)

finally:
    os.unlink(temp_path)
