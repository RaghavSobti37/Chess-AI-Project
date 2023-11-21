import pygame as p
import chess
from PIL import Image, ImageTk
import random

WIDTH = HEIGHT = 600
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
CAPTURED_SIZE = 60  # Size of the captured pieces display
MAX_FPS = 15
IMAGES = {}
CAPTURED_IMAGES = {'w': [], 'b': []}  # To store captured pieces

# Initialize Q-values
Q = {}
EPSILON = 0.2
ALPHA = 0.5
GAMMA = 0.9

def load_images():
    pieces = ['wp', 'wr', 'wn', 'wb', 'wk', 'wq', 'bp', 'br', 'bn', 'bb', 'bk', 'bq']
    for piece in pieces:
        image_path = "C:/Users/Raghav Raj Sobti/Downloads/AI-Chess/chess-ai/chess/images/" + piece + ".png"
        IMAGES[piece] = p.transform.scale(p.image.load(image_path), (SQ_SIZE, SQ_SIZE))

def draw_board(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row + col) % 2]
            p.draw.rect(screen, color, p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

# ...

def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board.piece_at(chess.square(col, 7 - row))
            if piece is not None:
                # Ensure that the piece symbol is consistently lowercased
                piece_symbol = piece.symbol().lower() if piece.symbol() != 'K' else 'k'
                img = IMAGES[piece_symbol]
                screen.blit(img, p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

# ...


def draw_captured_pieces(screen):
    # Draw captured pieces for white
    for i, piece in enumerate(CAPTURED_IMAGES['w']):
        img = IMAGES[piece]
        screen.blit(img, p.Rect((i % 4) * CAPTURED_SIZE, HEIGHT, CAPTURED_SIZE, CAPTURED_SIZE))

    # Draw captured pieces for black
    for i, piece in enumerate(CAPTURED_IMAGES['b']):
        img = IMAGES[piece]
        screen.blit(img, p.Rect((i % 4) * CAPTURED_SIZE, HEIGHT + CAPTURED_SIZE, CAPTURED_SIZE, CAPTURED_SIZE))

def update_q_value(state, action, reward, next_state):
    current_q = Q.get((state, action), 0)
    max_future_q = max(Q.get((next_state, next_action), 0) for next_action in get_legal_moves(next_state))
    new_q = (1 - ALPHA) * current_q + ALPHA * (reward + GAMMA * max_future_q)
    Q[(state, action)] = new_q

def choose_action(state):
    if random.uniform(0, 1) < EPSILON:
        return random.choice(get_legal_moves(state))
    else:
        return max(get_legal_moves(state), key=lambda move: Q.get((state, move), 0))

def get_legal_moves(state):
    legal_moves = []

    chess_board = chess.Board(state)
    for move in chess_board.legal_moves:
        # Check if the move is castling or en passant
        if move.uci() in ['e1g1', 'e1c1', 'e8g8', 'e8c8', 'e1g1c1', 'e8g8c8']:
            legal_moves.append(move.uci())
        else:
            # Add other legal moves
            legal_moves.append(move.uci())

    return legal_moves

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT + CAPTURED_SIZE * 2))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))

    load_images()

    board = chess.Board()

    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

        draw_board(screen)
        draw_pieces(screen, board)
        draw_captured_pieces(screen)

        # Q-learning updates during the game
        current_state = str(board)
        action = choose_action(current_state)
        board.push(chess.Move.from_uci(action))
        reward = 1 if board.is_checkmate() else 0
        next_state = str(board)
        update_q_value(current_state, action, reward, next_state)

        # Update captured pieces
        if board.is_capture(chess.Move.from_uci(action)):
            captured_piece = board.piece_at(chess.Move.from_uci(action).to_square).symbol().lower()
            CAPTURED_IMAGES['w' if board.turn == chess.WHITE else 'b'].append(captured_piece)

        p.display.flip()
        clock.tick(MAX_FPS)

    p.quit()

if __name__ == "__main__":
    main()
