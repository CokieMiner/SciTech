import tkinter as tk
from tkinter import ttk  # Import ttk for widgets
import ttkthemes  # For theming

class SciTechApp(ttkthemes.ThemedTk):
    def __init__(self):
        super().__init__()
        self.set_theme("plastik")
        self.title("SciTech Application")
        self.attributes("-zoomed", True)  # Maximize window cross-platform
        self._create_widgets()

    def _create_widgets(self):
        label = ttk.Label(self, text="Welcome to SciTech Application", font=("Helvetica", 16))
        label.pack(pady=20)

if __name__ == "__main__":
    app = SciTechApp()
    app.mainloop()