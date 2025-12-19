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

