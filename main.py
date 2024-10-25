import pygame
from pathlib import Path

pygame.init()
pygame.mixer.init()
Width = 900
Height = 600
screen = pygame.display.set_mode([Width,Height])
font = pygame.font.Font(Path('Helvetica.ttf'),20)
bigFont = pygame.font.Font(Path('helvetica-compressed-5871d14b6903a.otf'),40)
timer = pygame.time.Clock()
pygame.display.set_caption("Chess!")
fps = 60

# Color Codes - 
    # Background:#dbcabd
    # Boxes - 
        #Light Colored : #F0D9B5; Dark Colored:#B58863; Selected Box:#CED26B


# Game variables and images
blackPieces = ['Rook','Knight','Bishop','Queen','King','Bishop','Knight','Rook'
               ,'Pawn','Pawn','Pawn','Pawn','Pawn','Pawn','Pawn','Pawn']
blackPiecesLocation = [(8,1),(8,2),(8,3),(8,4),(8,5),(8,6),(8,7),(8,8),
                       (7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,7),(7,8)]

capturedWhitePieces = []

whitePieces = ['Rook','Knight','Bishop','Queen','King','Bishop','Knight','Rook'
               ,'Pawn','Pawn','Pawn','Pawn','Pawn','Pawn','Pawn','Pawn']
whitePiecesLocation = [(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),
                       (2,1),(2,2),(2,3),(2,4),(2,5),(2,6),(2,7),(2,8)]

capturedBlackPieces = []

# Pieces Values:
Pawn = 1
Knight = 3
Bishop = 3
Rook = 5
Queen = 9

# State:
#Initial white's Turn
# First number:
    # 0 = No one's Turn; 1 = White's Turn; 2=Black's Turn;
# Second Number: 
    # 0 = Nothing Selected; 1:Piece is Selected
# Third Number: (Status of The Match)
    # 0 = Not Started
    # 1 = Running
    # 2 = White Won
    # 3 = Black Won
    # 4 = Draw
    # 5 = Stalemate
state = [1,0,1] 

# Selected Piece:
selectedPiece = (0,0) 
#If something is selected: use the location coordinate as value else 0

# Valid Moves
validMoves=[]
# When Selected Piece is not (0,0), the number of possible move for that piece  is stored in this :)
kingCheck = 0
#if 1 then white in check, if 2 then black in check else none in check
# Images:
blackQueen = pygame.image.load(Path('Assets') / 'Bqueen.png')
blackKing = pygame.image.load(Path('Assets') / 'Bking.png')
blackRook = pygame.image.load(Path('Assets') / 'Brook.png')
blackKnight = pygame.image.load(Path('Assets') / 'Bknight.png')
blackBishop = pygame.image.load(Path('Assets') / 'Bbishop.png')
blackPawn = pygame.image.load(Path('Assets') / 'Bpawn.png')
whiteQueen = pygame.image.load(Path('Assets') / 'Wqueen.png')
whiteKing = pygame.image.load(Path('Assets') / 'Wking.png')
whiteRook = pygame.image.load(Path('Assets') / 'Wrook.png')
whiteKnight = pygame.image.load(Path('Assets') / 'Wknight.png')
whiteBishop = pygame.image.load(Path('Assets') / 'Wbishop.png')
whitePawn = pygame.image.load(Path('Assets') / 'Wpawn.png')

# Small Images:
smallBlackQueen = pygame.transform.scale(blackQueen,(30,30))
smallBlackKing = pygame.transform.scale(blackKing,(30,30))
smallBlackRook = pygame.transform.scale(blackRook,(30,30))
smallBlackBishop = pygame.transform.scale(blackBishop,(30,30))
smallBlackKnight = pygame.transform.scale(blackKnight,(30,30))
smallBlackPawn = pygame.transform.scale(blackPawn,(30,30))
smallWhiteQueen = pygame.transform.scale(whiteQueen,(30,30))
smallWhiteKing = pygame.transform.scale(whiteKing,(30,30))
smallWhiteRook = pygame.transform.scale(whiteRook,(30,30))
smallWhiteBishop = pygame.transform.scale(whiteBishop,(30,30))
smallWhiteKnight = pygame.transform.scale(whiteKnight,(30,30))
smallWhitePawn = pygame.transform.scale(whitePawn,(30,30))

