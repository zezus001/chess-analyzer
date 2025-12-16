from constants import FILES, OPPOSITE_COLOR, PIECE_MOVEMENTS, PIECE_CAPTURES, SLIDING_PIECES
class Board():
    def __init__(self):
        self.board = self.startPos()
        self.pieces = {}
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
        pass # define later

    def startingPieces(self):
        pass # use createPiece to initialize starting position

if __name__ == '__main__':
    board = Board()

    for rank in board.board:
        print(rank)