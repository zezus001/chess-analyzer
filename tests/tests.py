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
    board.clearBoard()
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
    board.clearBoard()
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
    board.clearBoard()
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
    board.clearBoard()
    rook = board.createPiece('rook', [4, 4], 'white')
    blocker = board.createPiece('pawn', [5, 4], 'white')  # own piece blocking
    moves = board.calculateSlidingMoves(rook)
    expectedMoves = [[3, 4], [2, 4], [1, 4], [4, 3], [4, 2], [4, 1], [4, 5], [4, 6], [4, 7], [4, 8]]
    print(sorted(moves), '\n', sorted(expectedMoves))
    assert sorted(moves) == sorted(expectedMoves)

def testCalculateSlidingMovesRookCapturing():
    board = Board()
    board.clearBoard()
    rook = board.createPiece('rook', [4, 4], 'white')
    enemy = board.createPiece('pawn', [5, 4], 'black')  # enemy piece to capture
    moves = board.calculateSlidingMoves(rook)
    expectedMoves = [[5, 4], [3, 4], [2, 4], [1, 4], [4, 3], [4, 2], [4, 1], [4, 5], [4, 6], [4, 7], [4, 8]]
    assert sorted(moves) == sorted(expectedMoves)

def testCalculateNonSlidingMovesKnight():
    board = Board()
    board.clearBoard()
    knight = board.createPiece('knight', [4, 4], 'white')
    moves = board.calculateNonSlidingMoves(knight)
    expectedMoves = [
        [6, 5], [6, 3], [2, 5], [2, 3],  # ±2 file, ±1 rank
        [5, 6], [5, 2], [3, 6], [3, 2]   # ±1 file, ±2 rank
    ]
    assert sorted(moves) == sorted(expectedMoves)

def testCalculateNonSlidingMovesKnightEdge():
    board = Board()
    board.clearBoard()
    knight = board.createPiece('knight', [1, 1], 'white')  # corner
    moves = board.calculateNonSlidingMoves(knight)
    expectedMoves = [[3, 2], [2, 3]]  # only 2 valid moves from corner
    assert sorted(moves) == sorted(expectedMoves)

def testCalculateNonSlidingMovesKing():
    board = Board()
    board.clearBoard()
    king = board.createPiece('king', [4, 4], 'white')
    moves = board.calculateNonSlidingMoves(king)
    expectedMoves = [
        [3, 3], [3, 4], [3, 5], [4, 3], [4, 5], [5, 3], [5, 4], [5, 5]
    ]
    assert sorted(moves) == sorted(expectedMoves)

def testCalculateNonSlidingMovesKingEdge():
    board = Board()
    board.clearBoard()
    king = board.createPiece('king', [1, 1], 'white')  # corner
    moves = board.calculateNonSlidingMoves(king)
    expectedMoves = [[1, 2], [2, 1], [2, 2]]
    assert sorted(moves) == sorted(expectedMoves)

def testCalculateNonSlidingMovesPawn():
    board = Board()
    board.clearBoard()
    pawn = board.createPiece('pawn', [4, 2], 'white')
    moves = board.calculatePawnMoves(pawn)
    expectedMoves = [[4, 3], [4, 4]]  # Single and double forward moves from starting position
    assert sorted(moves) == sorted(expectedMoves)

def testCalculateNonSlidingMovesPawnBlack():
    board = Board()
    board.clearBoard()
    pawn = board.createPiece('pawn', [4, 7], 'black')
    moves = board.calculatePawnMoves(pawn)
    expectedMoves = [[4, 6], [4, 5]]  # Single and double forward moves from starting position
    assert sorted(moves) == sorted(expectedMoves)

def testCalculateNonSlidingMovesPawnCapture():
    board = Board()
    board.clearBoard()
    pawn = board.createPiece('pawn', [4, 2], 'white')
    enemy1 = board.createPiece('pawn', [3, 3], 'black')  # diagonal left
    enemy2 = board.createPiece('pawn', [5, 3], 'black')  # diagonal right
    moves = board.calculatePawnMoves(pawn)
    expectedMoves = [[4, 3], [4, 4], [3, 3], [5, 3]]  # forward moves + captures
    assert sorted(moves) == sorted(expectedMoves)

def testCalculateNonSlidingMovesBlocking():
    board = Board()
    board.clearBoard()
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
    board.clearBoard()
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
    board.clearBoard()
    
    whiteKing = board.createPiece('king', [4, 4], 'white')   # d4
    board.kings['white'] = whiteKing
    
    bishop = board.createPiece('bishop', [7, 7], 'black')    # g7 diagonal
    assert board.isInCheck('white') == True


