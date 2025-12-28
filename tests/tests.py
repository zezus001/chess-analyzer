import pytest
from board import Board

def testOutOfBounds():
    board = Board()
    assert board.isOutOfBounds([0, 5]) == True
    assert board.isOutOfBounds([9, 5]) == True
    assert board.isOutOfBounds([5, 0]) == True
    assert board.isOutOfBounds([5, 9]) == True
    assert board.isOutOfBounds([5, 5]) == False

def testCalculateSlidingMovesRook():
    board = Board()
    board.pieces = {'white': {}, 'black': {}}
    rook = board.createPiece('rook', [4, 4], 'white')
    moves = board.calculateSlidingMoves(rook)
    expectedMoves = []
    
    # Horizontal and vertical moves
    for i in range(1, 9):
        if i != 4:
            expectedMoves.append([i, 4])  # horizontal
            expectedMoves.append([4, i])  # vertical

    print(sorted(moves), '\n', sorted(expectedMoves))
    assert sorted(moves) == sorted(expectedMoves)

def testCalculateSlidingMovesBishop():
    board = Board()
    board.pieces = {'white': {}, 'black': {}}
    bishop = board.createPiece('bishop', [4, 4], 'white')
    moves = board.calculateSlidingMoves(bishop)
    expectedMoves = []
    
    # Diagonal moves
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for direction in directions:
        step = 1
        while True:
            target = [4 + direction[0] * step, 4 + direction[1] * step]
            if not (1 <= target[0] <= 8 and 1 <= target[1] <= 8):
                break
            expectedMoves.append(target)
            step += 1

    print(sorted(moves), '\n', sorted(expectedMoves))
    assert sorted(moves) == sorted(expectedMoves)

def testCalculateSlidingMovesQueen():
    board = Board()
    board.pieces = {'white': {}, 'black': {}}
    queen = board.createPiece('queen', [4, 4], 'white')
    moves = board.calculateSlidingMoves(queen)
    expectedMoves = []
    
    # Horizontal, vertical, and diagonal moves
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    for direction in directions:
        step = 1
        while True:
            target = [4 + direction[0] * step, 4 + direction[1] * step]
            if not (1 <= target[0] <= 8 and 1 <= target[1] <= 8):
                break
            expectedMoves.append(target)
            step += 1

    print(sorted(moves), '\n', sorted(expectedMoves))
    assert sorted(moves) == sorted(expectedMoves)

def testCalculateSlidingMovesRookBlocking():
    board = Board()
    board.pieces = {'white': {}, 'black': {}}
    rook = board.createPiece('rook', [4, 4], 'white')
    blocker = board.createPiece('pawn', [5, 4], 'white')  # own piece blocking
    moves = board.calculateSlidingMoves(rook)
    expectedMoves = [[3, 4], [2, 4], [1, 4], [4, 3], [4, 2], [4, 1], [4, 5], [4, 6], [4, 7], [4, 8]]
    print(sorted(moves), '\n', sorted(expectedMoves))
    assert sorted(moves) == sorted(expectedMoves)

def testCalculateSlidingMovesRookCapturing():
    board = Board()
    board.pieces = {'white': {}, 'black': {}}
    rook = board.createPiece('rook', [4, 4], 'white')
    enemy = board.createPiece('pawn', [5, 4], 'black')  # enemy piece to capture
    moves = board.calculateSlidingMoves(rook)
    expectedMoves = [[5, 4], [3, 4], [2, 4], [1, 4], [4, 3], [4, 2], [4, 1], [4, 5], [4, 6], [4, 7], [4, 8]]
    assert sorted(moves) == sorted(expectedMoves)

def testCalculateNonSlidingMovesKnight():
    board = Board()
    board.pieces = {'white': {}, 'black': {}}
    knight = board.createPiece('knight', [4, 4], 'white')
    moves = board.calculateNonSlidingMoves(knight)
    expectedMoves = [
        [6, 5], [6, 3], [2, 5], [2, 3],  # ±2 file, ±1 rank
        [5, 6], [5, 2], [3, 6], [3, 2]   # ±1 file, ±2 rank
    ]
    assert sorted(moves) == sorted(expectedMoves)

def testCalculateNonSlidingMovesKnightEdge():
    board = Board()
    board.pieces = {'white': {}, 'black': {}}
    knight = board.createPiece('knight', [1, 1], 'white')  # corner
    moves = board.calculateNonSlidingMoves(knight)
    expectedMoves = [[3, 2], [2, 3]]  # only 2 valid moves from corner
    assert sorted(moves) == sorted(expectedMoves)

