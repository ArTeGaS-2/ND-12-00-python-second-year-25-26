from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.game import Game


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
