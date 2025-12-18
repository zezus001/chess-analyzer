from constants import FILES, OPPOSITE_COLOR, PIECE_MOVEMENTS, PIECE_CAPTURES, SLIDING_PIECES, PIECE_COUNTER

class Piece():
    def __init__(self, pieceType, pos, color, id):
        self.type = pieceType
        self.pos = pos
        self.color = color
        self.id = id # A unique identifier for piece lookup
        self.slides = pieceType in SLIDING_PIECES
        
class Board():
    def __init__(self):
        self.board = self.startPos() # Visual elements
        self.pieces = {
            'white': {},
            'black': {}
        }
        self.pieceCounters = {
            'white': PIECE_COUNTER.copy(),
            'black': PIECE_COUNTER.copy()
        }
        self.legalMoves = {}
        self.moveHistory = {}
        self.FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        self.turn = 'white'
        self.halfMoves = 0
        self.fullMoves = 0

        self.startingPieces()

    def startPos(self):
        return [
            ['r','n','b','q','k','b','n','r'],
            ['p','p','p','p','p','p','p','p'],
            [' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' '],
            ['P','P','P','P','P','P','P','P'],
            ['R','N','B','Q','K','B','N','R']
        ]
    
    def createPiece(self, pieceType, pos, color):
        piece = Piece(pieceType, pos, color, f'{pieceType}_{self.pieceCounters[pieceType]}')
        self.pieceCounters[color][pieceType] += 1
        self.pieces[color][piece.id] = piece

    def startingPieces(self):
        color = 'white'
        for rank in range(1, 9, 7):
            createPiece('rook', [1, rank], color)
            createPiece('knight', [2, rank], color)
            createPiece('bishop', [3, rank], color)
            createPiece('queen', [4, rank], color)
            createPiece('king', [5, rank], color)
            createPiece('bishop', [6, rank], color)
            createPiece('knight', [7, rank], color)
            createPiece('rook', [8, rank], color)
            color = 'black' # Loop runs twice, color will be set to black after first loop
        
        for boardFile in range(1, 9):
            createPiece('pawn', [boardFile, 2], 'white')
            createPiece('pawn', [boardFile, 7], 'black')

if __name__ == '__main__':
    board = Board()

    for rank in board.board:
        print(rank)
