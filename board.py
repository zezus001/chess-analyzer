from constants import FILES, OPPOSITE_COLOR, PIECE_MOVEMENTS, SLIDING_PIECES, PIECE_COUNTER

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

        self.genStartingPieces()

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

    def genStartingPieces(self):
        color = 'white'
        for rank in range(1, 9, 7):
            self.createPiece('rook', [1, rank], color)
            self.createPiece('knight', [2, rank], color)
            self.createPiece('bishop', [3, rank], color)
            self.createPiece('queen', [4, rank], color)
            self.createPiece('king', [5, rank], color)
            self.createPiece('bishop', [6, rank], color)
            self.createPiece('knight', [7, rank], color)
            self.createPiece('rook', [8, rank], color)
            color = 'black' # Loop runs twice, color will be set to black after first loop
        
        for boardFile in range(1, 9):
            self.createPiece('pawn', [boardFile, 2], 'white')
            self.createPiece('pawn', [boardFile, 7], 'black')

    def isInCheck(self, color):
        pass # for check detection and piece calculation filtering

    def calculateSlidingMoves(self, piece):
        moves = []
        directions = PIECE_MOVEMENTS[piece.type]
        for direction in directions:
            step = 1
            while True:
                newFile, newRank = piece.pos[0] + direction[0] * step, piece.pos[1] + direction[1] * step

                if newFile < 1 or newFile > 8 or newRank < 1 or newRank > 8:
                    break # Out of bounds

                targetSquare = [newFile, newRank]
                for pieces in self.pieces.values():
                    for targetPiece in pieces.values():
                        if targetPiece.pos == targetSquare:
                            if targetPiece.color == piece.color:
                                break # Blocked by own piece
                            else:
                                moves.append(targetSquare)
                                break # Stop sliding after capture
                        else:
                            moves.append(targetSquare) # Empty square
                    else:
                        continue
                    break # If slide is cut short the loop doesn't need to check the rest of the squares in that direction
                step += 1
        return moves
    
    def calculatePieceMoves(self, piece):
        if piece.slides:
            return self.calculateSlidingMoves(piece)
        else:
            pass # do later
    
    def calculateMoves(self, color):
        color = color if color else self.color

        return [self.calculatePieceMoves(piece for piece in self.pieces[color].values())]
    


if __name__ == '__main__':
    board = Board()

    for rank in board.board:
        print(rank)