def testIsInCheckByKnight():
    board = Board()
    board.clearBoard()
    
    whiteKing = board.createPiece('king', [4, 4], 'white')   # e4
    board.kings['white'] = whiteKing
    
    knight = board.createPiece('knight', [5, 6], 'black')    # f5 knight move
    assert board.isInCheck('white') == True


def testPieceBlockingPreventsCheck():
    board = Board()
    board.clearBoard()

    king = board.createPiece('king', [5, 1], 'white')        # e1
    board.kings['white'] = king
    
    rook = board.createPiece('rook', [5, 8], 'black')        # e8
    blocker = board.createPiece('pawn', [5, 4], 'white')     # e4 blocks line

    assert board.isInCheck('white') == False

def testPinnedPieceCannotMove():
    board = Board()
    board.clearBoard()
    
    king = board.createPiece('king', [5, 1], 'white')        # e1
    board.kings['white'] = king
    
    rook = board.createPiece('bishop', [5, 2], 'white')        # e2 pinned piece
    attacker = board.createPiece('rook', [5, 8], 'black')    # e8 pinning rook

    moves = board.calculateMoves('white')

    # Rook should either not appear or have no legal moves
    assert rook.id not in moves or len(moves[rook.id]) == 0

def testPinnedPieceCanCaptureAttacker():
    board = Board()
    board.clearBoard()
    
    king = board.createPiece('king', [5, 1], 'white')        # e1
    board.kings['white'] = king
    
    rook = board.createPiece('rook', [5, 2], 'white')        # e2
    attacker = board.createPiece('rook', [5, 5], 'black')    # e5 (direct pin & capturable)

    moves = board.calculateMoves('white')
    
    assert rook.id in moves
    assert [5, 5] in moves[rook.id]          # capture is legal

def testKingCannotMoveIntoCheck():
    board = Board()
    board.clearBoard()
    
    king = board.createPiece('king', [5, 1], 'white')        # e1
    board.kings['white'] = king
    
    rook = board.createPiece('rook', [1, 2], 'black')        # a2 controls file

    moves = board.calculateMoves('white')

    kingMoves = moves[king.id]
    
    assert kingMoves == [[6, 1], [4, 1]]

def testKingsCannotBeAdjacent():
    board = Board()
    board.clearBoard()
    
    whiteKing = board.createPiece('king', [4, 4], 'white')   # e5
    board.kings['white'] = whiteKing
    
    blackKing = board.createPiece('king', [6, 4], 'black')   # g6
    board.kings['black'] = blackKing

    whiteKingMoves = board.calculateMoves('white')[whiteKing.id]
    blackKingMoves = board.calculateMoves('black')[blackKing.id]

    for illegalMove in [[5, 3], [5, 4], [5, 5]]:
        assert illegalMove not in whiteKingMoves
        assert illegalMove not in blackKingMoves

def testDoubleCheck():
    board = Board()
    board.clearBoard()

    whiteKing = board.createPiece('king', [4, 3], 'white')
    board.kings['white'] = whiteKing
    whiteRook = board.createPiece('rook', [7, 4], 'white')

    blackQueen = board.createPiece('queen', [7, 6], 'black')
    blackRook = board.createPiece('rook', [6, 5], 'black')

    board.turn = 'black'
    assert board.isInCheck('white') == False

    board.makeMove(blackRook, [4, 5])  # Double check from queen and rook

    assert board.isInCheck('white') == True

    moves = board.calculateMoves()

    assert whiteKing.id in moves
    assert len(moves[whiteKing.id]) > 0  # King must move
    assert whiteRook.id not in moves  # Rook cannot block or capture

def testSimpleCheckmate():
    board = Board()
    board.clearBoard()

    # White king trapped in corner
    whiteKing = board.createPiece('king', [8, 1], 'white')
    board.kings['white'] = whiteKing

    # Black rooks delivering mate
    rook1 = board.createPiece('rook', [1, 1], 'black')       
    rook2 = board.createPiece('rook', [2, 2], 'black')       # ladder mate

    assert board.isInCheckmate() == True

def testSimpleStalemate():
    board = Board()
    board.clearBoard()

    # White king on h1 with no legal moves
    whiteKing = board.createPiece('king', [1, 1], 'white')
    board.kings['white'] = whiteKing

    # Black queen controlling all escape squares
    blackQueen = board.createPiece('queen', [3, 2], 'black')

    assert board.isInStalemate() == True

