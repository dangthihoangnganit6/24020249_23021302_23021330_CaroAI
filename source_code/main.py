import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
import copy
from constants import BOARD_SIZE, EMPTY, MAX_DEPTH
from logic import check_win
from minimax import get_best_move_minimax
from alphabeta import get_best_move_alphabeta
from benchmark import format_benchmark_stats
from run_experiments import states as EXPERIMENT_STATES

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
        """Màn hình chọn chế độ AI và Độ sâu tìm kiếm"""
        self.clear_window()
        
        frame = tk.Frame(self.root, padx=50, pady=50)
        frame.pack()
        
        tk.Label(frame, text="CHỌN CHẾ ĐỘ AI", font=("Arial", 16, "bold")).pack(pady=20)
        
        # Thêm lựa chọn độ sâu
        depth_frame = tk.Frame(frame)
        depth_frame.pack(pady=10)
        tk.Label(depth_frame, text="Độ sâu (Depth):", font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
        self.depth_var = tk.IntVar(value=3)
        tk.Spinbox(depth_frame, from_=1, to=3, textvariable=self.depth_var, width=5, font=("Arial", 11)).pack(side=tk.LEFT)
        
        tk.Button(frame, text="Chạy bằng Minimax", font=("Arial", 12), width=25,
                  command=lambda: self.start_game("minimax")).pack(pady=10)
        
        tk.Button(frame, text="Chạy bằng Alpha-Beta Pruning", font=("Arial", 12), width=25,
                  command=lambda: self.start_game("alphabeta")).pack(pady=10)
                  
        tk.Label(frame, text="--- HOẶC ---", font=("Arial", 10)).pack(pady=10)
        
        tk.Button(frame, text="Chế độ Thực nghiệm", font=("Arial", 12, "bold"), width=25, bg="lightyellow",
                  command=self.setup_experiment_menu).pack(pady=10)

    def setup_experiment_menu(self):
        """Màn hình chọn cấu hình chạy Thực nghiệm"""
        self.clear_window()
        frame = tk.Frame(self.root, padx=30, pady=30)
        frame.pack()
        
        tk.Label(frame, text="CHẾ ĐỘ THỰC NGHIỆM", font=("Arial", 16, "bold"), fg="blue").pack(pady=20)
        
        # Chọn State
        tk.Label(frame, text="1. Chọn trạng thái bàn cờ:", font=("Arial", 11, "bold")).pack(anchor="w", pady=(10, 2))
        self.state_var = tk.StringVar()
        state_options = list(EXPERIMENT_STATES.keys())
        self.state_var.set(state_options[0])
        tk.OptionMenu(frame, self.state_var, *state_options).pack(fill=tk.X)
        
        # Chọn Thuật toán
        tk.Label(frame, text="2. Chọn Thuật toán:", font=("Arial", 11, "bold")).pack(anchor="w", pady=(15, 2))
        self.algo_var = tk.StringVar(value="minimax")
        tk.OptionMenu(frame, self.algo_var, "minimax", "alphabeta").pack(fill=tk.X)
        
        # Chọn Độ sâu
        tk.Label(frame, text="3. Chọn Độ sâu (1-3):", font=("Arial", 11, "bold")).pack(anchor="w", pady=(15, 2))
        self.exp_depth_var = tk.IntVar(value=3)
        tk.Spinbox(frame, from_=1, to=3, textvariable=self.exp_depth_var, width=10, font=("Arial", 11)).pack(anchor="w")
        
        tk.Button(frame, text="Bắt đầu Thực nghiệm", font=("Arial", 12, "bold"), bg="lightblue", width=25,
                  command=self.start_experiment).pack(pady=30)
                  
        tk.Button(frame, text="Quay lại", font=("Arial", 10), width=15, command=self.setup_menu).pack()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def start_game(self, mode):
        """Khởi tạo ván đấu mới: reset bàn cờ, lượt đi và biến khóa tương tác"""
        self.ai_mode = mode
        self.current_depth = self.depth_var.get()
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.turn = 'X'
        self.is_ai_thinking = False
        self.clear_window()
        self.setup_game_ui()
        
    def start_experiment(self):
        """Khởi tạo ván đấu từ trạng thái có sẵn và tự động cho AI chạy"""
        state_name = self.state_var.get()
        self.ai_mode = self.algo_var.get()
        self.current_depth = self.exp_depth_var.get()
        
        # Nạp trạng thái bàn cờ
        self.board = copy.deepcopy(EXPERIMENT_STATES[state_name])
        self.turn = self.ai_piece # Ép lượt của AI để AI tự động đánh
        self.is_ai_thinking = True # Khóa bàn cờ ngay lập tức
        
        self.clear_window()
        self.setup_game_ui()
        
        # Hiển thị các quân cờ đã có sẵn lên GUI
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                piece = self.board[r][c]
                if piece != EMPTY:
                    color = "blue" if piece == 'X' else "red"
                    self.buttons[r][c].config(text=piece, fg=color, state=tk.DISABLED, disabledforeground=color)
        
        self.stats_label.config(text=f"Đang chạy {self.ai_mode.upper()}...")
        # Gọi AI sau 500ms để GUI kịp render
        self.root.after(500, self.trigger_ai)

    def setup_game_ui(self):
        """Giao diện bàn cờ và bảng thông số"""
        self.main_frame = tk.Frame(self.root, padx=10, pady=10)
        self.main_frame.pack()
        
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
        
        self.info_frame = tk.Frame(self.main_frame, padx=20)
        self.info_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Label(self.info_frame, text="THÔNG SỐ AI", font=("Arial", 12, "bold")).pack(pady=10)
        
        tk.Label(self.info_frame, text=f"Thuật toán: {self.ai_mode.upper() if self.ai_mode else ''}", font=("Arial", 10, "italic")).pack(anchor="nw")
        tk.Label(self.info_frame, text=f"Độ sâu hiện tại: {self.current_depth if hasattr(self, 'current_depth') else ''}", font=("Arial", 10, "italic")).pack(anchor="nw")
        
        self.stats_label = tk.Label(self.info_frame, text="Đang đợi nước đi...", 
                                   font=("Arial", 10), justify=tk.LEFT)
        self.stats_label.pack(anchor="nw", pady=(10, 0))
        
        tk.Button(self.info_frame, text="Quay lại Menu", command=self.setup_menu).pack(side=tk.BOTTOM, pady=20)

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
        
        # Cần capture stdout nếu muốn sạch sẽ, nhưng trong GUI print ra terminal cũng không sao
        # (Ở đây ta vẫn dùng hàm gốc)
        if self.ai_mode == "minimax":
            move, stats = get_best_move_minimax(self.board, self.ai_piece, depth=self.current_depth)
        else:
            move, stats = get_best_move_alphabeta(self.board, self.ai_piece, depth=self.current_depth)
            
        if move:
            self.make_move(move[0], move[1], self.ai_piece)
            self.display_stats(stats)
            
        self.is_ai_thinking = False
        self.turn = self.player_piece
        self.check_game_over()

    def display_stats(self, stats):
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
            self.is_ai_thinking = True
            return True
        return False

if __name__ == "__main__":
    root = tk.Tk()
    app = CaroGameGUI(root)
    root.mainloop()
