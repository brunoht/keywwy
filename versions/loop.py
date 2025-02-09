import sys
import time
import keyboard, pyautogui
import asyncio

blocked = False

def handle_keyboard_event(event):
    if event.event_type == keyboard.KEY_DOWN:
        print(f"key pressed: {event.name}")
        if not blocked: # Only process if not blocked
            asyncio.run_coroutine_threadsafe(handle_action(event.name), loop)
    return False

async def handle_action(name):
    global blocked
    
    if blocked: return
    
    blocked = True
    x, y = pyautogui.position()
    w, h = pyautogui.size()

    match name:
        case 'up':
            y = max(5, y - (10 * 1))
            pyautogui.moveTo(x, y)
    
    blocked = False

async def main_loop():
    global loop
    loop = asyncio.get_event_loop()
    keyboard.hook(handle_keyboard_event, suppress=False)
    while True:
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main_loop())