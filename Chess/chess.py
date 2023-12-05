'''
Chess
Arttu Ikonen
University of Turku
'''

import pygame, os, os.path
pygame.init()

windowWidth = 400
windowHeight = 400
tileWidth = windowWidth // 8
tileHeight = windowHeight // 8
window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Chess')

BOARDDARK = (107,97,94)
BOARDLIGHT = (250,250,250)
BOARDMOVES = (140, 171, 161)
BOARDSELECTED = (179, 165, 85)

playerTurn = 'white'
legalMoves = []
spriteFolder = 'sprites/'
startX, startY, endX, endY = None, None, None, None

boardMatrix = [
    ['blackRook', 'blackKnight', 'blackBishop', 'blackKing', 'blackQueen', 'blackBishop', 'blackKnight', 'blackRook'],
    ['blackPawn', 'blackPawn', 'blackPawn', 'blackPawn', 'blackPawn', 'blackPawn', 'blackPawn', 'blackPawn'],
    ['','','','','','','',''],
    ['','','','','','','',''],
    ['','','','','','','',''],
    ['','','','','','','',''],
    ['whitePawn', 'whitePawn', 'whitePawn', 'whitePawn', 'whitePawn', 'whitePawn', 'whitePawn', 'whitePawn'],
    ['whiteRook', 'whiteKnight', 'whiteBishop', 'whiteQueen', 'whiteKing', 'whiteBishop', 'whiteKnight', 'whiteRook'],
]


if os.path.exists('./save.txt'):
    if os.stat('save.txt').st_size != 0:

        with open('save.txt') as saveFile:
            for row in saveFile:
                saveData = row.split(',')
                playerTurn = saveData[0]
                pieceNumber = 1
                for xIndex in range(8):
                    for yIndex in range(8):
                        boardMatrix[yIndex][xIndex] = '' if saveData[pieceNumber] == 'empty' else saveData[pieceNumber] 
                        pieceNumber += 1
                 
def getSprite(x: int, y: int):

    piece = boardMatrix[y][x]

    pieceSprites = {
        'blackPawn'  : 'blackPawn.png',
        'blackRook'  : 'blackRook.png',
        'blackKnight': 'blackKnight.png',
        'blackBishop': 'blackBishop.png',
        'blackQueen' : 'blackQueen.png',
        'blackKing'  : 'blackKing.png',
        'whitePawn'  : 'whitePawn.png',
        'whiteRook'  : 'whiteRook.png',
        'whiteKnight': 'whiteKnight.png',
        'whiteBishop': 'whiteBishop.png',
        'whiteQueen' : 'whiteQueen.png',
        'whiteKing'  : 'whiteKing.png'
    }

    spriteFile = pieceSprites.get(piece)

    return None if spriteFile is None else pygame.image.load(spriteFolder + spriteFile)

def drawBoard():

    for x in range(8):
        for y in range(8):

            squareColor = BOARDMOVES if (x, y) in legalMoves else BOARDSELECTED if (x, y) == (startX, startY) else BOARDDARK if (x + y) % 2 == 0 else BOARDLIGHT
            squareRect = pygame.Rect(x * tileWidth, y * tileHeight, tileWidth, tileHeight)
            pygame.draw.rect(window, squareColor, squareRect)

            sprite = getSprite(x, y)
            if sprite is not None:
                spriteRect = sprite.get_rect()
                spriteRect.center = (x * tileWidth + tileWidth / 2, y * tileHeight + tileHeight / 2)
                window.blit(sprite, spriteRect)
                
