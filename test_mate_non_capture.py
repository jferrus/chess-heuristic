import chess
from ai import ChessAI

def test_non_capture_mate():
    # Back rank mate for White: Rd8 is mate.
    # . . . . . . k .
    # p p p . . p p p
    # . . . . . . . .
    # . . . . . . . .
    # . . . . . . . .
    # . . . . . . . .
    # . . . . . . . .
    # . . . R . . . .
    board = chess.Board("6k1/ppp2ppp/8/8/8/8/8/3R4 w - - 0 1")
    
    print("Initial Position (White to move, Rd8 is mate):")
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
            print(f"FAILURE: AI chose {san_move} instead of Rd8#.")
    else:
        print("FAILURE: AI found no move.")

if __name__ == "__main__":
    test_non_capture_mate()
