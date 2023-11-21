"""
Handling the AI moves.
"""
import random
import numpy as np

piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}

knight_scores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.45, 0.65, 0.65, 0.45, 0.5, 0.2],
                 [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                 [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                 [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                 [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                 [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

rook_scores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
               [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

queen_scores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
               [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
               [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
               [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
               [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

piece_position_scores = {"wN": knight_scores,
                         "bN": knight_scores[::-1],
                         "wB": bishop_scores,
                         "bB": bishop_scores[::-1],
                         "wQ": queen_scores,
                         "bQ": queen_scores[::-1],
                         "wR": rook_scores,
                         "bR": rook_scores[::-1],
                         "wp": pawn_scores,
                         "bp": pawn_scores[::-1]}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3

def getOpeningMove(chessboard):
    # Convert the chessboard to a FEN-like string
    def boardToFEN(board):
        fen = ''
        for row in board:
            empty_count = 0
            for square in row:
                if square == '--':
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen += str(empty_count)
                        empty_count = 0
                    fen += square
            if empty_count > 0:
                fen += str(empty_count)
            fen += '/'
        return fen[:-1]  # Remove '/'

    fen = boardToFEN(chessboard)

    # Opening moves based on FEN strings
    openings = {
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR": ["e2e4", "d2d4", "Nf3", "c4"],
        # King's Pawn Opening
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR": ["e2e4", "d2d4"],
        # English Opening
        "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR": ["d2d4", "e4e5", "c2c4"],
        # Queen's Pawn Opening
        "rnbqkbnr/ppp1pppp/8/3p4/3P4/8/PPP2PPP/RNBQKBNR": ["d2d4", "d7d5", "c2c4"],
        # Queen's Gambit
        "rnbqkbnr/pppp1ppp/8/8/3P4/8/PPP2PPP/RNBQKBNR": ["d2d4", "e7e6", "c2c4"],
        # Queen's Gambit Declined
        "rnbqkbnr/pp2pppp/8/3p4/3P4/8/PPP2PPP/RNBQKBNR": ["d2d4", "d7d5", "c2c4", "b8c6"],
        # King's Indian Defense
        "rnbqkbnr/ppp2ppp/8/3pp3/3P4/8/PPP2PPP/RNBQKBNR": ["d2d4", "e7e5", "c2c4"],
        # Budapest Gambit
        "r1bqkbnr/pppp1ppp/8/3Pp3/8/8/PPP2PPP/RNBQKBNR": ["d2d4", "e4d3"],
        # Scandinavian Defense
        "rnbqkbnr/pppp1ppp/8/3Pp3/8/8/PPP2PPP/RNBQKBNR": ["d2d4", "e4d3", "e7e5"],
        # Grünfeld Defense
        "r1bqkbnr/ppp2ppp/8/3p1P2/8/8/PPP2PPP/RNBQKBNR": ["d2d4", "d7d5", "e4e5"],
        # Alekhine Defense
        "r1bqkbnr/pp2ppp1/8/3P4/8/8/PPP2PPP/RNBQKBNR": ["d2d4", "d7d5", "e4e5", "f8d6"]
    }

    # Check if the current position has an opening move
    if fen in openings:
        return random.choice(openings[fen])
    else:
        # If no specific opening is defined, return a random legal move
        legal_moves = ["a2a3", "a2a4", "b2b3", "b2b4", "c2c3", "c2c4", "d2d3", "d2d4", 
                       "e2e3", "e2e4", "f2f3", "f2f4", "g2g3", "g2g4", "h2h3", "h2h4"]
        return random.choice(legal_moves)

def findBestMove(game_state, valid_moves, return_queue):
    global next_move
    next_move = None
    random.shuffle(valid_moves)
    findMoveNegaMaxAlphaBeta(game_state, valid_moves, DEPTH, -CHECKMATE, CHECKMATE,
                             1 if game_state.white_to_move else -1)
    return_queue.put(next_move)


def findMoveNegaMaxAlphaBeta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
    global next_move
    if depth == 0:
        return turn_multiplier * scoreBoard(game_state)
    # move ordering - implement later //TODO
    max_score = -CHECKMATE
    for move in valid_moves:
        game_state.makeMove(move)
        next_moves = game_state.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        game_state.undoMove()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score


def scoreBoard(game_state):
    """
    Score the board. A positive score is good for white, a negative score is good for black.
    """
    if game_state.checkmate:
        if game_state.white_to_move:
            return -CHECKMATE  # black wins
        else:
            return CHECKMATE  # white wins
    elif game_state.stalemate:
        return STALEMATE
    score = 0
    for row in range(len(game_state.board)):
        for col in range(len(game_state.board[row])):
            piece = game_state.board[row][col]
            if piece != "--":
                piece_position_score = 0
                if piece[1] != "K":
                    piece_position_score = piece_position_scores[piece][row][col]
                if piece[0] == "w":
                    score += piece_score[piece[1]] + piece_position_score
                if piece[0] == "b":
                    score -= piece_score[piece[1]] + piece_position_score

    return score

# Initialize Q-values
Q = {}
EPSILON = 0.2
ALPHA = 0.5
GAMMA = 0.9

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

    chess_board = self.board(state)
    for move in chess_board.legal_moves:
        # Check if the move is castling or en passant
        if move.uci() in ['e1g1', 'e1c1', 'e8g8', 'e8c8', 'e1g1c1', 'e8g8c8']:
            legal_moves.append(move.uci())
        else:
            # Add other legal moves
            legal_moves.append(move.uci())

    return legal_moves
 
def findRandomMove(valid_moves):
    """
    Picks and returns a random valid move.
    """
    return random.choice(valid_moves)

