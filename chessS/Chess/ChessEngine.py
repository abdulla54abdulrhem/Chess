class GameState():
    def _init_(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.enpassantPossible = () #cordinates for the square




    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteMove = not self.whiteMove
        print("white move now is ",self.whiteMove)
        # update the King Location
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        #enpassnt move
        if move.isEnpassntMove:
            self.board[move.startRow][move.endCol] = '--'

        #update enpassnt possible
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow)  == 2: #pawn adv
            self.enpassantPossible = ((move.startRow + move.endRow)// 2, move.startCol)
        else:
            self.enpassantPossible = ()







#undo last move
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteMove = not self.whiteMove
            # update the King Location
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
            #undo enpassnt
            if move.isEnpassntMove:
                self.board[move.endRow][move.endCol] = '--' #leace the sq blank
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)
            #ubdo a 2 sq pawn adv
            if move.pieceMoved[1]  == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()
            self.checkMate = False
            self.staleMate = False



    def getValidMoves(self):
        tempEnpassntPossible = self.enpassantPossible
        moves = self.getAllPossibleMoves()
        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i])
            self.whiteMove = not self.whiteMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteMove = not self.whiteMove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        self.enpassantPossible = tempEnpassntPossible
        return moves

    def inCheck(self):
        if self.whiteMove:
            return self.squreUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squreUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def squreUnderAttack(self, r, c):
        self.whiteMove = not self.whiteMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteMove = not self.whiteMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False

    def getAllPossibleMoves(self):
