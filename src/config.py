import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self.debug = os.getenv('DEBUG', 'false').lower() == 'true'
        
        self.toggle = os.getenv('TOGGLE', 'esc')

        self.move_up = os.getenv('MOVE_UP', 'up')
        self.move_down = os.getenv('MOVE_DOWN', 'down') 
        self.move_left = os.getenv('MOVE_LEFT', 'left')
        self.move_right = os.getenv('MOVE_RIGHT', 'right')

        self.move_diagonal_up_left = os.getenv('MOVE_DIAGONAL_UP_LEFT', 'insert')
        self.move_diagonal_up_right = os.getenv('MOVE_DIAGONAL_UP_RIGHT', 'home')
        self.move_diagonal_down_left = os.getenv('MOVE_DIAGONAL_DOWN_LEFT', 'delete')
        self.move_diagonal_down_right = os.getenv('MOVE_DIAGONAL_DOWN_RIGHT', 'end')

        self.mouse_click = os.getenv('MOUSE_CLICK', 'f')
        self.mouse_click_right = os.getenv('MOUSE_CLICK_RIGHT', 'g')
        self.mouse_scroll_up = os.getenv('MOUSE_SCROLL_UP', 'page up')
        self.mouse_scroll_down = os.getenv('MOUSE_SCROLL_DOWN', 'page down')

        self.speed_up = os.getenv('SPEED_UP', 'd')
        self.speed_down = os.getenv('SPEED_DOWN', 's')

        self.action = os.getenv('ACTION', 'a')

        self.action_move_top_left = os.getenv('ACTION_MOVE_TOP_LEFT', 'insert')
        self.action_move_top_center = os.getenv('ACTION_MOVE_TOP_CENTER', 'home')
        self.action_move_top_right = os.getenv('ACTION_MOVE_TOP_RIGHT', 'page up')
        self.action_move_middle_left = os.getenv('ACTION_MOVE_MIDDLE_LEFT', 'delete')
        self.action_move_middle_center = os.getenv('ACTION_MOVE_MIDDLE_CENTER', 'end')
        self.action_move_middle_right = os.getenv('ACTION_MOVE_MIDDLE_RIGHT', 'page down')
        self.action_move_bottom_left = os.getenv('ACTION_MOVE_BOTTOM_LEFT', 'left')
        self.action_move_bottom_center = os.getenv('ACTION_MOVE_BOTTOM_CENTER', 'down')
        self.action_move_bottom_right = os.getenv('ACTION_MOVE_BOTTOM_RIGHT', 'right')

        self.action_click_hold = os.getenv('ACTION_CLICK_HOLD', 'f')
        self.action_click_release = os.getenv('ACTION_CLICK_RELEASE', 'g')

        