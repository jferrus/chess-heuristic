import chess
from ai import ChessAI

def test_mate_in_1():
    # Simple mate in 1 for White: Queen to f7 is mate.
    # r . b q k b n r
    # p p p p . Q p p
    # . . . . . . . .
    # . . . . p . . .
    # . . . . . . . .
    # . . . . . . . .
    # P P P P . P P P
    # R N B . K B N R
    board = chess.Board("r1bqkbnr/pppp1Qpp/8/4p3/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 1")
    # Wait, the above is already mate. Let's backtrack one move.
    
    # Position: Scholar's Mate setup
    # r . b q k b n r
    # p p p p . p p p
    # . . . . . . . .
    # . . . . . . . .
    # . . . . . . . .
    # . . . . . Q . .
    # P P P P . P P P
    # R N B . K B N R
    # White has Queen on f3 (or h5) and Bishop on c4.
    board = chess.Board("r1bqkbnr/pppp1ppp/2n5/4p2Q/2B1P3/8/PPPP1PPP/RNB1KBNR w KQkq - 0 1")
    
    print("Initial Position (White to move, Qf7 is mate):")
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
    test_mate_in_1()
