import os
from PIL import Image, ImageDraw
from pystray import Icon, MenuItem, Menu
import asyncio

class Keywwy:

    def __init__(self, config):
        self.app_name = "Keywwy"
        self.window_message = f"{self.app_name} ready"
        self.config = config
        self.loop = None

    def create_image(self):
        image = Image.new('RGB', (64, 64), (255, 255, 255))
        dc = ImageDraw.Draw(image)
        dc.rectangle((0, 0, 64, 64), fill=(0, 0, 0))
        return image

    def setup_tray(self):
        icon_image = self.create_image()
        menu = Menu(
            MenuItem('Sair', self.force_exit)
        )
        icon = Icon(self.app_name, icon_image, menu=menu)
        return icon

    def message(self, message = None, log = None):
        if message: print(message)
        if log: self.log(log)

    def log(self, message):
        if self.config.debug: 
            print(message)

    async def run(self):
        self.loop = asyncio.get_event_loop()
        self.icon = self.setup_tray()
        self.icon.run_detached()
        self.message(self.window_message)
    
        while True:
            try:
                await asyncio.sleep(0.01)
            except Exception as e:
                print(e)
                self.force_exit()

    def force_exit(self):
        try:
            if self.icon: self.icon.stop()
            self.keyboard.unhook_all()
        finally:
            os._exit(1)  # Force terminate all threads