def testCalculateNonSlidingMovesKing():
    board = Board()
    board.pieces = {'white': {}, 'black': {}}
    king = board.createPiece('king', [4, 4], 'white')
    moves = board.calculateNonSlidingMoves(king)
    expectedMoves = [
        [3, 3], [3, 4], [3, 5], [4, 3], [4, 5], [5, 3], [5, 4], [5, 5]
    ]
    assert sorted(moves) == sorted(expectedMoves)

def testCalculateNonSlidingMovesKingEdge():
    board = Board()
    board.pieces = {'white': {}, 'black': {}}
    king = board.createPiece('king', [1, 1], 'white')  # corner
    moves = board.calculateNonSlidingMoves(king)
    expectedMoves = [[1, 2], [2, 1], [2, 2]]
    assert sorted(moves) == sorted(expectedMoves)

def testCalculateNonSlidingMovesPawn():
    board = Board()
    board.pieces = {'white': {}, 'black': {}}
    pawn = board.createPiece('pawn', [4, 2], 'white')
    moves = board.calculatePawnMoves(pawn)
    expectedMoves = [[4, 3], [4, 4]]  # Single and double forward moves from starting position
    assert sorted(moves) == sorted(expectedMoves)

def testCalculateNonSlidingMovesPawnBlack():
    board = Board()
    board.pieces = {'white': {}, 'black': {}}
    pawn = board.createPiece('pawn', [4, 7], 'black')
    moves = board.calculatePawnMoves(pawn)
    expectedMoves = [[4, 6], [4, 5]]  # Single and double forward moves from starting position
    assert sorted(moves) == sorted(expectedMoves)

def testCalculateNonSlidingMovesPawnCapture():
    board = Board()
    board.pieces = {'white': {}, 'black': {}}
    pawn = board.createPiece('pawn', [4, 2], 'white')
    enemy1 = board.createPiece('pawn', [3, 3], 'black')  # diagonal left
    enemy2 = board.createPiece('pawn', [5, 3], 'black')  # diagonal right
    moves = board.calculatePawnMoves(pawn)
    expectedMoves = [[4, 3], [4, 4], [3, 3], [5, 3]]  # forward moves + captures
    assert sorted(moves) == sorted(expectedMoves)

def testCalculateNonSlidingMovesBlocking():
    board = Board()
    board.pieces = {'white': {}, 'black': {}}
    knight = board.createPiece('knight', [4, 4], 'white')
    blocker = board.createPiece('pawn', [6, 5], 'white')  # block one knight move
    moves = board.calculateNonSlidingMoves(knight)
    expectedMoves = [
        [6, 3], [2, 5], [2, 3],  # remaining moves
        [5, 6], [5, 2], [3, 6], [3, 2]
    ]
    assert sorted(moves) == sorted(expectedMoves)

def testCalculateNonSlidingMovesCapturing():
    board = Board()
    board.pieces = {'white': {}, 'black': {}}
    knight = board.createPiece('knight', [4, 4], 'white')
    enemy = board.createPiece('pawn', [6, 5], 'black')  # enemy on knight move square
    moves = board.calculateNonSlidingMoves(knight)
    expectedMoves = [
        [6, 5], [6, 3], [2, 5], [2, 3],  # includes capture
        [5, 6], [5, 2], [3, 6], [3, 2]
    ]
    assert sorted(moves) == sorted(expectedMoves)

def testCalculateStartingPositionMoves():
    board = Board()
    movesWhite = board.calculateMoves('white')
    movesBlack = board.calculateMoves('black')
    
    # Flatten the list of move lists from the dict values
    allWhiteMoves = [move for pieceMoves in movesWhite.values() for move in pieceMoves]
    allBlackMoves = [move for pieceMoves in movesBlack.values() for move in pieceMoves]
    
    # Check total moves: 16 pawn moves + 4 knight moves = 20 for each color
    assert len(allWhiteMoves) == 20
    assert len(allBlackMoves) == 20
    
    # Check specific knight moves
    # White knight on b1 (2,1) can move to a3 (1,3) and c3 (3,3)
    assert [1, 3] in allWhiteMoves
    assert [3, 3] in allWhiteMoves
    # White knight on g1 (7,1) can move to f3 (6,3) and h3 (8,3)
    assert [6, 3] in allWhiteMoves
    assert [8, 3] in allWhiteMoves
    
    # Black knight on b8 (2,8) can move to a6 (1,6) and c6 (3,6)
    assert [1, 6] in allBlackMoves
    assert [3, 6] in allBlackMoves
    # Black knight on g8 (7,8) can move to f6 (6,6) and h6 (8,6)
    assert [6, 6] in allBlackMoves
    assert [8, 6] in allBlackMoves
    
    # Check pawn double moves (from rank 2 to 4 for white, rank 7 to 5 for black)
    whiteDoubleMoves = [move for move in allWhiteMoves if move[1] == 4]  # rank 4
    blackDoubleMoves = [move for move in allBlackMoves if move[1] == 5]  # rank 5
    assert len(whiteDoubleMoves) == 8  # 8 pawns
    assert len(blackDoubleMoves) == 8  # 8 pawns

