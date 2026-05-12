from constants import BOARD_SIZE, WIN_COUNT, SCORES

def get_valid_moves(board): #Trả về danh sách các ô trống còn lại
    move =[] #Tạo mảng trống
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            if board[row][column] == EMPTY: #Nếu thấy có ô trống trên bàn cờ
                move.append([r, c]) #thêm ô trống đấy vào mảng để player có thể lựa chọn về sau (tức đưa node vào fringe để xét)
    return move 

def check_in(board): #Xét xem ai thắng
    current_direction = [[0, 1], [1, 0], [1, 1], [1, -1]] # Ngang, Dọc, Chéo chính, Chéo phụ
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            if board[row][column] == EMPTY:
                continue
            for dr, dc in current_direction: # Với mỗi ô có quân cờ, máy sẽ lần lượt nhìn về 4 hướng (dr, dc: Độ dịch)
                count = 1 #Bắt đầu đếm số lượng 'X'/'O' có trên bàn cờ
                for i in range(1, WIN_COUNT):
                    new_row, new_column = row + dr*i, column + dc*i #Với i chạy từ 1-4, công thức để tính ra hàng mới, cột mới mà X/O đánh vào chính là: hàng/cột hiện tại + độ dịch hàng/cột * hệ số i
                    if 0 <= new_row <= BOARD_SIZE and 0 <= new_column <= BOARD_SIZE:
                        count += 1
                    else:
                        break
                if count > WIN_COUNT:
                    return board[row][column]
    if not get_valid_moves(board):
        return 'Hoà'
    
def Tinh_Diem(board, ai_piece, human_piece): #Tính điểm để sét xem ai thắng
    winner = check_in(board)
    human_piece += 'O' if ai_piece == 'X' else 'X' # Tự suy ra quân của người, rồi tự chọn quân cho mình
    if winner == 'O':
        return SCORES['WIN']
    elif winner == 'X':
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
                    if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[new_row][new_column] == player:
                        count += 1
                    else:
                        break
                if count == 3: #Nếu 1 trong 2 được 3 con
                    score += SCORES['AI_3_OPEN'] if is_ai else SCORES['PLAYER_3']
                elif count ==2: #Nếu 1 trong 2 được 2 con
                    score += SCORES['AI_2'] if is_ai else SCORES['PLAYER_2']
    return score


