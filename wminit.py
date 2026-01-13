import tkinter as tk
from tkinter import ttk, messagebox
# Import Image and ImageTk from Pillow (pip install Pillow)
from PIL import Image, ImageTk, ImageOps

# Use the modern constant for resampling
# For older versions of Pillow, use Image.ANTIALIAS
try:
    Resampling = Image.Resampling.LANCZOS
except AttributeError:
    pass


# --- Calculator Application Class (remains the same) ---
class CalculatorApp:
    def __init__(self, parent_window):
        self.window = parent_window
        self.window.title("Calculator")
        self.window.geometry("300x400")
        self.window.resizable(0, 0)
        self.window.configure(bg='#f0f0f0')
        self.expression = ""
        self.input_text = tk.StringVar()
        input_frame = tk.Frame(self.window, width=300, height=50, bd=0, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        input_frame.pack(side=tk.TOP)
        input_field = tk.Entry(input_frame, font=('arial', 18, 'bold'), textvariable=self.input_text, width=50, bg="#eee", bd=0, justify=tk.RIGHT)
        input_field.pack(ipady=10)
        btns_frame = tk.Frame(self.window, width=300, height=350, bg="grey")
        btns_frame.pack()
        tk.Button(btns_frame, text="C", width=32, height=3, bd=0, bg="#eee", cursor="hand2", command=lambda: self.clear_display()).grid(row=0, column=0, columnspan=3, padx=1, pady=1)
        tk.Button(btns_frame, text="/", width=10, height=3, bd=0, bg="#eee", cursor="hand2", command=lambda: self.on_button_click("/")).grid(row=0, column=3, padx=1, pady=1)
        tk.Button(btns_frame, text="7", width=10, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: self.on_button_click("7")).grid(row=1, column=0, padx=1, pady=1)
        tk.Button(btns_frame, text="8", width=10, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: self.on_button_click("8")).grid(row=1, column=1, padx=1, pady=1)
        tk.Button(btns_frame, text="9", width=10, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: self.on_button_click("9")).grid(row=1, column=2, padx=1, pady=1)
        tk.Button(btns_frame, text="*", width=10, height=3, bd=0, bg="#eee", cursor="hand2", command=lambda: self.on_button_click("*")).grid(row=1, column=3, padx=1, pady=1)
        tk.Button(btns_frame, text="4", width=10, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: self.on_button_click("4")).grid(row=2, column=0, padx=1, pady=1)
        tk.Button(btns_frame, text="5", width=10, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: self.on_button_click("5")).grid(row=2, column=1, padx=1, pady=1)
        tk.Button(btns_frame, text="6", width=10, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: self.on_button_click("6")).grid(row=2, column=2, padx=1, pady=1)
        tk.Button(btns_frame, text="-", width=10, height=3, bd=0, bg="#eee", cursor="hand2", command=lambda: self.on_button_click("-")).grid(row=2, column=3, padx=1, pady=1)
        tk.Button(btns_frame, text="1", width=10, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: self.on_button_click("1")).grid(row=3, column=0, padx=1, pady=1)
        tk.Button(btns_frame, text="2", width=10, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: self.on_button_click("2")).grid(row=3, column=1, padx=1, pady=1)
        tk.Button(btns_frame, text="3", width=10, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: self.on_button_click("3")).grid(row=3, column=2, padx=1, pady=1)
        tk.Button(btns_frame, text="+", width=10, height=3, bd=0, bg="#eee", cursor="hand2", command=lambda: self.on_button_click("+")).grid(row=3, column=3, padx=1, pady=1)
        tk.Button(btns_frame, text="0", width=21, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: self.on_button_click("0")).grid(row=4, column=0, columnspan=2, padx=1, pady=1)
        tk.Button(btns_frame, text=".", width=10, height=3, bd=0, bg="#eee", cursor="hand2", command=lambda: self.on_button_click(".")).grid(row=4, column=2, padx=1, pady=1)
        tk.Button(btns_frame, text="=", width=10, height=3, bd=0, bg="#eee", cursor="hand2", command=lambda: self.calculate_result()).grid(row=4, column=3, padx=1, pady=1)
    
    def on_button_click(self, char):
        self.expression += str(char)
        self.input_text.set(self.expression)
    def clear_display(self):
        self.expression = ""
        self.input_text.set("")
    def calculate_result(self):
        try:
            result = str(eval(self.expression))
            self.input_text.set(result)
            self.expression = result
        except Exception as e:
            messagebox.showerror("Error", "Invalid input or calculation error.")
            self.expression = ""
            self.input_text.set("")


# --- Main Desktop Simulation Class ---
class DesktopSim:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulated Desktop")
        self.root.attributes("-fullscreen", True)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Store a reference to the original background image
        self.original_bg_image = None
        self.bg_image_tk = None
        self.background_label = None
        self.bg_image_path = 'bg5.png' # Set your 4K image path here

        # Desktop Area
        self.desktop_frame = tk.Frame(root, bg='darkblue')
        self.desktop_frame.grid(row=0, column=0, sticky='nsew')
        
        # Load and set up the initial background
        self.load_background()
        
        # Bind the resize event to the dynamic_resize function
        # This calls dynamic_resize whenever the desktop_frame changes size
        self.desktop_frame.bind('<Configure>', self.dynamic_resize)

        # Taskbar Area
        self.taskbar_frame = tk.Frame(root, bg='gray', height=40)
        self.taskbar_frame.grid(row=1, column=0, sticky='nsew')
        self.taskbar_frame.grid_propagate(False)

        # Add Taskbar Buttons
        tk.Button(self.taskbar_frame, text="Start", command=self.show_menu).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.taskbar_frame, text="App 1", command=self.open_app1).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.taskbar_frame, text="Calc", command=self.open_calculator).pack(side=tk.LEFT, padx=5, pady=5)


    def load_background(self):
        """Loads the original background image file."""
        try:
            # Open image using Pillow and store the original
            self.original_bg_image = Image.open(self.bg_image_path)
            # The initial display will happen via dynamic_resize called by the <Configure> event
        except FileNotFoundError:
            print(f"Background image '{self.bg_image_path}' not found. Using default darkblue background.")
        except Exception as e:
            print(f"An error occurred loading the background image: {e}")

    def dynamic_resize(self, event):
        """Dynamically resizes the background image to fill the desktop frame."""
        if self.original_bg_image is None:
            return

        # Get current width and height of the desktop frame
        current_width = event.width
        current_height = event.height

        if current_width <= 0 or current_height <= 0:
            return

        # Resize the original image using high-quality LANCZOS resampling
        # This prevents the image from becoming pixelated when scaling down a 4K image
        resized_image = self.original_bg_image.resize(
            (current_width, current_height), 
            Resampling
        )
        
        # Create a Tkinter compatible photo image
        self.bg_image_tk = ImageTk.PhotoImage(resized_image)

        # Update the label with the new image
        if self.background_label is None:
            self.background_label = tk.Label(self.desktop_frame, image=self.bg_image_tk)
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
            # Send the label to the bottom layer so other widgets/icons appear on top
            self.background_label.lower() 
        else:
            self.background_label.configure(image=self.bg_image_tk)


    def show_menu(self):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Open App 1", command=self.open_app1)
        menu.add_command(label="Calculator", command=self.open_calculator)
        menu.add_command(label="Exit", command=self.root.destroy)
        try:
            menu.tk_popup(self.root.winfo_pointerx(), self.root.winfo_pointery() - 100)
        finally:
            menu.grab_release()

    def open_app1(self):
        app_window = tk.Toplevel(self.root)
        app_window.title("Application 1")
        app_window.geometry("400x300")
        tk.Label(app_window, text="This is a simulated application window.").pack(pady=20)
        tk.Button(app_window, text="Close", command=app_window.destroy).pack(pady=10)

    def open_calculator(self):
        calc_window = tk.Toplevel(self.root)
        CalculatorApp(calc_window)


if __name__ == "__main__":
    root = tk.Tk()
    desktop_sim = DesktopSim(root)
    root.mainloop()