def testPinnedPieceCheckmate():
    board = Board()
    board.clearBoard()

    whiteKing = board.createPiece('king', [1, 1], 'white')        # a1
    board.kings['white'] = whiteKing
    pinnedQueen = board.createPiece('queen', [2, 2], 'white')     # b2

    blackPawn = board.createPiece('pawn', [2, 3], 'black')          # b3
    blackRook = board.createPiece('rook', [3, 2], 'black')
    blackBishop = board.createPiece('bishop', [6, 6], 'black')

    board.turn = 'black'
    board.makeMove(blackRook, [3, 1])

    assert board.isInCheckmate() == True

def testStalemateWithPinnedPiece():
    board = Board()
    board.clearBoard()

    whiteKing = board.createPiece('king', [1, 1], 'white')        # a1
    board.kings['white'] = whiteKing
    pinnedPawn = board.createPiece('pawn', [2, 2], 'white')     # b2

    blackKing = board.createPiece('king', [4, 2], 'black')        # d2
    board.kings['black'] = blackKing
    blackLightBishop = board.createPiece('bishop', [3, 4], 'black')          # c4
    blackDarkBishop = board.createPiece('bishop', [4, 4], 'black')

    board.turn = 'black'
    board.makeMove(blackKing, [3, 2])

    assert board.isInStalemate() == True

def testStalemateWithManyPieces():
    board = Board()
    board.clearBoard()

    whiteKing = board.createPiece('king', [1, 3], 'white')        # a3
    board.kings['white'] = whiteKing
    whiteRook = board.createPiece('rook', [2, 4], 'white')       # b4
    whiteBishop = board.createPiece('bishop', [2, 3], 'white')   # b3

    blackBishop = board.createPiece('bishop', [3, 5], 'black')         # c5
    blackKnight = board.createPiece('knight', [3, 8], 'black')         # b6
    blackRook1 = board.createPiece('rook', [6, 3], 'black')         # f3
    blackRook2 = board.createPiece('rook', [3, 2], 'black')         # c2

    whiteDPawn = board.createPiece('pawn', [4, 6], 'white')     # d6
    blackDPawn = board.createPiece('pawn', [4, 7], 'black')     # d7
    whiteEPawn = board.createPiece('pawn', [5, 5], 'white')     # e5
    blackEPawn = board.createPiece('pawn', [5, 6], 'black')     # e6
    whiteFPawn = board.createPiece('pawn', [6, 4], 'white')     # f4
    blackFPawn = board.createPiece('pawn', [6, 5], 'black')     # f5
    whiteGPawn = board.createPiece('pawn', [7, 3], 'white')     # g3
    blackGPawn = board.createPiece('pawn', [7, 4], 'black')     # g4
    whiteHPawn = board.createPiece('pawn', [8, 2], 'white')     # h2
    blackHPawn = board.createPiece('pawn', [8, 3], 'black')     # h3

    board.turn = 'black'
    board.makeMove(blackKnight, [2, 6])

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

def testCastleKingside():
    board = Board()
    
    # Clear squares between king and rook
    board.removePiece(board.getPieceAt([6, 1]))  # f1
    board.removePiece(board.getPieceAt([7, 1]))  # g1

    # Ensure no checks on path
    assert board.canCastleKingside() == True

    board.makeMove(board.kings['white'], [7, 1])  # e1 to g1
    king = board.kings['white']
    rook = board.pieces['white']['rook_2']  # h1 rook
    assert king.pos == [7, 1]
    assert rook.pos == [6, 1]

def testCastleQueenside():
    board = Board()
    
    # Clear squares between king and rook
    board.removePiece(board.getPieceAt([2, 1]))  # f1
    board.removePiece(board.getPieceAt([3, 1]))  # f1
    board.removePiece(board.getPieceAt([4, 1]))  # g1

    # Ensure no checks on path
    assert board.canCastleQueenside() == True

    board.makeMove(board.kings['white'], [3, 1])  # e1 to c1
    king = board.kings['white']
    rook = board.pieces['white']['rook_1']  # a1 rook
    assert king.pos == [3, 1]
    assert rook.pos == [4, 1]

