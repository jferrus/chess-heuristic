import chess
import random
from heuristics import evaluate_board, PIECE_VALUES

class ChessAI:
    def __init__(self, depth=3):
        self.depth = depth

    def get_best_move(self, board):
        best_move = None
        best_value = -float('inf') if board.turn == chess.WHITE else float('inf')
        
        moves = self.order_moves(board)

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

    def order_moves(self, board):
        """Sort moves to improve Alpha-Beta pruning performance.
        Prioritizes:
        1. Captures (MVV-LVA: Most Valuable Victim - Least Valuable Aggressor)
        2. Other moves (by basic heuristic evaluation)
        """
        moves = list(board.legal_moves)
        move_scores = []
        
        for move in moves:
            score = 0
            # MVV-LVA for captures
            captured_piece = board.piece_at(move.to_square)
            if captured_piece:
                # Value ranges from ~100 to ~20000. 
                # Formula: 10 * VictimValue - AggressorValue
                # This ensures we prefer taking a Queen with a Pawn over taking a Pawn with a Queen.
                aggressor_type = board.piece_at(move.from_square).piece_type
                score = 10 * PIECE_VALUES[captured_piece.piece_type] - PIECE_VALUES[aggressor_type]
                score += 100000  # Ensure captures are evaluated before non-captures in ordering
            else:
                # For non-captures, we can still use the heuristic, but maybe less weight
                # Or just keep them below captures for ordering
                # board.push(move)
                # score = evaluate_board(board)
                # board.pop()
                score = 0 # Simple ordering for non-captures to save time, or use heuristic
            
            move_scores.append((score, move))
        
        # Sort descending - highest scores first for both colors because we've 
        # normalized the score to "goodness for current player"
        move_scores.sort(key=lambda x: x[0], reverse=True)
            
        return [m[1] for m in move_scores]

    def minimax(self, board, depth, alpha, beta, is_maximizing):
        if depth == 0 or board.is_game_over():
            return evaluate_board(board)

        moves = self.order_moves(board)

        if is_maximizing:
            max_eval = -float('inf')
            for move in moves:
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
            for move in moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
