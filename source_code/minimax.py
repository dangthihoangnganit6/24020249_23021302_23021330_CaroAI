# ============================================================
#  minimax.py – Pure Minimax (no pruning) – Level 1
#
#  Uses evaluate() from alphabeta.py to ensure identical scoring,
#  guaranteeing the same move choices as Alpha-Beta (just slower).
# ============================================================

import time
from constants import BOARD_SIZE, EMPTY, PLAYER_X, AI_O
from logic import check_win, get_valid_moves, is_full
from alphabeta import evaluate   # shared heuristic

states_count = 0


def minimax(board, depth, is_maximizing):
    """
    Pure Minimax (no α-β pruning).

    Returns (score, best_move):
      score      – heuristic value
      best_move  – (row, col), or None at leaf nodes
    """
    global states_count
    states_count += 1

    # --- Terminal / depth-limit ---
    if depth == 0 or check_win(board, AI_O) or check_win(board, PLAYER_X) or is_full(board):
        return evaluate(board), None

    valid_moves = get_valid_moves(board)
    best_move   = None

    if is_maximizing:                   # AI (MAX)
        max_eval = float('-inf')
        for move in valid_moves:
            r, c = move
            board[r][c] = AI_O
            eval_val, _ = minimax(board, depth - 1, False)
            board[r][c] = EMPTY

            if eval_val > max_eval:
                max_eval  = eval_val
                best_move = move
        return max_eval, best_move

    else:                               # Human (MIN)
        min_eval = float('inf')
        for move in valid_moves:
            r, c = move
            board[r][c] = PLAYER_X
            eval_val, _ = minimax(board, depth - 1, True)
            board[r][c] = EMPTY

            if eval_val < min_eval:
                min_eval  = eval_val
                best_move = move
        return min_eval, best_move


def get_ai_move_minimax(board, depth):
    """
    Entry point called by main.py.
    Runs pure Minimax, prints performance metrics, returns best (row, col).
    """
    global states_count
    states_count = 0

    start = time.time()
    score, move = minimax(board, depth, True)
    elapsed = time.time() - start

    print(f"\n--- Minimax (depth={depth}) ---")
    print(f"  Giá trị đánh giá : {score}")
    print(f"  Số trạng thái    : {states_count}")
    print(f"  Thời gian chạy   : {elapsed:.4f}s")
    if move:
        print(f"  Nước đi chọn     : hàng {move[0]}, cột {move[1]}")

    return move
