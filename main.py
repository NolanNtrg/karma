import sys
from pathlib import Path

# Le package karma est dans src/, absent de sys.path sans installation via pip install -e .
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from karma.game import Game

if __name__ == "__main__":
    game = Game()
    game.run()