whitePieceImages = [whiteBishop,whiteKing,whiteKnight,whitePawn,whiteQueen,whiteRook]
blackPieceImages = [blackBishop,blackKing,blackKnight,blackPawn,blackQueen,blackRook]
smallWhiteImages = [smallWhiteBishop,smallWhiteKing,smallWhiteKnight,smallWhitePawn,smallWhiteQueen,smallWhiteRook]
smallBlackImages = [smallBlackBishop,smallBlackKing,smallBlackKnight,smallBlackPawn,smallBlackQueen,smallBlackRook]
pieceNames=['Bishop','King','Knight','Pawn','Queen','Rook'] #To Lookup Images Based on Names (Helps in finding Index of Image)
dialogs = ["Start Game","White's Turn","Black's Turn","White Won","Black Won","Draw","Stalemate"]

# Sound Effects
move = pygame.mixer.Sound(Path('Assets') / 'Sounds' / 'pieceMove.mp3')
capture = pygame.mixer.Sound(Path('Assets') / 'Sounds' / 'capture.mp3')
check = pygame.mixer.Sound(Path('Assets') / 'Sounds' / 'checkKing.mp3')
castle = pygame.mixer.Sound(Path('Assets') / 'Sounds' / 'castle.mp3')

# Drawing Board:
def drawBoard(): 
    # Drawing The Chess Board:
    for Row in range(1,9):  #Row
        for Column in range(1,9): #Column
            if (Row+Column)%2==0: # if even then dark light colored box
                pygame.draw.rect(screen,'#B58863',[(Column-1)*75,(Row-1)*75,75,75]) #Dark Colored Boxes
            else:
                pygame.draw.rect(screen,'#F0D9B5',[(Column-1)*75,(Row-1)*75,75,75]) #Light Colored Boxes
    
    #Drawing The Right Menu:
    #Drawing the Info Text:
    if state[0]==1:
        screen.blit(bigFont.render(dialogs[1],True,'black'),[660,550])
    elif state[0]==2:
        screen.blit(bigFont.render(dialogs[2],True,'black'),[660,550])


# Draw the Pieces:
def drawPieces():
    #Highlighting the selected Piece Box:
    if selectedPiece[0]>0 and selectedPiece[0]<9 and selectedPiece[1]>0 and selectedPiece[1]<9 :
        pygame.draw.rect(screen,'#CED26B',[(selectedPiece[1]-1)*75,(selectedPiece[0]-1)*75,75,75])
    
    # #For Friendly Possible Moves:
    # for validMove in validMoves:
    #     if (state[0]==1 and (validMove in whitePiecesLocation)) or (state[0]==2 and (validMove in blackPiecesLocation)) :
    #         pygame.draw.rect(screen,'gray',[(validMove[1]-1)*75+10,(validMove[0]-1)*75+10,55,55],border_radius=28)
    #Drawing White Pieces:
    for i in range(len(whitePieces)):
        piece = whitePieces[i]
        pos = whitePiecesLocation[i]
        for j in range(len(pieceNames)):
            if piece==pieceNames[j]:
                pieceImg = whitePieceImages[j]
        screen.blit(pieceImg,[((pos[1]-1)*75)+7.5,(pos[0]-1)*75+7.5])
    #Drawing Black Pieces:
    for i in range(len(blackPieces)):
        piece = blackPieces[i]
        pos = blackPiecesLocation[i]
        for j in range(len(pieceNames)):
            if piece==pieceNames[j]:
                pieceImg = blackPieceImages[j]
        screen.blit(pieceImg,[((pos[1]-1)*75)+7.5,(pos[0]-1)*75+7.5])
        
    # Now Highlighting The Possible Move Boxes
    for validMove in validMoves:
        if (state[0]==1 and (validMove in blackPiecesLocation)) or (state[0]==2 and (validMove in whitePiecesLocation)) :
            pygame.draw.rect(screen,'brown',[(validMove[1]-1)*75,(validMove[0]-1)*75,75,75],2)
        elif  (state[0]==1 and (validMove in whitePiecesLocation)) or (state[0]==2 and (validMove in blackPiecesLocation))  :
            pygame.draw.rect(screen,'brown',[(validMove[1]-1)*75+30,(validMove[0]-1)*75+30,15,15],5)
        elif (validMove[0]>0 and validMove[0]<9 and validMove[1]>0 and validMove[1]<9) :
            pygame.draw.rect(screen,'brown',[(validMove[1]-1)*75+30,(validMove[0]-1)*75+30,15,15],border_radius=10)
    
    #Highlighiting King Check:
    if kingCheck==1:
        pos = whitePiecesLocation[whitePieces.index('King')]
        pygame.draw.rect(screen,'red',[(pos[1]-1)*75,(pos[0]-1)*75,75,75],5)
    if kingCheck==2:
        pos = blackPiecesLocation[blackPieces.index('King')]
        pygame.draw.rect(screen,'red',[(pos[1]-1)*75,(pos[0]-1)*75,75,75],5)

