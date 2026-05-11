# ============================================================
#  main.py – Game loop + AI mode selector + Level-3 comparison
# ============================================================

import sys
from constants import BOARD_SIZE, EMPTY, PLAYER_X, AI_O
from logic import check_win, is_full
from minimax  import get_ai_move_minimax
from alphabeta import get_ai_move_ab, evaluate


# ------------------------------------------------------------------
# Board display
# ------------------------------------------------------------------
def print_board(board):
    """Pretty-print the board with row/column indices."""
    col_header = "   " + "  ".join(f"{c:1}" for c in range(BOARD_SIZE))
    print(col_header)
    print("   " + "--" * BOARD_SIZE)
    for r, row in enumerate(board):
        cells = "  ".join('.' if v == EMPTY else ('X' if v == PLAYER_X else 'O')
                          for v in row)
        print(f"{r:2}| {cells}")
    print()


# ------------------------------------------------------------------
# Level-3: compare both algorithms on the current board state
# ------------------------------------------------------------------
def compare_algorithms(board, depth):
    """
    Run both Minimax and Alpha-Beta on the same board and depth,
    then print a comparison table (Value, Nodes, Time, Same move?).
    """
    import time
    from minimax   import minimax,    states_count as _  # noqa – import module
    from alphabeta import alpha_beta                      # noqa

    import minimax   as mm_mod
    import alphabeta as ab_mod

    print("\n" + "="*55)
    print("  LEVEL 3 – Algorithm Comparison")
    print("="*55)

    # --- Minimax ---
    mm_mod.states_count = 0
    t0 = time.time()
    mm_score, mm_move = mm_mod.minimax(board, depth, True)
    mm_time  = time.time() - t0
    mm_nodes = mm_mod.states_count

    # --- Alpha-Beta ---
    ab_mod.states_count = 0
    t0 = time.time()
    ab_score, ab_move = ab_mod.alpha_beta(board, depth,
                                          float('-inf'), float('inf'), True)
    ab_time  = time.time() - t0
    ab_nodes = ab_mod.states_count

    same_move  = mm_move == ab_move
    same_score = mm_score == ab_score

    print(f"{'Metric':<22} {'Minimax':>14} {'Alpha-Beta':>14}")
    print("-"*52)
    print(f"{'Value':<22} {mm_score:>14} {ab_score:>14}")
    print(f"{'Nodes searched':<22} {mm_nodes:>14} {ab_nodes:>14}")
    print(f"{'Time (s)':<22} {mm_time:>14.4f} {ab_time:>14.4f}")
    print(f"{'Best move':<22} {str(mm_move):>14} {str(ab_move):>14}")
    print(f"{'Same move?':<22} {'YES ✓' if same_move else 'NO ✗':>14}")
    if mm_nodes > 0:
        reduction = (1 - ab_nodes / mm_nodes) * 100
        print(f"{'Node reduction':<22} {reduction:>13.1f}%")
    print("="*55 + "\n")

    return ab_move   # use Alpha-Beta's answer (faster, identical result)


# ------------------------------------------------------------------
# Human move input
# ------------------------------------------------------------------
def get_human_move(board):
    while True:
        try:
            raw = input("Nhập nước đi (hàng cột, vd: 4 5): ").strip()
            r, c = map(int, raw.split())
            if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE):
                print("  Tọa độ ngoài bàn cờ, thử lại.")
                continue
            if board[r][c] != EMPTY:
                print("  Ô đã được đánh, chọn ô khác.")
                continue
            return r, c
        except (ValueError, IndexError):
            print("  Nhập sai định dạng. Hãy nhập: hàng cột  (vd: 4 5)")


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
def main():
    print("=" * 45)
    print("       CARO (GOMOKU) – 4-in-a-row          ")
    print("=" * 45)
    print(f"Bàn cờ {BOARD_SIZE}x{BOARD_SIZE}  |  Thắng khi có 4 quân liên tiếp\n")

    print("Chọn chế độ AI:")
    print("  1. Minimax          (Level 1 – chậm hơn)")
    print("  2. Alpha-Beta       (Level 2 – nhanh hơn)")
    print("  3. So sánh cả hai   (Level 3 – hiện bảng so sánh trước mỗi nước đi)")

    while True:
        choice = input("Nhập lựa chọn (1/2/3): ").strip()
        if choice in ('1', '2', '3'):
            break
        print("  Vui lòng nhập 1, 2 hoặc 3.")

    while True:
        try:
            depth = int(input("Nhập độ sâu tìm kiếm (khuyến nghị 3): ").strip())
            if 1 <= depth <= 6:
                break
            print("  Vui lòng nhập số từ 1 đến 6.")
        except ValueError:
            print("  Vui lòng nhập một số nguyên.")

    board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]

    print("\nBạn là X, máy là O.  Nhập tọa độ theo dạng: hàng cột\n")
    print_board(board)

    while True:
        # --- Human move ---
        r, c = get_human_move(board)
        board[r][c] = PLAYER_X
        print_board(board)

        if check_win(board, PLAYER_X):
            print("🎉 Bạn thắng! Chúc mừng!")
            break
        if is_full(board):
            print("🤝 Hòa cờ!")
            break

        # --- AI move ---
        print("Máy đang suy nghĩ...")

        if choice == '1':
            move = get_ai_move_minimax(board, depth)
        elif choice == '2':
            move = get_ai_move_ab(board, depth)
        else:
            # Level 3: compare, then play Alpha-Beta's move
            move = compare_algorithms(board, depth)

        if move is None:
            print("🤝 Hòa cờ!")
            break

        board[move[0]][move[1]] = AI_O
        print_board(board)

        if check_win(board, AI_O):
            print("🤖 Máy thắng!")
            break
        if is_full(board):
            print("🤝 Hòa cờ!")
            break


if __name__ == "__main__":
    main()