########################################################print("hey white move is ", self.whiteMove)
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteMove) or (turn == 'b' and not self.whiteMove):
                    piece = self.board[r][c][1]
                    if piece == 'p':
                        self.getPawnMoves(r,c,moves)
                    elif piece == 'R':
                        self.getRookMoves(r,c,moves)
                    elif piece == 'N':
                        self.getKnightMoves(r,c,moves)
                    elif piece == 'B':
                        self.getBishopMoves(r,c,moves)
                    elif piece == 'Q':
                        self.getQueenMoves(r,c,moves)
                    elif piece == 'K':
                        self.getKingMoves(r,c,moves)


        return moves

    def getPawnMoves(self, r, c, moves):
        """
        Get all possible moves for a pawn at position (r, c).
        Append the moves to the `moves` list.
        """
        pieceColor = self.board[r][c][0]  # Get the color of the pawn
        if self.whiteMove:  # White pawn
            direction = -1  # Pawns move upward for white
            startRow = 6  # White pawns start at row 6
            enemyColor = 'b'  # Black is the enemy color
        else:  # Black pawn
            direction = 1  # Pawns move downward for black
            startRow = 1  # Black pawns start at row 1
            enemyColor = 'w'  # White is the enemy color

        # Check the square in front of the pawn
        if self.board[r + direction][c] == "--":
            moves.append(Move((r, c), (r + direction, c), self.board))
            # Check if the pawn is on its starting position and can move two squares forward
            if r == startRow and self.board[r + 2 * direction][c] == "--":
                moves.append(Move((r, c), (r + 2 * direction, c), self.board))

        # Check for capturing moves
        if c - 1 >= 0:  # Check left capture
            if self.board[r + direction][c - 1][0] == enemyColor:
                moves.append(Move((r, c), (r + direction, c - 1), self.board))
            elif (r + direction, c-1) == self.enpassantPossible:
                moves.append(Move((r, c), (r + direction, c - 1), self.board))

        if c + 1 <= 7:  # Check right capture
            if self.board[r + direction][c + 1][0] == enemyColor:
                moves.append(Move((r, c), (r + direction, c + 1), self.board))
            elif (r + direction, c+1) == self.enpassantPossible:
                moves.append(Move((r, c), (r + direction, c + 1), self.board))


    def getRookMoves(self, r, c, moves):
        """
        Get all possible moves for a rook at position (r, c).
        Append the moves to the `moves` list.
        """
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Possible directions: right, down, left, up

        pieceColor = self.board[r][c][0]  # Get the color of the rook

        for direction in directions:
            for i in range(1, 8):  # Rooks can move up to 7 squares in any direction
                endRow = r + direction[0] * i
                endCol = c + direction[1] * i

                if 0 <= endRow < 8 and 0 <= endCol < 8:  # Check if the position is within the board

                    if self.board[endRow][endCol] == "--":  # Empty square, valid move
                        moves.append(Move((r, c), (endRow, endCol), self.board))

                    elif self.board[endRow][endCol][0] != pieceColor:  # Enemy piece, valid capture
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break

                    else:  # Same color piece, cannot move further in this direction
                        break

                else:  # Position is outside the board, stop searching in this direction
                    break
    def getKnightMoves(self, r, c, moves):
        """
        Get all possible moves for a knight at position (r, c).
        Append the moves to the `moves` list.
        """
        knightMoves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                       (1, -2), (1, 2), (2, -1), (2, 1)]  # Possible knight moves

        pieceColor = self.board[r][c][0]  # Get the color of the knight

        for move in knightMoves:
            endRow = r + move[0]
            endCol = c + move[1]

            if 0 <= endRow < 8 and 0 <= endCol < 8:  # Check if the position is within the board

                if self.board[endRow][endCol] == "--":  # Empty square, valid move
                    moves.append(Move((r, c), (endRow, endCol), self.board))

                elif self.board[endRow][endCol][0] != pieceColor:  # Enemy piece, valid capture
                    moves.append(Move((r, c), (endRow, endCol), self.board))
    def getBishopMoves(self, r, c, moves):
        """
        Get all possible moves for a bishop at position (r, c).
        Append the moves to the `moves` list.
        """
        pieceColor = self.board[r][c][0]  # Get the color of the bishop

        # Bishop moves along the diagonals
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for direction in directions:
            for i in range(1, 8):
                endRow = r + direction[0] * i
                endCol = c + direction[1] * i

                if 0 <= endRow < 8 and 0 <= endCol < 8:  # Check if the position is within the board

                    if self.board[endRow][endCol] == "--":  # Empty square, valid move
                        moves.append(Move((r, c), (endRow, endCol), self.board))

                    elif self.board[endRow][endCol][0] != pieceColor:  # Enemy piece, valid capture
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break

                    else:  # Friendly piece, invalid move
                        break
                else:  # Out of board bounds, invalid move
                    break
    def getQueenMoves(self, r, c, moves):
        """
        Get all possible moves for a queen at position (r, c).
        Append the moves to the `moves` list.
        """
        pieceColor = self.board[r][c][0]  # Get the color of the queen

        # Queen moves along the diagonals, ranks, and files
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for direction in directions:
            for i in range(1, 8):
                endRow = r + direction[0] * i
                endCol = c + direction[1] * i

                if 0 <= endRow < 8 and 0 <= endCol < 8:  # Check if the position is within the board

                    if self.board[endRow][endCol] == "--":  # Empty square, valid move
                        moves.append(Move((r, c), (endRow, endCol), self.board))

                    elif self.board[endRow][endCol][0] != pieceColor:  # Enemy piece, valid capture
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break

                    else:  # Friendly piece, invalid move
                        break
                else:  # Out of board bounds, invalid move
                    break
    def getKingMoves(self, r, c, moves):
        """
        Get all possible moves for a king at position (r, c).
        Append the moves to the `moves` list.
        """
        pieceColor = self.board[r][c][0]  # Get the color of the king

        # King can move one square in any direction
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for direction in directions:
            endRow = r + direction[0]
            endCol = c + direction[1]

            if 0 <= endRow < 8 and 0 <= endCol < 8:  # Check if the position is within the board
                if self.board[endRow][endCol] == "--":  # Empty square, valid move
                    moves.append(Move((r, c), (endRow, endCol), self.board))
                elif self.board[endRow][endCol][0] != pieceColor:  # Enemy piece, valid capture
                    moves.append(Move((r, c), (endRow, endCol), self.board))

class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def _init_(self , startSq , endSq ,board, enpassantPossible = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7)
        self.isEnpassntMove = enpassantPossible
        if self.isEnpassntMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'



        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        #print(self.moveID)
    #overriding the equals method
    def _eq_(self,other):
        if isinstance(other,Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)


    def getRankFile(self, r, c):

        return self.colsToFiles[c] + self.rowsToRanks[r];