# Drawing Dead Pieces:
def drawDeadPieces():
    for i in range(len(capturedBlackPieces)):
        if 600+30*i>870:
            screen.blit(smallBlackImages[pieceNames.index(capturedBlackPieces[i])],[600+30*(i-10),40 ])
        screen.blit(smallBlackImages[pieceNames.index(capturedBlackPieces[i])],[600+30*i,10 ])
    for j in range(len(capturedWhitePieces)):
        if 600+30*j>870:
            screen.blit(smallWhiteImages[pieceNames.index(capturedWhitePieces[j])],[600+30*(j-10),100 ])
        screen.blit(smallWhiteImages[pieceNames.index(capturedWhitePieces[j])],[600+30*j,70 ])

# def checkKing(): #To check if any king is in check [Incomplete]
#     whiteKingLoc = whitePiecesLocation[whitePieces.index('King')]
#     blackKingLoc = blackPiecesLocation[blackPieces.index('King')]
#     isCheck = 0
#     #For White:
#     allyPieces = whitePiecesLocation
#     oppPieces = blackPiecesLocation
#     oppPiecesNames = blackPieces
#     # For Right boxes:
#     for rightBox in range(column+1,9):
#         Box = (row,rightBox)
#         if (Box in allyPieces) or (Box in oppPieces):
#             if (Box in oppPieces):
#                 if oppPiecesNames[oppPieces.index(Box)]=="Rook" or oppPiecesNames[oppPieces.index(Box)]=="Queen":
#                     isCheck = 1
#             break
#     # For Left boxes:
#     for leftBox in range(column-1,0,-1):
#         Box = (row,leftBox)
#         if (Box in allyPieces) or (Box in oppPieces):
#             if (Box in oppPieces):
#                 if oppPiecesNames[oppPieces.index(Box)]=="Rook" or oppPiecesNames[oppPieces.index(Box)]=="Queen":
#                     isCheck = 1
#             break
#     # For Top boxes:
#     for topBox in range(row-1,0,-1):
#         Box = (topBox,column)
#         if (Box in allyPieces) or (Box in oppPieces):
#             if (Box in oppPieces):
#                 if oppPiecesNames[oppPieces.index(Box)]=="Rook" or oppPiecesNames[oppPieces.index(Box)]=="Queen":
#                     isCheck = 1
#             break
#     # For Bottom boxes:
#     for bottomBox in range(row+1,9):
#         Box = (bottomBox,column)
#         if (Box in allyPieces) or (Box in oppPieces):
#             if (Box in oppPieces):
#                 if oppPiecesNames[oppPieces.index(Box)]=="Rook" or oppPiecesNames[oppPieces.index(Box)]=="Queen":
#                     isCheck = 1
#             break
#     return isCheck
def checkKing(king_location, allyPieces, oppPieces, oppPiecesNames):
    row, column = king_location
    isCheck = 0
    
    # Directions for straight moves (Rooks and Queens)
    directions = [
        (0, 1),  # Right
        (0, -1),  # Left
        (-1, 0),  # Up
        (1, 0)   # Down
    ]
    
    for direction in directions:
        dx, dy = direction
        x, y = row, column
        
        while 1 <= x <= 8 and 1 <= y <= 8:
            x += dx
            y += dy
            Box = (x, y)
            if Box in allyPieces:
                break
            if Box in oppPieces:
                piece_index = oppPieces.index(Box)
                if oppPiecesNames[piece_index] in ["Rook", "Queen"]:
                    isCheck = 1
                break

    # Directions for diagonal moves (Bishops and Queens)
    diagonal_directions = [
        (-1, -1),  # Top Left
        (-1, 1),   # Top Right
        (1, -1),   # Bottom Left
        (1, 1)     # Bottom Right
    ]

    for direction in diagonal_directions:
        dx, dy = direction
        x, y = row, column
        
        while 1 <= x <= 8 and 1 <= y <= 8:
            x += dx
            y += dy
            Box = (x, y)
            if Box in allyPieces:
                break
            if Box in oppPieces:
                piece_index = oppPieces.index(Box)
                if oppPiecesNames[piece_index] in ["Bishop", "Queen"]:
                    isCheck = 1
                break

    # Check for Knight attacks (must check specific squares)
    knight_moves = [
        (-2, -1), (-2, 1),   # Up 2 Left 1, Up 2 Right 1
        (-1, -2), (-1, 2),   # Up 1 Left 2, Up 1 Right 2
        (1, -2), (1, 2),     # Down 1 Left 2, Down 1 Right 2
        (2, -1), (2, 1)      # Down 2 Left 1, Down 2 Right 1
    ]
    
    for move in knight_moves:
        x, y = row + move[0], column + move[1]
        Box = (x, y)
        if Box in oppPieces:
            piece_index = oppPieces.index(Box)
            if oppPiecesNames[piece_index] == "Knight":
                isCheck = 1
                break

    return isCheck

