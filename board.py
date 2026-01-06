from constants import FILES, OTHER_COLOR, PIECE_MOVEMENTS, SLIDING_PIECES, PIECE_COUNTER

class Piece():
    def __init__(self, pieceType, pos, color, id):
        self.type = pieceType
        self.pos = pos
        self.color = color
        self.id = id # A unique identifier for piece lookup
        self.slides = pieceType in SLIDING_PIECES
        
class Board():
    def __init__(self):
        self.starterBoard()
    
    def clearBoard(self): # Sets board variables to default values
        self.board = self.startPos() # Visual elements
        self.boardArray = [[None for _ in range(8)] for _ in range(8)] # Logical elements
        self.pieces = {
            'white': {},
            'black': {}
        }
        self.canCastle = {
            'white': {'kingside': True, 'queenside': True},
            'black': {'kingside': True, 'queenside': True}
        }
        self.pieceCounters = {
            'white': PIECE_COUNTER.copy(),
            'black': PIECE_COUNTER.copy()
        }
        self.gameOutcome = {
            'gameOver': False,
            'reason': None,
            'winner': None
        }
        self.legalMoves = {}
        self.moveHistory = []
        self.kings = {}  # Store kings for quick access
        self.enPassantSquare = None
        self.check = False
        self.FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        self.turn = 'white'
        self.halfMoves = 0
        self.fullMoves = 0
    
    def starterBoard(self):
        self.clearBoard()
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
    
    def setPieceOnBoardArray(self, piece, pos):
        self.boardArray[pos[1]-1][pos[0]-1] = piece
    
    def removePieceFromBoardArray(self, pos):
        self.boardArray[pos[1]-1][pos[0]-1] = None
    
    def createPiece(self, pieceType, pos, color):
        self.pieceCounters[color][pieceType] += 1
        pieceId = f'{pieceType}_{self.pieceCounters[color][pieceType]}'

        piece = Piece(pieceType, pos, color, pieceId)
        self.pieces[color][piece.id] = piece
        self.setPieceOnBoardArray(piece, pos)
        
        return piece
        
    def movePiece(self, piece, pos):
        self.removePieceFromBoardArray(piece.pos)
        piece.pos = pos
        self.setPieceOnBoardArray(piece, pos)

    def removePiece(self, piece):
        self.removePieceFromBoardArray(piece.pos)
        del self.pieces[piece.color][piece.id]

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
        return self.boardArray[pos[1]-1][pos[0]-1]

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
                    if occupyingPiece.color != piece.color:
                        moves.append(targetSquare) # Can capture enemy piece, add move and stop sliding

                    break # Blocked by a piece, stop sliding
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
                if only_squares: # For calculating attack squares only
                    moves.append(captureSquare)
                else: # For calculating actual moves
                    occupyingPiece = self.getPieceAt(captureSquare)
                    if occupyingPiece and occupyingPiece.color != piece.color:
                        moves.append(captureSquare)
                    elif self.enPassantSquare and captureSquare == self.enPassantSquare:
                        moves.append(captureSquare)

        return moves

    def calculatePawnMoves(self, piece):
        moves = []
        direction = 1 if piece.color == 'white' else -1
        startRank = 2 if piece.color == 'white' else 7

        # Forward move
        forwardSquare = [piece.pos[0], piece.pos[1] + direction]
        if not self.isSquareOccupied(forwardSquare) and not self.isOutOfBounds(forwardSquare):
            moves.append(forwardSquare)

            # Double move from starting position
            if piece.pos[1] == startRank:
                doubleForwardSquare = [piece.pos[0], piece.pos[1] + 2 * direction]
                if not self.isSquareOccupied(doubleForwardSquare) and not self.isOutOfBounds(doubleForwardSquare):
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

    def calculateAttackSquares(self, color=None):
        color = color if color else self.turn
        attackSquares = set()
        for piece in self.pieces[color].values():
            pieceAttackSquares = self.calculatePieceAttackSquares(piece)
            for square in pieceAttackSquares:
                attackSquares.add(tuple(square)) # Tuple for hashing
        return attackSquares
    
    def isSquareAttacked(self, pos, color=None):
        color = color if color else OTHER_COLOR[self.turn] # Check if square is attacked by opponent
        attackSquares = self.calculateAttackSquares(color)
        return tuple(pos) in attackSquares
    
    def canCastleKingside(self, color=None):
        color = color if color else self.turn
        rank = 1 if color == 'white' else 8

        if not self.canCastle[color]['kingside']:
            return False
        
        castlingRook = self.getPieceAt([8, rank])
        if not castlingRook or castlingRook.type != 'rook' or castlingRook.color != color:
            return False
        
        squaresBetween = [[6, rank], [7, rank]]
        for square in squaresBetween:
            if self.isSquareOccupied(square) or self.isSquareAttacked(square, OTHER_COLOR[color]):
                return False
        
        return True
    
    def canCastleQueenside(self, color=None):
        color = color if color else self.turn
        rank = 1 if color == 'white' else 8

        if not self.canCastle[color]['queenside']:
            return False
        
        king = self.kings.get(color)
        if king.pos != [5, rank]:
            return False
        
        castlingRook = self.getPieceAt([1, rank])
        if not castlingRook or castlingRook.type != 'rook' or castlingRook.color != color:
            return False
        
        squaresBetween = [[2, rank], [3, rank], [4, rank]]
        for square in squaresBetween:
            if self.isSquareOccupied(square) or self.isSquareAttacked(square, OTHER_COLOR[color]):
                return False
        
        return True

    def isInCheck(self, color=None):
        color = color if color else self.turn
        
        king = self.kings[color]
        if king and self.isSquareAttacked(king.pos, OTHER_COLOR[color]):
            return True
        
        return False
    
    def filterLegalMoves(self, moves, color=None): # Removes moves that would leave king in check
        color = color if color else self.turn
        filteredMoves = {}

        # This process automatically handles pins as well

        for pieceId, pieceMoves in moves.items():
            filteredPieceMoves = []
            piece = self.pieces[color][pieceId]
            originalPos = piece.pos.copy()

            for move in pieceMoves:
                captured = self.getPieceAt(move) 
                if captured:
                    self.removePiece(captured) # Temporarily remove captured piece

                self.movePiece(piece, move) # Temporarily move piece
                if not self.isInCheck(color): # If the king is not in check after move, it's legal
                    filteredPieceMoves.append(move)

                self.movePiece(piece, originalPos) # Move piece back
                if captured:
                    self.pieces[captured.color][captured.id] = captured # Restore captured piece
                    self.setPieceOnBoardArray(captured, move) # Place captured piece back on board array

            if filteredPieceMoves: # Only add if there are legal moves, avoids empty lists in dictionary
                filteredMoves[pieceId] = filteredPieceMoves

        return filteredMoves
    
    def calculateMoves(self, color=None):
        color = color if color else self.turn

        pseudoMoves = {piece.id: self.calculatePieceMoves(piece) for piece in self.pieces[color].values()}
        filteredMoves = self.filterLegalMoves(pseudoMoves, color)

        if self.canCastleKingside(color):
            king = self.kings[color]
            filteredMoves[king.id].append([7, king.pos[1]])
        if self.canCastleQueenside(color):
            king = self.kings[color]
            filteredMoves[king.id].append([3, king.pos[1]])

        return filteredMoves
        
    def isInCheckmate(self):
        if not self.isInCheck():
            return False

        legalMoves = self.calculateMoves()
        if not legalMoves:
            return True

        return False
    
    def isInStalemate(self):
        if self.isInCheck():
            return False

        legalMoves = self.calculateMoves()
        if not legalMoves:
            return True

        return False
    
    def isGameOver(self):
        inCheck = self.isInCheck()
        legalMoves = self.calculateMoves()

        checkmate = inCheck and not legalMoves
        stalemate = not inCheck and not legalMoves

        return {
            'gameOver': checkmate or stalemate,
            'reason': 'checkmate' if checkmate else 'stalemate' if stalemate else None,
            'winner': OTHER_COLOR[self.turn] if checkmate else None
        } # might change later
    
    def promotePawn(self, pawn, newType='queen'):
        self.removePiece(pawn)
        promotedPiece = self.createPiece(newType, pawn.pos, pawn.color)

        # Trying to remove the pawn after creating the promoted piece would remove the new piece instead since they have the same position
        
        return promotedPiece

    def makeMove(self, piece, pos):
        target = self.getPieceAt(pos)
        if target and target.id != piece.id:
            self.removePiece(target)
        elif piece.type == 'pawn' and pos == self.enPassantSquare:
            direction = 1 if piece.color == 'white' else -1
            capturedPawn = self.getPieceAt([pos[0], pos[1] - direction])
            self.removePiece(capturedPawn)

        if piece.type == 'king':
            netHorizontalMove = abs(pos[0] - piece.pos[0])
            if netHorizontalMove == 2: # The king is moving two squares, indicating castling
                rank = piece.pos[1]
                if pos[0] == 7: # Kingside
                    rook = self.getPieceAt([8, rank]) # h rook
                    self.movePiece(rook, [6, rank])
                elif pos[0] == 3: # Queenside
                    rook = self.getPieceAt([1, rank]) # a rook
                    self.movePiece(rook, [4, rank])

        if piece.type == 'king':
            self.canCastle[piece.color]['kingside'] = False
            self.canCastle[piece.color]['queenside'] = False
        elif piece.type == 'rook':
            if piece.pos[0] == 1:
                self.canCastle[piece.color]['queenside'] = False
            elif piece.pos[0] == 8:
                self.canCastle[piece.color]['kingside'] = False

        self.enPassantSquare = None
        if piece.type == 'pawn':
            startingRank = 2 if piece.color == 'white' else 7
            twoSquareAdvanceRank = 4 if piece.color == 'white' else 5
            if piece.pos[1] == startingRank and pos[1] == twoSquareAdvanceRank:
                self.enPassantSquare = [piece.pos[0], piece.pos[1] + (1 if piece.color == 'white' else -1)]

        originalPos = piece.pos.copy()
        self.movePiece(piece, pos)

        if piece.type == 'pawn' or target:
            self.halfMoves = 0
        else:
            self.halfMoves += 1
        if self.turn == 'black':
            self.fullMoves += 1

        if piece.type == 'pawn':
            backRank = 8 if piece.color == 'white' else 1
            if piece.pos[1] == backRank:
                self.promotePawn(piece, 'queen') # Auto promote to queen for simplicity until user input is added

        self.recordMove(piece, originalPos, pos)

        self.turn = OTHER_COLOR[self.turn]

        assert not self.isOutOfBounds(piece.pos)
    
    def recordMove(self, piece, fromPos, toPos):
        moveRecord = {
            'pieceId': piece.id,
            'from': fromPos,
            'to': toPos,
            'boardArray': self.boardArray.copy(),
            'pieces': self.pieces.copy(),
            'canCastle': self.canCastle.copy(),
            'enPassantSquare': self.enPassantSquare,
            'turn': self.turn,
            'halfMoves': self.halfMoves,
            'fullMoves': self.fullMoves
        }
        self.moveHistory.append(moveRecord)

if __name__ == '__main__':
    board = Board()

    for rank in board.board:
        print(rank)