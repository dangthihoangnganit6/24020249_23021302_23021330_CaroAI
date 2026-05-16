import time
import math
from logic import check_win, get_refined_moves, Tinh_Diem
from constants import EMPTY, SCORES, MAX_DEPTH

xet_trang_thai = 0

def alpha_beta(board, depth, alpha, beta, is_maximizing, ai_piece):
    """
    Thuật toán Alpha-Beta Pruning để cắt tỉa các nhánh vô hiệu.
    """
    global xet_trang_thai
    xet_trang_thai += 1
    
    human_piece = 'O' if ai_piece == 'X' else 'X'
    
    # Xét trạng thái kết thúc
    winner = check_win(board)
    if winner == ai_piece:
        return SCORES['WIN'] + depth
    elif winner == human_piece:
        return SCORES['LOSE'] - depth
    elif winner == 'Hoà':
        return 0
        
    if depth == 0:
        return Tinh_Diem(board, ai_piece, human_piece)
    
    # Sử dụng chung bộ sinh nước đi đã tối ưu
    valid_moves = get_refined_moves(board)
    
    if is_maximizing:
        best_score = -math.inf
        for row, column in valid_moves:
            board[row][column] = ai_piece
            score = alpha_beta(board, depth - 1, alpha, beta, False, ai_piece)
            board[row][column] = EMPTY
            
            best_score = max(score, best_score)
            alpha = max(alpha, best_score)
            
            # Cắt tỉa Alpha-Beta
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = math.inf
        for row, column in valid_moves:
            board[row][column] = human_piece
            score = alpha_beta(board, depth - 1, alpha, beta, True, ai_piece)
            board[row][column] = EMPTY
            
            best_score = min(score, best_score)
            beta = min(beta, best_score)
            
            # Cắt tỉa Alpha-Beta
            if beta <= alpha:
                break
        return best_score

def get_best_move_alphabeta(board, ai_piece, depth=MAX_DEPTH):
    """
    Hàm tìm nước đi tốt nhất sử dụng Alpha-Beta Pruning.
    """
    global xet_trang_thai
    xet_trang_thai = 0
    start_time = time.time()
    
    best_score = -math.inf
    best_move = None
    alpha = -math.inf
    beta = math.inf
    
    # Sử dụng chung bộ sinh nước đi đã tối ưu
    valid_moves = get_refined_moves(board)
    
    for row, column in valid_moves:
        board[row][column] = ai_piece
        score = alpha_beta(board, depth - 1, alpha, beta, False, ai_piece)
        board[row][column] = EMPTY
        
        if score > best_score:
            best_score = score
            best_move = (row, column)
            
        alpha = max(alpha, best_score)
            
    end_time = time.time()
    
    if best_move:
        print(f"\n[ALPHA-BETA AI ({ai_piece})] Đã chọn nước đi: Hàng {best_move[0]}, Cột {best_move[1]}")
        print(f"- Điểm đánh giá (Heuristic): {best_score}")
        print(f"- Độ sâu (Depth): {depth}")
        print(f"- Số trạng thái đã xét: {xet_trang_thai}")
        print(f"- Thời gian chạy: {end_time - start_time:.4f} giây")
        print("-" * 40)
        
    return best_move
