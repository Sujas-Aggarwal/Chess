WIDTH, HEIGHT = 900, 600  # Screen dimensions
BOX_SIZE = WIDTH // 8    # Size of each BOX
FPS = 60

PieceNames = ['pawn','knight','bishop','rook','queen','king']

# Game Status
class GameStatus:
    NOT_STARTED = 0
    RUNNING = 1
    WHITE_WON = 2
    BLACK_WON = 3
    DRAW = 4
    STALEMATE = 5

class Color:
    WHITE = 0
    BLACK = 1
    NONE = 2
