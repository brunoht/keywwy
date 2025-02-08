import keyboard, pyautogui
import asyncio

class MouseController:

    def __init__(self, app):
        self.app = app

        self.keyboard = keyboard
        self.mouse_speed = 10  # Velocidade de movimento do mouse
        self.active = True # Estado do modo Keywwy
        self.acceleration = 1 # Aceleração do mouse
        self.last_key = None # Última tecla pressionada
        self.safe_margin = 5 # Margem de segurança
        self.keyboard.hook(self._handle_keyboard_event, suppress=self.active)
        self.modifiers = {
            'ctrl': False,
            'alt': False,
            'shift': False
        }
        self.action = False
        self.blocked = False

    def _handle_keyboard_event(self, event):
        if event.event_type == keyboard.KEY_DOWN:
            if not self.blocked:
                if not self.app.loop or self.app.loop.is_closed():
                    return False
                asyncio.run_coroutine_threadsafe(self.handle_keypress(event), self.app.loop)
        elif event.event_type == keyboard.KEY_UP:
            self.handle_keyrelease(event)
        return False

    async def handle_keypress(self, event):
        if self.blocked: return
        self.blocked = True
        print(f"key pressed: {event.name}")
        if event.name in self.modifiers:
            if self.modifiers[event.name] == True and self.last_key == event.name:
                self.modifiers[event.name] = False
                self.toggle_mode()
            elif self.modifiers[event.name] == True:
                self.modifiers[event.name] = False
                self.app.message("")
            else:
                self.modifiers[event.name] = True
                self.app.message(f"{event.name} pressionado")
        else:
            self.app.message(f"")
            self.modifiers = dict.fromkeys(self.modifiers, False)
            self.handle_action(event.name)
        self.last_key = event.name
        print(f"modifiers: {self.modifiers}")
        self.blocked = False
        return not self.active

    def handle_keyrelease(self, event):
        print(f"key released: {event.name}")
        return not self.active

    def toggle_mode(self):
        self.active = not self.active
        self.keyboard.unhook_all()
        self.keyboard.hook(self._handle_keyboard_event, suppress=self.active)
        if self.active:
            self.app.message("Keywwy ativado")
        else:
            self.app.message("Keywwy desativado")
        print(f"toggle mode: {self.active}")

    def handle_action(self, name):
        if not self.active: return

        x, y = pyautogui.position()
        w, h = pyautogui.size()

        if self.action == True:
            self.app.message(f"Ação")
            print(f"action: {name}")
            match name:
                case 'insert':
                    self.app.message(f"Canto superior esquerdo")
                    self.move_top_left()
                    self.action = False
                case 'home':
                    self.app.message(f"Centro superior")
                    self.move_top_center()
                    self.action = False
                case 'page up':
                    self.app.message(f"Canto superior direito")
                    self.move_top_right()
                    self.action = False

                case 'delete':
                    self.app.message(f"Canto esquerdo")
                    self.move_center_left()
                    self.action = False
                case 'end':
                    self.app.message(f"Centro")
                    self.move_center()
                    self.action = False
                case 'page down':
                    self.app.message(f"Canto direito")
                    self.move_center_right()
                    self.action = False

                case 'left':
                    self.app.message(f"Canto inferior esquerdo")
                    self.move_bottom_left()
                    self.action = False
                case 'down':
                    self.app.message(f"Centro inferior")
                    self.move_bottom_center()
                    self.action = False
                case 'right':
                    self.app.message(f"Canto inferior direito")
                    self.move_bottom_right()
                    self.action = False

                case _:
                    self.action = False
                    self.app.message(f"Ação cancelada")
        else:
            match name:
                case 'up':
                    self.move_up(x, y, w, h)
                    self.app.message(f"Cima")
                case 'down':
                    self.move_down(x, y, w, h)
                    self.app.message(f"Baixo")
                case 'left':
                    self.move_left(x, y, w, h)
                    self.app.message(f"Esquerda")
                case 'right':
                    self.move_right(x, y, w, h)
                    self.app.message(f"Direita")
                
                case 'insert':
                    self.move_diagonal_up_left(x, y, w, h)
                    self.app.message(f"Diagonal superior esquerda")
                case 'home':
                    self.move_diagonal_up_right(x, y, w, h)
                    self.app.message(f"Diagonal superior direita")
                case 'delete':
                    self.move_diagonal_down_left(x, y, w, h)
                    self.app.message(f"Diagonal inferior esquerda")
                case 'end':
                    self.move_diagonal_down_right(x, y, w, h)
                    self.app.message(f"Diagonal inferior direita")
                case 'page up':
                    self.roll_up()
                    self.app.message(f"Rolar para cima")
                case 'page down':
                    self.roll_down()
                    self.app.message(f"Rolar para baixo")

                case 'f':
                    self.click()
                case 'g':
                    self.click_right()
                case 'd':
                    self.speed_up()
                    self.app.message(f"Aumenta velocidade: {self.acceleration}")
                case 's':
                    self.speed_down()
                    self.app.message(f"Diminui velocidade: {self.acceleration}")
                
                case 'a':
                    self.action = True

                case _:
                    pass
    
    def move_up(self, current_x, current_y, screen_width, screen_height, exec=True):
        x = current_x
        y = max(self.safe_margin, current_y - (self.mouse_speed * self.acceleration))
        if exec : pyautogui.moveTo(x, y)
        return x, y

    def move_down(self, current_x, current_y, screen_width, screen_height, exec=True):
        x = current_x
        y = min(screen_height - self.safe_margin, current_y + (self.mouse_speed * self.acceleration))
        if exec : pyautogui.moveTo(x, y)
        return x, y 
    
    def move_left(self, current_x, current_y, screen_width, screen_height, exec=True):
        x = max(self.safe_margin, current_x - (self.mouse_speed * self.acceleration))
        y = current_y
        if exec : pyautogui.moveTo(x, y)
        return x, y 

    def move_right(self, current_x, current_y, screen_width, screen_height, exec=True):
        x = min(screen_width - self.safe_margin, current_x + (self.mouse_speed * self.acceleration))
        y = current_y
        if exec : pyautogui.moveTo(x, y)
        return x, y
    
    def move_diagonal_up_left(self, current_x, current_y, screen_width, screen_height, exec=True):
        left_x, left_y = self.move_left(current_x, current_y, screen_width, screen_height, False)
        up_x, up_y = self.move_up(current_x, current_y, screen_width, screen_height, False)
        if exec : pyautogui.moveTo(left_x, up_y)
        return left_x, up_y

    def move_diagonal_up_right(self, current_x, current_y, screen_width, screen_height, exec=True):
        right_x, right_y = self.move_right(current_x, current_y, screen_width, screen_height, False)
        up_x, up_y = self.move_up(current_x, current_y, screen_width, screen_height, False)
        if exec : pyautogui.moveTo(right_x, up_y)
        return right_x, up_y

    def move_diagonal_down_left(self, current_x, current_y, screen_width, screen_height, exec=True):
        left_x, left_y = self.move_left(current_x, current_y, screen_width, screen_height, False)
        down_x, down_y = self.move_down(current_x, current_y, screen_width, screen_height, False)
        if exec : pyautogui.moveTo(left_x, down_y)
        return left_x, down_y

    def move_diagonal_down_right(self, current_x, current_y, screen_width, screen_height, exec=True):
        right_x, right_y = self.move_right(current_x, current_y, screen_width, screen_height, False)
        down_x, down_y = self.move_down(current_x, current_y, screen_width, screen_height, False)
        if exec : pyautogui.moveTo(right_x, down_y)
        return right_x, down_y
    
    def move_center_left(self):
        pyautogui.moveTo(self.safe_margin, pyautogui.size()[1] / 2)

    def move_center_right(self):
        pyautogui.moveTo(pyautogui.size()[0] - self.safe_margin, (pyautogui.size()[1] / 2) - self.safe_margin)

    def move_center(self):
        pyautogui.moveTo(pyautogui.size()[0] / 2, pyautogui.size()[1] / 2)

    def move_top_left(self):
        pyautogui.moveTo(self.safe_margin, self.safe_margin)

    def move_top_right(self):
        pyautogui.moveTo(pyautogui.size()[0], self.safe_margin)

    def move_top_center(self):
        pyautogui.moveTo(pyautogui.size()[0] / 2, self.safe_margin)

    def move_bottom_left(self):
        pyautogui.moveTo(self.safe_margin, pyautogui.size()[1] - self.safe_margin)

    def move_bottom_right(self):
        pyautogui.moveTo(pyautogui.size()[0] - self.safe_margin, pyautogui.size()[1] - self.safe_margin)

    def move_bottom_center(self):
        pyautogui.moveTo(pyautogui.size()[0] / 2, pyautogui.size()[1] - self.safe_margin)


    def speed_up(self):
        self.acceleration = min(100, self.acceleration + 2)
    
    def speed_down(self):
        self.acceleration = max(1, self.acceleration - 2)

    def click(self):
        pyautogui.click()

    def click_right(self):
        pyautogui.click(button='right')

    def roll_up(self):
        pyautogui.scroll(self.acceleration * 10)
    
    def roll_down(self):
        pyautogui.scroll(-self.acceleration * 10)