import chess
from ai import ChessAI

def test_queen_sacrifice():
    # Position: White Queen can take a Pawn on e5, but it's protected by Black's Knight on f7.
    # If the AI only looks 3 plys deep, it might see:
    # 1. Qxe5 (Gain Pawn) -> Depth 1
    # 2. Nxf7 (Recapture Queen) -> Depth 2
    # 3. ... (White's move) -> Depth 3
    # Wait, 3 plys is White-Black-White. 
    # If depth=3:
    # 1. Qxe5 (W)
    # 2. Nxf7 (B)
    # 3. dxe5 (W) - wait, this is not right.
    
    # Static evaluation after 3 plys without quiescence:
    # If it stops exactly at 3 plys, it might not "see" the consequence if the last move is not a capture for the active player but they are about to lose material.
    
    # Let's set up a standard "bait" position.
    # White to move.
    board = chess.Board("r1bqkbnr/pppp1ppp/2n5/4p3/4Q3/2N5/PPPPPPPP/R1B1KBNR w KQkq - 0 1")
    # In this position, the White Queen on e4 can take the Pawn on e5.
    # The Pawn on e5 is protected by the Knight on c6.
    # Qxe5 is a bad move.
    
    ai = ChessAI(depth=3)
    best_move = ai.get_best_move(board)
    
    print(f"Current Turn: {'White' if board.turn == chess.WHITE else 'Black'}")
    print(f"Best Move: {best_move}")
    
    if best_move and board.is_capture(best_move):
        captured_piece = board.piece_at(best_move.to_square)
        if best_move.to_square == chess.E5:
            print("FAILURE: AI chose to capture the protected pawn with the Queen!")
        else:
            print(f"AI chose a capture: {best_move}")
    else:
        print(f"AI chose a non-capture move: {best_move}")

if __name__ == "__main__":
    test_queen_sacrifice()