#Checking for Valid Moves:
def checkValidMoves(pos,turn):
    validMoves = []
    row = pos[0]
    column = pos[1]
    if turn==1: #White
        piece = whitePieces[whitePiecesLocation.index(pos)]
        oppPieces = blackPiecesLocation
        allyPieces = whitePiecesLocation
    elif turn ==2: #Black
        piece = blackPieces[blackPiecesLocation.index(pos)]
        oppPieces = whitePiecesLocation
        allyPieces = blackPiecesLocation
    match piece:
        # case 'Pawn':
        #     if turn==1: #White
        #         if (row+1,column) not in oppPieces:
        #             validMoves.append((row+1,column))
        #         # if row==2: #Initial Double
        #         #     if not ((row+1,column) in allyPieces) or ((row+1,column) in oppPieces):
        #         #         validMoves.append((row+2,column))
        #         if row == 2:  # White pawn initial move
        #             if (row+1, column) not in allyPieces and (row+2, column) not in oppPieces:
        #                 validMoves.append((row+2, column))
        #         if (row+1,column+1) in oppPieces: #bottom right
        #             validMoves.append((row+1,column+1))
        #         if (row+1,column-1) in oppPieces: #bottom left
        #             validMoves.append((row+1,column-1))
        #     if turn==2: #Black
        #         if (row+1,column) not in oppPieces:
        #             validMoves.append((row-1,column))
        #         if row==7: #Initial Double
        #             if not (((row-1,column) in allyPieces) or ((row-1,column) in oppPieces)):
        #                 validMoves.append((row-2,column))
        #         if (row-1,column+1) in oppPieces: #top right
        #             validMoves.append((row-1,column+1))
        #         if (row-1,column-1) in oppPieces: #top left
        #             validMoves.append((row-1,column-1))
        case 'Pawn':
            if turn == 1:  # White's turn
                # Forward move by 1 square
                if (row + 1, column) not in allyPieces and (row + 1, column) not in oppPieces:
                    validMoves.append((row + 1, column))

                # Initial double move (only from row 2)
                if row == 2:
                    if (row + 1, column) not in allyPieces and (row + 1, column) not in oppPieces and (row + 2, column) not in allyPieces and (row + 2, column) not in oppPieces:
                        validMoves.append((row + 2, column))

                # Capture moves
                if (row + 1, column + 1) in oppPieces:  # Capture on the bottom right diagonal
                    validMoves.append((row + 1, column + 1))
                if (row + 1, column - 1) in oppPieces:  # Capture on the bottom left diagonal
                    validMoves.append((row + 1, column - 1))

            if turn == 2:  # Black's turn
                # Forward move by 1 square
                if (row - 1, column) not in allyPieces and (row - 1, column) not in oppPieces:
                    validMoves.append((row - 1, column))

                # Initial double move (only from row 7)
                if row == 7:
                    if (row - 1, column) not in allyPieces and (row - 1, column) not in oppPieces and (row - 2, column) not in allyPieces and (row - 2, column) not in oppPieces:
                        validMoves.append((row - 2, column))

                # Capture moves
                if (row - 1, column + 1) in oppPieces:  # Capture on the top right diagonal
                    validMoves.append((row - 1, column + 1))
                if (row - 1, column - 1) in oppPieces:  # Capture on the top left diagonal
                    validMoves.append((row - 1, column - 1))

        # case 'Rook':
        #     # For Right boxes:
        #     for rightBox in range(column+1,9):
        #         Box = (row,rightBox)
        #         validMoves.append(Box)
        #         if (Box in allyPieces) or (Box in oppPieces):
        #             break
        #     # For Left boxes:
        #     for leftBox in range(column-1,0,-1):
        #         Box = (row,leftBox)
        #         validMoves.append(Box)
        #         if (Box in allyPieces) or (Box in oppPieces):
        #             break
        #     # For Top boxes:
        #     for topBox in range(row-1,0,-1):
        #         Box = (topBox,column)
        #         validMoves.append(Box)
        #         if (Box in allyPieces) or (Box in oppPieces):
        #             break
        #     # For Bottom boxes:
        #     for bottomBox in range(row+1,9):
        #         Box = (bottomBox,column)
        #         validMoves.append(Box)
        #         if (Box in allyPieces) or (Box in oppPieces):
        #             break
        case 'Rook':
            # For Right boxes:
            for rightBox in range(column + 1, 9):
                Box = (row, rightBox)
                if Box in allyPieces:
                    break  # Stop if blocked by an ally
                validMoves.append(Box)
                if Box in oppPieces:
                    break  # Stop after capturing opponent

            # For Left boxes:
            for leftBox in range(column - 1, 0, -1):
                Box = (row, leftBox)
                if Box in allyPieces:
                    break
                validMoves.append(Box)
                if Box in oppPieces:
                    break

            # For Top boxes:
            for topBox in range(row - 1, 0, -1):
                Box = (topBox, column)
                if Box in allyPieces:
                    break
                validMoves.append(Box)
                if Box in oppPieces:
                    break

            # For Bottom boxes:
            for bottomBox in range(row + 1, 9):
                Box = (bottomBox, column)
                if Box in allyPieces:
                    break
                validMoves.append(Box)
                if Box in oppPieces:
                    break

        # case 'Knight':
        #     validMoves.append((pos[0]+2,pos[1]+1))
        #     validMoves.append((pos[0]+2,pos[1]-1))
        #     validMoves.append((pos[0]-2,pos[1]+1))
        #     validMoves.append((pos[0]-2,pos[1]-1))
        #     validMoves.append((pos[0]+1,pos[1]+2))
        #     validMoves.append((pos[0]+1,pos[1]-2))
        #     validMoves.append((pos[0]-1,pos[1]+2))
        #     validMoves.append((pos[0]-1,pos[1]-2))
        case 'Knight':
            knightMoves = [(row+2, column+1), (row+2, column-1), (row-2, column+1), (row-2, column-1),
                           (row+1, column+2), (row+1, column-2), (row-1, column+2), (row-1, column-2)]
            for move in knightMoves:
                if 1 <= move[0] <= 8 and 1 <= move[1] <= 8:  # Stay within the bounds of the board
                    if move not in allyPieces:
                        validMoves.append(move)

        # case 'King':
        #     validMoves.append((pos[0]+1,pos[1]))
        #     validMoves.append((pos[0]+1,pos[1]-1))
        #     validMoves.append((pos[0]+1,pos[1]+1))
        #     validMoves.append((pos[0],pos[1]+1))
        #     validMoves.append((pos[0]-1,pos[1]+1))
        #     validMoves.append((pos[0],pos[1]-1))
        #     validMoves.append((pos[0]-1,pos[1]-1))
        #     validMoves.append((pos[0]-1,pos[1]))
        case 'King':
            # Check all possible one-square movements
            for drow in [-1, 0, 1]:  # -1, 0, 1 for vertical movement
                for dcol in [-1, 0, 1]:  # -1, 0, 1 for horizontal movement
                    if (drow, dcol) != (0, 0):  # Exclude the current position
                        newRow, newCol = row + drow, column + dcol
                        if 1 <= newRow <= 8 and 1 <= newCol <= 8:  # Within board limits
                            Box = (newRow, newCol)
                            if Box in allyPieces:
                                continue  # Skip if it's occupied by an ally
                            validMoves.append(Box)

        # case 'Queen':
        #     #For Plus Shaped Movements
        #     # For Right boxes:
        #     for rightBox in range(column+1,9):
        #         Box = (row,rightBox)
        #         validMoves.append(Box)
        #         if (Box in allyPieces) or (Box in oppPieces):
        #             break
        #     # For Left boxes:
        #     for leftBox in range(column-1,0,-1):
        #         Box = (row,leftBox)
        #         validMoves.append(Box)
        #         if (Box in allyPieces) or (Box in oppPieces):
        #             break
        #     # For Top boxes:
        #     for topBox in range(row-1,0,-1):
        #         Box = (topBox,column)
        #         validMoves.append(Box)
        #         if (Box in allyPieces) or (Box in oppPieces):
        #             break
        #     # For Bottom boxes:
        #     for bottomBox in range(row+1,9):
        #         Box = (bottomBox,column)
        #         validMoves.append(Box)
        #         if (Box in allyPieces) or (Box in oppPieces):
        #             break


        #     # For Diagnols

        #     #Top Left
        #     tlBox= (row-1,column-1)
        #     while tlBox[0]>0 and tlBox[1]>0:
        #         validMoves.append(tlBox)
        #         if (tlBox in allyPieces) or (tlBox in oppPieces):
        #             break
        #         tlBox = (tlBox[0]-1,tlBox[1]-1)
        #     #Top Right
        #     trBox= (row-1,column+1)
        #     while trBox[0]>0 and trBox[1]<9:
        #         validMoves.append(trBox)
        #         if (trBox in allyPieces) or (trBox in oppPieces):
        #             break
        #         trBox = (trBox[0]-1,trBox[1]+1)

        #     #Bottom Left
        #     blBox= (row+1,column-1)
        #     while blBox[0]<9 and blBox[1]>0:
        #         validMoves.append(blBox)
        #         if (blBox in allyPieces) or (blBox in oppPieces):
        #             break
        #         blBox = (blBox[0]+1,blBox[1]-1)

        #     #Bottom Right
        #     brBox= (row+1,column+1)
        #     while brBox[0]<9 and brBox[1]<9:
        #         validMoves.append(brBox)
        #         if (brBox in allyPieces) or (brBox in oppPieces):
        #             break
        #         brBox = (brBox[0]+1,brBox[1]+1)
        case 'Queen':
            # For Plus Shaped Movements (Rook-like)
            
            # For Right boxes:
            for rightBox in range(column+1, 9):
                Box = (row, rightBox)
                if Box in allyPieces:
                    break  # Blocked by ally, stop further movement
                validMoves.append(Box)  # Add only if it's not blocked by an ally
                if Box in oppPieces:
                    break  # Capture opponent, but stop further movement after this

            # For Left boxes:
            for leftBox in range(column-1, 0, -1):
                Box = (row, leftBox)
                if Box in allyPieces:
                    break
                validMoves.append(Box)
                if Box in oppPieces:
                    break

            # For Top boxes:
            for topBox in range(row-1, 0, -1):
                Box = (topBox, column)
                if Box in allyPieces:
                    break
                validMoves.append(Box)
                if Box in oppPieces:
                    break

            # For Bottom boxes:
            for bottomBox in range(row+1, 9):
                Box = (bottomBox, column)
                if Box in allyPieces:
                    break
                validMoves.append(Box)
                if Box in oppPieces:
                    break

            # For Diagonal Movements (Bishop-like)

            # Top Left Diagonal
            tlBox = (row-1, column-1)
            while tlBox[0] > 0 and tlBox[1] > 0:  # Within board limits
                if tlBox in allyPieces:
                    break  # Blocked by ally
                validMoves.append(tlBox)
                if tlBox in oppPieces:
                    break  # Capture opponent and stop further movement
                tlBox = (tlBox[0]-1, tlBox[1]-1)  # Move diagonally to the top-left

            # Top Right Diagonal
            trBox = (row-1, column+1)
            while trBox[0] > 0 and trBox[1] < 9:
                if trBox in allyPieces:
                    break
                validMoves.append(trBox)
                if trBox in oppPieces:
                    break
                trBox = (trBox[0]-1, trBox[1]+1)  # Move diagonally to the top-right

            # Bottom Left Diagonal
            blBox = (row+1, column-1)
            while blBox[0] < 9 and blBox[1] > 0:
                if blBox in allyPieces:
                    break
                validMoves.append(blBox)
                if blBox in oppPieces:
                    break
                blBox = (blBox[0]+1, blBox[1]-1)  # Move diagonally to the bottom-left

            # Bottom Right Diagonal
            brBox = (row+1, column+1)
            while brBox[0] < 9 and brBox[1] < 9:
                if brBox in allyPieces:
                    break
                validMoves.append(brBox)
                if brBox in oppPieces:
                    break
                brBox = (brBox[0]+1, brBox[1]+1)  # Move diagonally to the bottom-right


        # case 'Bishop':
        #     #Top Left
        #     tlBox= (row-1,column-1)
        #     while tlBox[0]>0 and tlBox[1]>0:
        #         validMoves.append(tlBox)
        #         if (tlBox in allyPieces) or (tlBox in oppPieces):
        #             break
        #         tlBox = (tlBox[0]-1,tlBox[1]-1)
        #     #Top Right
        #     trBox= (row-1,column+1)
        #     while trBox[0]>0 and trBox[1]<9:
        #         validMoves.append(trBox)
        #         if (trBox in allyPieces) or (trBox in oppPieces):
        #             break
        #         trBox = (trBox[0]-1,trBox[1]+1)

        #     #Bottom Left
        #     blBox= (row+1,column-1)
        #     while blBox[0]<9 and blBox[1]>0:
        #         validMoves.append(blBox)
        #         if (blBox in allyPieces) or (blBox in oppPieces):
        #             break
        #         blBox = (blBox[0]+1,blBox[1]-1)

        #     #Bottom Right
        #     brBox= (row+1,column+1)
        #     while brBox[0]<9 and brBox[1]<9:
        #         validMoves.append(brBox)
        #         if (brBox in allyPieces) or (brBox in oppPieces):
        #             break
        #         brBox = (brBox[0]+1,brBox[1]+1).

        case 'Bishop':
            # Top Left Diagonal
            tlBox = (row - 1, column - 1)
            while tlBox[0] > 0 and tlBox[1] > 0:  # Within board limits
                if tlBox in allyPieces:
                    break  # Stop if blocked by an ally
                validMoves.append(tlBox)
                if tlBox in oppPieces:
                    break  # Stop after capturing opponent
                tlBox = (tlBox[0] - 1, tlBox[1] - 1)

            # Top Right Diagonal
            trBox = (row - 1, column + 1)
            while trBox[0] > 0 and trBox[1] < 9:
                if trBox in allyPieces:
                    break
                validMoves.append(trBox)
                if trBox in oppPieces:
                    break
                trBox = (trBox[0] - 1, trBox[1] + 1)

            # Bottom Left Diagonal
            blBox = (row + 1, column - 1)
            while blBox[0] < 9 and blBox[1] > 0:
                if blBox in allyPieces:
                    break
                validMoves.append(blBox)
                if blBox in oppPieces:
                    break
                blBox = (blBox[0] + 1, blBox[1] - 1)

            # Bottom Right Diagonal
            brBox = (row + 1, column + 1)
            while brBox[0] < 9 and brBox[1] < 9:
                if brBox in allyPieces:
                    break
                validMoves.append(brBox)
                if brBox in oppPieces:
                    break
                brBox = (brBox[0] + 1, brBox[1] + 1)


    return validMoves



