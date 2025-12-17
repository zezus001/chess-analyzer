from constants import FILES, OPPOSITE_COLOR, PIECE_MOVEMENTS, PIECE_CAPTURES, SLIDING_PIECES

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
            'pawn': 0,
            'knight': 0,
            'bishop': 0,
            'rook': 0,
            'queen': 0,
            'king': 0
        }
        self.legalMoves = {} # for later
        self.moveHistory = {}
        self.FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        self.turn = 'white'
        self.halfMoves = 0
        self.fullMoves = 0

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
        self.pieceCounters[pieceType] += 1
        self.pieces[color][piece.id] = piece

    def startingPieces(self):
        pass # todo: use createPiece to initialize starting position

if __name__ == '__main__':
    board = Board()

    for rank in board.board:
        print(rank)