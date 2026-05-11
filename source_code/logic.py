# ============================================================
#  logic.py – Board helpers: win detection & move generation
# ============================================================

from constants import BOARD_SIZE, EMPTY, WIN_LEN, NEIGHBOR_RADIUS

DIRS = [(0, 1), (1, 0), (1, 1), (1, -1)]   # right, down, diag↘, diag↗


def check_win(board, player):
    """
    Return True if *player* has WIN_LEN consecutive marks anywhere.
    No double-end block rule – blocked lines still count as a win.
    """
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] != player:
                continue
            for dr, dc in DIRS:
                count = 1
                for step in range(1, WIN_LEN):
                    nr, nc = r + dr * step, c + dc * step
                    if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE \
                            and board[nr][nc] == player:
                        count += 1
                    else:
                        break
                if count >= WIN_LEN:
                    return True
    return False


def is_full(board):
    """Return True when every cell is occupied."""
    return all(board[r][c] != EMPTY
               for r in range(BOARD_SIZE)
               for c in range(BOARD_SIZE))


def get_valid_moves(board):
    """
    Candidate moves: empty cells within NEIGHBOR_RADIUS of any placed piece.
    Improvements (per spec):
      1. Only cells near existing pieces (reduces branching).
      2. If board is empty, return the centre cell.
      3. Sort by Manhattan distance to centre (prefer central moves).
    """
    candidates = set()
    has_piece = False

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == EMPTY:
                continue
            has_piece = True
            for dr in range(-NEIGHBOR_RADIUS, NEIGHBOR_RADIUS + 1):
                for dc in range(-NEIGHBOR_RADIUS, NEIGHBOR_RADIUS + 1):
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE
                            and board[nr][nc] == EMPTY):
                        candidates.add((nr, nc))

    if not has_piece:
        return [(BOARD_SIZE // 2, BOARD_SIZE // 2)]

    centre = BOARD_SIZE // 2
    return sorted(candidates,
                  key=lambda m: abs(m[0] - centre) + abs(m[1] - centre))