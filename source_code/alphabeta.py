# ============================================================
#  alphabeta.py – Alpha-Beta Pruning + shared evaluate() function
# ============================================================
#
#  evaluate() is shared with minimax.py to guarantee identical
#  scoring so that both algorithms always agree on the best move.
# ============================================================

import time
from constants import (BOARD_SIZE, EMPTY, PLAYER_X, AI_O,
                       WIN_LEN, SCORE_WIN, SCORE_LOSE,
                       SCORE_ATTACK_3, SCORE_DEFEND_3,
                       SCORE_ATTACK_2, SCORE_DEFEND_2)
from logic import check_win, get_valid_moves, is_full, DIRS


# Module-level counter reset before each AI call
states_count = 0


# ------------------------------------------------------------------
# Helper: score a single line of WIN_LEN cells for one player
# ------------------------------------------------------------------
def _score_window(window, player):
    """
    Score a sliding window of WIN_LEN cells.
    Returns a heuristic value from the perspective of *player*.
    """
    opponent = PLAYER_X if player == AI_O else AI_O

    player_count   = window.count(player)
    opponent_count = window.count(opponent)
    empty_count    = window.count(EMPTY)

    # Opponent already occupies some cells → window is useless for player
    if opponent_count > 0:
        return 0

    if player_count == WIN_LEN:
        return SCORE_WIN if player == AI_O else SCORE_LOSE

    if player == AI_O:
        if player_count == 3 and empty_count == 1:
            return SCORE_ATTACK_3
        if player_count == 2 and empty_count == 2:
            return SCORE_ATTACK_2
    else:  # PLAYER_X (human)
        if player_count == 3 and empty_count == 1:
            return SCORE_DEFEND_3
        if player_count == 2 and empty_count == 2:
            return SCORE_DEFEND_2

    return 0


# ------------------------------------------------------------------
# evaluate – heuristic board assessment (shared with minimax.py)
# ------------------------------------------------------------------
def evaluate(board):
    """
    Heuristic evaluation of *board*:
      +SCORE_WIN  / -SCORE_WIN   for terminal wins
      scored streaks for 3-in-a-row and 2-in-a-row patterns

    Positive score  → AI is better.
    Negative score  → Human is better.
    """
    # Fast terminal checks
    if check_win(board, AI_O):     return SCORE_WIN
    if check_win(board, PLAYER_X): return SCORE_LOSE

    total = 0

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            for dr, dc in DIRS:
                # Build a window of WIN_LEN cells
                window = []
                for step in range(WIN_LEN):
                    nr, nc = r + dr * step, c + dc * step
                    if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                        window.append(board[nr][nc])
                    else:
                        break
                if len(window) < WIN_LEN:
                    continue

                total += _score_window(window, AI_O)
                total += _score_window(window, PLAYER_X)

    return total


# ------------------------------------------------------------------
# alpha_beta – recursive search with α-β pruning
# ------------------------------------------------------------------
def alpha_beta(board, depth, alpha, beta, is_maximizing):
    """
    Minimax with Alpha-Beta pruning.

    Returns (score, best_move):
      score      – heuristic value of the position
      best_move  – (row, col) of the best move, or None at leaf nodes
    """
    global states_count
    states_count += 1

    # --- Terminal / depth-limit conditions ---
    if depth == 0 or check_win(board, AI_O) or check_win(board, PLAYER_X) or is_full(board):
        return evaluate(board), None

    valid_moves = get_valid_moves(board)
    best_move   = None

    if is_maximizing:                       # AI's turn  (MAX)
        max_eval = float('-inf')
        for move in valid_moves:
            r, c = move
            board[r][c] = AI_O
            eval_val, _ = alpha_beta(board, depth - 1, alpha, beta, False)
            board[r][c] = EMPTY

            if eval_val > max_eval:
                max_eval  = eval_val
                best_move = move
            alpha = max(alpha, eval_val)
            if beta <= alpha:               # β-cutoff (prune)
                break
        return max_eval, best_move

    else:                                   # Human's turn (MIN)
        min_eval = float('inf')
        for move in valid_moves:
            r, c = move
            board[r][c] = PLAYER_X
            eval_val, _ = alpha_beta(board, depth - 1, alpha, beta, True)
            board[r][c] = EMPTY

            if eval_val < min_eval:
                min_eval  = eval_val
                best_move = move
            beta = min(beta, eval_val)
            if beta <= alpha:               # α-cutoff (prune)
                break
        return min_eval, best_move


# ------------------------------------------------------------------
# Public API
# ------------------------------------------------------------------
def get_ai_move_ab(board, depth):
    """
    Entry point called by main.py.
    Runs Alpha-Beta, prints performance metrics, returns best (row, col).
    """
    global states_count
    states_count = 0

    start = time.time()
    score, move = alpha_beta(board, depth, float('-inf'), float('inf'), True)
    elapsed = time.time() - start

    print(f"\n--- Alpha-Beta Pruning (depth={depth}) ---")
    print(f"  Giá trị đánh giá : {score}")
    print(f"  Số trạng thái    : {states_count}")
    print(f"  Thời gian chạy   : {elapsed:.4f}s")
    if move:
        print(f"  Nước đi chọn     : hàng {move[0]}, cột {move[1]}")

    return move