def generateMoves(x: int, y: int) -> list:

    moves = []

    startPiece = boardMatrix[y][x]
    if startPiece == '': return moves

    startPieceColor = startPiece[:5]
    startPieceType = startPiece[5:]

    match startPieceType:
        case 'Pawn':

            if startPieceColor == 'white':
                direction, startY = -1, 6
            else:
                direction, startY = 1, 1

            if 0 <= y + direction <= 7:

                if isEmpty(x, y + direction):
                    moves.append((x, y + direction))
                    if y == startY and isEmpty(x, y + direction * 2):
                        moves.append((x, y + direction * 2))

                if x - 1 >= 0 and not isEmpty(x - 1, y + direction):
                    endPieceColor = boardMatrix[y + direction][x - 1][:5]
                    if startPieceColor != endPieceColor:
                         moves.append((x - 1, y + direction))

                if x + 1 <= 7 and not isEmpty(x + 1, y + direction):
                    endPieceColor = boardMatrix[y + direction][x + 1][:5]
                    if startPieceColor != endPieceColor:
                         moves.append((x + 1, y + direction))

        case 'Rook':

            for index in range(1, 8 - x):
                if not isEmpty(x + index, y):
                    endPieceColor = boardMatrix[y][x + index][:5]
                    if startPieceColor == endPieceColor: 
                        break
                    else:
                        moves.append((x + index, y))
                        break
                else:
                    moves.append((x + index, y))

            for index in range(1, 8 - y):
                if not isEmpty(x, y + index):
                    endPieceColor = boardMatrix[y + index][x][:5]
                    if startPieceColor == endPieceColor: 
                        break
                    else:
                        moves.append((x, y + index))
                        break
                else:
                    moves.append((x, y + index))

            for index in range(1, x + 1):
                if not isEmpty(x - index, y):
                    endPieceColor = boardMatrix[y][x - index][:5]
                    if startPieceColor == endPieceColor: 
                        break
                    else:
                        moves.append((x - index, y))
                        break
                else:
                    moves.append((x - index, y))

            for index in range(1, y + 1):
                if not isEmpty(x, y - index):
                    endPieceColor = boardMatrix[y - index][x][:5]
                    if startPieceColor == endPieceColor: 
                        break
                    else:
                        moves.append((x, y - index))
                        break
                else:
                    moves.append((x, y - index))

        case 'Knight':

            if x - 1 >= 0 and y - 2 >= 0:
                if not isEmpty(x - 1, y - 2):
                    endPieceColor = boardMatrix[y - 2][x - 1][:5]
                    if startPieceColor != endPieceColor:
                        moves.append((x - 1, y - 2))            
                else:
                    moves.append((x - 1, y - 2))

            if x - 2 >= 0 and y - 1 >= 0:
                if not isEmpty(x - 2, y - 1):
                    endPieceColor = boardMatrix[y - 1][x - 2][:5]
                    if startPieceColor != endPieceColor:
                        moves.append((x - 2, y - 1))
                else:
                    moves.append((x - 2, y - 1))

            if x + 1 <= 7 and y - 2 >= 0:
                if not isEmpty(x + 1, y - 2):
                    endPieceColor = boardMatrix[y - 2][x + 1][:5]
                    if startPieceColor != endPieceColor:
                        moves.append((x + 1, y - 2))            
                else:
                    moves.append((x + 1, y - 2))

            if x + 2 <= 7 and y - 1 >= 0:
                if not isEmpty(x + 2, y - 1):
                    endPieceColor = boardMatrix[y - 1][x + 2][:5]
                    if startPieceColor != endPieceColor:
                        moves.append((x + 2, y - 1))
                else:
                    moves.append((x + 2, y - 1))

            if x - 1 >= 0 and y + 2 <= 7:
                if not isEmpty(x - 1, y + 2):
                    endPieceColor = boardMatrix[y + 2][x - 1][:5]
                    if startPieceColor != endPieceColor:
                        moves.append((x - 1, y + 2))            
                else:
                    moves.append((x - 1, y + 2))

            if x - 2 >= 0 and y + 1 <= 7:
                if not isEmpty(x - 2, y + 1):
                    endPieceColor = boardMatrix[y + 1][x - 2][:5]
                    if startPieceColor != endPieceColor:
                        moves.append((x - 2, y + 1))
                else:
                    moves.append((x - 2, y + 1))

            if x + 1 <= 7 and y + 2 <= 7:
                if not isEmpty(x + 1, y + 2):
                    endPieceColor = boardMatrix[y + 2][x + 1][:5]
                    if startPieceColor != endPieceColor:
                        moves.append((x + 1, y + 2))         
                else:
                    moves.append((x + 1, y + 2))

            if x + 2 <= 7 and y + 1 <= 7:
                if not isEmpty(x + 2, y + 1):
                    endPieceColor = boardMatrix[y + 1][x + 2][:5]
                    if startPieceColor != endPieceColor:
                        moves.append((x + 2, y + 1))
                else:
                    moves.append((x + 2, y + 1))

        case 'Bishop':
            
            for index in range(1, min(8 - x, 8 - y)):
                if not isEmpty(x + index, y + index):
                    endPieceColor = boardMatrix[y + index][x + index][:5]
                    if startPieceColor == endPieceColor: 
                        break
                    else:
                        moves.append((x + index, y + index))
                        break
                else:
                    moves.append((x + index, y + index))

            for index in range(1, min(x + 1, y + 1)):
                if not isEmpty(x - index, y - index):
                    endPieceColor = boardMatrix[y - index][x - index][:5]
                    if startPieceColor == endPieceColor: 
                        break
                    else:
                        moves.append((x - index, y - index))
                        break
                else:
                    moves.append((x - index, y - index))

            for index in range(1, min(8 - x, y + 1)):
                if not isEmpty(x + index, y - index):
                    endPieceColor = boardMatrix[y - index][x + index][:5]
                    if startPieceColor == endPieceColor: 
                        break
                    else:
                        moves.append((x + index, y - index))
                        break
                else:
                    moves.append((x + index, y - index))

            for index in range(1, min(x + 1, 8 - y)):
                if not isEmpty(x - index, y + index):
                    endPieceColor = boardMatrix[y + index][x - index][:5]
                    if startPieceColor == endPieceColor: 
                        break
                    else:
                        moves.append((x - index, y + index))
                        break
                else:
                    moves.append((x - index, y + index))

        case 'Queen':

            for index in range(1, 8 - x):
                if not isEmpty(x + index, y):
                    endPieceColor = boardMatrix[y][x + index][:5]
                    if startPieceColor == endPieceColor: 
                        break
                    else:
                        moves.append((x + index, y))
                        break
                else:
                    moves.append((x + index, y))

            for index in range(1, 8 - y):
                if not isEmpty(x, y + index):
                    endPieceColor = boardMatrix[y + index][x][:5]
                    if startPieceColor == endPieceColor: 
                        break
                    else:
                        moves.append((x, y + index))
                        break
                else:
                    moves.append((x, y + index))

            for index in range(1, x + 1):
                if not isEmpty(x - index, y):
                    endPieceColor = boardMatrix[y][x - index][:5]
                    if startPieceColor == endPieceColor: 
                        break
                    else:
                        moves.append((x - index, y))
                        break
                else:
                    moves.append((x - index, y))

            for index in range(1, y + 1):
                if not isEmpty(x, y - index):
                    endPieceColor = boardMatrix[y - index][x][:5]
                    if startPieceColor == endPieceColor: 
                        break
                    else:
                        moves.append((x, y - index))
                        break
                else:
                    moves.append((x, y - index))

            for index in range(1, min(8 - x, 8 - y)):
                if not isEmpty(x + index, y + index):
                    endPieceColor = boardMatrix[y + index][x + index][:5]
                    if startPieceColor == endPieceColor: 
                        break
                    else:
                        moves.append((x + index, y + index))
                        break
                else:
                    moves.append((x + index, y + index))

            for index in range(1, min(x + 1, y + 1)):
                if not isEmpty(x - index, y - index):
                    endPieceColor = boardMatrix[y - index][x - index][:5]
                    if startPieceColor == endPieceColor: 
                        break
                    else:
                        moves.append((x - index, y - index))
                        break
                else:
                    moves.append((x - index, y - index))

            for index in range(1, min(8 - x, y + 1)):
                if not isEmpty(x + index, y - index):
                    endPieceColor = boardMatrix[y - index][x + index][:5]
                    if startPieceColor == endPieceColor: 
                        break
                    else:
                        moves.append((x + index, y - index))
                        break
                else:
                    moves.append((x + index, y - index))

            for index in range(1, min(x + 1, 8 - y)):
                if not isEmpty(x - index, y + index):
                    endPieceColor = boardMatrix[y + index][x - index][:5]
                    if startPieceColor == endPieceColor: 
                        break
                    else:
                        moves.append((x - index, y + index))
                        break
                else:
                    moves.append((x - index, y + index))

        case 'King':
            
            for xIndex in range(-1, 2):
                for yIndex in range(-1, 2):
                    if 0 <= x + xIndex <= 7 and 0 <= y + yIndex <= 7:
                        if not isEmpty(x + xIndex, y + yIndex):
                            endPieceColor = boardMatrix[y + yIndex][x + xIndex][:5]
                            if startPieceColor != endPieceColor: 
                                moves.append((x + xIndex, y + yIndex))
                        else:
                            moves.append((x + xIndex, y + yIndex))

    return moves

