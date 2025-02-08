from src.keywwy import Keywwy
from src.mouse import MouseController

if __name__ == "__main__":
    app = Keywwy()
    MouseController(app)
    app.run()