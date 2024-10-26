import pygame
from config import PieceNames, Color
from utils import AssestsHandler
from piece import Piece
from board import Board, Move

# Colors
BACKGROUND_COLOR = '#dbcabd'
BOX_LIGHT_COLOR = '#F0D9B5'
BOX_DARK_COLOR = '#B58863'
BOX_SELECTED_COLOR = '#CED26B'

class GameWindow:
    def __init__(self, screen):
        self.screen = screen
        self.smallImageScaling = (30,30)
        self.font = AssestsHandler.loadFont('Helvetica.ttf',20)
        self.bigFont = AssestsHandler.loadFont('helvetica-compressed-5871d14b6903a.otf',40)
        self.PieceImages = [[],[]]
        self.smallPieceImages = [[],[]]
        self._loadImages()

        # sounds
        self.move = AssestsHandler.loadSound('pieceMove.mp3')
        self.capture = AssestsHandler.loadSound('capture.mp3')
        self.check = AssestsHandler.loadSound('checkKing.mp3')
        self.castle = AssestsHandler.loadSound('castle.mp3')

    def _loadImages(self):
        for piece in PieceNames:
            whiteImage = AssestsHandler.loadImage('W'+piece+'.png')
            blackImage = AssestsHandler.loadImage('B'+piece+'.png')
            whiteSmallImage = AssestsHandler.scaleImage(whiteImage, self.smallImageScaling)
            blackSmallImage = AssestsHandler.scaleImage(blackImage, self.smallImageScaling)
            self.PieceImages[Color.WHITE].append(whiteImage)
            self.PieceImages[Color.BLACK].append(blackImage)
            self.smallPieceImages[Color.WHITE].append(whiteSmallImage)
            self.smallPieceImages[Color.BLACK].append(blackSmallImage)

    def _drawBoard(self):
        # Drawing The Chess Board:
        for Row in range(1,9):  #Row
            for Column in range(1,9): #Column
                if (Row+Column)%2==0: # if even then dark light colored box
                    pygame.draw.rect(self.screen, BOX_DARK_COLOR,[(Column-1)*75,(Row-1)*75,75,75]) #Dark Colored Boxes
                else:
                    pygame.draw.rect(self.screen, BOX_LIGHT_COLOR,[(Column-1)*75,(Row-1)*75,75,75]) #Light Colored Boxes
    
    # draw highlighted box
    def _drawHighlightedBox(self, board:Board, position):
        assert 0<position[0]<9 and 0<position[1]<9
        # Highlighting the selected Piece Box:
        pygame.draw.rect(self.screen, BOX_SELECTED_COLOR,[(position[1]-1)*75,(position[0]-1)*75,75,75])
        self._drawPiece(board.pieceAt(position), board.colorOfPieceAt(position), position)

    def _drawPiece(self, piece:Piece, color:Color, position):
        self.screen.blit(self.PieceImages[color][piece],[((position[1]-1)*75)+7.5,(position[0]-1)*75+7.5])
    
    def _drawPieces(self, Pieces, PiecesLocation):
        #Drawing Pieces
        # white
        for piece, pos in zip(Pieces[Color.WHITE], PiecesLocation[Color.WHITE]):
            self._drawPiece(piece, Color.WHITE, pos)
        # black
        for piece, pos in zip(Pieces[Color.BLACK], PiecesLocation[Color.BLACK]):
            self._drawPiece(piece, Color.BLACK, pos)

    def _drawDeadPieces(self, capturedPieces):
        for i in range(len(capturedPieces[Color.BLACK])):
            if 600+30*i>870:
                self.screen.blit(self.smallPieceImages[Color.BLACK][capturedPieces[Color.BLACK][i]],[600+30*(i-10),40 ])
            self.screen.blit(self.smallPieceImages[Color.BLACK][capturedPieces[Color.BLACK][i]],[600+30*i,10 ])
        for j in range(len(capturedPieces[Color.WHITE])):
            if 600+30*j>870:
                self.screen.blit(self.smallPieceImages[Color.WHITE][capturedPieces[Color.WHITE][j]],[600+30*(j-10),100 ])
            self.screen.blit(self.smallPieceImages[Color.WHITE][capturedPieces[Color.WHITE][j]],[600+30*j,70 ])

    def _drawValidMoves(self, board:Board, square):
        moves = board.getValidMoves(square)
        for end,move in moves.items():
            box = move.end
            if move.capture is not None:
                pygame.draw.rect(self.screen,'brown',[(box[1]-1)*75,(box[0]-1)*75,75,75],2)
            else:
                pygame.draw.rect(self.screen,'brown',[(box[1]-1)*75+30,(box[0]-1)*75+30,15,15],border_radius=10)
    
    def _drawInfo(self, info, color='black'):
        self.screen.blit(self.bigFont.render(info,True,color),[660,550])
    
    def drawMenu(self, board, info):
        """ Draws the right Menu, captured Pieces, as well as any additional information."""
        self._drawDeadPieces(board.getCapturedPieces())
        self._drawInfo(info)

    def drawBoard(self, board, selected_piece = None):
        """ Draws the current state of the board."""
        self._drawBoard()
        self._drawPieces(board.getPieces(), board.getPiecesLocation())
        if selected_piece is not None and board.pieceAt(selected_piece) is not None:
            self._drawHighlightedBox(board, selected_piece)
            self._drawValidMoves(board, selected_piece)

    def makeSound(self, move):
        if move.capture is not None:
            pygame.mixer.Sound.play(self.capture)
        else:
            pygame.mixer.Sound.play(self.move)

    def fill(self, color = BACKGROUND_COLOR):
        self.screen.fill(color)