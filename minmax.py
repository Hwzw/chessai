def alpha_beta(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate(board)

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = alpha_beta(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = alpha_beta(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

scoring= {'p': -1,
          'n': -3,
          'b': -3,
          'r': -5,
          'q': -9,
          'k': 0,
          'P': 1,
          'N': 3,
          'B': 3,
          'R': 5,
          'Q': 9,
          'K': 0,
          }

# Piece-Square tables
piece_square_tables = {
    'P': [0, 0, 0, 0, 0, 0, 0, 0,
          1, 2, 2, -4, -4, 2, 2, 1,
          1, -1, -2, 0, 0, -2, -1, 1,
          0, 0, 0, 4, 4, 0, 0, 0,
          1, 1, 2, 5, 5, 2, 1, 1,
          2, 2, 4, 6, 6, 4, 2, 2,
          10, 10, 10, 10, 10, 10, 10, 10,
          0, 0, 0, 0, 0, 0, 0, 0],

    'N': [-10, -8, -6, -6, -6, -6, -8, -10,
          -8, -4, 0, 1, 1, 0, -4, -8,
          -6, 1, 2, 3, 3, 2, 1, -6,
          -6, 0, 3, 4, 4, 3, 0, -6,
          -6, 1, 3, 4, 4, 3, 1, -6,
          -6, 0, 2, 3, 3, 2, 0, -6,
          -8, -4, 0, 0, 0, 0, -4, -8,
          -10, -8, -6, -6, -6, -6, -8, -10],

    'B': [-4, -2, -2, -2, -2, -2, -2, -4,
          -2, 1, 0, 0, 0, 0, 1, -2,
          -2, 2, 2, 2, 2, 2, 0, -2,
          -2, 0, 2, 2, 2, 2, 0, -2,
          -2, 1, 1, 2, 2, 1, 1, -2,
          -2, 0, 1, 2, 2, 1, 0, -2,
          -2, 0, 0, 0, 0, 0, 0, -2,
          -4, -2, -2, -2, -2, -2, -2, -4],

    'R': [0, 0, 0, 1, 1, 0, 0, 0,
          -1, 0, 0, 0, 0, 0, 0, -1,
          -1, 0, 0, 0, 0, 0, 0, -1,
          -1, 0, 0, 0, 0, 0, 0, -1,
          -1, 0, 0, 0, 0, 0, 0, -1,
          -1, 0, 0, 0, 0, 0, 0, -1,
          1, 2, 2, 2, 2, 2, 2, 1,
          0, 0, 0, 0, 0, 0, 0, 0],

    'Q': [-4, -2, -2, -1, -1, -2, -2, -4,
          -2, 0, 0, 0, 0, 0, 0, -2,
          -2, 0, 1, 1, 1, 1, 0, -2,
          -1, 0, 1, 1, 1, 1, 0, -1,
          0, 0, 1, 1, 1, 1, 0, -1,
          -2, 1, 1, 1, 1, 1, 0, -2,
          -2, 0, 1, 0, 0, 0, 0, -2,
          -4, -2, -2, -1, -1, -2, -2, -4],

    'K': [-6, -8, -8, -10, -10, -8, -8, -6,
          -6, -8, -8, -10, -10, -8, -8, -6,
          -6, -8, -8, -10, -10, -8, -8, -6,
          -6, -8, -8, -10, -10, -8, -8, -6,
          -4, -6, -6, -8, -8, -6, -6, -4,
          -2, -4, -4, -4, -4, -4, -4, -2,
          4, 4, 0, 0, 0, 0, 4, 4,
          4, 6, 2, 0, 0, 2, 6, 4],
    'p': list(reversed([0, 0, 0, 0, 0, 0, 0, 0,
          1, 2, 2, -4, -4, 2, 2, 1,
          1, -1, -2, 0, 0, -2, -1, 1,
          0, 0, 0, 4, 4, 0, 0, 0,
          1, 1, 2, 5, 5, 2, 1, 1,
          2, 2, 4, 6, 6, 4, 2, 2,
          10, 10, 10, 10, 10, 10, 10, 10,
          0, 0, 0, 0, 0, 0, 0, 0]
    )),
    'n': list(reversed([-10, -8, -6, -6, -6, -6, -8, -10,
          -8, -4, 0, 1, 1, 0, -4, -8,
          -6, 1, 2, 3, 3, 2, 1, -6,
          -6, 0, 3, 4, 4, 3, 0, -6,
          -6, 1, 3, 4, 4, 3, 1, -6,
          -6, 0, 2, 3, 3, 2, 0, -6,
          -8, -4, 0, 0, 0, 0, -4, -8,
          -10, -8, -6, -6, -6, -6, -8, -10])),
    'b': list(reversed([-4, -2, -2, -2, -2, -2, -2, -4,
          -2, 1, 0, 0, 0, 0, 1, -2,
          -2, 2, 2, 2, 2, 2, 0, -2,
          -2, 0, 2, 2, 2, 2, 0, -2,
          -2, 1, 1, 2, 2, 1, 1, -2,
          -2, 0, 1, 2, 2, 1, 0, -2,
          -2, 0, 0, 0, 0, 0, 0, -2,
          -4, -2, -2, -2, -2, -2, -2, -4])),
    'r': list(reversed([0, 0, 0, 1, 1, 0, 0, 0,
          -1, 0, 0, 0, 0, 0, 0, -1,
          -1, 0, 0, 0, 0, 0, 0, -1,
          -1, 0, 0, 0, 0, 0, 0, -1,
          -1, 0, 0, 0, 0, 0, 0, -1,
          -1, 0, 0, 0, 0, 0, 0, -1,
          1, 2, 2, 2, 2, 2, 2, 1,
          0, 0, 0, 0, 0, 0, 0, 0])),
    'q': list(reversed([-4, -2, -2, -1, -1, -2, -2, -4,
          -2, 0, 0, 0, 0, 0, 0, -2,
          -2, 0, 1, 1, 1, 1, 0, -2,
          -1, 0, 1, 1, 1, 1, 0, -1,
          0, 0, 1, 1, 1, 1, 0, -1,
          -2, 1, 1, 1, 1, 1, 0, -2,
          -2, 0, 1, 0, 0, 0, 0, -2,
          -4, -2, -2, -1, -1, -2, -2, -4])),
    'k': list(reversed([-6, -8, -8, -10, -10, -8, -8, -6,
          -6, -8, -8, -10, -10, -8, -8, -6,
          -6, -8, -8, -10, -10, -8, -8, -6,
          -6, -8, -8, -10, -10, -8, -8, -6,
          -4, -6, -6, -8, -8, -6, -6, -4,
          -2, -4, -4, -4, -4, -4, -4, -2,
          4, 4, 0, 0, 0, 0, 4, 4,
          4, 6, 2, 0, 0, 2, 6, 4])),
}


#simple evaluation function
def evaluate(BOARD):
    score = 0
    pieces = BOARD.piece_map()
    for key in pieces:
        piece_type = str(pieces[key])
        score += scoring[piece_type]
        score += (piece_square_tables[piece_type][key])/10

    return score

def get_best_move(board, depth):
    best_move = None
    max_eval = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    for move in board.legal_moves:
        board.push(move)
        eval = alpha_beta(board, depth - 1, alpha, beta, True)
        board.pop()
        if eval > max_eval:
            max_eval = eval
            best_move = move
    return best_move
def get_worst_move(board, depth):
    worst_move = None
    min_eval = float('inf')
    alpha = float('-inf')
    beta = float('inf')
    for move in board.legal_moves:
        board.push(move)
        eval = alpha_beta(board, depth - 1, alpha, beta, True)
        board.pop()
        if eval < min_eval:
            min_eval = eval
            worst_move = move
    return worst_move