def testIsInCheckByQueen():
    board = Board()
    # Move white king to e4 (5,4)
    board.kings['white'].pos = [5, 4]
    # Place black queen on d4 (4,4), attacking the king
    queen = board.createPiece('queen', [4, 4], 'black')
    assert board.isInCheck('white') == True

def testIsInCheckByRook():
    board = Board()
    # Move white king to e4 (5,4)
    board.kings['white'].pos = [5, 4]
    # Place black rook on h4 (8,4), attacking horizontally
    rook = board.createPiece('rook', [8, 4], 'black')
    assert board.isInCheck('white') == True

def testIsInCheckByPawn():
    board = Board()
    # Move white king to e4 (5,4)
    board.kings['white'].pos = [5, 4]
    # Place black pawn on d5 (4,5), attacking diagonally
    pawn = board.createPiece('pawn', [4, 5], 'black')
    assert board.isInCheck('white') == True

def testNotInCheck():
    board = Board()
    # Starting position, no one in check
    assert board.isInCheck('white') == False
    assert board.isInCheck('black') == False

def testIsInCheckBlack():
    board = Board()
    # Move black king to e5 (5,5)
    board.kings['black'].pos = [5, 5]
    # Place white queen on d5 (4,5), attacking the king
    queen = board.createPiece('queen', [4, 5], 'white')
    assert board.isInCheck('black') == True

def testIsInCheckByBishop():
    board = Board()
    board.pieces = {'white': {}, 'black': {}}
    
    whiteKing = board.createPiece('king', [4, 4], 'white')   # d4
    board.kings['white'] = whiteKing
    
    bishop = board.createPiece('bishop', [7, 7], 'black')    # g7 diagonal
    assert board.isInCheck('white') == True


def testIsInCheckByKnight():
    board = Board()
    board.pieces = {'white': {}, 'black': {}}
    
    whiteKing = board.createPiece('king', [4, 4], 'white')   # e4
    board.kings['white'] = whiteKing
    
    knight = board.createPiece('knight', [5, 6], 'black')    # f5 knight move
    assert board.isInCheck('white') == True


def testPieceBlockingPreventsCheck():
    board = Board()
    board.pieces = {'white': {}, 'black': {}}

    king = board.createPiece('king', [5, 1], 'white')        # e1
    board.kings['white'] = king
    
    rook = board.createPiece('rook', [5, 8], 'black')        # e8
    blocker = board.createPiece('pawn', [5, 4], 'white')     # e4 blocks line

    assert board.isInCheck('white') == False

def testPinnedPieceCannotMove():
    board = Board()
    board.pieces = {'white': {}, 'black': {}}
    
    king = board.createPiece('king', [5, 1], 'white')        # e1
    board.kings['white'] = king
    
    rook = board.createPiece('bishop', [5, 2], 'white')        # e2 pinned piece
    attacker = board.createPiece('rook', [5, 8], 'black')    # e8 pinning rook

    moves = board.calculateMoves('white')

    # Rook should either not appear or have no legal moves
    assert rook.id not in moves or len(moves[rook.id]) == 0

def testPinnedPieceCanCaptureAttacker():
    board = Board()
    board.pieces = {'white': {}, 'black': {}}
    
    king = board.createPiece('king', [5, 1], 'white')        # e1
    board.kings['white'] = king
    
    rook = board.createPiece('rook', [5, 2], 'white')        # e2
    attacker = board.createPiece('rook', [5, 5], 'black')    # e5 (direct pin & capturable)

    moves = board.calculateMoves('white')
    
    assert rook.id in moves
    assert [5, 5] in moves[rook.id]          # capture is legal

def testKingCannotMoveIntoCheck():
    board = Board()
    board.pieces = {'white': {}, 'black': {}}
    
    king = board.createPiece('king', [5, 1], 'white')        # e1
    board.kings['white'] = king
    
    rook = board.createPiece('rook', [1, 2], 'black')        # a2 controls file

    moves = board.calculateMoves('white')

    kingMoves = moves[king.id]
    
    assert kingMoves == [[6, 1], [4, 1]]

def testKingsCannotBeAdjacent():
    board = Board()
    board.pieces = {'white': {}, 'black': {}}
    
    whiteKing = board.createPiece('king', [4, 4], 'white')   # e5
    board.kings['white'] = whiteKing
    
    blackKing = board.createPiece('king', [6, 4], 'black')   # g6
    board.kings['black'] = blackKing

    whiteKingMoves = board.calculateMoves('white')[whiteKing.id]
    blackKingMoves = board.calculateMoves('black')[blackKing.id]

    for illegalMove in [[5, 3], [5, 4], [5, 5]]:
        assert illegalMove not in whiteKingMoves
        assert illegalMove not in blackKingMoves

