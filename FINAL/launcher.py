import os
import subprocess
import sys
import time
import webbrowser

base = os.path.dirname(sys.argv[0])

# possible locations
paths = [
    os.path.join(base, "app", "AI_Music_Player.exe"),
    os.path.join(base, "AI_Music_Player", "AI_Music_Player.exe"),
    os.path.join(base, "app", "AI_Music_Player", "AI_Music_Player.exe"),
]

target = None
for p in paths:
    if os.path.exists(p):
        target = p
        break

if not target:
    from tkinter import messagebox
    messagebox.showerror("Error", "Main application not found!\nCheck app folder.")
    sys.exit(1)

# ✅ BACKEND START
subprocess.Popen(target)

# ✅ NEW ADDED – WAIT AND OPEN BROWSER
time.sleep(4)

try:
    webbrowser.open("http://127.0.0.1:5000")
except:
    pass
