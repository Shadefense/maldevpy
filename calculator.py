import tkinter as tk
from tkinter import ttk, messagebox

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
if __name__ == "__main__":
    app = CalculatorApp
    root = tk.Tk()
    root.mainloop()