import pyautogui
import keyboard

class KeyttyClone:
    def __init__(self):
        self.mouse_speed = 10  # Velocidade de movimento do mouse
        self.active = False  # Estado do modo Keytty

        # Configurar atalhos
        keyboard.add_hotkey('ctrl+shift+space', self.toggle_mode)
        self.setup_controls()

        

    def toggle_mode(self):
        self.active = not self.active
        if self.active:
            print("Modo Keytty ativado")
        else:
            print("Modo Keytty desativado")

    def setup_controls(self):
        # Movimento simples
        keyboard.add_hotkey('h', lambda: self.move_mouse(-self.mouse_speed, 0))
        keyboard.add_hotkey('k', lambda: self.move_mouse(0, -self.mouse_speed))
        keyboard.add_hotkey('l', lambda: self.move_mouse(self.mouse_speed, 0))
        keyboard.add_hotkey('j', lambda: self.move_mouse(0, self.mouse_speed))

        # Movimento de seção
        keyboard.add_hotkey('c', lambda: self.move_to_section('center'))
        keyboard.add_hotkey('w', lambda: self.move_to_section('top_left'))
        keyboard.add_hotkey('e', lambda: self.move_to_section('top_right'))
        keyboard.add_hotkey('s', lambda: self.move_to_section('bottom_left'))
        keyboard.add_hotkey('d', lambda: self.move_to_section('bottom_right'))

        # Ações
        keyboard.add_hotkey('a', self.perform_action)

    def move_mouse(self, x, y):
        if self.active:
            pyautogui.moveRel(x, y)

    def move_to_section(self, position):
        if self.active:
            width, height = pyautogui.size()
            positions = {
                'center': (width / 2, height / 2),
                'top_left': (0, 0),
                'top_right': (width, 0),
                'bottom_left': (0, height),
                'bottom_right': (width, height),
            }
            pyautogui.moveTo(*positions[position])

    def perform_action(self):
        if not self.active:
            return

        print("Digite o comando de ação:")
        command = keyboard.read_event().name

        actions = {
            ',': lambda: pyautogui.click(button='left'),
            '.': lambda: pyautogui.click(button='right'),
            ';': lambda: pyautogui.doubleClick(),
            'o': lambda: pyautogui.scroll(100),
            'p': lambda: pyautogui.scroll(-100),
            '[': lambda: pyautogui.hscroll(-100),
            ']': lambda: pyautogui.hscroll(100),
            'n': lambda: pyautogui.mouseDown(),
            'm': lambda: pyautogui.mouseUp(),
        }

        if command in actions:
            actions[command]()

if __name__ == "__main__":
    app = KeyttyClone()
    print("Aplicativo iniciado. Pressione Ctrl+Shift+Space para ativar/desativar o modo Keytty.")
    keyboard.wait('esc')  # O aplicativo continua rodando até que 'esc' seja pressionado