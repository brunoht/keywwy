from src.keywwy import Keywwy
from src.mouse import MouseController
import asyncio

if __name__ == "__main__":
    app = Keywwy()
    MouseController(app)
    asyncio.run(app.run())