def removeIllegalMoves(x: int, y:int, moves: list) -> list:

    finalMoves = []

    for move in moves:
        
        endX, endY = move

        startPiece, endPiece = boardMatrix[y][x], boardMatrix[endY][endX]

        fromTo(x, y, endX, endY)

        if not playerIsChecked():
            finalMoves.append(move)

        boardMatrix[y][x], boardMatrix[endY][endX] = startPiece, endPiece

    return finalMoves

def fromTo(startX: int, startY: int, endX: int, endY: int):

    try:
        boardMatrix[endY][endX] = boardMatrix[startY][startX]
        boardMatrix[startY][startX] = ''
 
    except IndexError:
        print('Start or end tile out of bounds.')

def playerIsChecked() -> bool:

    playerKingPosition = ()
    opponentMoves = []

    for x in range(8):
        for y in range(8):
            if not isEmpty(x, y):

                piece = boardMatrix[y][x]
                pieceColor = piece[:5]
                pieceType = piece[5:]

                if pieceColor == playerTurn and pieceType == 'King':
                    playerKingPosition = (x, y)

                if pieceColor != playerTurn:
                    opponentMoves.extend(generateMoves(x, y))

    return playerKingPosition in opponentMoves

def anyMovesAvailabe(player: str) -> bool:

    moves = []

    for xIndex in range(8):
        for yIndex in range(8):
            if not isEmpty(xIndex, yIndex):
                piece = boardMatrix[yIndex][xIndex]
                pieceColor = piece[:5]
                if pieceColor == player:
                    moves.extend(removeIllegalMoves(xIndex, yIndex, generateMoves(xIndex, yIndex)))

    return len(moves) > 0

