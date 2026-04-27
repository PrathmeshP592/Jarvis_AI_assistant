import subprocess
import webbrowser
from datetime import datetime


def run_system_command(user_input: str):
    text = user_input.lower().strip()

    # ---------- OPEN CHROME ----------
    if "open chrome" in text or "open browser" in text:
        try:
            subprocess.Popen("start chrome", shell=True)
            return "Opening Chrome."
        except:
            webbrowser.open("https://www.google.com")
            return "Opening browser."

    # ---------- OPEN NOTEPAD ----------
    if "open notepad" in text:
        subprocess.Popen("notepad")
        return "Opening Notepad."

    # ---------- OPEN CALCULATOR ----------
    if "open calculator" in text or "open calc" in text:
        subprocess.Popen("calc")
        return "Opening Calculator."

    # ---------- OPEN VS CODE ----------
    if "open vs code" in text or "open vscode" in text:
        subprocess.Popen("code", shell=True)
        return "Opening VS Code."

    # ---------- OPEN YOUTUBE ----------
    if "open youtube" in text:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."

    # ---------- TIME ----------
    if "time" in text:
        now = datetime.now().strftime("%I:%M %p")
        return f"It is {now}."

    return None