def testBlackCastleKingside():
    board = Board()
    
    # Clear squares between king and rook
    board.removePiece(board.getPieceAt([6, 8]))  # f8
    board.removePiece(board.getPieceAt([7, 8]))  # g8

    # Ensure no checks on path
    assert board.canCastleKingside('black') == True

    board.makeMove(board.kings['black'], [7, 8])  # e8 to g8
    king = board.kings['black']
    rook = board.pieces['black']['rook_2']  # h8 rook
    assert king.pos == [7, 8]
    assert rook.pos == [6, 8]

def testCannotCastleThroughCheck():
    board = Board()
    
    # Clear squares between king and rook
    board.removePiece(board.getPieceAt([6, 1]))  # f1
    board.removePiece(board.getPieceAt([7, 1]))  # g1

    # Place an enemy knight attacking the square the king would pass through
    enemyKnight = board.createPiece('knight', [5, 3], 'black')

    assert board.canCastleKingside() == False

def testBlackCannotCastleThroughCheck():
    board = Board()
    
    # Clear squares between king and rook
    board.removePiece(board.getPieceAt([6, 8]))  # f8
    board.removePiece(board.getPieceAt([7, 8]))  # g8
    
    # Place an enemy knight attacking the square the king would pass through
    enemyKnight = board.createPiece('knight', [5, 6], 'white')

    assert board.canCastleKingside('black') == False
    
def testCannotCastleIfKingMoves():
    board = Board()
    
    # Clear squares between king and rook
    board.removePiece(board.getPieceAt([6, 1]))  # f1
    board.removePiece(board.getPieceAt([7, 1]))  # g1

    # Move the king
    board.makeMove(board.kings['white'], [6, 1])

    assert board.canCastleKingside() == False

def testCannotCastleIfRookMoves():
    board = Board()
    
    # Clear squares between king and rook
    board.removePiece(board.getPieceAt([6, 1]))  # f1
    board.removePiece(board.getPieceAt([7, 1]))  # g1

    # Move the rook
    rook = board.pieces['white']['rook_2']  # h1 rook
    board.makeMove(rook, [7, 1])

    assert board.canCastleKingside() == False

def testEnPassantCapture():
    board = Board()
    
    whitePawn = board.pieces['white']['pawn_5']  # e pawn
    blackPawn = board.pieces['black']['pawn_4']  # d pawn

    # White pawn moves e2 to e4
    whitePawn.pos = [5, 5]  # Move white pawn to e5 directly for test
    # Black pawn moves d7 to d5
    board.makeMove(blackPawn, [4, 5])
    # White pawn captures en passant d5
    board.turn = 'white'  # Ensure it's white's turn
    board.makeMove(whitePawn, [4, 6])

    assert whitePawn.pos == [4, 6]
    assert 'pawn_4' not in board.pieces['black']  # Black pawn should be captured
    
    whitePawn = board.pieces['white']['pawn_4']  # d pawn
    blackPawn = board.pieces['black']['pawn_3']  # c pawn

    board.pieces['black']['pawn_3'].pos = [3, 4]  # Move black pawn to c4 directly for test
    # White pawn moves d2 to d4
    board.makeMove(whitePawn, [4, 4])
    # Black pawn captures en passant d3
    board.turn = 'black'  # Ensure it's black's turn
    board.makeMove(blackPawn, [4, 3])

    assert blackPawn.pos == [4, 3]
    assert 'pawn_4' not in board.pieces['white']  # White pawn should be captured

def testCannotEnPassantAfterOneMove():
    board = Board()
    
    whitePawn = board.pieces['white']['pawn_5']  # e pawn
    blackPawn = board.pieces['black']['pawn_4']  # d pawn

    # White pawn moves e2 to e4
    whitePawn.pos = [5, 5]  # Move white pawn to e5 directly for test
    # Black pawn moves d7 to d5
    board.turn = 'black'
    board.makeMove(blackPawn, [4, 5])
    # White makes a different move
    otherWhitePawn = board.pieces['white']['pawn_6']  # f pawn
    board.makeMove(otherWhitePawn, [6, 4])
    # Now black tries to capture en passant
    otherBlackPawn = board.pieces['black']['pawn_3']  # c pawn
    board.makeMove(otherBlackPawn, [3, 6])  # Filler move

    whitePawnCaptures = board.calculatePawnCaptures(whitePawn, False)
    
    assert board.enPassantSquare is None
    assert [4, 6] not in whitePawnCaptures  # e5 to d6 should not be possible 

