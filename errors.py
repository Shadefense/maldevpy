import winsound
import threading
import ctypes
import time
import random

# Windows API Constants for 2026
MB_ICONHAND = 0x10       # The "Red X" Error Icon
MB_TOPMOST = 0x40000     # Ensures the window is "Always on Top"
MB_SYSTEMMODAL = 0x1000  # Higher priority "Topmost" style

def move_window_to_random(title):
    """Finds the popup window by title and teleports it to a random spot."""
    time.sleep(0.05) # Tiny delay to allow window creation
    
    # Detect screen size for 2026 displays
    width = ctypes.windll.user32.GetSystemMetrics(0)
    height = ctypes.windll.user32.GetSystemMetrics(1)
    
    # Generate random coordinates
    rand_x = random.randint(50, width - 400)
    rand_y = random.randint(50, height - 200)
    
    hwnd = ctypes.windll.user32.FindWindowW(None, title)
    if hwnd:
        # Move window (X, Y, Width, Height, repaint)
        ctypes.windll.user32.MoveWindow(hwnd, rand_x, rand_y, 350, 150, True)

def spawn_error(error_id):
    title = f"CRITICAL ERROR {error_id}"
    msg = f"Memory breach at {hex(random.randint(0x1000, 0xFFFF))}"
    
    # Play the rapid error sound [Method 2]
    winsound.MessageBeep(MB_ICONHAND)
    
    # Start background thread to move the window [Non-blocking]
    threading.Thread(target=move_window_to_random, args=(title,), daemon=True).start()
    
    # Display the popup with Topmost and System Modal flags
    # MB_ICONHAND | MB_TOPMOST | MB_SYSTEMMODAL
    ctypes.windll.user32.MessageBoxW(0, msg, title, 0x10 | 0x40000 | 0x1000)

def rapid_chaos(count=20):
    for i in range(count):
        # Fire off popups rapidly in their own threads
        threading.Thread(target=spawn_error, args=(i,)).start()
        time.sleep(0.1) # Frequency of appearance

if __name__ == "__main__":
    print("Initiating chaotic error sequence...")
    rapid_chaos(9999)
