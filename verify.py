import chess
from heuristics import evaluate_board
from ai import ChessAI

def test_evaluation():
    board = chess.Board()
    score = evaluate_board(board)
    print(f"Initial board score: {score}")
    assert score == 0, "Initial score should be 0"
    
    # Give white an advantage
    board.remove_piece_at(chess.D7) # Remove black queen pawn
    score = evaluate_board(board)
    print(f"Score after removing black pawn: {score}")
    assert score > 0, "White should have advantage"

def test_ai():
    board = chess.Board()
    ai = ChessAI(depth=2)
    move = ai.get_best_move(board)
    print(f"AI best move: {move}")
    assert move is not None, "AI should return a move"

if __name__ == "__main__":
    try:
        test_evaluation()
        test_ai()
        print("Tests passed!")
    except Exception as e:
        print(f"Tests failed: {e}")
