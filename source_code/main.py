import os
from constants import BOARD_SIZE, EMPTY, MAX_DEPTH
from logic import check_win
from minimax import get_best_move_minimax
from alphabeta import get_best_move_alphabeta

def print_board(board):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("   " + " ".join(str(i) for i in range(BOARD_SIZE)))
    for i, row in enumerate(board):
        print(f"{i:2} {' '.join(row)}")
    print("-" * 25)

def main():
    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    
    print("=== CHÀO MỪNG ĐẾN VỚI GAME CARO AI (9x9, THẮNG 4) ===")
    print("1. Chạy AI bằng Minimax truyền thống")
    print("2. Chạy AI bằng Alpha-Beta Pruning")
    
    choice = input("Chọn chế độ AI (1/2): ")
    ai_mode = "alphabeta" if choice == '2' else "minimax"
    
    print(f"\nBạn đã chọn: {'Alpha-Beta' if ai_mode == 'alphabeta' else 'Minimax'}")
    
    player_piece = 'X'
    ai_piece = 'O'
    
    turn = 'X'  # Người đi trước
    
    while True:
        print_board(board)
        winner = check_win(board)
        if winner:
            if winner == 'Hoà':
                print("Kết quả: Hòa!")
            else:
                print(f"Kết quả: {winner} thắng!")
            break
            
        if turn == player_piece:
            print(f"Lượt của bạn ({player_piece})")
            try:
                r = int(input(f"Nhập hàng (0-{BOARD_SIZE-1}): "))
                c = int(input(f"Nhập cột (0-{BOARD_SIZE-1}): "))
                if board[r][c] == EMPTY:
                    board[r][c] = player_piece
                    turn = ai_piece
                else:
                    print("Ô đã có quân, hãy chọn lại!")
                    input("Nhấn Enter để tiếp tục...")
            except (ValueError, IndexError):
                print("Tọa độ không hợp lệ!")
                input("Nhấn Enter để tiếp tục...")
        else:
            print(f"AI ({ai_piece}) đang suy nghĩ...")
            if ai_mode == "alphabeta":
                move = get_best_move_alphabeta(board, ai_piece)
            else:
                move = get_best_move_minimax(board, ai_piece)
                
            if move:
                board[move[0]][move[1]] = ai_piece
                turn = player_piece
            else:
                print("AI không tìm thấy nước đi (Hòa)!")
                break

if __name__ == "__main__":
    main()
