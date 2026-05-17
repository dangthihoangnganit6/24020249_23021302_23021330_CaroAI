from constants import BOARD_SIZE, WIN_COUNT, SCORES, EMPTY

def get_valid_moves(board): #Trả về danh sách các ô trống còn lại
    move =[] #Tạo mảng trống
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            if board[row][column] == EMPTY: #Nếu thấy có ô trống trên bàn cờ
                move.append([row, column]) #thêm ô trống đấy vào mảng để player có thể lựa chọn về sau (tức đưa node vào fringe để xét)
    return move 

def check_win(board): #Xét xem ai thắng
    current_direction = [[0, 1], [1, 0], [1, 1], [1, -1]] # Ngang, Dọc, Chéo chính, Chéo phụ
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            if board[row][column] == EMPTY:
                continue
            for dr, dc in current_direction: # Với mỗi ô có quân cờ, máy sẽ lần lượt nhìn về 4 hướng (dr, dc)
                count = 1 #Bắt đầu đếm số lượng 'X'/'O' có trên bàn cờ
                for i in range(1, WIN_COUNT):
                    new_row, new_column = row + dr*i, column + dc*i #Với i chạy từ 1-4, công thức để tính ra hàng mới, cột mới mà X/O đánh vào chính là: hàng/cột hiện tại + độ dịch hàng/cột * hệ số i
                    if 0 <= new_row < BOARD_SIZE and 0 <= new_column < BOARD_SIZE and board[new_row][new_column] == board[row][column]:
                        count += 1
                    else:
                        break
                if count >= WIN_COUNT:
                    return board[row][column]
    if not get_valid_moves(board):
        return 'Hoà'
    return None #TH bàn cờ bị đầy, chưa ăn 4
    
def Tinh_Diem(board, ai_piece, human_piece): #Tính điểm để sét xem ai thắng
    winner = check_win(board)
    human_piece = 'O' if ai_piece == 'X' else 'X' # Tự suy ra quân của người, rồi tự chọn quân cho mình
    if winner == ai_piece:
        return SCORES['WIN']
    elif winner == human_piece:
        return SCORES['LOSE']
    elif winner == 'Hoà':
        return 0
    score = 0
    #Từ phần này trở xuống đến hết break thì giống hệt bên 'check_in(board)'
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            if board[row][column] == EMPTY: 
                continue
            player = board[row][column]
            is_ai = (player == ai_piece)
            
            for dr, dc in directions:
                count = 1
                for i in range(1, WIN_COUNT):
                    new_row, new_column = row + dr * i, column + dc * i
                    if 0 <= new_row < BOARD_SIZE and 0 <= new_column < BOARD_SIZE and board[new_row][new_column] == player:
                        count += 1
                    else:
                        break
                if count == 3: #Nếu 1 trong 2 được 3 con
                    score += SCORES['AI_3_OPEN'] if is_ai else SCORES['PLAYER_3']
                elif count ==2: #Nếu 1 trong 2 được 2 con
                    score += SCORES['AI_2'] if is_ai else SCORES['PLAYER_2']
    return score

def get_refined_moves(board):
    """
    Chỉ sinh các nước đi gần các quân đã đánh (Candidate Moves).
    Sắp xếp theo thứ tự ưu tiên: 
    1. Ô có khả năng tạo chuỗi (gần nhiều quân cờ khác).
    2. Ô gần tâm bàn cờ.
    """
    from constants import NEIGHBOR_RADIUS
    
    occupied_positions = []
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] != EMPTY:
                occupied_positions.append((r, c))
    
    # Nếu bàn cờ trống, ưu tiên đánh vào trung tâm
    if not occupied_positions:
        center = BOARD_SIZE // 2
        return [[center, center]]
    
    candidates = set()
    for r, c in occupied_positions:
        for dr in range(-NEIGHBOR_RADIUS, NEIGHBOR_RADIUS + 1):
            for dc in range(-NEIGHBOR_RADIUS, NEIGHBOR_RADIUS + 1):
                nr, nc = r + dr, c + dc
                if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                    if board[nr][nc] == EMPTY:
                        candidates.add((nr, nc))
    
    # Hàm tính độ ưu tiên: Càng gần quân đã đánh và càng gần tâm càng tốt
    center_r, center_c = BOARD_SIZE // 2, BOARD_SIZE // 2
    
    def move_priority(pos):
        r, c = pos
        # Ưu tiên 1: Số lượng quân cờ xung quanh (phạm vi 1 ô)
        nearby_count = 0
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if dr == 0 and dc == 0: continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                    if board[nr][nc] != EMPTY:
                        nearby_count += 1
        
        # Ưu tiên 2: Khoảng cách đến tâm
        dist_to_center = (r - center_r)**2 + (c - center_c)**2
        
        # Trả về tuple để sắp xếp: nearby_count giảm dần (nên để dấu âm), dist_to_center tăng dần
        return (-nearby_count, dist_to_center)
    
    sorted_candidates = sorted(list(candidates), key=move_priority)
    
    return [list(pos) for pos in sorted_candidates]


