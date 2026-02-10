import chess
from ai import ChessAI

def test_black_mate_in_1():
    # Simple mate in 1 for Black: Qf2 is mate.
    # r n b . k b n r
    # p p p p . p p p
    # . . . . . . . .
    # . . . . . . . .
    # . . . . . . . .
    # . . . . . q . .
    # P P P P . . P P
    # R N B . K B N R
    # White king is on e1. Black Queen on f3. Black Bishop on c5.
    board = chess.Board("rnb1kbnr/pppp1ppp/8/2b1p3/4P3/5q2/PPPP1PPP/RNBQKBNR w KQkq - 0 1")
    # Actually, let's make it Black's turn.
    board = chess.Board("rnb1kbnr/pppp1ppp/8/2b1p3/4P3/5q2/PPPP1PPP/RNBQKBNR b KQkq - 0 1")
    
    print("Initial Position (Black to move, Qf2 is mate):")
    print(board)
    
    ai = ChessAI(depth=3)
    best_move = ai.get_best_move(board)
    
    print(f"Best Move: {best_move}")
    if best_move:
        san_move = board.san(best_move)
        print(f"Move in SAN: {san_move}")
        
        board.push(best_move)
        if board.is_checkmate():
            print("SUCCESS: AI found the mate!")
        else:
            print(f"FAILURE: AI chose {san_move} instead of a mating move.")
    else:
        print("FAILURE: AI found no move.")

if __name__ == "__main__":
    test_black_mate_in_1()
