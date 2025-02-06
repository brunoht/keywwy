import tkinter as tk
import pyautogui
import keyboard
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw

class MouseControllerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mouse Controller")
        self.root.geometry("300x50")
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(1)  # Remover bordas da janela
        self.label = tk.Label(root, text="", font=("Arial", 12))
        self.label.pack()
        #centralize o label no centro da tela   
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.root.update_idletasks()
        self.root.lift()
        self.root.focus_force()


        # Variáveis para controle
        self.running = True
        self.mouse_speed = 10  # Velocidade de movimento do mouse

        # Iniciar a detecção do teclado
        self.start_keyboard_detection()

    def start_keyboard_detection(self):
        keyboard.add_hotkey('ctrl+shift+m', self.toggle_control_mode)

    def toggle_control_mode(self):
        self.running = not self.running
        if self.running:
            self.label.config(text="Modo de Controle Ativado")
            self.control_mouse()
        else:
            self.label.config(text="Modo de Controle Desativado")

    def control_mouse(self):
        if self.running:
            if keyboard.is_pressed('w'):
                pyautogui.moveRel(0, -self.mouse_speed)
                self.label.config(text="Comando: w (Cima)")
            elif keyboard.is_pressed('s'):
                pyautogui.moveRel(0, self.mouse_speed)
                self.label.config(text="Comando: s (Baixo)")
            elif keyboard.is_pressed('a'):
                pyautogui.moveRel(-self.mouse_speed, 0)
                self.label.config(text="Comando: a (Esquerda)")
            elif keyboard.is_pressed('d'):
                pyautogui.moveRel(self.mouse_speed, 0)
                self.label.config(text="Comando: d (Direita)")
            elif keyboard.is_pressed(';'):
                pyautogui.click()
                self.label.config(text="Comando: ; (Clique)")

            # Chama novamente para continuar verificando
            self.root.after(100, self.control_mouse)

    def quit(self, icon, item):
        self.running = False
        icon.stop()
        self.root.quit()

def create_image():
    # Criação de um ícone de tray simples
    image = Image.new('RGB', (64, 64), (255, 255, 255))
    dc = ImageDraw.Draw(image)
    dc.rectangle((0, 0, 64, 64), fill=(0, 0, 0))
    return image

def setup_tray(app):
    # Configuração do ícone de tray
    icon_image = create_image()
    menu = Menu(MenuItem('Quit', app.quit))
    icon = Icon("Mouse Controller", icon_image, menu=menu)
    icon.run_detached()

if __name__ == "__main__":
    root = tk.Tk()
    app = MouseControllerApp(root)
    setup_tray(app)
    root.mainloop()