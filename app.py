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
safe_margin = 5  # pixels from screen edge
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

def move_up(acceleration=1):
    global safe_margin, mouse_speed
    current_x, current_y = pyautogui.position()
    screen_width, screen_height = pyautogui.size()
    return max(safe_margin, current_y - (mouse_speed * acceleration))

def move_down(acceleration=1):
    global safe_margin, mouse_speed
    current_x, current_y = pyautogui.position()
    screen_width, screen_height = pyautogui.size()
    return min(screen_height - safe_margin, current_y + (mouse_speed * acceleration))

def move_left(acceleration=1):
    global safe_margin, mouse_speed
    current_x, current_y = pyautogui.position()
    screen_width, screen_height = pyautogui.size()
    return max(safe_margin, current_x - (mouse_speed * acceleration))

def move_right(acceleration=1):
    global safe_margin, mouse_speed
    current_x, current_y = pyautogui.position()
    screen_width, screen_height = pyautogui.size()
    return min(screen_width - safe_margin, current_x + (mouse_speed * acceleration))

def handle_keypress(event):
    global active, window_message, label, alt
    
    if not active: return

    # Debug output to see all event properties
    # print(f"Event: {event.name}")

    current_x, current_y = pyautogui.position()
    screen_width, screen_height = pyautogui.size()
    safe_margin = 5  # pixels from screen edge

    if event.name == 'up':
        pyautogui.moveTo(current_x, move_up())
        window_message = "Cima"
    elif event.name == 'down':
        pyautogui.moveTo(current_x, move_down())
        window_message = "Baixo"
    elif event.name == 'left':
        pyautogui.moveTo(move_left(), current_y)
        window_message = "Esquerda"
    elif event.name == 'right':
        pyautogui.moveTo(move_right(), current_y)
        window_message = "Direita"

    if event.name == 'w':
        pyautogui.moveTo(current_x, move_up(10))
        window_message = "Cima"
    elif event.name == 'x':
        pyautogui.moveTo(current_x, move_down(10))
        window_message = "Baixo"
    elif event.name == 'a':
        pyautogui.moveTo(move_left(10), current_y)
        window_message = "Esquerda"
    elif event.name == 'd':
        pyautogui.moveTo(move_right(10), current_y)
        window_message = "Direita"

    if event.name == 'q':
        pyautogui.moveTo(move_left(10), move_up(10))
        window_message = "Diagonal superior esquerda"
    elif event.name == 'e':
        pyautogui.moveTo(move_right(10), move_up(10))
        window_message = "Diagonal superior direita"
    elif event.name == 'z':
        pyautogui.moveTo(move_left(10), move_down(10))
        window_message = "Diagonal inferior esquerda"
    elif event.name == 'c':
        pyautogui.moveTo(move_right(10), move_down(10))
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