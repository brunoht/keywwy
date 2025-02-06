import sys, os
import keyboard
import ctypes
import pyautogui
from tkinter import *
from tkinter import ttk
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw

WS_EX_TRANSPARENT = 0x00000020
GWL_EXSTYLE = -20

mouse_speed = 10  # Velocidade de movimento do mouse
active = True  # Estado do modo Keywwy
alt = False
window_message = "Modo Keywwy ativado"

root = Tk()
root.title("Mouse Controller")

# center window
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
root.geometry("+{}+{}".format(positionRight, positionDown))

# window 50% transparent
root.attributes('-alpha', 0.2)

# hide window border
root.overrideredirect(True)

# window always on top
root.wm_attributes("-topmost", True)

# window size
root.geometry("300x50")

# window not resizable
root.resizable(False, False)

# window click through
root.attributes("-transparentcolor", "white")

# window text
label = Label(root, text=window_message, font=("Arial", 12))
label.pack()

def toggle_control_mode():
    global active
    active = not active
    if active:
        print("Modo Keywwy ativado")
        # Start suppressing keys when active
        keyboard.on_press(handle_keypress, suppress=True)
        window_message = "Modo Keywwy ativado"
        label.config(text=window_message)
        # bring window to front
        root.deiconify()
    else:
        print("Modo Keywwy desativado")
        # Stop suppressing keys when inactive
        keyboard.unhook_all()
        # Reattach only the toggle hotkey
        keyboard.add_hotkey('ctrl+shift+alt', toggle_control_mode)

def handle_keypress(event):
    global active, window_message, label, alt
    
    if not active: return

    # Debug output to see all event properties
    print(f"Event: {event.name}")

    if event.name == 'up':
        current_x, current_y = pyautogui.position()
        pyautogui.moveTo(current_x, current_y - mouse_speed)
        window_message = "Cima"
    elif event.name == 'down':
        current_x, current_y = pyautogui.position()
        pyautogui.moveTo(current_x, current_y + mouse_speed)
        window_message = "Baixo"
    elif event.name == 'left':
        current_x, current_y = pyautogui.position()
        pyautogui.moveTo(current_x - mouse_speed, current_y)
        window_message = "Esquerda"
    elif event.name == 'right':
        current_x, current_y = pyautogui.position()
        pyautogui.moveTo(current_x + mouse_speed, current_y)
        window_message = "Direita"

    if event.name == 'w':
        current_x, current_y = pyautogui.position()
        pyautogui.moveTo(current_x, current_y - (mouse_speed*10))
        window_message = "Cima 10x"
    elif event.name == 'x':
        current_x, current_y = pyautogui.position()
        pyautogui.moveTo(current_x, current_y + (mouse_speed*10))
        window_message = "Baixo 10x"
    elif event.name == 'a':
        current_x, current_y = pyautogui.position()
        pyautogui.moveTo(current_x - (mouse_speed*10), current_y)
        window_message = "Esquerda 10x"
    elif event.name == 'd':
        current_x, current_y = pyautogui.position()
        pyautogui.moveTo(current_x + (mouse_speed*10), current_y)
        window_message = "Direita 10x"

    if event.name == 'q':
        current_x, current_y = pyautogui.position()
        pyautogui.moveTo(current_x - (mouse_speed*10), current_y - (mouse_speed*10))
        window_message = "Diagonal superior esquerda"
    elif event.name == 'e':
        current_x, current_y = pyautogui.position()
        pyautogui.moveTo(current_x + (mouse_speed*10), current_y - (mouse_speed*10))
        window_message = "Diagonal superior direita"
    elif event.name == 'z':
        current_x, current_y = pyautogui.position()
        pyautogui.moveTo(current_x - (mouse_speed*10), current_y + (mouse_speed*10))
        window_message = "Diagonal inferior esquerda"
    elif event.name == 'c':
        current_x, current_y = pyautogui.position()
        pyautogui.moveTo(current_x + (mouse_speed*10), current_y + (mouse_speed*10))
        window_message = "Diagonal inferior direita"

    #center of the screen
    elif event.name == 's':
        width, height = pyautogui.size()
        pyautogui.moveTo(width / 2, height / 2)
        window_message = "Center"

    elif event.name == 'alt':
        alt = not alt
        window_message = ""

    elif event.name == 'space':
        if alt:
            # simulate alt+click
            keyboard.press('alt')
            pyautogui.click()
            keyboard.release('alt')
        else:
            pyautogui.click()
        window_message = "Click"


    elif event.name == 'esc':
        toggle_control_mode()
        window_message = "Modo Keywwy desativado"
        # minimize window to tray
        root.withdraw()

    if alt:
        label.config(text=f"ALT + {window_message}")
    else:
        label.config(text=window_message)

# Initial setup - only attach the toggle hotkey
keyboard.add_hotkey('ctrl+shift+alt', toggle_control_mode)

def make_click_through():
    # Get window handle
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    # Get window style
    style = ctypes.windll.user32.GetWindowLongA(hwnd, GWL_EXSTYLE)
    # Add transparent flag
    ctypes.windll.user32.SetWindowLongA(hwnd, GWL_EXSTYLE, style | WS_EX_TRANSPARENT)

# Add this after window creation
root.after(10, make_click_through)  # Schedule after window is created

print("Modo Keywwy ativado")
# Start suppressing keys when active
keyboard.on_press(handle_keypress, suppress=True)

def create_image():
    image = Image.new('RGB', (64, 64), (255, 255, 255))
    dc = ImageDraw.Draw(image)
    dc.rectangle((0, 0, 64, 64), fill=(0, 0, 0))
    return image

def quit_app(icon, item):
    keyboard.unhook_all()
    icon.stop()
    root.after(0, root.destroy)  # Schedule destroy on main thread
    root.quit()
    os._exit(0)  # Force terminate all threads

def setup_tray():
    icon_image = create_image()
    menu = Menu(
        MenuItem('Quit', quit_app)
    )
    icon = Icon("Mouse Controller", icon_image, menu=menu)
    return icon

def start_app():
    icon = setup_tray()
    icon.run_detached()
    root.protocol('WM_DELETE_WINDOW', lambda: quit_app(icon, None))  # Handle window close
    root.mainloop()

if __name__ == '__main__':
    start_app()