import pygame
import chess
import sys
import os
from engine import ChessEngine
from ai import ChessAI

# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 8
SQ_SIZE = WIDTH // COLS
BOARD_COLOR_1 = (235, 235, 208)
BOARD_COLOR_2 = (119, 148, 85)
HIGHLIGHT_COLOR = (186, 202, 43)

class ChessGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess with Modifiable Heuristics")
        self.engine = ChessEngine()
        self.ai = ChessAI(depth=3)
        self.assets = {}
        self.load_assets()
        self.selected_square = None
        self.running = True

    def load_assets(self):
        pieces = ['wP', 'wN', 'wB', 'wR', 'wQ', 'wK', 'bP', 'bN', 'bB', 'bR', 'bQ', 'bK']
        for piece in pieces:
            path = os.path.join("assets", f"{piece}.png")
            try:
                img = pygame.image.load(path)
                self.assets[piece] = pygame.transform.scale(img, (SQ_SIZE, SQ_SIZE))
            except Exception as e:
                print(f"Error loading {path}: {e}")

    def draw_board(self):
        for r in range(ROWS):
            for c in range(COLS):
                color = BOARD_COLOR_1 if (r + c) % 2 == 0 else BOARD_COLOR_2
                pygame.draw.rect(self.screen, color, (c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

        if self.selected_square is not None:
            r, c = 7 - chess.square_rank(self.selected_square), chess.square_file(self.selected_square)
            pygame.draw.rect(self.screen, HIGHLIGHT_COLOR, (c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    def draw_pieces(self):
        for square in chess.SQUARES:
            piece = self.engine.board.piece_at(square)
            if piece:
                color = 'w' if piece.color == chess.WHITE else 'b'
                type = piece.symbol().upper()
                name = f"{color}{type}"
                img = self.assets.get(name)
                if img:
                    # chess library uses 0 for a1, pygame uses (0,0) for top-left
                    # So square 0 (a1) is row 7, col 0
                    r, c = 7 - chess.square_rank(square), chess.square_file(square)
                    self.screen.blit(img, (c * SQ_SIZE, r * SQ_SIZE))

    def get_square_from_pos(self, pos):
        x, y = pos
        col = x // SQ_SIZE
        row = 7 - (y // SQ_SIZE)
        return chess.square(col, row)

    def handle_click(self, pos):
        square = self.get_square_from_pos(pos)
        
        if self.selected_square is None:
            piece = self.engine.board.piece_at(square)
            if piece and piece.color == self.engine.board.turn:
                self.selected_square = square
        else:
            move = chess.Move(self.selected_square, square)
            # Handle promotion to Queen by default for simplicity
            if self.engine.board.piece_at(self.selected_square).piece_type == chess.PAWN:
                if (chess.square_rank(square) == 7 and self.engine.board.turn == chess.WHITE) or \
                   (chess.square_rank(square) == 0 and self.engine.board.turn == chess.BLACK):
                    move.promotion = chess.QUEEN

            if move in self.engine.board.legal_moves:
                self.engine.make_move(move)
                self.selected_square = None
                self.draw()
                # AI Turn
                if not self.engine.is_game_over():
                    self.ai_move()
            else:
                # If clicked on another of own pieces, change selection
                piece = self.engine.board.piece_at(square)
                if piece and piece.color == self.engine.board.turn:
                    self.selected_square = square
                else:
                    self.selected_square = None

    def ai_move(self):
        pygame.display.set_caption("AI is thinking...")
        best_move = self.ai.get_best_move(self.engine.board)
        if best_move:
            self.engine.make_move(best_move)
        pygame.display.set_caption("Chess with Modifiable Heuristics")

    def draw(self):
        self.draw_board()
        self.draw_pieces()
        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.engine.board.turn == chess.WHITE: # Player only moves white for this demo
                         self.handle_click(event.pos)

            self.draw()
            
            if self.engine.is_game_over():
                status = self.engine.get_status()
                pygame.display.set_caption(f"Game Over: {status}")

        pygame.quit()

if __name__ == "__main__":
    gui = ChessGUI()
    gui.run()
