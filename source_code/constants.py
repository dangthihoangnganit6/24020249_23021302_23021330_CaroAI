# Kích thước bàn cờ và luật chơi
BOARD_SIZE = 9  # Tối thiểu 9x9
WIN_COUNT = 4   # Thắng 4 quân
EMPTY = '.'

# MAX là Máy (O), MIN là Người (X), ô trống là dấu chấm (.)
# Không xét luật chặn hai đầu
SCORES = {
    'WIN': 10000,         # Máy có 4 quân liên tiếp
    'LOSE': -10000,       # Người chơi có 4 quân liên tiếp
    'AI_3_OPEN': 800,     # Máy có 3 quân, còn khả năng mở rộng
    'PLAYER_3': -800,     # Người có 3 quân (ưu tiên chặn nên điểm âm lớn)
    'AI_2': 10,           # Máy có 2 quân
    'PLAYER_2': -20       # Người có 2 quân
}

MAX_DEPTH = 3  # Độ sâu tìm kiếm
NEIGHBOR_RADIUS = 2  # Phạm vi tìm kiếm xung quanh quân đã đánh
