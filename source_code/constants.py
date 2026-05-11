# ============================================================
#  constants.py – Shared configuration for the Caro AI project
# ============================================================

BOARD_SIZE = 9          # Minimum 9x9
EMPTY      = 0
PLAYER_X   = 1          # Human (MIN)
AI_O       = 2          # AI    (MAX)
WIN_LEN    = 4          # 4 consecutive marks to win
NEIGHBOR_RADIUS = 2     # Candidate moves within 2 squares of any piece

# --- Heuristic scores (highest priority first) ---
SCORE_WIN      =  1_000_000   # AI 4-in-a-row
SCORE_LOSE     = -1_000_000   # Human 4-in-a-row
SCORE_ATTACK_3 =     10_000   # AI open-3
SCORE_DEFEND_3 =    -50_000   # Human open-3 (block > attack)
SCORE_ATTACK_2 =        100   # AI 2-streak
SCORE_DEFEND_2 =       -150   # Human 2-streak