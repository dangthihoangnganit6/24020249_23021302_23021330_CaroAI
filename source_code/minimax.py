import time
import math
from logic import check_win, get_valid_moves, Tinh_Diem
from constants import EMPTY, SCORES, MAX_DEPTH

xet_trang_thai = 0

def minimax(board, depth, is_maximizing, ai_piece): #depth: độ sâu còn lại ; is_maximizing: Biến kiểu Đúng/Sai. Nếu là True, AI đang đóng vai chính mình (tìm điểm cao nhất). Nếu là False, AI đang giả vờ đóng vai đối thủ (tìm điểm thấp nhất để hại mình).
    global xet_trang_thai #Mỗi lần AI "nghĩ" về một trạng thái bàn cờ mới, cộng 1 vào đây. Đây chính là con số "Số trạng thái đã xét"
    xet_trang_thai += 1
    
    human_piece = 'O' if ai_piece == 'X' else 'X'
    #Xét thắng/thua/hoà
    winner = check_win(board)
    if winner == ai_piece: 
        return SCORES['WIN'] + depth 
    elif winner == human_piece: 
        return SCORES['LOSE'] - depth
    elif winner == 'Tie': 
        return 0
        
    if depth == 0: #Hết độ sâu,gọi hàm để tính điểm
        return Tinh_Diem(board, ai_piece, human_piece) # Truyền ai_piece xuống hàm Tinh_Diem
    
    valid_moves = get_valid_moves(board)
    
    if is_maximizing:
        best_score = -math.inf #gán cho biến best_score giá trị âm vô cực, đảm bảo rằng bất kỳ nước đi đầu tiên nào AI thử nghiệm cũng sẽ có điểm số lớn hơn âm vô cực (vì AI phe Max)
        for row, column in valid_moves:
            board[row][column] = ai_piece # AI thử đặt quân của mình vào bản cờ ảo
            score = minimax(board, depth - 1, False, ai_piece)
            board[row][column] = EMPTY #Sau khi AI "ảo" xong một nước đi, nó phải xóa quân cờ đó đi để trả lại bàn cờ sạch sẽ ban đầu trước khi thử nước đi khác, không thì AI sẽ bị lặp
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf #gán cho biến best_score giá trị dương vô cực, đảm bảo bất kỳ nước đi nào người chơi đánh ra cũng sẽ có điểm nhỏ hơn dương vô cực (vì người chơi phe Min)
        for row, column in valid_moves:
            board[row][column] = human_piece # AI tưởng tượng đối thủ đặt quân
            score = minimax(board, depth - 1, True, ai_piece)
            board[row][column] = EMPTY #Tương tự trên
            best_score = min(score, best_score)
        return best_score

def get_best_move_minimax(board, ai_piece, depth=MAX_DEPTH):
    global xet_trang_thai
    xet_trang_thai = 0 # Reset bộ đếm về 0 trước khi bắt đầu nghĩ
    start_time = time.time() #Bắt đầu tính thời gian
    
    best_score = -math.inf
    best_move = None
    valid_moves = get_valid_moves(board)
    
    for row, column in valid_moves:
        board[row][column] = ai_piece
        score = minimax(board, depth - 1, False, ai_piece)
        board[row][column] = EMPTY
        
        if score > best_score:
            best_score = score
            best_move = (row, column)
            
    end_time = time.time() #Dừng tính thời gian
    
    if best_move: #In ra
        print(f"\n[MINIMAX AI ({ai_piece})] Đã chọn nước đi: Hàng {best_move[0]}, Cột {best_move[1]}")
        print(f"- Điểm đánh giá (Heuristic): {best_score}")
        print(f"- Độ sâu (Depth): {depth}")
        print(f"- Số trạng thái đã xét: {xet_trang_thai}")
        print(f"- Thời gian chạy: {end_time - start_time:.4f} giây")
        print("-" * 40)
        
    return best_move