def testSimpleCheckmate():
    board = Board()
    board.pieces = {'white': {}, 'black': {}}

    # White king trapped in corner
    whiteKing = board.createPiece('king', [8, 1], 'white')
    board.kings['white'] = whiteKing

    # Black rooks delivering mate
    rook1 = board.createPiece('rook', [1, 1], 'black')       
    rook2 = board.createPiece('rook', [2, 2], 'black')       # ladder mate

    assert board.isInCheckmate() == True

def testSimpleStalemate():
    board = Board()
    board.pieces = {'white': {}, 'black': {}}

    # White king on h1 with no legal moves
    whiteKing = board.createPiece('king', [1, 1], 'white')
    board.kings['white'] = whiteKing

    # Black queen controlling all escape squares
    blackQueen = board.createPiece('queen', [3, 2], 'black')

    assert board.isInStalemate() == True

def testFoolsMate():
    board = Board()

    board.makeMove(board.pieces['white']['pawn_6'], [6, 3])  # f3
    board.makeMove(board.pieces['black']['pawn_5'], [5, 5])  # e5
    board.makeMove(board.pieces['white']['pawn_7'], [7, 4])  # g3
    board.makeMove(board.pieces['black']['queen_1'], [8, 4])  # Qh4#
    
    assert board.isInCheckmate() == True

def testScholarMate():
    board = Board()

    board.makeMove(board.pieces['white']['pawn_5'], [5, 4])  # e4
    board.makeMove(board.pieces['black']['pawn_5'], [5, 5])  # e5
    board.makeMove(board.pieces['white']['bishop_2'], [3, 4])  # Bc4
    board.makeMove(board.pieces['black']['knight_1'], [3, 6])  # Nf6
    board.makeMove(board.pieces['white']['queen_1'], [8, 5])  # Qh5
    board.makeMove(board.pieces['black']['knight_2'], [6, 6])  # Nf6
    board.makeMove(board.pieces['white']['queen_1'], [6, 7])  # Qxf7#

    assert board.isInCheckmate() == True

def testCanCastleKingside():
    board = Board()
    
    # Clear squares between king and rook
    board.pieces['white'] = {pid: p for pid, p in board.pieces['white'].items() if p.type not in ['knight', 'bishop', 'queen']}
    
    # Ensure no checks on path
    assert board.canCastleKingside() == True

def testCanCastleQueenside():
    board = Board()
    
    # Clear squares between king and rook
    board.pieces['white'] = {pid: p for pid, p in board.pieces['white'].items() if p.type not in ['knight', 'bishop', 'queen']}
    
    # Ensure no checks on path
    assert board.canCastleQueenside() == True

def testBlackCanCastleKingside():
    board = Board()
    
    # Clear squares between king and rook
    board.pieces['black'] = {pid: p for pid, p in board.pieces['black'].items() if p.type not in ['knight', 'bishop', 'queen']}
    
    for piece in board.pieces['black'].values():
        print(piece.type, piece.pos)
    # Ensure no checks on path
    assert board.canCastleKingside('black') == True

def testCannotCastleThroughCheck():
    board = Board()
    
    # Clear squares between king and rook
    board.pieces['white'] = {pid: p for pid, p in board.pieces['white'].items() if p.type not in ['knight', 'bishop', 'queen']}
    
    # Place an enemy knight attacking the square the king would pass through
    enemyKnight = board.createPiece('knight', [5, 3], 'black')

    assert board.canCastleKingside() == False

def testBlackCannotCastleThroughCheck():
    board = Board()
    
    # Clear squares between king and rook
    board.pieces['black'] = {pid: p for pid, p in board.pieces['black'].items() if p.type not in ['knight', 'bishop', 'queen']}
    
    # Place an enemy knight attacking the square the king would pass through
    enemyKnight = board.createPiece('knight', [5, 6], 'white')

    assert board.canCastleKingside('black') == False
    
def testCannotCastleIfKingMoves():
    board = Board()
    
    # Clear squares between king and rook
    board.pieces['white'] = {pid: p for pid, p in board.pieces['white'].items() if p.type not in ['knight', 'bishop', 'queen']}

    # Move the king
    board.makeMove(board.kings['white'], [6, 1])

    assert board.canCastleKingside() == False

def testCannotCastleIfRookMoves():
    board = Board()
    
    # Clear squares between king and rook
    board.pieces['white'] = {pid: p for pid, p in board.pieces['white'].items() if p.type not in ['knight', 'bishop', 'queen']}

    # Move the rook
    rook = board.getPieceAt([8, 1])
    board.makeMove(rook, [7, 1])

    assert board.canCastleKingside() == False