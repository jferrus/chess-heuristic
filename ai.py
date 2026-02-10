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
            board_value = self.minimax(board, self.depth - 1, alpha, beta, board.turn == chess.WHITE)
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
        2. Killer moves or other heuristics could be added here
        """
        moves = list(board.legal_moves)
        move_scores = []
        
        for move in moves:
            score = 0
            captured_piece = board.piece_at(move.to_square)
            if captured_piece:
                aggressor_type = board.piece_at(move.from_square).piece_type
                # MVV-LVA: Formula: 10 * VictimValue - AggressorValue
                score = 10 * PIECE_VALUES[captured_piece.piece_type] - PIECE_VALUES[aggressor_type]
                score += 10000  # Ensure captures are evaluated before non-captures
            
            move_scores.append((score, move))
        
        move_scores.sort(key=lambda x: x[0], reverse=True)
        return [m[1] for m in move_scores]

    def minimax(self, board, depth, alpha, beta, is_maximizing):
        if board.is_game_over():
            return evaluate_board(board, depth)
        
        if depth == 0:
            return self.quiescence_search(board, alpha, beta, is_maximizing)

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

    def quiescence_search(self, board, alpha, beta, is_maximizing):
        """Continues searching captures until a 'quiet' position is reached."""
        if board.is_game_over():
            return evaluate_board(board, 0)

        in_check = board.is_check()
        stand_pat = evaluate_board(board, 0)
        
        if is_maximizing:
            if not in_check:
                if stand_pat >= beta:
                    return beta
                if alpha < stand_pat:
                    alpha = stand_pat
            
            # If in check, consider all moves to get out of check
            # Otherwise, only consider captures
            if in_check:
                moves = list(board.legal_moves)
            else:
                moves = [m for m in board.legal_moves if board.is_capture(m)]
                
            move_scores = []
            for move in moves:
                captured_piece = board.piece_at(move.to_square)
                aggressor_type = board.piece_at(move.from_square).piece_type
                # Default score for non-captures in check is 0 (will be evaluated after captures)
                score = 0
                if captured_piece:
                    score = 10 * PIECE_VALUES[captured_piece.piece_type if captured_piece else chess.PAWN] - PIECE_VALUES[aggressor_type]
                move_scores.append((score, move))
            move_scores.sort(key=lambda x: x[0], reverse=True)
            moves = [m[1] for m in move_scores]

            for move in moves:
                board.push(move)
                eval = self.quiescence_search(board, alpha, beta, False)
                board.pop()
                
                if eval >= beta:
                    return beta
                if eval > alpha:
                    alpha = eval
            return alpha
        else:
            if not in_check:
                if stand_pat <= alpha:
                    return alpha
                if beta > stand_pat:
                    beta = stand_pat
                
            if in_check:
                moves = list(board.legal_moves)
            else:
                moves = [m for m in board.legal_moves if board.is_capture(m)]
                
            move_scores = []
            for move in moves:
                captured_piece = board.piece_at(move.to_square)
                aggressor_type = board.piece_at(move.from_square).piece_type
                score = 0
                if captured_piece:
                    score = 10 * PIECE_VALUES[captured_piece.piece_type if captured_piece else chess.PAWN] - PIECE_VALUES[aggressor_type]
                move_scores.append((score, move))
            move_scores.sort(key=lambda x: x[0], reverse=True)
            moves = [m[1] for m in move_scores]

            for move in moves:
                board.push(move)
                eval = self.quiescence_search(board, alpha, beta, True)
                board.pop()
                
                if eval <= alpha:
                    return alpha
                if eval < beta:
                    beta = eval
            return beta
