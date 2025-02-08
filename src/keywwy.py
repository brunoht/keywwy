import os
import ctypes
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageDraw
from pystray import Icon, MenuItem, Menu

class Keywwy:

    def __init__(self):
        self.app_name = "Keywwy"
        self.window_message = "Aplicação Iniciada"

        self.root = Tk()
        self.root.title(self.app_name)

        # center window
        self.windowWidth = self.root.winfo_reqwidth()
        self.windowHeight = self.root.winfo_reqheight()
        self.positionRight = int(self.root.winfo_screenwidth()/2 - self.windowWidth/2)
        self.positionDown = int(self.root.winfo_screenheight()/2 - self.windowHeight/2)
        self.root.geometry("+{}+{}".format(self.positionRight, self.positionDown))

        self.root.attributes('-alpha', 0.2) # window 50% transparent
        self.root.overrideredirect(True) # hide window border
        self.root.wm_attributes("-topmost", True) # window always on top
        self.root.geometry("300x50") # window size
        self.root.resizable(False, False) # window not resizable
        self.root.attributes("-transparentcolor", "white") # window click through

        # window text
        self.label = Label(self.root, text=self.window_message, font=("Arial", 12))
        self.label.pack()

        # Schedule after window is created (click through)
        self.root.after(10, self.make_click_through)

    def message(self, message):
        self.label.config(text=message)

    def make_click_through(self):
        WS_EX_TRANSPARENT = 0x00000020
        GWL_EXSTYLE = -20
        hwnd = ctypes.windll.user32.GetForegroundWindow() # Get window handle
        style = ctypes.windll.user32.GetWindowLongA(hwnd, GWL_EXSTYLE) # Get window style
        ctypes.windll.user32.SetWindowLongA(hwnd, GWL_EXSTYLE, style | WS_EX_TRANSPARENT) # Add transparent flag

    def create_image(self):
        image = Image.new('RGB', (64, 64), (255, 255, 255))
        dc = ImageDraw.Draw(image)
        dc.rectangle((0, 0, 64, 64), fill=(0, 0, 0))
        return image

    def setup_tray(self):
        icon_image = self.create_image()
        menu = Menu(
            MenuItem('Sair', self.quit_app)
        )
        icon = Icon(self.app_name, icon_image, menu=menu)
        return icon

    def quit_app(self, icon, item):
        self.icon.stop()
        self.root.after(0, self.root.destroy)  # Schedule destroy on main thread
        self.root.quit()
        os._exit(0)  # Force terminate all threads

    def run(self):
        self.icon = self.setup_tray()
        self.icon.run_detached()
        self.root.protocol('WM_DELETE_WINDOW', lambda: quit_app(icon, None))  # Handle window close
        self.root.mainloop()