# Main Game Loop
isGameOn = True
while isGameOn:
    timer.tick(fps)
    screen.fill('#dbcabd')  #Background
    drawBoard()
    drawPieces()
    drawDeadPieces()
    

    
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #If User clicked on Cross
            isGameOn= False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button==1: #If User Left Clicked On Somewhere
            column = event.pos[0]//75 + 1
            row = event.pos[1]//75 + 1
            coord = (row,column)
            if state[0]==1: # For White:
                if state[1]==0: #Selecting The Piece To Move
                    if coord in whitePiecesLocation:
                        selectedPiece = (row,column)
                        state[1]=1
                        # Add Function to Change The Valid Moves Variable
                        validMoves = checkValidMoves(selectedPiece,1)
                elif state[1]==1: #Selecting The Location to Move The Piece to
                    if coord in whitePiecesLocation:
                        selectedPiece = coord
                        validMoves = checkValidMoves(selectedPiece,1)
                    elif coord in validMoves:
                        if coord in blackPiecesLocation:
                            index = blackPiecesLocation.index(coord)
                            capturedBlackPieces.append(blackPieces[index])
                            blackPiecesLocation.pop(index)
                            blackPieces.pop(index)
                            pygame.mixer.Sound.play(capture)
                        else:
                            pygame.mixer.Sound.play(move)
                        whitePiecesLocation[whitePiecesLocation.index(selectedPiece)] = coord
                        state[1]=0
                        selectedPiece = (0,0)
                        validMoves =[]
                        state[0]=2
                        # kingCheck = checkKing()
                    else:
                        state[1]=0
                        selectedPiece = (0,0)
                        validMoves =[]
            elif state[0]==2: # For Black:
                if state[1]==0: #Selecting The Piece To Move
                    if coord in blackPiecesLocation:
                        selectedPiece = (row,column)
                        state[1]=1
                        # Add Function to Change The Valid Moves Variable
                        validMoves = checkValidMoves(selectedPiece,2)
                elif state[1]==1: #Selecting The Location to Move The Piece to
                    if coord in blackPiecesLocation:
                        selectedPiece = coord
                        validMoves = checkValidMoves(selectedPiece,2)
                    elif coord in validMoves:
                        if coord in whitePiecesLocation:
                            index = whitePiecesLocation.index(coord)
                            capturedWhitePieces.append(whitePieces[index])
                            whitePiecesLocation.pop(index)
                            whitePieces.pop(index)
                            pygame.mixer.Sound.play(capture)
                        else:
                            pygame.mixer.Sound.play(move)
                        blackPiecesLocation[blackPiecesLocation.index(selectedPiece)] = coord
                        state[1]=0
                        selectedPiece = (0,0)
                        validMoves = []
                        state[0]=1
                        # kingCheck = checkKing()
                    else:
                        state[1]=0
                        selectedPiece = (0,0)
                        validMoves = []
                    

    pygame.display.flip()
pygame.quit()


# Credits:
    # ICONS By Wikipedia 
    # user: Cburnett - 
    # https://commons.wikimedia.org/wiki/Category:PNG_chess_pieces/Standard_transparent, CC BY-SA 3.0, 
    # https://commons.wikimedia.org/w/index.php?curid=55002446
    # Developer : Sujas Kumar Aggarwal
    # Sorry If I Forgot to give credit to any of the asset owner
