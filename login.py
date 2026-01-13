import tkinter as tk
from tkinter import font
import hashlib
import sys
import argparse
import json
from PIL import Image, ImageTk, ImageDraw, ImageStat
import os
import time

# --- Configuration ---
STORED_HASH_HEX = "a53cc20b2a2e7d93014527c3a9d691d3088e02a514faeb3e22caf50456c57f52"
COPYRIGHT_TEXT = "Application © 2025 Isaac Mecham"
BACKGROUND_IMAGE_PATH = "bg6.jpg"
ACCOUNT_NAME = "Shadefense"
ACCOUNT_ICON_PATH = "account.png"
LOADING_COLOR = "white"
CONFIG_PATH = "config.json"

# Extended configuration defaults (highly tweakable)
WINDOW_TITLE = "Hashed Passphrase Exit Window"
FULLSCREEN = True
WM_OVERRIDDENIRECT = True
BG_COLOR = "black"

# Time/date fonts and colors
TIME_FONT_FAMILY = "Helvetica"
TIME_FONT_SIZE = 64
TIME_FONT_COLOR = "white"
TIME_BACKGROUND_COLOR = None  # None means transparent; draw rectangle behind text
TIME_BACKGROUND_PADDING = 10  # pixels of padding around text for background
TIME_BORDER_WIDTH = 0  # 0 means no border; set to >0 for a visible border
TIME_BORDER_COLOR = "black"
TIME_FONT_WEIGHT = "bold"

DATE_FONT_FAMILY = "Helvetica"
DATE_FONT_SIZE = 20
DATE_FONT_COLOR = "white"
DATE_BACKGROUND_COLOR = None
DATE_BACKGROUND_PADDING = 10
DATE_BORDER_WIDTH = 0  # 0 means no border
DATE_BORDER_COLOR = "black"
DATE_FONT_WEIGHT = "bold"

# Username/account
USERNAME_FONT_FAMILY = "Helvetica"
USERNAME_FONT_SIZE = 20
USERNAME_FONT_WEIGHT = "bold"
ACCOUNT_ICON_SIZE = 160

# Entry box / text
ENTRY_WIDTH = 400
ENTRY_HEIGHT = 40
ENTRY_FILL_COLOR = "white"
ENTRY_OUTLINE_COLOR = "white"
ENTRY_TEXT_FONT_FAMILY = "Helvetica"
ENTRY_TEXT_FONT_SIZE = 16
ENTRY_TEXT_COLOR = "black"

# Error text
ERROR_FONT_SIZE = 12
ERROR_FONT_COLOR = "red"

# Loading animation
LOADING_ARC_WIDTH = 8
LOADING_RADIUS = 60
LOADING_ROTATION_STEP = 6
LOADING_DELAY_MS = 50

# Timings
SUCCESS_SCREEN_DURATION_MS = 8000
SPLASH_UPDATE_INTERVAL_MS = 1000

# Copyright
COPYRIGHT_FONT_FAMILY = "Helvetica"
COPYRIGHT_FONT_SIZE = 10
COPYRIGHT_COLOR = "gray"

# Outline offsets for username outline drawing (can be replaced by a different list in config)
OUTLINE_OFFSETS = [(-2, -2), (-2, -1), (-2, 0), (-2, 1),
                   (-1, -2), (-1, 2), (0, -2), (0, 2),
                   (1, -2), (1, 2), (2, -1), (2, 0), (2, 1)]


