import keyboard, pyautogui
import asyncio

class MouseController:

    def __init__(self, app):
        self.app = app
        self.config = app.config

        self.keyboard = keyboard
        self.mouse_speed = 10  # Velocidade de movimento do mouse
        self.active = True # Estado do modo Keywwy
        self.acceleration = 1 # Aceleração do mouse
        self.last_key = None # Última tecla pressionada
        self.safe_margin = 5 # Margem de segurança
        self.keyboard.hook(self._handle_keyboard_event, suppress=self.active)
        self.modifiers = {
            'esc': False,
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
        self.app.log(f"key pressed: {event.name}")
        if event.name in self.modifiers:
            if self.modifiers[event.name] == True and self.last_key == event.name and event.name == self.config.toggle:
                self.modifiers[event.name] = False
                self.toggle_mode()
            elif self.modifiers[event.name] == True:
                self.modifiers[event.name] = False
                self.app.message("")
            else:
                self.modifiers[event.name] = True
                self.app.message(f"{event.name} pressed")
        else:
            self.app.message(f"")
            self.modifiers = dict.fromkeys(self.modifiers, False)
            self.handle_action(event.name)
        self.last_key = event.name
        self.app.log(f"modifiers: {self.modifiers}")
        self.blocked = False
        return not self.active

    def handle_keyrelease(self, event):
        self.app.log(f"key released: {event.name}")
        return not self.active

    def toggle_mode(self):
        self.active = not self.active
        self.keyboard.unhook_all()
        self.keyboard.hook(self._handle_keyboard_event, suppress=self.active)
        if self.active:
            self.app.message("Keywwy enabled")
        else:
            self.app.message("Keywwy disabled")
        self.app.log(f"toggle mode: {self.active}")

    def handle_action(self, name):
        if not self.active: return

        x, y = pyautogui.position()
        w, h = pyautogui.size()

        if self.action == True: # ACTION MODE
            
            match name:
                case self.config.action_move_top_left:
                    self.action_move_top_left()
                case self.config.action_move_top_center:
                    self.action_move_top_center()
                case self.config.action_move_top_right:
                    self.action_move_top_right()
                    
                case self.config.action_move_middle_left:
                    self.action_move_middle_left()
                case self.config.action_move_middle_center:
                    self.action_move_middle_center()
                case self.config.action_move_middle_right:
                    self.action_move_middle_right()

                case self.config.action_move_bottom_left:
                    self.action_move_bottom_left()
                case self.config.action_move_bottom_center:
                    self.action_move_bottom_center()
                case self.config.action_move_bottom_right:
                    self.action_move_bottom_right()

                case self.config.action_click_hold:
                    self.action_click_hold()

                case self.config.action_click_release:
                    self.action_click_release()

                case _:
                    self.action_canceled()
        else:
            match name:
                case self.config.move_up:
                    self.action_move_up(x, y, w, h)
                case self.config.move_down:
                    self.action_move_down(x, y, w, h)
                case self.config.move_left:
                    self.action_move_left(x, y, w, h)
                case self.config.move_right:
                    self.action_move_right(x, y, w, h)
                
                case self.config.move_diagonal_up_left:
                    self.action_move_diagonal_up_left(x, y, w, h)
                case self.config.move_diagonal_up_right:
                    self.action_move_diagonal_up_right(x, y, w, h)
                case self.config.move_diagonal_down_left:
                    self.action_move_diagonal_down_left(x, y, w, h)
                case self.config.move_diagonal_down_right:
                    self.action_move_diagonal_down_right(x, y, w, h)
                case self.config.mouse_scroll_up:
                    self.action_mouse_scroll_up()
                case self.config.mouse_scroll_down:
                    self.action_mouse_scroll_down()

                case self.config.mouse_click:
                    self.action_mouse_click()
                case self.config.mouse_click_right:
                    self.action_mouse_click_right()
                case self.config.speed_up:
                    self.action_speed_up()
                case self.config.speed_down:
                    self.action_speed_down()
                
                case self.config.action:
                    self.action_mode()

                case _:
                    pass
    
    def move_up(self, current_x, current_y, screen_width, screen_height):
        x = current_x
        y = max(self.safe_margin, current_y - (self.mouse_speed * self.acceleration))
        return x, y

    def move_down(self, current_x, current_y, screen_width, screen_height):
        x = current_x
        y = min(screen_height - self.safe_margin, current_y + (self.mouse_speed * self.acceleration))
        return x, y 
    
    def move_left(self, current_x, current_y, screen_width, screen_height):
        x = max(self.safe_margin, current_x - (self.mouse_speed * self.acceleration))
        y = current_y
        return x, y 

    def move_right(self, current_x, current_y, screen_width, screen_height):
        x = min(screen_width - self.safe_margin, current_x + (self.mouse_speed * self.acceleration))
        y = current_y
        return x, y
    
    def move_diagonal_up_left(self, current_x, current_y, screen_width, screen_height):
        left_x, left_y = self.move_left(current_x, current_y, screen_width, screen_height)
        up_x, up_y = self.move_up(current_x, current_y, screen_width, screen_height)
        return left_x, up_y

    def move_diagonal_up_right(self, current_x, current_y, screen_width, screen_height):
        right_x, right_y = self.move_right(current_x, current_y, screen_width, screen_height)
        up_x, up_y = self.move_up(current_x, current_y, screen_width, screen_height)
        return right_x, up_y

    def move_diagonal_down_left(self, current_x, current_y, screen_width, screen_height):
        left_x, left_y = self.move_left(current_x, current_y, screen_width, screen_height)
        down_x, down_y = self.move_down(current_x, current_y, screen_width, screen_height)
        return left_x, down_y

    def move_diagonal_down_right(self, current_x, current_y, screen_width, screen_height):
        right_x, right_y = self.move_right(current_x, current_y, screen_width, screen_height)
        down_x, down_y = self.move_down(current_x, current_y, screen_width, screen_height)
        return right_x, down_y
    
    def action_mode(self):
        self.action = True
        self.app.message(message="Action Mode", log=f"action: {self.action}")

    def action_canceled(self):
        self.action = False
        self.app.message(f"Action Canceled", log=f"action: {self.action}")

    def action_move_middle_left(self):
        self.app.message(f"Move middle left")
        pyautogui.moveTo(self.safe_margin, pyautogui.size()[1] / 2)
        self.action = False

    def action_move_middle_right(self):
        self.app.message(f"Move middle right")
        pyautogui.moveTo(pyautogui.size()[0] - self.safe_margin, (pyautogui.size()[1] / 2) - self.safe_margin)
        self.action = False

    def action_move_middle_center(self):
        self.app.message(f"Move middle center")
        pyautogui.moveTo(pyautogui.size()[0] / 2, pyautogui.size()[1] / 2)
        self.action = False

    def action_move_top_left(self):
        self.app.message(f"Move top left")
        pyautogui.moveTo(self.safe_margin, self.safe_margin)
        self.action = False

    def action_move_top_right(self):
        self.app.message(f"Move top right")
        pyautogui.moveTo(pyautogui.size()[0], self.safe_margin)
        self.action = False

    def action_move_top_center(self):
        self.app.message(f"Move top center")
        pyautogui.moveTo(pyautogui.size()[0] / 2, self.safe_margin)
        self.action = False

    def action_move_bottom_left(self):
        self.app.message(f"Move bottom left")
        pyautogui.moveTo(self.safe_margin, pyautogui.size()[1] - self.safe_margin)
        self.action = False

    def action_move_bottom_right(self):
        self.app.message(f"Move bottom right")
        pyautogui.moveTo(pyautogui.size()[0] - self.safe_margin, pyautogui.size()[1] - self.safe_margin)
        self.action = False

    def action_move_bottom_center(self):
        self.app.message(f"Move bottom center")
        pyautogui.moveTo(pyautogui.size()[0] / 2, pyautogui.size()[1] - self.safe_margin)
        self.action = False

    def set_speed(self, speed):
        self.acceleration = speed

    def action_speed_up(self):
        self.acceleration = min(100, self.acceleration + 2)
        self.app.message(f"Speed up: {self.acceleration}")
        self.action = False
    
    def action_speed_down(self):
        self.acceleration = max(1, self.acceleration - 2)
        self.app.message(f"Speed down: {self.acceleration}")
        self.action = False

    def action_mouse_click(self):
        pyautogui.click()
        self.action = False

    def action_mouse_click_right(self):
        pyautogui.click(button='right')
        self.action = False

    def action_move_up(self, current_x, current_y, screen_width, screen_height):
        self.app.message(f"Move up")
        x, y = self.move_up(current_x, current_y, screen_width, screen_height)
        pyautogui.moveTo(x, y)
        self.action = False

    def action_move_down(self, current_x, current_y, screen_width, screen_height):
        self.app.message(f"Move down")
        x, y = self.move_down(current_x, current_y, screen_width, screen_height)
        pyautogui.moveTo(x, y)
        self.action = False
    
    def action_move_left(self, current_x, current_y, screen_width, screen_height):
        self.app.message(f"Mode left")
        x, y = self.move_left(current_x, current_y, screen_width, screen_height)
        pyautogui.moveTo(x, y)
        self.action = False

    def action_move_right(self, current_x, current_y, screen_width, screen_height):
        self.app.message(f"Move right")
        x, y = self.move_right(current_x, current_y, screen_width, screen_height)
        pyautogui.moveTo(x, y)
        self.action = False

    def action_move_diagonal_up_left(self, current_x, current_y, screen_width, screen_height):
        self.app.message(f"Move diagonal up left")
        x, y = self.move_diagonal_up_left(current_x, current_y, screen_width, screen_height)
        pyautogui.moveTo(x, y)
        self.action = False

    def action_move_diagonal_up_right(self, current_x, current_y, screen_width, screen_height):
        self.app.message(f"Move diagonal up right")
        x, y = self.move_diagonal_up_right(current_x, current_y, screen_width, screen_height)
        pyautogui.moveTo(x, y)
        self.action = False
    
    def action_move_diagonal_down_left(self, current_x, current_y, screen_width, screen_height):
        self.app.message(f"Diagonal inferior esquerda")
        x, y = self.move_diagonal_down_left(current_x, current_y, screen_width, screen_height)
        pyautogui.moveTo(x, y)
        self.action = False
    
    def action_move_diagonal_down_right(self, current_x, current_y, screen_width, screen_height):
        self.app.message(f"Move diagonal down right")
        x, y = self.move_diagonal_down_right(current_x, current_y, screen_width, screen_height)
        pyautogui.moveTo(x, y)
        self.action = False

    def action_click_hold(self):
        self.app.message(f"Click hold")
        pyautogui.mouseDown()
        self.action = False

    def action_click_release(self):
        self.app.message(f"Click released")
        pyautogui.mouseUp()
        self.action = False

    def action_mouse_scroll_up(self):
        pyautogui.scroll(self.acceleration * 10)
        self.app.message(message="Scroll Up")
        self.action = False
    
    def action_mouse_scroll_down(self):
        pyautogui.scroll(-self.acceleration * 10)
        self.app.message(message="Scroll Down")
        self.action = False