def testPromotion():
    board = Board()
    board.clearBoard()
    
    whitePawn = board.createPiece('pawn', [1, 7], 'white')  # a pawn

    # White pawn moves a7 to a8 and promotes to queen
    board.makeMove(whitePawn, [1, 8])

    promotedPiece = board.getPieceAt([1, 8])
    assert promotedPiece is not None
    assert promotedPiece.type == 'queen'
    assert promotedPiece.pos == [1, 8]

def testBlackPromotion():
    board = Board()
    board.clearBoard()

    blackPawn = board.createPiece('pawn', [8, 2], 'black')  # h pawn

    # Black pawn moves h2 to h1 and promotes to queen
    board.turn = 'black'
    board.makeMove(blackPawn, [8, 1])

    promotedPiece = board.getPieceAt([8, 1])
    assert promotedPiece is not None
    assert promotedPiece.type == 'queen'
    assert promotedPiece.pos == [8, 1]

def testPromotionIntoCheck():
    board = Board()
    board.clearBoard()
    
    blackKing = board.createPiece('king', [8, 8], 'black')        # h8
    board.kings['black'] = blackKing

    whitePawn = board.createPiece('pawn', [1, 7], 'white')  # h pawn

    board.makeMove(whitePawn, [1, 8])

    assert board.isInCheck() == True

def testPromotionIntoCheckmate():
    board = Board()
    board.clearBoard()
    
    blackKing = board.createPiece('king', [8, 8], 'black')        # h8
    board.kings['black'] = blackKing

    whiteRook = board.createPiece('rook', [2, 7], 'white')        # b7
    whitePawn = board.createPiece('pawn', [1, 7], 'white')  # a pawn

    board.makeMove(whitePawn, [1, 8])

    assert board.isInCheckmate() == True

def testPromotionWithCapture():
    board = Board()
    board.clearBoard()

    blackKnight = board.createPiece('knight', [2, 8], 'black')

    whitePawn = board.createPiece('pawn', [1, 7], 'white')  # a pawn

    # White pawn moves a7 to b8 capturing black pawn and promotes to queen
    board.makeMove(whitePawn, [2, 8])

    promotedPiece = board.getPieceAt([2, 8])
    assert promotedPiece is not None
    assert promotedPiece.type == 'queen'
    assert promotedPiece.pos == [2, 8]
    assert 'knight_3' not in board.pieces['black']  # Black pawn should be captured

def testPromotionIntoDoubleCheck():
    board = Board()
    board.clearBoard()
    
    blackKing = board.createPiece('king', [3, 7], 'black')        # h8
    board.kings['black'] = blackKing
    blackRook = board.createPiece('rook', [2, 1], 'black')        # e8
    
    whitePawn = board.createPiece('pawn', [2, 7], 'white')  # a pawn
    whiteQueen = board.createPiece('queen', [1, 7], 'white')        # e1

    board.makeMove(whitePawn, [2, 8])

    assert board.isInCheck() == True
    
    moves = board.calculateMoves()

    assert blackKing.id in moves
    assert len(moves[blackKing.id]) > 0  # King must move
    assert blackRook.id not in moves  # Rook cannot block or capture

def testPromotionIntoStalemate():
    board = Board()
    board.clearBoard()
    
    blackKing = board.createPiece('king', [1, 7], 'black')        # h8
    board.kings['black'] = blackKing

    whiteKing = board.createPiece('king', [3, 6], 'white')        # g7
    whitePawn = board.createPiece('pawn', [3, 7], 'white')  # a pawn

    board.makeMove(whitePawn, [3, 8])

    assert board.isInStalemate() == True

def testSmokeBasicGameFlow():
    board = Board()

    # 1. Board initializes
    assert board.turn == 'white'
    assert len(board.pieces['white']) == 16
    assert len(board.pieces['black']) == 16
    assert board.kings['white'] is not None
    assert board.kings['black'] is not None

    # 2. Legal moves exist for both sides
    white_moves = board.calculateMoves('white')
    assert white_moves
    assert any(white_moves.values())

    # 3. Make a legal white move
    piece_id, moves = next(iter(white_moves.items()))
    move = moves[0]
    piece = board.pieces['white'][piece_id]

    board.makeMove(piece, move)

    # 4. State updated correctly
    assert piece.pos == move
    assert board.turn == 'black'

    # 5. Black can move
    black_moves = board.calculateMoves('black')
    assert black_moves
    assert any(black_moves.values())

    # 6. Board array matches piece positions
    for color in ['white', 'black']:
        for p in board.pieces[color].values():
            x, y = p.pos
            assert board.boardArray[y - 1][x - 1] == p
