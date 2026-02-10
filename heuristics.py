import chess

# --- Modifiable Heuristics ---

# Piece values
PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

# Positional bonuses: Weight for being in the center or developed
# (Higher values encourage pieces to move to those squares)
PAWN_TABLE = [
     0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 40, 40, 20, 10, 10,
     5,  5, 20, 15, 15, 20,  5,  5,
     0,  0, 15, 20, 20, 15,  0,  0,
     5,  5, 10, 15, 15, 10,  5,  5,
     5, 10, 10,-20,-20, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0
]

KNIGHT_TABLE = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -30,  5, 20, 30, 20, 20,  5,-30,
    -30,  0, 20, 20, 20, 20,  0,-30,
    -30,  5, 20, 20, 20, 20,  5,-30,
    -30,  0, 25, 20, 20, 25,  0,-30,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50
]

BISHOP_TABLE = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -10, 10, 10, 20, 20, 10, 10,-10,
    -10,  0, 20, 30, 30, 20,  0,-10,
    -10,  5, 20, 30, 30, 20,  5,-10,
    -10, 10, 15, 20, 20, 15, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20
]

ROOK_TABLE = [
      0,  0,  0,  0,  0,  0,  0,  0,
      5, 10, 10, 10, 10, 10, 10,  5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
      0,  0,  0,  5,  5,  0,  0,  0
]

QUEEN_TABLE = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
     -5,  0,  5,  5,  5,  5,  0, -5,
      0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, 5, 5,-10,-10,-20
]

KING_TABLE = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
     20, 20,  0,  0,  0,  0, 20, 20,
     20, 30, 10,  0,  0, 10, 30, 20
]

TABLES = {
    chess.PAWN: PAWN_TABLE,
    chess.KNIGHT: KNIGHT_TABLE,
    chess.BISHOP: BISHOP_TABLE,
    chess.ROOK: ROOK_TABLE,
    chess.QUEEN: QUEEN_TABLE,
    chess.KING: KING_TABLE
}

def evaluate_board(board, depth=0):
    if board.is_checkmate():
        # Score adjusted by depth to prefer shorter mates
        mate_score = 99999 + depth
        if board.turn == chess.WHITE:
            return -mate_score
        else:
            return mate_score
    
    # All draws (stalemate, repetition, etc.) should be 0
    if board.is_game_over():
        return 0

    score = 0
    # Add material value and positional bonuses
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            val = PIECE_VALUES[piece.piece_type]

            # Tables are defined from White's perspective: Row 0 is Rank 8, Row 7 is Rank 1.
            # White a1 (sq 0) -> Rank 1 (index 56)
            # Black a8 (sq 56) -> Black's Rank 1 (index 56)
            if piece.color == chess.WHITE:
                idx = square ^ 56
            else:
                idx = square
            
            table_bonus = TABLES[piece.piece_type][idx]
            
            if piece.color == chess.WHITE:
                score += val + table_bonus
            else:
                score -= (val + table_bonus)

    return score
