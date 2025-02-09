from src.config import Config
from src.keywwy import Keywwy
from src.mouse import MouseController
import asyncio

if __name__ == "__main__":
    config = Config()
    app = Keywwy(config)
    MouseController(app)
    asyncio.run(app.run())