def isEmpty(x: int, y:int) -> bool:
    return boardMatrix[y][x] == ''

def squareFromMousePosition() -> tuple:
    x, y = pygame.mouse.get_pos()
    return (x // tileWidth, y // tileHeight)

def changePlayerTurn(playerTurn: str) -> str:
    playerTurn = 'black' if playerTurn == 'white' else 'white'
    return playerTurn



while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open('save.txt', 'w') as saveFile:
                saveFile.write(f'{playerTurn},')
                for xIndex in range(8):
                    for yIndex in range(8):
                        if boardMatrix[yIndex][xIndex] == '':
                            saveFile.write(f'empty,')
                        else:
                            saveFile.write(f'{boardMatrix[yIndex][xIndex]},')
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
        
            selectedSquare = squareFromMousePosition()
            sqareX, squareY = selectedSquare
            squareColor = boardMatrix[squareY][sqareX][:5]
            
            if legalMoves == [] or squareColor == playerTurn:
                startX, startY = selectedSquare
                startPiece = boardMatrix[startY][startX]
                startPieceColor = startPiece[:5]
                if startPieceColor == playerTurn:
                    legalMoves = removeIllegalMoves(startX, startY, generateMoves(startX, startY))
            else:
                endX, endY = selectedSquare
                if selectedSquare in legalMoves:
                    fromTo(startX, startY, endX, endY)
                    playerTurn = changePlayerTurn(playerTurn)
                    startX, startY = None, None
                    if not anyMovesAvailabe(playerTurn):
                        pygame.quit()
                else:
                    startX, startY = endX, endY
                endX, endY = None, None
                legalMoves = []
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:

                playerTurn = 'white'
                legalMoves = []
                startX, startY, endX, endY = None, None, None, None
                boardMatrix = [
                    ['blackRook', 'blackKnight', 'blackBishop', 'blackKing', 'blackQueen', 'blackBishop', 'blackKnight', 'blackRook'],
                    ['blackPawn', 'blackPawn', 'blackPawn', 'blackPawn', 'blackPawn', 'blackPawn', 'blackPawn', 'blackPawn'],
                    ['','','','','','','',''],
                    ['','','','','','','',''],
                    ['','','','','','','',''],
                    ['','','','','','','',''],
                    ['whitePawn', 'whitePawn', 'whitePawn', 'whitePawn', 'whitePawn', 'whitePawn', 'whitePawn', 'whitePawn'],
                    ['whiteRook', 'whiteKnight', 'whiteBishop', 'whiteQueen', 'whiteKing', 'whiteBishop', 'whiteKnight', 'whiteRook'],
                ]

    window.fill('black')
    drawBoard() 
    pygame.display.flip()