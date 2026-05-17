# Kích thước bàn cờ và luật chơi
BOARD_SIZE = 9  # Tối thiểu 9x9
WIN_COUNT = 4   # Thắng 4 quân
EMPTY = '.'

# MAX là Máy (O), MIN là Người (X), ô trống là dấu chấm (.)
# Không xét luật chặn hai đầu
SCORES = {
    'WIN': 1000000,         # Máy có 4 quân liên tiếp
    'LOSE': -1000000,       # Người chơi có 4 quân liên tiếp
    'AI_3_OPEN': 10000,     # Máy có 3 quân, còn khả năng mở rộng
    'PLAYER_3': -100000,     # Người có 3 quân (ưu tiên chặn nên điểm âm lớn)
    'AI_2': 200,           # Máy có 2 quân
    'PLAYER_2': -1000       # Người có 2 quân
}

MAX_DEPTH = 3  # Độ sâu tìm kiếm
NEIGHBOR_RADIUS = 2  # Phạm vi tìm kiếm xung quanh quân đã đánh
