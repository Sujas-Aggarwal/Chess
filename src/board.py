from piece import *
from config import Color

class Move:
    def __init__(self, piece, color, start, end, capture=None, promotion=False, castle=False, enPassantSquare = None):
        self.piece = piece
        self.color = color
        self.start = start
        self.end = end
        self.capture = capture
        self.promotion = promotion
        self.castle = castle
        self.enPassantSquare = enPassantSquare

class Board:
    def __init__(self):
        # Game variables and images
        self.pieces = [
            # white
            [ Piece.ROOK,Piece.KNIGHT,Piece.BISHOP,Piece.QUEEN,Piece.KING,Piece.BISHOP,Piece.KNIGHT,Piece.ROOK,
            Piece.PAWN,Piece.PAWN,Piece.PAWN,Piece.PAWN,Piece.PAWN,Piece.PAWN,Piece.PAWN,Piece.PAWN ],
            # black
            [ Piece.ROOK,Piece.KNIGHT,Piece.BISHOP,Piece.QUEEN,Piece.KING,Piece.BISHOP,Piece.KNIGHT,Piece.ROOK,
            Piece.PAWN,Piece.PAWN,Piece.PAWN,Piece.PAWN,Piece.PAWN,Piece.PAWN,Piece.PAWN,Piece.PAWN ]
        ]
        self.piecesLocation = [
            # white
            [(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),
            (2,1),(2,2),(2,3),(2,4),(2,5),(2,6),(2,7),(2,8)],
            # black
            [(8,1),(8,2),(8,3),(8,4),(8,5),(8,6),(8,7),(8,8),
            (7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,7),(7,8)]
        ]
        self.capturedPieces = [[],[]]
        self.history = []
        self.validMoves = {}
        self.bishopDirections = [(1,1), (1,-1), (-1,1), (-1,-1)]
        self.rookDirections = [(1,0), (0,1), (-1,0), (0,-1)]
        self.knightDirections = [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (-1,2), (1,-2), (-1,-2)]
        self.kingDirections = [(1,1), (1,-1), (-1,1), (-1,-1), (1,0), (0,1), (-1,0), (0,-1)]

    def getCapturedPieces(self):
        return self.capturedPieces
    
    def getPieces(self):
        return self.pieces
    
    def getPiecesLocation(self):
        return self.piecesLocation

    def pieceAt(self, square):
        if square in self.piecesLocation[Color.WHITE]:
            return self.pieces[Color.WHITE][self.piecesLocation[Color.WHITE].index(square)]
        elif square in self.piecesLocation[Color.BLACK]:
            return self.pieces[Color.BLACK][self.piecesLocation[Color.BLACK].index(square)]
        return None

    def colorOfPieceAt(self, square):
        if square in self.piecesLocation[Color.WHITE]:
            return Color.WHITE
        elif square in self.piecesLocation[Color.BLACK]:
            return Color.BLACK
        return Color.NONE

    def lastMove(self):
        if not self.history:
            return None
        return self.history[-1]
    
    def _inRange(self, square):
        return 1 <= square[0] <= 8 and 1 <= square[1] <= 8
    
    def _getPawnPsuedoMoves(self, square, color, opponent_color) -> Move:
        direction = 1 if color == Color.WHITE else -1
        moves = []
        # forward by 1 square
        end_square = (square[0]+direction, square[1])
        if self._inRange(end_square) and self.pieceAt(end_square) == None:
            if end_square[0] == 8 or end_square[0] == 1:
                moves.append (Move(Piece.PAWN, color, square, end_square, promotion=Piece.BISHOP))
                moves.append (Move(Piece.PAWN, color, square, end_square, promotion=Piece.ROOK))
                moves.append (Move(Piece.PAWN, color, square, end_square, promotion=Piece.KNIGHT))
                moves.append (Move(Piece.PAWN, color, square, end_square, promotion=Piece.QUEEN))
            else:
                moves.append(Move(Piece.PAWN, color, square, end_square))
        # forward 2 square
        if (square[0]==2 and color==Color.WHITE) or (square[0]==7 and color==Color.BLACK):
            end_square = (square[0]+2*direction, square[1])
            if self.pieceAt(end_square) == None:
                moves.append(Move(Piece.PAWN, color, square, end_square, enPassantSquare=(square[0]+direction, square[1])))
        
        # diagonal capture
        for i in range(-1,2,2):
            end_square = (square[0]+direction, square[1]+i)
            if self._inRange(end_square) and self.colorOfPieceAt(end_square) == opponent_color:
                pieceAtEnd = self.pieceAt(end_square)
                moves.append(Move(Piece.PAWN, color, square, end_square, capture=pieceAtEnd))
        return moves

    def _getBishopPsuedoMoves(self, square, color, opponent_color):
        moves = []
        for rowInc,colInc in self.bishopDirections:
            end_square = (square[0]+rowInc, square[1]+colInc)
            while self._inRange(end_square):
                pieceAtEnd = self.pieceAt(end_square)
                if pieceAtEnd is not None:
                    if self.colorOfPieceAt(end_square) == opponent_color:
                        moves.append(Move(Piece.BISHOP, color, square, end_square, capture=pieceAtEnd))
                    break
                else:
                    moves.append(Move(Piece.BISHOP, color, square, end_square))

                end_square = (end_square[0] + rowInc, end_square[1] + colInc)

        return moves

    def  _getKnightPsuedoMoves(self, square, color, opponent_color):
        moves = []
        for rowInc, colInc in self.knightDirections:
            end_square = (square[0]+rowInc, square[1]+colInc)
            if not self._inRange(end_square):
                continue
            pieceAtEnd = self.pieceAt(end_square)
            if pieceAtEnd is None:
                moves.append(Move(Piece.KNIGHT, color, square, end_square))
            elif self.colorOfPieceAt(end_square) == opponent_color:
                moves.append(Move(Piece.KNIGHT, color, square, end_square, capture=pieceAtEnd))

        return moves

    def _getRookPsuedoMoves(self, square, color, opponent_color):
        moves = []
        for rowInc,colInc in self.rookDirections:
            end_square = (square[0]+rowInc, square[1]+colInc)
            while self._inRange(end_square):
                pieceAtEnd = self.pieceAt(end_square)
                if pieceAtEnd is not None:
                    if self.colorOfPieceAt(end_square) == opponent_color:
                        moves.append(Move(Piece.ROOK, color, square, end_square, capture=pieceAtEnd))
                    break
                else:
                    moves.append(Move(Piece.ROOK, color, square, end_square))

                end_square = (end_square[0] + rowInc, end_square[1] + colInc)

        return moves

    def _getQueenPsuedoMoves(self, square, color, opponent_color):
        moves = self._getBishopPsuedoMoves(square, color, opponent_color)
        moves.extend(self._getRookPsuedoMoves(square, color, opponent_color))
        return moves

    def _getKingPsuedoMoves(self, square, color, opponent_color):
        moves = []
        for rowInc, colInc in self.kingDirections:
            end_square = (square[0]+rowInc, square[1]+colInc)
            if not self._inRange(end_square):
                continue
            pieceAtEnd = self.pieceAt(end_square)
            if pieceAtEnd is None:
                moves.append(Move(Piece.KING, color, square, end_square))
            elif self.colorOfPieceAt(end_square) == opponent_color:
                moves.append(Move(Piece.KING, color, square, end_square, capture=pieceAtEnd))

        return moves
        
    def getPsuedoValidMoves(self, square) -> Move:
        piece = self.pieceAt(square)
        color =  self.colorOfPieceAt(square)
        opponent_color = Color.BLACK if color == Color.WHITE else Color.WHITE

        match piece:
            case Piece.PAWN:
                return self._getPawnPsuedoMoves(square, color, opponent_color)
            case Piece.KNIGHT:
                return self._getKnightPsuedoMoves(square, color, opponent_color)
            case  Piece.BISHOP:
                return self._getBishopPsuedoMoves(square, color, opponent_color)
            case  Piece.ROOK:
                return self._getRookPsuedoMoves(square, color, opponent_color)
            case  Piece.QUEEN:
                return self._getQueenPsuedoMoves(square, color, opponent_color)
            case  Piece.KING:
                return self._getKingPsuedoMoves(square, color, opponent_color)

        raise ValueError (f"Invalid piece type: {piece}")

    def getValidMoves(self, square):
        if square in self.validMoves:
            return self.validMoves[square]

        moves = self.getPsuedoValidMoves(square)
        self.validMoves[square] = {}
        for move in moves:
            self.validMoves[square][move.end] = move

        return self.validMoves[square]
    
    def makeMove(self, start, end):
        assert 0<start[0]<9 and 0<start[1]<9 and 0<end[0]<9 and 0<end[1]<9

        movingPiece = self.pieceAt(start)
        color = self.colorOfPieceAt(start)
        opponent_color = Color.BLACK if color == Color.WHITE else Color.WHITE

        if movingPiece == None or end not in self.getValidMoves(start):
            return False
        
        assert end in self.getValidMoves(start)

        move = self.getValidMoves(start)[end]
        index = self.piecesLocation[color].index(start)

        if move.capture is not None:
            self.capturedPieces[opponent_color].append(move.capture)
            self.pieces[opponent_color].remove(move.capture)
            if move.enPassantSquare is None:
                self.piecesLocation[opponent_color].remove(move.end)
            else:
                self.piecesLocation[opponent_color].remove(move.enPassantSquare)

        self.piecesLocation[color][index] = end
        if move.promotion:
            self.pieces[color][index] = move.promotion

        self.history.append(move)
        self.validMoves = {}

        return True