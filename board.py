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
        self.kings = {}  # Store kings for quick access
        self.check = False
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

    def drawBoard(self):
        for rank in self.board:
            print(' '.join(rank))
    
    def createPiece(self, pieceType, pos, color):
        piece = Piece(pieceType, pos, color, f'{pieceType}_{self.pieceCounters[color][pieceType]}')
        self.pieceCounters[color][pieceType] += 1
        self.pieces[color][piece.id] = piece
        return piece # for testing

    def genStartingPieces(self):
        color = 'white'
        for rank in [1, 8]:
            self.createPiece('rook', [1, rank], color)
            self.createPiece('knight', [2, rank], color)
            self.createPiece('bishop', [3, rank], color)
            self.createPiece('queen', [4, rank], color)
            self.createPiece('bishop', [6, rank], color)
            self.createPiece('knight', [7, rank], color)
            self.createPiece('rook', [8, rank], color)

            king = self.createPiece('king', [5, rank], color)
            self.kings[color] = king

            color = 'black' # Loop runs twice, color will be set to black after first loop
        
        for boardFile in range(1, 9):
            self.createPiece('pawn', [boardFile, 2], 'white')
            self.createPiece('pawn', [boardFile, 7], 'black')

    def isOutOfBounds(self, pos):
        return not (1 <= pos[0] <= 8 and 1 <= pos[1] <= 8)

    def getPieceAt(self, pos):
        for colorPieces in self.pieces.values():
            for piece in colorPieces.values():
                if piece.pos == pos:
                    return piece
        return None

    def isSquareOccupied(self, pos):
        return self.getPieceAt(pos) is not None

    def calculateSlidingMoves(self, piece):
        moves = []
        directions = PIECE_MOVEMENTS[piece.type]
        for direction in directions:
            step = 1
            while True:
                targetSquare = [piece.pos[0] + direction[0] * step, piece.pos[1] + direction[1] * step]

                if self.isOutOfBounds(targetSquare):
                    break

                occupyingPiece = self.getPieceAt(targetSquare)
                if occupyingPiece:
                    if occupyingPiece.color == piece.color:
                        break # Blocked by own piece, stop sliding in this direction
                    else:
                        moves.append(targetSquare) # Can capture enemy piece, add move and stop sliding
                        break
                else:
                    moves.append(targetSquare) # Empty square, add move
                step += 1
        return moves

    def calculateNonSlidingMoves(self, piece):
        moves = []
        directions = PIECE_MOVEMENTS[piece.type]
        for direction in directions:
            targetSquare = [piece.pos[0] + direction[0], piece.pos[1] + direction[1]]

            if self.isOutOfBounds(targetSquare):
                continue

            occupyingPiece = self.getPieceAt(targetSquare)
            if occupyingPiece and occupyingPiece.color == piece.color:
                continue # Blocked by own piece

            moves.append(targetSquare) # Can move to empty square or capture enemy piece
        return moves

    def calculatePawnCaptures(self, piece, only_squares=False):
        moves = []
        direction = 1 if piece.color == 'white' else -1

        for fileOffset in [-1, 1]:
            captureSquare = [piece.pos[0] + fileOffset, piece.pos[1] + direction]
            if not self.isOutOfBounds(captureSquare):
                if only_squares:
                    moves.append(captureSquare)
                else:
                    occupyingPiece = self.getPieceAt(captureSquare)
                    if occupyingPiece and occupyingPiece.color != piece.color:
                        moves.append(captureSquare)

        return moves

    def calculatePawnMoves(self, piece):
        moves = []
        direction = 1 if piece.color == 'white' else -1
        startRank = 2 if piece.color == 'white' else 7

        # Forward move
        forwardSquare = [piece.pos[0], piece.pos[1] + direction]
        if not self.isSquareOccupied(forwardSquare):
            moves.append(forwardSquare)

            # Double move from starting position
            if piece.pos[1] == startRank:
                doubleForwardSquare = [piece.pos[0], piece.pos[1] + 2 * direction]
                if not self.isSquareOccupied(doubleForwardSquare):
                    moves.append(doubleForwardSquare)

        # Captures
        moves.extend(self.calculatePawnCaptures(piece, False))

        return moves
    
    def calculatePieceMoves(self, piece):
        if piece.type == 'pawn':
            return self.calculatePawnMoves(piece)

        if piece.slides:
            return self.calculateSlidingMoves(piece)
        
        return self.calculateNonSlidingMoves(piece)

    def calculatePieceAttackSquares(self, piece):
        if piece.type == 'pawn':
            return self.calculatePawnCaptures(piece, only_squares=True)
        
        # For non-pawns, attack squares are the same as move squares
        return self.calculatePieceMoves(piece)

    def calculateAttackSquares(self, color):
        color = color if color else self.color
        attackSquares = set()
        for piece in self.pieces[color].values():
            pieceAttackSquares = self.calculatePieceAttackSquares(piece)
            for square in pieceAttackSquares:
                attackSquares.add(tuple(square)) # Use tuple to make it hashable
        return attackSquares

    def isInCheck(self, color):
        color = color if color else self.color

        attackSquares = self.calculateAttackSquares(OPPOSITE_COLOR[color])
        king = self.kings.get(color)
        if king and tuple(king.pos) in attackSquares:
            return True
        
        return False
    
    def calculateMoves(self, color):
        color = color if color else self.color

        return {piece.id: self.calculatePieceMoves(piece) for piece in self.pieces[color].values()}
    


if __name__ == '__main__':
    board = Board()

    for rank in board.board:
        print(rank)
