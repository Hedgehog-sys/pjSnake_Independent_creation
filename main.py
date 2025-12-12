import traceback
from game import *

if __name__ == "__main__":
    try:
        game = Game()
        game.run()
    except Exception:
        with open("error.log", "w", encoding="utf-8") as f:
            traceback.print_exc(file=f)
        raise