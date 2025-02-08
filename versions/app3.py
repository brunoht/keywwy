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
current_key = None
acceleration = 1
last_key_time = 0
waiting_for_shift = False

root = Tk()
root.title("Mouse Controller")
activation_command = 'ctrl+ctrl'

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

def toggle_active(e):
    global waiting_for_shift
    if e.name == 'ctrl':
        waiting_for_shift = True
    elif e.name == 'shift' and waiting_for_shift:
        # active = not active
        # window_message = "Modo Keywwy ativado" if active else "Modo Keywwy desativado"
        # label.config(text=window_message)
        waiting_for_shift = False
        toggle_control_mode()
    else:
        waiting_for_shift = False
    

# keyboard.on_press(toggle_active)

def toggle_control_mode():
    global active, activation_command, window_message, label
    active = not active
    if active:
        print("Modo Keywwy ativado")
        # Start suppressing keys when active
        keyboard.on_press(handle_keypress, suppress=True)
        keyboard.on_release(handle_keyrelease, suppress=True)
        window_message = "Modo Keywwy ativado"
        label.config(text=window_message)
        # bring window to front
        root.deiconify()
    else:
        print("Modo Keywwy desativado")
        # Stop suppressing keys when inactive
        keyboard.unhook_all()
        # Reattach only the toggle hotkey
        keyboard.add_hotkey(activation_command, toggle_control_mode)

def move_up():
    global safe_margin, mouse_speed, acceleration
    current_x, current_y = pyautogui.position()
    screen_width, screen_height = pyautogui.size()
    return max(safe_margin, current_y - (mouse_speed * acceleration))

def move_down():
    global safe_margin, mouse_speed, acceleration
    current_x, current_y = pyautogui.position()
    screen_width, screen_height = pyautogui.size()
    return min(screen_height - safe_margin, current_y + (mouse_speed * acceleration))

def move_left():
    global safe_margin, mouse_speed, acceleration
    current_x, current_y = pyautogui.position()
    screen_width, screen_height = pyautogui.size()
    return max(safe_margin, current_x - (mouse_speed * acceleration))

def move_right():
    global safe_margin, mouse_speed, acceleration
    current_x, current_y = pyautogui.position()
    screen_width, screen_height = pyautogui.size()
    return min(screen_width - safe_margin, current_x + (mouse_speed * acceleration))

def speed_up():
    global acceleration
    acceleration = min(10, acceleration + 5)

def speed_down():
    global acceleration
    acceleration = max(1, acceleration - 5)

def handle_keypress(event):
    global active, current_key
    toggle_active(event)
    if not active or event.name == current_key: return
    current_key = event.name # Store the current pressed key
    handle_movement(current_key)

def handle_keyrelease(event):
    global current_key
    if event.name == current_key:
        current_key = None

def handle_movement(key):
    global alt, window_message, label, acceleration

    if not key: return

    current_x, current_y = pyautogui.position()
    screen_width, screen_height = pyautogui.size()
    safe_margin = 5  # pixels from screen edge

    if key == 'up':
        pyautogui.moveTo(current_x, move_up())
        window_message = "Cima"
    elif key == 'down':
        pyautogui.moveTo(current_x, move_down())
        window_message = "Baixo"
    elif key == 'left':
        pyautogui.moveTo(move_left(), current_y)
        window_message = "Esquerda"
    elif key == 'right':
        pyautogui.moveTo(move_right(), current_y)
        window_message = "Direita"

    elif key == 'q':
        speed_up()
        window_message = f"Acelerando: {acceleration}"

    elif key == 'a':
        speed_down()
        window_message = f"Desacelerando: {acceleration}"

    # if key == 'w':
    #     pyautogui.moveTo(current_x, move_up(10))
    #     window_message = "Cima"
    # elif key == 's':
    #     pyautogui.moveTo(current_x, move_down(10))
    #     window_message = "Baixo"
    # elif key == 'a':
    #     pyautogui.moveTo(move_left(10), current_y)
    #     window_message = "Esquerda"
    # elif key == 'd':
    #     pyautogui.moveTo(move_right(10), current_y)
    #     window_message = "Direita"

    if key == 'w':
        pyautogui.moveTo(move_left(), move_up())
        window_message = "Diagonal superior esquerda"
    elif key == 'e':
        pyautogui.moveTo(move_right(), move_up())
        window_message = "Diagonal superior direita"
    elif key == 's':
        pyautogui.moveTo(move_left(), move_down())
        window_message = "Diagonal inferior esquerda"
    elif key == 'd':
        pyautogui.moveTo(move_right(), move_down())
        window_message = "Diagonal inferior direita"

    #center of the screen
    elif key == 'c':
        width, height = pyautogui.size()
        pyautogui.moveTo(width / 2, height / 2)
        window_message = "Center"

    elif key == 'alt':
        alt = not alt
        window_message = ""

    elif key == 'z':
        if alt:
            # simulate alt+click
            keyboard.press('alt')
            pyautogui.click()
            keyboard.release('alt')
        else:
            pyautogui.click()
        window_message = "Click"

    elif key == 'x':
        pyautogui.rightClick()
        window_message = "Right Click"

    # elif key == 'space':
    #     toggle_control_mode()
    #     window_message = "Modo Keywwy desativado"
    #     # minimize window to tray
    #     root.withdraw()

    

    if alt:
        label.config(text=f"ALT + {window_message}")
    else:
        label.config(text=window_message)

# Initial setup - only attach the toggle hotkey

# keyboard.add_hotkey(activation_command, toggle_control_mode)

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
keyboard.on_release(handle_keyrelease, suppress=True)

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