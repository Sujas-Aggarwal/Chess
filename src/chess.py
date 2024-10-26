import pygame
from gui import GameWindow
from board import Board
from config import FPS, GameStatus, Color

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.board = Board()
        self.window = GameWindow(screen)
        self.timer = pygame.time.Clock()
        self.turn = Color.WHITE
        self.game_status = GameStatus.RUNNING
        self.running = False
        self.selectedBox = None
        self.dialogs = ["Start Game","White's Turn","Black's Turn","White Won","Black Won","Draw","Stalemate"]

    def start(self):
        self.running = True
        while self.running:
            self.timer.tick(FPS)
            self._draw()
            self._handleEvents()

    def _handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #If User clicked on Cross
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button==1: #If User Left Clicked On Somewhere
                column = event.pos[0]//75 + 1
                row = event.pos[1]//75 + 1
                if 0<row<9 and 0<column<9:
                    coord = (row,column)
                    if self.selectedBox is not None:
                        if self.board.makeMove(self.selectedBox, coord):
                            self._playSound(self.board.lastMove())
                            self.turn = Color.BLACK if self.turn == Color.WHITE else Color.WHITE
                        self.selectedBox = None

                    elif self.board.colorOfPieceAt(coord) == self.turn:
                        self.selectedBox = coord

    def _playSound(self,move):
        self.window.makeSound(move)

    def _getInfo(self) -> str:
        return self.dialogs[self.turn+1]

    def _draw(self):
        self.window.fill()
        self.window.drawBoard(self.board, self.selectedBox)
        self.window.drawMenu(self.board, self._getInfo())
        pygame.display.flip()
