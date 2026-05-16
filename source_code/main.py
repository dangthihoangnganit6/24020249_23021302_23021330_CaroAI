import tkinter as tk
from tkinter import messagebox
import time
from constants import BOARD_SIZE, EMPTY, MAX_DEPTH
from logic import check_win
from minimax import get_best_move_minimax
from alphabeta import get_best_move_alphabeta
from benchmark import format_benchmark_stats

class CaroGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Caro AI - 9x9 (Thắng 4)")
        self.root.resizable(False, False)
        
        self.ai_mode = None  # 'minimax' hoặc 'alphabeta'
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.player_piece = 'X'
        self.ai_piece = 'O'
        self.turn = 'X'
        self.is_ai_thinking = False
        
        self.setup_menu()
        
    def setup_menu(self):
        """Màn hình chọn chế độ AI"""
        self.clear_window()
        
        frame = tk.Frame(self.root, padx=50, pady=50)
        frame.pack()
        
        tk.Label(frame, text="CHỌN CHẾ ĐỘ AI", font=("Arial", 16, "bold")).pack(pady=20)
        
        tk.Button(frame, text="Chạy bằng Minimax", font=("Arial", 12), width=25,
                  command=lambda: self.start_game("minimax")).pack(pady=10)
        
        tk.Button(frame, text="Chạy bằng Alpha-Beta Pruning", font=("Arial", 12), width=25,
                  command=lambda: self.start_game("alphabeta")).pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def start_game(self, mode):
        """Khởi tạo ván đấu mới: reset bàn cờ, lượt đi và biến khóa tương tác"""
        self.ai_mode = mode
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.turn = 'X'
        self.is_ai_thinking = False
        self.clear_window()
        self.setup_game_ui()

    def setup_game_ui(self):
        """Giao diện bàn cờ và bảng thông số"""
        # Frame chính
        self.main_frame = tk.Frame(self.root, padx=10, pady=10)
        self.main_frame.pack()
        
        # Frame bàn cờ
        self.board_frame = tk.Frame(self.main_frame)
        self.board_frame.pack(side=tk.LEFT)
        
        self.buttons = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                btn = tk.Button(self.board_frame, text="", font=("Arial", 14, "bold"),
                                width=3, height=1,
                                command=lambda r=r, c=c: self.on_click(r, c))
                btn.grid(row=r, column=c)
                self.buttons[r][c] = btn
        
        # Frame thông số (Benchmark)
        self.info_frame = tk.Frame(self.main_frame, padx=20)
        self.info_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Label(self.info_frame, text="THÔNG SỐ AI", font=("Arial", 12, "bold")).pack(pady=10)
        
        self.stats_label = tk.Label(self.info_frame, text="Đang đợi nước đi...", 
                                   font=("Arial", 10), justify=tk.LEFT)
        self.stats_label.pack(anchor="nw")
        
        tk.Button(self.info_frame, text="Chơi lại", command=self.setup_menu).pack(side=tk.BOTTOM, pady=20)

    def on_click(self, r, c):
        if self.is_ai_thinking or self.board[r][c] != EMPTY or self.turn != self.player_piece:
            return
        
        # Người đánh
        self.make_move(r, c, self.player_piece)
        
        if not self.check_game_over():
            self.turn = self.ai_piece
            self.root.after(500, self.trigger_ai)

    def make_move(self, r, c, piece):
        self.board[r][c] = piece
        color = "blue" if piece == 'X' else "red"
        self.buttons[r][c].config(text=piece, fg=color, state=tk.DISABLED, disabledforeground=color)

    def trigger_ai(self):
        self.is_ai_thinking = True
        self.stats_label.config(text="AI đang suy nghĩ...")
        self.root.update_idletasks()
        
        # Gọi hàm AI tương ứng
        if self.ai_mode == "minimax":
            move, stats = get_best_move_minimax(self.board, self.ai_piece)
        else:
            move, stats = get_best_move_alphabeta(self.board, self.ai_piece)
            
        if move:
            self.make_move(move[0], move[1], self.ai_piece)
            self.display_stats(stats)
            
        self.is_ai_thinking = False
        self.turn = self.player_piece
        self.check_game_over()

    def display_stats(self, stats):
        """Hiển thị thông số Benchmark lên GUI bằng module benchmark"""
        text = format_benchmark_stats(stats)
        self.stats_label.config(text=text)

    def check_game_over(self):
        winner = check_win(self.board)
        if winner:
            if winner == 'Hoà':
                messagebox.showinfo("Kết thúc", "Trận đấu Hòa!")
            else:
                msg = "Bạn đã thắng!" if winner == self.player_piece else "AI đã thắng!"
                messagebox.showinfo("Kết thúc", msg)
            self.is_ai_thinking = True # Khóa bàn cờ
            return True
        return False

if __name__ == "__main__":
    root = tk.Tk()
    app = CaroGameGUI(root)
    root.mainloop()
