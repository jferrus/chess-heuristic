import chess

class ChessEngine:
    def __init__(self, fen=None):
        if fen:
            self.board = chess.Board(fen)
        else:
            self.board = chess.Board()

    def get_legal_moves(self):
        return list(self.board.legal_moves)

    def make_move(self, move):
        """move can be a chess.Move object or a UCI string."""
        if isinstance(move, str):
            move = chess.Move.from_uci(move)
        
        if move in self.board.legal_moves:
            self.board.push(move)
            return True
        return False

    def undo_move(self):
        if len(self.board.move_stack) > 0:
            self.board.pop()
            return True
        return False

    def is_game_over(self):
        return self.board.is_game_over()

    def get_status(self):
        if self.board.is_checkmate():
            return "Checkmate"
        if self.board.is_stalemate():
            return "Stalemate"
        if self.board.is_insufficient_material():
            return "Insufficient Material"
        if self.board.is_check():
            return "Check"
        return "Ongoing"

    def get_fen(self):
        return self.board.fen()

    def reset(self):
        self.board.reset()
