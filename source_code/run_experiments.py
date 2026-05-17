import sys
import os
import copy
from minimax import get_best_move_minimax
from alphabeta import get_best_move_alphabeta

sys.stdout.reconfigure(encoding='utf-8')

class SuppressPrint:
    """Lớp hỗ trợ chặn các lệnh in ra màn hình (print) từ các file thuật toán"""
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w', encoding='utf-8')
    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

def create_board(layout):
    """Chuyển đổi mảng chuỗi (string) thành ma trận 2 chiều"""
    return [list(row) for row in layout]

# Khởi tạo 6 trạng thái bàn cờ đặc trưng (9x9)
states = {
    "State 1: Đầu ván (Bàn cờ có 1 quân trung tâm)": create_board([
        ".........",
        ".........",
        ".........",
        ".........",
        "....X....",
        ".........",
        ".........",
        ".........",
        "........."
    ]),
    "State 2: Giữa ván (Thế cờ giằng co, nhiều quân rải rác)": create_board([
        ".........",
        ".........",
        ".........",
        "....X....",
        "...XOO...",
        "....O....",
        ".........",
        ".........",
        "........."
    ]),
    "State 3: Máy (O) có thể thắng ngay (Có chuỗi 3 quân O)": create_board([
        ".........",
        ".........",
        ".........",
        "...OOO...", # Máy O có cơ hội thắng ngay nếu đánh vào vị trí 3 hoặc 7 (0-indexed)
        "....XX...",
        ".........",
        ".........",
        ".........",
        "........."
    ]),
    "State 4: Người (X) sắp thắng, Máy (O) cần chặn (Có chuỗi 3 quân X)": create_board([
        ".........",
        ".........",
        ".........",
        "...XXX...", # Người X có chuỗi 3, O buộc phải chặn ở 2 đầu
        "....O....",
        ".........",
        ".........",
        ".........",
        "........."
    ]),
    "State 5: Hai bên đều có cơ hội tấn công": create_board([
        ".........",
        ".........",
        "..X.O....",
        "..O.XX...",
        "...O.X...",
        ".........",
        ".........",
        ".........",
        "........."
    ]),
    "State 6: Trạng thái nhiều nước đi hợp lệ (Test sức mạnh cắt tỉa)": create_board([
        ".........",
        ".........",
        "..X...O..",
        "...O.X...",
        "....X....",
        "...O.X...",
        "..X...O..",
        ".........",
        "........."
    ])
}

def run_experiments():
    depths = [1, 2, 3]
    ai_piece = 'O'
    
    print("# Kết quả Thực nghiệm AI Game Caro 9x9 (Minimax vs Alpha-Beta)\n")
    
    for state_name, board in states.items():
        print(f"## {state_name}\n")
        print("| Thuật toán | Độ sâu | Nước đi chọn | Điểm Heuristic | Số trạng thái đã xét | Thời gian chạy (s) |")
        print("|---|:---:|:---:|---:|---:|---:|")
        
        for depth in depths:
            # --- Chạy Minimax ---
            board_copy_mm = copy.deepcopy(board)
            with SuppressPrint():
                move_mm, stats_mm = get_best_move_minimax(board_copy_mm, ai_piece, depth=depth)
            
            # --- Chạy Alpha-Beta ---
            board_copy_ab = copy.deepcopy(board)
            with SuppressPrint():
                move_ab, stats_ab = get_best_move_alphabeta(board_copy_ab, ai_piece, depth=depth)
            
            # Xử lý format chuỗi kết quả
            move_str_mm = f"({stats_mm['move'][0]}, {stats_mm['move'][1]})" if stats_mm['move'] else "None"
            move_str_ab = f"({stats_ab['move'][0]}, {stats_ab['move'][1]})" if stats_ab['move'] else "None"
            
            # In dòng kết quả Minimax
            print(f"| Minimax | {depth} | {move_str_mm} | {stats_mm['score']} | {stats_mm['states']} | {stats_mm['time']:.4f} |")
            # In dòng kết quả Alpha-Beta
            print(f"| Alpha-Beta | {depth} | {move_str_ab} | {stats_ab['score']} | {stats_ab['states']} | {stats_ab['time']:.4f} |")
            
        print("\n")

if __name__ == '__main__':
    run_experiments()
