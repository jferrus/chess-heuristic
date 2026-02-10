import chess
from ai import ChessAI

def reproduce():
    # Sequence: 
    # 1. e4 e5 
    # 2. Nf3 d5 (User said Kf3, which is Nf3)
    # 3. exd5 Qxd5 
    # 4. d3 ...
    board = chess.Board()
    board.push_san("e4")
    board.push_san("e5")
    board.push_san("Nf3")
    board.push_san("d5")
    board.push_san("exd5")
    board.push_san("Qxd5")
    board.push_san("d3")
    
    print("Position after 4. d3:")
    print(board)
    print(f"Turn: {'White' if board.turn == chess.WHITE else 'Black'}")
    
    ai = ChessAI(depth=3)
    best_move = ai.get_best_move(board)
    
    print(f"Best Move for Black: {best_move}")
    
    if best_move and board.san(best_move) == "Qxf3":
        print("BUG REPRODUCED: AI chose Qxf3!")
    else:
        print(f"AI chose: {board.san(best_move) if best_move else 'None'}")

if __name__ == "__main__":
    reproduce()
