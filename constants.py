FILES = 'abcdefgh'

OPPOSITE_COLOR = {
    'white': 'black',
    'black': 'white'
}
SLIDING_PIECES = ('queen', 'bishop', 'rook')

# rook: horizontal and vertical directions
ROOK_MOVES = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1)
]

# bishop: diagonals
BISHOP_MOVES = [
    (1, 1),   # down-right
    (1, -1),  # down-left
    (-1, 1),  # up-right
    (-1, -1)  # up-left
]

# queen: rook + bishop
QUEEN_MOVES = ROOK_MOVES + BISHOP_MOVES

# knight: L-shapes
KNIGHT_MOVES = [
    (2, 1),
    (2, -1),
    (-2, 1),
    (-2, -1),
    (1, 2),
    (1, -2),
    (-1, 2),
    (-1, -2)
]

# king: like queen but only 1 square
KING_MOVES = QUEEN_MOVES  # Board logic will limit to 1 step

# pawn moves: separate handling recommended
# define only directions; distances handled in move logic
PAWN_MOVES = [(1, 0)]  # forward, will invert based on color

PIECE_MOVEMENTS = {
    "rook": ROOK_MOVES,
    "bishop": BISHOP_MOVES,
    "queen": QUEEN_MOVES,
    "knight": KNIGHT_MOVES,
    "king": KING_MOVES,
    "pawn": PAWN_MOVES
}
