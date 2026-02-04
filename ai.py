import chess
import random
from heuristics import evaluate_board

class ChessAI:
    def __init__(self, depth=3):
        self.depth = depth

    def get_best_move(self, board):
        best_move = None
        best_value = -float('inf') if board.turn == chess.WHITE else float('inf')
        
        # Simple shuffle to avoid deterministic moves for equal evaluations
        moves = list(board.legal_moves)
        random.shuffle(moves)

        alpha = -float('inf')
        beta = float('inf')

        for move in moves:
            board.push(move)
            board_value = self.minimax(board, self.depth - 1, alpha, beta, not (board.turn == chess.WHITE))
            board.pop()

            if board.turn == chess.WHITE:
                if board_value > best_value:
                    best_value = board_value
                    best_move = move
                alpha = max(alpha, best_value)
            else:
                if board_value < best_value:
                    best_value = board_value
                    best_move = move
                beta = min(beta, best_value)
            
            if beta <= alpha:
                break

        return best_move

    def minimax(self, board, depth, alpha, beta, is_maximizing):
        if depth == 0 or board.is_game_over():
            return evaluate_board(board)

        if is_maximizing:
            max_eval = -float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