def create_hashed_window_sha256():
    root = tk.Tk()
    root.title(WINDOW_TITLE)
    if FULLSCREEN:
        try:
            root.attributes('-fullscreen', True)
        except Exception:
            pass
    if WM_OVERRIDDENIRECT:
        try:
            root.wm_overrideredirect(True)
        except Exception:
            pass
    root.configure(bg=BG_COLOR)

    root.update()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Load background image (keep a PIL reference for sampling/colors)
    background_photo = None
    bg_pil = None
    if os.path.exists(BACKGROUND_IMAGE_PATH):
        try:
            bg_image = Image.open(BACKGROUND_IMAGE_PATH)
            img_width, img_height = bg_image.size
            screen_ratio = screen_width / screen_height
            img_ratio = img_width / img_height
            
            if screen_ratio > img_ratio:
                new_width = screen_width
                new_height = int(screen_width / img_ratio)
            else:
                new_height = screen_height
                new_width = int(screen_height * img_ratio)
            
            bg_image = bg_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            if new_width > screen_width or new_height > screen_height:
                left = (new_width - screen_width) // 2
                top = (new_height - screen_height) // 2
                bg_image = bg_image.crop((left, top, left + screen_width, top + screen_height))
            
            # keep a PIL copy for sampling later
            bg_pil = bg_image.copy()
            background_photo = ImageTk.PhotoImage(bg_pil)
        except Exception as e:
            print(f"Error loading background: {e}")

    # Create main canvas (everything draws here)
    canvas = tk.Canvas(root, width=screen_width, height=screen_height, highlightthickness=0, bd=0, bg=BG_COLOR)
    canvas.pack(fill=tk.BOTH, expand=True)
    
    # Draw background image on canvas
    if background_photo:
        canvas.create_image(0, 0, image=background_photo, anchor='nw', tags='background')
        canvas.tag_lower('background')

    # State management
    state = {'current_screen': 'splash'}  # 'splash', 'login', 'success'
    password_input = {'text': ''}

    # Helper: choose text fill and outline color based on sampled region near username
    def choose_text_colors(pil_image, center_x, center_y, sample_w=360, sample_h=120):
        # Defaults
        default_fill = 'white'
        default_outline = '#0d0d0d'

        try:
            if pil_image is None:
                return default_fill, default_outline

            w, h = pil_image.size
            # sample box centered at the username position
            left = int(max(0, center_x - sample_w // 2))
            top = int(max(0, center_y - sample_h // 2))
            right = int(min(w, center_x + sample_w // 2))
            bottom = int(min(h, center_y + sample_h // 2))

            if right <= left or bottom <= top:
                return default_fill, default_outline

            crop = pil_image.crop((left, top, right, bottom))

            # compute average brightness (L) and average RGB
            l_stat = ImageStat.Stat(crop.convert('L'))
            l_avg = l_stat.mean[0]
            rgb_stat = ImageStat.Stat(crop.convert('RGB'))
            r_avg, g_avg, b_avg = rgb_stat.mean

            # Heuristics for color choice
            if l_avg > 150:
                # bright background -> dark text
                fill = '#0d0d0d'
                outline = 'white'
            elif l_avg < 90:
                # dark background -> light text with dark outline
                fill = 'white'
                outline = '#0d0d0d'
            else:
                # mid-tones: prefer a light text; but if strongly blue, use a cyan accent
                if b_avg > r_avg + 20 and b_avg > g_avg + 20:
                    fill = '#9be7ff'
                    outline = '#0d0d0d'
                else:
                    fill = 'white'
                    outline = '#0d0d0d'

            return fill, outline
        except Exception:
            return default_fill, default_outline

    # Load account icon
    account_icon_photo = None
    if os.path.exists(ACCOUNT_ICON_PATH):
        try:
            icon_img = Image.open(ACCOUNT_ICON_PATH).convert('RGBA')
            icon_img = icon_img.resize((ACCOUNT_ICON_SIZE, ACCOUNT_ICON_SIZE), Image.Resampling.LANCZOS)
            account_icon_photo = ImageTk.PhotoImage(icon_img)
        except Exception:
            pass

    # Time labels for splash screen
    time_label_id = None
    date_label_id = None

    def update_time():
        nonlocal time_label_id, date_label_id
        if state['current_screen'] != 'splash':
            root.after(SPLASH_UPDATE_INTERVAL_MS, update_time)
            return
        
        # Clear old time/date if they exist
        if time_label_id:
            canvas.delete(time_label_id)
        if date_label_id:
            canvas.delete(date_label_id)
        
        now = time.localtime()
        time_str = time.strftime('%H:%M:%S', now)
        date_str = time.strftime('%A, %B %d, %Y', now)
        
        # Draw time
        time_font = font.Font(family=TIME_FONT_FAMILY, size=TIME_FONT_SIZE, weight=TIME_FONT_WEIGHT)
        time_x = screen_width // 2
        time_y = screen_height * 0.15
        
        # Measure text bounds for background/border
        time_bbox = canvas.create_text(time_x, time_y, text=time_str, fill=TIME_FONT_COLOR, font=time_font, state='hidden')
        bbox = canvas.bbox(time_bbox)
        canvas.delete(time_bbox)
        
        if bbox:
            x1, y1, x2, y2 = bbox
            
            # Draw background rectangle if configured
            if TIME_BACKGROUND_COLOR:
                canvas.create_rectangle(
                    x1 - TIME_BACKGROUND_PADDING, y1 - TIME_BACKGROUND_PADDING,
                    x2 + TIME_BACKGROUND_PADDING, y2 + TIME_BACKGROUND_PADDING,
                    fill=TIME_BACKGROUND_COLOR, outline=TIME_BACKGROUND_COLOR
                )
            
            # Draw border rectangle if configured
            if TIME_BORDER_WIDTH > 0:
                canvas.create_rectangle(
                    x1 - TIME_BACKGROUND_PADDING, y1 - TIME_BACKGROUND_PADDING,
                    x2 + TIME_BACKGROUND_PADDING, y2 + TIME_BACKGROUND_PADDING,
                    fill='', outline=TIME_BORDER_COLOR, width=TIME_BORDER_WIDTH
                )
        
        time_label_id = canvas.create_text(
            time_x, time_y,
            text=time_str, fill=TIME_FONT_COLOR, font=time_font,
        )
        
        # Draw date
        date_font = font.Font(family=DATE_FONT_FAMILY, size=DATE_FONT_SIZE, weight=DATE_FONT_WEIGHT)
        date_x = screen_width // 2
        date_y = screen_height * 0.25
        
        # Measure text bounds for background/border
        date_bbox = canvas.create_text(date_x, date_y, text=date_str, fill=DATE_FONT_COLOR, font=date_font, state='hidden')
        bbox = canvas.bbox(date_bbox)
        canvas.delete(date_bbox)
        
        if bbox:
            x1, y1, x2, y2 = bbox
            
            # Draw background rectangle if configured
            if DATE_BACKGROUND_COLOR:
                canvas.create_rectangle(
                    x1 - DATE_BACKGROUND_PADDING, y1 - DATE_BACKGROUND_PADDING,
                    x2 + DATE_BACKGROUND_PADDING, y2 + DATE_BACKGROUND_PADDING,
                    fill=DATE_BACKGROUND_COLOR, outline=DATE_BACKGROUND_COLOR
                )
            
            # Draw border rectangle if configured
            if DATE_BORDER_WIDTH > 0:
                canvas.create_rectangle(
                    x1 - DATE_BACKGROUND_PADDING, y1 - DATE_BACKGROUND_PADDING,
                    x2 + DATE_BACKGROUND_PADDING, y2 + DATE_BACKGROUND_PADDING,
                    fill='', outline=DATE_BORDER_COLOR, width=DATE_BORDER_WIDTH
                )
        
        date_label_id = canvas.create_text(
            date_x, date_y,
            text=date_str, fill=DATE_FONT_COLOR, font=date_font
        )
        
        root.after(SPLASH_UPDATE_INTERVAL_MS, update_time)

    def draw_splash():
        state['current_screen'] = 'splash'
        canvas.delete('all')
        if background_photo:
            canvas.create_image(0, 0, image=background_photo, anchor='nw', tags='background')
            canvas.tag_lower('background')
        update_time()

    def draw_login():
        state['current_screen'] = 'login'
        canvas.delete('all')
        if background_photo:
            canvas.create_image(0, 0, image=background_photo, anchor='nw')
        
        # Draw account icon or placeholder
        if account_icon_photo:
            canvas.create_image(screen_width // 2, screen_height * 0.38, image=account_icon_photo)
        else:
            # Draw placeholder circle
            x = screen_width // 2
            y = screen_height * 0.38
            canvas.create_oval(x - ACCOUNT_ICON_SIZE//2, y - ACCOUNT_ICON_SIZE//2, x + ACCOUNT_ICON_SIZE//2, y + ACCOUNT_ICON_SIZE//2, fill='#333333', outline='#666666', width=2)
        
        # Draw username with dynamic color + outline for readability
        username_font = font.Font(family=USERNAME_FONT_FAMILY, size=USERNAME_FONT_SIZE, weight=USERNAME_FONT_WEIGHT)
        ux = int(screen_width // 2)
        uy = int(screen_height * 0.55)
        if bg_pil:
            fill_color, outline_color = choose_text_colors(bg_pil, ux, uy)
        else:
            fill_color, outline_color = 'white', '#0d0d0d'

        # Draw outline by drawing the text at offsets, then main text on top
        for ox, oy in OUTLINE_OFFSETS:
            canvas.create_text(ux + ox, uy + oy, text=ACCOUNT_NAME, fill=outline_color, font=username_font)
        canvas.create_text(ux, uy, text=ACCOUNT_NAME, fill=fill_color, font=username_font)
        
        # Draw password entry box (using canvas rectangle)
        entry_y = screen_height * 0.65
        entry_width = ENTRY_WIDTH
        entry_height = ENTRY_HEIGHT
        canvas.create_rectangle(
            screen_width // 2 - entry_width // 2,
            entry_y - entry_height // 2,
            screen_width // 2 + entry_width // 2,
            entry_y + entry_height // 2,
            fill=ENTRY_FILL_COLOR, outline=ENTRY_OUTLINE_COLOR
        )
        
        # Text display for password (masked)
        password_display_id = canvas.create_text(
            screen_width // 2 - entry_width // 2 + 20,
            entry_y,
            text='',
            fill=ENTRY_TEXT_COLOR,
            font=(ENTRY_TEXT_FONT_FAMILY, ENTRY_TEXT_FONT_SIZE),
            anchor='w'
        )
        
        # Store reference for updates
        state['password_display_id'] = password_display_id # pyright: ignore[reportArgumentType]
        state['entry_y'] = entry_y # pyright: ignore[reportArgumentType]
        state['entry_width'] = entry_width # pyright: ignore[reportArgumentType]
        
        # Error message placeholder
        state['error_label_id'] = canvas.create_text(screen_width // 2, screen_height * 0.72, text='', fill=ERROR_FONT_COLOR, font=(TIME_FONT_FAMILY, ERROR_FONT_SIZE)) # pyright: ignore[reportArgumentType]

    def draw_success():
        state['current_screen'] = 'success'
        canvas.delete('all')
        if background_photo:
            canvas.create_image(0, 0, image=background_photo, anchor='nw')
        
        # Draw account icon
        if account_icon_photo:
            canvas.create_image(screen_width // 2, screen_height * 0.35, image=account_icon_photo)
        else:
            x = screen_width // 2
            y = screen_height * 0.35
            canvas.create_oval(x - ACCOUNT_ICON_SIZE//2, y - ACCOUNT_ICON_SIZE//2, x + ACCOUNT_ICON_SIZE//2, y + ACCOUNT_ICON_SIZE//2, fill='#333333', outline='#666666', width=2)
        
        # Draw username with dynamic color + outline for readability
        username_font = font.Font(family=USERNAME_FONT_FAMILY, size=USERNAME_FONT_SIZE, weight=USERNAME_FONT_WEIGHT)
        ux = int(screen_width // 2)
        uy = int(screen_height * 0.55)
        if bg_pil:
            fill_color, outline_color = choose_text_colors(bg_pil, ux, uy)
        else:
            fill_color, outline_color = 'white', '#0d0d0d'

        for ox, oy in OUTLINE_OFFSETS:
            canvas.create_text(ux + ox, uy + oy, text=ACCOUNT_NAME, fill=outline_color, font=username_font)
        canvas.create_text(ux, uy, text=ACCOUNT_NAME, fill=fill_color, font=username_font)
        
        # Start loading animation
        state['rotation'] = 0 # pyright: ignore[reportArgumentType]
        animate_loading_circle()

    rotation_id = None
    
    def animate_loading_circle():
        nonlocal rotation_id
        if state['current_screen'] != 'success':
            return
        
        if rotation_id:
            canvas.delete(rotation_id)
        
        # Draw rotating arc
        x = screen_width // 2
        y = screen_height * 0.75
        radius = 60
        arc_width = 8
        
        rotation = state['rotation']
        # Use LOADING_COLOR config variable for the stroke color of the arc.
        rotation_id = canvas.create_arc(
            x - LOADING_RADIUS, y - LOADING_RADIUS,
            x + LOADING_RADIUS, y + LOADING_RADIUS,
            start=rotation, extent=90, outline=LOADING_COLOR, width=LOADING_ARC_WIDTH, style='arc'
        )
        
        state['rotation'] = (rotation + LOADING_ROTATION_STEP) % 360 # pyright: ignore[reportOperatorIssue]
        root.after(LOADING_DELAY_MS, animate_loading_circle)

    def check_passphrase():
        entered_text = password_input['text']
        input_hash = hashlib.sha256(entered_text.encode('utf-8')).hexdigest()
        
        if input_hash == STORED_HASH_HEX:
            draw_success()
            root.after(SUCCESS_SCREEN_DURATION_MS, root.destroy)
        else:
            password_input['text'] = ''
            canvas.itemconfig(state['password_display_id'], text='')
            canvas.itemconfig(state['error_label_id'], text='Incorrect Passphrase!')
            root.after(2000, lambda: canvas.itemconfig(state['error_label_id'], text=''))

    def on_key_press(event):
        if state['current_screen'] == 'splash':
            draw_login()
        elif state['current_screen'] == 'login':
            if event.char == '\r':  # Enter key
                check_passphrase()
            elif event.keysym == 'BackSpace':
                password_input['text'] = password_input['text'][:-1]
            elif len(event.char) == 1 and event.char.isprintable():
                password_input['text'] += event.char
            
            # Update display
            display_text = '*' * len(password_input['text'])
            canvas.itemconfig(state['password_display_id'], text=display_text)

    def on_mouse_click(event):
        if state['current_screen'] == 'splash':
            draw_login()

    # Bind events
    root.bind('<Key>', on_key_press)
    root.bind('<Button-1>', on_mouse_click)
    
    # Draw copyright
    copyright_font = font.Font(family=COPYRIGHT_FONT_FAMILY, size=COPYRIGHT_FONT_SIZE)
    canvas.create_text(
        screen_width - 10, screen_height - 10,
        text=COPYRIGHT_TEXT, fill=COPYRIGHT_COLOR, font=copyright_font, anchor='se'
    )

    # Start with splash screen
    draw_splash()

    root.mainloop()


def load_config(path=CONFIG_PATH):
    """Load configuration from a JSON file and override module-level defaults for this session.

    Allowed keys that may be present in the JSON file:
      - STORED_HASH_HEX
      - COPYRIGHT_TEXT
      - BACKGROUND_IMAGE_PATH
      - ACCOUNT_NAME
      - ACCOUNT_ICON_PATH
      - LOADING_COLOR
      - WINDOW_TITLE
      - FULLSCREEN
      - WM_OVERRIDDENIRECT
      - BG_COLOR
      - TIME_FONT_FAMILY
      - TIME_FONT_SIZE
      - TIME_FONT_COLOR
      - TIME_BACKGROUND_COLOR
      - TIME_BACKGROUND_PADDING
      - TIME_BORDER_WIDTH
      - TIME_BORDER_COLOR
      - TIME_FONT_WIEGHT
      - DATE_FONT_FAMILY
      - DATE_FONT_SIZE
      - DATE_FONT_COLOR
      - DATE_BACKGROUND_COLOR
      - DATE_BACKGROUND_PADDING
      - DATE_BORDER_WIDTH
      - DATE_BORDER_COLOR
      - DATE_FONT_WEIGHT
      - USERNAME_FONT_FAMILY
      - USERNAME_FONT_SIZE
      - USERNAME_FONT_WEIGHT
      - ACCOUNT_ICON_SIZE
      - ENTRY_WIDTH
      - ENTRY_HEIGHT
      - ENTRY_FILL_COLOR
      - ENTRY_OUTLINE_COLOR
      - ENTRY_TEXT_FONT_FAMILY
      - ENTRY_TEXT_FONT_SIZE
      - ENTRY_TEXT_COLOR
      - ERROR_FONT_SIZE
      - ERROR_FONT_COLOR
      - LOADING_ARC_WIDTH
      - LOADING_RADIUS
      - LOADING_ROTATION_STEP
      - LOADING_DELAY_MS
      - SUCCESS_SCREEN_DURATION_MS
      - SPLASH_UPDATE_INTERVAL_MS
      - COPYRIGHT_FONT_FAMILY
      - COPYRIGHT_FONT_SIZE
      - COPYRIGHT_COLOR
      - OUTLINE_OFFSETS
    """
    try:
        if not os.path.exists(path):
            return
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        # If config is malformed or unreadable, skip silently (keeps defaults)
        print(f"Warning: could not read config '{path}': {e}")
        return

    allowed = {
        'STORED_HASH_HEX', 'COPYRIGHT_TEXT', 'BACKGROUND_IMAGE_PATH',
        'ACCOUNT_NAME', 'ACCOUNT_ICON_PATH', 'LOADING_COLOR',
        'WINDOW_TITLE', 'FULLSCREEN', 'WM_OVERRIDDENIRECT', 'BG_COLOR',
        'TIME_FONT_FAMILY', 'TIME_FONT_SIZE', 'TIME_FONT_COLOR', 'TIME_BACKGROUND_COLOR', 'TIME_BACKGROUND_PADDING', 'TIME_BORDER_WIDTH', 'TIME_BORDER_COLOR', 'TIME_FONT_WEIGHT',
        'DATE_FONT_FAMILY', 'DATE_FONT_SIZE', 'DATE_FONT_COLOR', 'DATE_BACKGROUND_COLOR', 'DATE_BACKGROUND_PADDING', 'DATE_BORDER_WIDTH', 'DATE_BORDER_COLOR', 'DATE_FONT_WIEGHT',
        'USERNAME_FONT_FAMILY', 'USERNAME_FONT_SIZE', 'USERNAME_FONT_WEIGHT', 'ACCOUNT_ICON_SIZE',
        'ENTRY_WIDTH', 'ENTRY_HEIGHT', 'ENTRY_FILL_COLOR', 'ENTRY_OUTLINE_COLOR',
        'ENTRY_TEXT_FONT_FAMILY', 'ENTRY_TEXT_FONT_SIZE', 'ENTRY_TEXT_COLOR',
        'ERROR_FONT_SIZE', 'ERROR_FONT_COLOR',
        'LOADING_ARC_WIDTH', 'LOADING_RADIUS', 'LOADING_ROTATION_STEP', 'LOADING_DELAY_MS',
        'SUCCESS_SCREEN_DURATION_MS', 'SPLASH_UPDATE_INTERVAL_MS',
        'COPYRIGHT_FONT_FAMILY', 'COPYRIGHT_FONT_SIZE', 'COPYRIGHT_COLOR',
        'OUTLINE_OFFSETS'
    }

    for key, val in data.items():
        if key in allowed:
            # Set module-level variable for this session
            globals()[key] = val

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hashed Passphrase Exit Window")
    parser.add_argument('--generate-hash', action='store_true', help='Prompt to generate a SHA256 hash from a passphrase')
    parser.add_argument('--background', '-b', type=str, help='Path to a background image to use')
    args = parser.parse_args()

    # Load config file (if present) to override defaults for this session
    load_config(CONFIG_PATH)

    if args.generate_hash:
        password_to_hash = input("Enter password to hash: ")
        hashed_password = hashlib.sha256(password_to_hash.encode('utf-8')).hexdigest()
        print(f"\nYour new SHA256 HASH is:\n{hashed_password}\n\nCopy this value into the STORED_HASH_HEX variable.")
    else:
        # Allow overriding the background image from the command line (CLI takes precedence)
        if args.background:
            BACKGROUND_IMAGE_PATH = args.background
        create_hashed_window_sha256()
