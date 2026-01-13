import tkinter as tk
import hashlib
import sys
from PIL import Image, ImageTk
import os
import time

# --- Configuration ---
# This specific string is the SHA-256 hash of the word 'exitnow'
STORED_HASH_HEX = "cd8c6be0075e6ca97779ab726775727aa214bf95129c99ac6b4d7e995f9c1a0b"
COPYRIGHT_TEXT = "Application © 2025 Isaac Mecham" # Update the year and name as needed
BACKGROUND_IMAGE_PATH = "background.png"  # Replace with your image path
ACCOUNT_NAME = "User"  # Change to desired username
ACCOUNT_ICON_PATH = "account.png"  # Optional: path to account icon

def create_hashed_window_sha256():
    root = tk.Tk()
    root.title("Hashed Passphrase Exit Window")
    root.attributes('-fullscreen', True)
    root.wm_overrideredirect(True)
    root.configure(bg='black')

    # --- Load and set background image ---
    bg_canvas = None
    if os.path.exists(BACKGROUND_IMAGE_PATH):
        try:
            # Load image with PIL
            background_image = Image.open(BACKGROUND_IMAGE_PATH)
            root.update()
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            
            # Get original dimensions
            img_width, img_height = background_image.size
            screen_ratio = screen_width / screen_height
            img_ratio = img_width / img_height
            
            # Calculate optimal resize dimensions
            if screen_ratio > img_ratio:
                new_width = screen_width
                new_height = int(screen_width / img_ratio)
            else:
                new_height = screen_height
                new_width = int(screen_height * img_ratio)
            
            # Resize with highest quality resampling
            background_image = background_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Crop to exact screen size
            if new_width > screen_width or new_height > screen_height:
                left = (new_width - screen_width) // 2
                top = (new_height - screen_height) // 2
                background_image = background_image.crop((left, top, left + screen_width, top + screen_height))
            
            # Use PPM format to bypass PhotoImage limitations
            # PPM is uncompressed and preserves full quality
            background_photo = ImageTk.PhotoImage(background_image)
            
            # Create canvas for rendering
            bg_canvas = tk.Canvas(root, width=screen_width, height=screen_height, highlightthickness=0, bd=0, bg='black')
            bg_canvas.place(relwidth=1, relheight=1)
            bg_canvas.create_image(0, 0, image=background_photo, anchor='nw')
            # Keep reference to prevent garbage collection
            if not hasattr(root, '_bg_photos'):
                root._bg_photos = []
            root._bg_photos.append(background_photo)
        except Exception as e:
            print(f"Error loading image: {e}")
            root.configure(bg='black')
    else:
        root.configure(bg='black')

    # --- Splash and login UI setup ---
    # We'll create two layered frames: `splash_frame` (time/date) and `login_frame` (icon + username + entry)
    splash_frame = tk.Frame(root, highlightthickness=0, bd=0)
    splash_frame.place(relwidth=1, relheight=1)

    # Add background image to splash if it exists
    if os.path.exists(BACKGROUND_IMAGE_PATH):
        try:
            splash_bg_image = Image.open(BACKGROUND_IMAGE_PATH)
            splash_screen_width = root.winfo_screenwidth()
            splash_screen_height = root.winfo_screenheight()
            
            img_width, img_height = splash_bg_image.size
            screen_ratio = splash_screen_width / splash_screen_height
            img_ratio = img_width / img_height
            
            if screen_ratio > img_ratio:
                new_width = splash_screen_width
                new_height = int(splash_screen_width / img_ratio)
            else:
                new_height = splash_screen_height
                new_width = int(splash_screen_height * img_ratio)
            
            splash_bg_image = splash_bg_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            if new_width > splash_screen_width or new_height > splash_screen_height:
                left = (new_width - splash_screen_width) // 2
                top = (new_height - splash_screen_height) // 2
                splash_bg_image = splash_bg_image.crop((left, top, left + splash_screen_width, top + splash_screen_height))
            
            splash_bg_photo = ImageTk.PhotoImage(splash_bg_image)
            splash_bg_canvas = tk.Canvas(splash_frame, width=splash_screen_width, height=splash_screen_height, highlightthickness=0, bd=0)
            splash_bg_canvas.place(relwidth=1, relheight=1)
            splash_bg_canvas.create_image(0, 0, image=splash_bg_photo, anchor='nw')
            if not hasattr(root, '_bg_photos'):
                root._bg_photos = []
            root._bg_photos.append(splash_bg_photo)
        except Exception:
            pass

    login_frame = tk.Frame(root, highlightthickness=0, bd=0)
    # login_frame will be placed when needed

    # Time and date labels on the splash screen
    time_label = tk.Label(splash_frame, text="", font=("Helvetica", 64), fg='white', highlightthickness=0, bd=0, takefocus=0, state='disabled', disabledforeground='white')
    time_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    date_label = tk.Label(splash_frame, text="", font=("Helvetica", 20), fg='white', highlightthickness=0, bd=0, takefocus=0, state='disabled', disabledforeground='white')
    date_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Function to update time every second
    def update_time():
        now = time.localtime()
        time_label.config(text=time.strftime('%H:%M:%S', now))
        date_label.config(text=time.strftime('%A, %B %d, %Y', now))
        # schedule next update
        splash_frame.after(1000, update_time)

    # --- Function to show the success screen and exit ---
    def show_success_and_exit():
        # Hide any UI elements
        try:
            login_frame.place_forget()
        except Exception:
            pass
        try:
            splash_frame.place_forget()
        except Exception:
            pass

        # Create a new frame for the success screen (icon + username + loading circle)
        # Use no background to blend with image
        success_frame = tk.Frame(root, highlightthickness=0, bd=0)
        success_frame.place(relwidth=1, relheight=1)
        
        # Add background image to success screen if it exists
        if os.path.exists(BACKGROUND_IMAGE_PATH):
            try:
                success_bg_image = Image.open(BACKGROUND_IMAGE_PATH)
                success_root_update = root.winfo_screenwidth()
                success_root_height = root.winfo_screenheight()
                
                # Resize background image
                img_width, img_height = success_bg_image.size
                screen_ratio = success_root_update / success_root_height
                img_ratio = img_width / img_height
                
                if screen_ratio > img_ratio:
                    new_width = success_root_update
                    new_height = int(success_root_update / img_ratio)
                else:
                    new_height = success_root_height
                    new_width = int(success_root_height * img_ratio)
                
                success_bg_image = success_bg_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                if new_width > success_root_update or new_height > success_root_height:
                    left = (new_width - success_root_update) // 2
                    top = (new_height - success_root_height) // 2
                    success_bg_image = success_bg_image.crop((left, top, left + success_root_update, top + success_root_height))
                
                success_bg_photo = ImageTk.PhotoImage(success_bg_image)
                
                # Create canvas with transparent background inside success_frame
                success_bg_canvas = tk.Canvas(success_frame, width=success_root_update, height=success_root_height, highlightthickness=0, bd=0, highlightbackground='#1a1a1a', bg='#1a1a1a')
                success_bg_canvas.place(relwidth=1, relheight=1)
                success_bg_canvas.create_image(0, 0, image=success_bg_photo, anchor='nw')
                success_bg_canvas.tag_lower('all')  # Send all canvas items to back
                if not hasattr(root, '_bg_photos'):
                    root._bg_photos = []
                root._bg_photos.append(success_bg_photo)
            except Exception:
                pass

        # Re-display the icon
        icon_container_success = tk.Frame(success_frame, width=200, height=200, highlightthickness=0, bd=0)
        icon_container_success.pack_propagate(False)
        icon_container_success.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

        account_icon_label_success = tk.Label(icon_container_success, highlightthickness=0, bd=0, takefocus=0)
        account_icon_label_success.pack(fill='both', expand=True)

        # Load and display the account icon again
        if os.path.exists(ACCOUNT_ICON_PATH):
            try:
                icon_img = Image.open(ACCOUNT_ICON_PATH).convert('RGBA')
                icon_img = icon_img.resize((160, 160), Image.Resampling.LANCZOS)
                icon_photo = ImageTk.PhotoImage(icon_img)
                account_icon_label_success.config(image=icon_photo)
                if not hasattr(root, '_bg_photos'):
                    root._bg_photos = []
                root._bg_photos.append(icon_photo)
            except Exception:
                canvas_icon = tk.Canvas(icon_container_success, width=160, height=160, highlightthickness=0, bg='', bd=0, highlightbackground='')
                canvas_icon.pack()
                canvas_icon.create_oval(8, 8, 152, 152, fill='#333333', outline='#666666')
        else:
            canvas_icon = tk.Canvas(icon_container_success, width=160, height=160, highlightthickness=0, bg='#1a1a1a', bd=0, highlightbackground='#1a1a1a')
            canvas_icon.pack()
            canvas_icon.create_oval(8, 8, 152, 152, fill='#333333', outline='#666666')

        # Re-display the username
        username_label_success = tk.Label(success_frame, text=ACCOUNT_NAME, font=("Helvetica", 20), fg='white', padx=20, pady=6, highlightthickness=0, bd=0, takefocus=0, state='disabled', disabledforeground='white')
        username_label_success.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        # Create a canvas for the loading circle animation (below username)
        success_canvas = tk.Canvas(success_frame, width=200, height=200, bg='#1a1a1a', highlightthickness=0, bd=0, highlightbackground='#1a1a1a')
        success_canvas.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

        # Animation state
        rotation = [0]

        def animate_circle():
            success_canvas.delete("all")
            # Draw rotating arc (loading circle)
            arc_width = 8
            circle_radius = 60
            success_canvas.create_arc(
                100 - circle_radius, 100 - circle_radius,
                100 + circle_radius, 100 + circle_radius,
                start=rotation[0], extent=90, fill='lime', width=arc_width, style='arc'
            )
            rotation[0] = (rotation[0] + 6) % 360
            success_canvas.after(50, animate_circle)

        animate_circle()

        # Wait 8 seconds, then destroy the window
        root.after(8000, root.destroy)

    # --- Function to check the input (modified) ---
    def check_passphrase(event=None):
        entered_text = entry_box.get()
        input_hash = hashlib.sha256(entered_text.encode('utf-8')).hexdigest()

        if input_hash == STORED_HASH_HEX:
            show_success_and_exit() # Call the new success function
        else:
            entry_box.delete(0, tk.END)
            error_label.config(text="Incorrect Passphrase!", fg="red")
            root.after(2000, lambda: error_label.config(text=""))

    # --- UI Elements for login_frame (centered near bottom) ---
    # Add background image to login frame if it exists
    if os.path.exists(BACKGROUND_IMAGE_PATH):
        try:
            login_bg_image = Image.open(BACKGROUND_IMAGE_PATH)
            login_screen_width = root.winfo_screenwidth()
            login_screen_height = root.winfo_screenheight()
            
            img_width, img_height = login_bg_image.size
            screen_ratio = login_screen_width / login_screen_height
            img_ratio = img_width / img_height
            
            if screen_ratio > img_ratio:
                new_width = login_screen_width
                new_height = int(login_screen_width / img_ratio)
            else:
                new_height = login_screen_height
                new_width = int(login_screen_height * img_ratio)
            
            login_bg_image = login_bg_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            if new_width > login_screen_width or new_height > login_screen_height:
                left = (new_width - login_screen_width) // 2
                top = (new_height - login_screen_height) // 2
                login_bg_image = login_bg_image.crop((left, top, left + login_screen_width, top + login_screen_height))
            
            login_bg_photo = ImageTk.PhotoImage(login_bg_image)
            login_bg_canvas = tk.Canvas(login_frame, width=login_screen_width, height=login_screen_height, highlightthickness=0, bd=0)
            login_bg_canvas.place(relwidth=1, relheight=1)
            login_bg_canvas.create_image(0, 0, image=login_bg_photo, anchor='nw')
            if not hasattr(root, '_bg_photos'):
                root._bg_photos = []
            root._bg_photos.append(login_bg_photo)
        except Exception:
            pass
    
    # Account icon area (use image if ACCOUNT_ICON_PATH exists, otherwise placeholder circle)
    icon_container = tk.Frame(login_frame, width=200, height=200, highlightthickness=0, bd=0)
    icon_container.pack_propagate(False)
    icon_container.place(relx=0.5, rely=0.38, anchor=tk.CENTER)

    account_icon_label = tk.Label(icon_container, highlightthickness=0, bd=0)
    account_icon_label.pack(fill='both', expand=True)

    # username text
    username_label = tk.Label(login_frame, text=ACCOUNT_NAME, font=("Helvetica", 20), fg='white', padx=20, pady=6, highlightthickness=0, bd=0, takefocus=0, state='disabled', disabledforeground='white')
    username_label.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

    entry_box = tk.Entry(login_frame, show="*", font=("Helvetica", 16), width=30, bg='white', fg='black', relief=tk.FLAT, bd=0, highlightthickness=0, insertwidth=2, insertbackground='white')
    entry_box.place(relx=0.5, rely=0.65, anchor=tk.CENTER)
    entry_box.bind('<Return>', check_passphrase)

    error_label = tk.Label(login_frame, text="", font=("Helvetica", 12), fg="red", highlightthickness=0, bd=0, takefocus=0, state='disabled', disabledforeground='red')
    error_label.place(relx=0.5, rely=0.72, anchor=tk.CENTER)

        # Load account icon if available
    try:
        icon_img = Image.open(ACCOUNT_ICON_PATH).convert('RGBA')
        # Resize to fit container while keeping aspect
        icon_img = icon_img.resize((160, 160), Image.Resampling.LANCZOS)
        icon_photo = ImageTk.PhotoImage(icon_img)
        account_icon_label.config(image=icon_photo)
        # keep reference
        if not hasattr(root, '_bg_photos'):
            root._bg_photos = []
        root._bg_photos.append(icon_photo)
    except Exception:
        # fallback: draw a circle on a Canvas inside icon_container
        canvas_icon = tk.Canvas(icon_container, width=160, height=160, highlightthickness=0, bg='#1a1a1a', bd=0, highlightbackground='#1a1a1a')
        canvas_icon.pack()
        canvas_icon.create_oval(8, 8, 152, 152, fill='#333333', outline='#666666')
    
    # --- COPYRIGHT STATEMENT (Bottom Right) ---
    copyright_label = tk.Label(root, 
                               text=COPYRIGHT_TEXT, 
                               font=("Helvetica", 10), 
                               bg="#0d0d0d", 
                               fg='gray')
    copyright_label.place(relx=1.0, rely=1.0, anchor='se') 

    # Function to transition from splash to login
    def show_login(event=None):
        # stop splash bindings and hide splash_frame
        splash_frame.place_forget()
        # place the login_frame to cover screen
        login_frame.place(relwidth=1, relheight=1)
        entry_box.focus_set()

    # Bind any mouse click or key to switch to login (only while splash is visible)
    root.bind('<Button-1>', show_login)
    root.bind('<Key>', show_login)

    # Start updating the time on splash
    update_time()

    root.mainloop()

if __name__ == "__main__":
    if "--generate-hash" in sys.argv:
        password_to_hash = input("Enter password to hash: ")
        hashed_password = hashlib.sha256(password_to_hash.encode('utf-8')).hexdigest()
        print(f"\nYour new SHA256 HASH is:\n{hashed_password}\n\nCopy this value into the STORED_HASH_HEX variable.")
    else:
        create_hashed_window_sha256()