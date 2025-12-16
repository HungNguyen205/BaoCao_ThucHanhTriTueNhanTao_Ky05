import numpy as np
from IPython.display import clear_output # Thư viện để xóa output, hỗ trợ animation
import matplotlib.pyplot as plt # Thư viện để vẽ đồ thị và biểu đồ
import math   # Thư viện chứa các hàm toán học cơ bản
from core import EMPTY, PLAYER_X, PLAYER_O, CaroAI

class CaroBoard:
    def __init__(self, size_n, size_m=None):
        """
        Khởi tạo bàn cờ n x n.

        Args:
            n (int): Kích thước cạnh của bàn cờ (mặc định = 10).
        """
        self.rows = size_n
        self.cols = size_m if size_m else size_n
        self.grid = np.zeros((self.rows, self.cols), dtype=int)

        # Luật thắng tự động
        min_dim = min(self.rows, self.cols)
        self.win_k = 3 if min_dim <= 3 else (4 if min_dim <= 5 else 5)
        print(f"--> Tạo bàn {self.rows}x{self.cols}. Luật thắng: Nối {self.win_k}.")

    def is_valid(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] == EMPTY

    def make_move(self, r, c, player):
        if self.is_valid(r, c):
            self.grid[r][c] = player
            return True
        return False

    def check_winner(self):
        """
        Kiểm tra xem người chơi chỉ định đã thắng chưa (có 5 quân liên tiếp).

        Args:
            player (int): Giá trị đại diện người chơi (1 hoặc -1).

        Returns:
            bool: True nếu người chơi này đã thắng, ngược lại False.
        """
        k = self.win_k
        dirs = [(0, 1), (1, 0), (1, 1), (1, -1)] # 4 hướng: ngang, dọc, chéo chính, chéo phụ
        for r in range(self.rows):
            for c in range(self.cols):
                p = self.grid[r][c] #Giá trị ô hiện tại
                if p == EMPTY: continue
                for dr, dc in dirs:
                    if (0 <= r + (k-1)*dr < self.rows) and (0 <= c + (k-1)*dc < self.cols): # Kiểm tra trong phạm vi
                        if all(self.grid[r + i*dr][c + i*dc] == p for i in range(k)): # Kiểm tra k ô liên tiếp
                            return p
        return 0

    def is_full(self):
        """
        Kiểm tra bàn cờ đã đầy chưa (Hòa).

        Returns:
            bool: True nếu không còn ô trống, False nếu còn.
        """
        return np.all(self.grid != EMPTY)

    def get_nearby_empty_cells(self, radius=1):
        """
        Tìm các ô trống lân cận các ô đã đánh (phạm vi 2 ô).
        Giúp thuật toán Minimax chỉ tập trung vào các khu vực có ý nghĩa thay vì duyệt toàn bộ bàn cờ.

        Returns:
            list[tuple]: Danh sách tọa độ (row, col) các ô trống đáng quan tâm.
        """
        indices = np.argwhere(self.grid != EMPTY)
        if len(indices) == 0: return [(self.rows//2, self.cols//2)]

        candidates = set()
        for r, c in indices:
            for dr in range(-radius, radius+1):
                for dc in range(-radius, radius+1):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid[nr][nc] == EMPTY:
                        candidates.add((nr, nc))
        return list(candidates)

class CaroVisualizer:
    @staticmethod
    def draw(board, last_move=None, ai_scores=None):
        clear_output(wait=True)
        # Tự động chỉnh size ảnh
        fig_w = max(5, board.cols * 0.6)
        fig_h = max(5, board.rows * 0.6)
        fig, ax = plt.subplots(figsize=(fig_w, fig_h))

        # 1. Cấu hình trục để ô vuông chẵn
        ax.set_xlim(0, board.cols)
        ax.set_ylim(board.rows, 0) # Đảo trục Y
        ax.set_aspect('equal') # Bắt buộc ô phải vuông

        # 2. Vẽ lưới (Grid) thủ công để đảm bảo đẹp
        # Vẽ các đường ngang
        for r in range(board.rows + 1):
            ax.axhline(r, color='black', linewidth=1)
        # Vẽ các đường dọc
        for c in range(board.cols + 1):
            ax.axvline(c, color='black', linewidth=1)

        # Tắt trục mặc định
        ax.axis('on')
        ax.set_xticks(np.arange(0.5, board.cols, 1))
        ax.set_yticks(np.arange(0.5, board.rows, 1))

        # Đánh số tọa độ ở giữa ô (hoặc dùng tick labels)
        ax.set_xticklabels(range(board.cols))
        ax.set_yticklabels(range(board.rows))
        ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False) # Số cột hiện ở trên

        # 3. Vẽ X và O
        for r in range(board.rows):
            for c in range(board.cols):
                val = board.grid[r][c]
                if val == PLAYER_X:
                    # Vẽ X
                    ax.plot(c + 0.5, r + 0.5, marker='x', markersize=20,
                            color='blue', markeredgewidth=3)
                elif val == PLAYER_O:
                    # Vẽ O
                    ax.plot(c + 0.5, r + 0.5, marker='o', markersize=20,
                            markeredgecolor='red', markerfacecolor='none', markeredgewidth=3)

        # 4. Highlight nước vừa đi (Màu vàng nhạt)
        if last_move:
            lr, lc = last_move
            rect = plt.Rectangle((lc, lr), 1, 1, color='yellow', alpha=0.3, zorder=0)
            ax.add_patch(rect)

        # 5. Heatmap điểm số
        if ai_scores:
            for (r, c), score in ai_scores.items():
                s_txt = f"{int(score/1000)}k" if abs(score)>=1000 else f"{int(score)}"
                ax.text(c+0.5, r+0.85, s_txt, ha='center', va='center',
                        fontsize=8, color='purple', alpha=0.8)

        plt.title(f"Luật thắng: {board.win_k} ô liên tiếp", pad=20)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def print_board(board, last_move=None):
        print("\nBàn cờ hiện tại:")
        print("   " + " ".join(f"{i:2}" for i in range(board.cols)))
        print("  +" + "---+" * board.cols)
        for r in range(board.rows):
            row_str = f"{r:2}|"
            for c in range(board.cols):
                val = board.grid[r][c]
                if val == PLAYER_X:
                    cell = " X "
                elif val == PLAYER_O:
                    cell = " O "
                else:
                    cell = " . "
                if last_move and (r, c) == last_move:
                    cell = f"[{cell[1]}]"  # Highlight last move
                row_str += cell + "|"
            print(row_str)
            print("  +" + "---+" * board.cols)
        print()


def run_caro_final():
    print("="*50)
    print("CARO AI ❌⭕")
    print("="*50)

    # 1. Nhập Ma trận (Kích thước)
    while True:
        try:
            print("\nNhập kích thước bàn cờ (VD: '3x3', '5x5', '10x10'):")
            raw = input(">> Kích thước: ").lower().replace(' ', '')

            if 'x' in raw:
                rows, cols = map(int, raw.split('x'))
            else:
                rows = cols = int(raw)

            if rows < 3 or cols < 3:
                print("Kích thước phải >= 3x3.")
            elif rows > 15 or cols > 15:
                print("Kích thước tối đa 15x15.")
            else:
                break
        except:
            print("Định dạng sai (VD đúng: 5x5).")

    # 2. Khởi tạo
    board = CaroBoard(rows, cols)
    ai = CaroAI(depth=3)
    CaroVisualizer.draw(board)
    CaroVisualizer.print_board(board)

    print(f"\n[LUẬT CHƠI] Bạn là X (Xanh). AI là O (Vòng tròn Đỏ).")
    print(f"Điều kiện thắng: {board.win_k} ô liên tiếp.")

    while True:
        # --- HUMAN TURN ---
        while True:
            try:
                txt = input("\n[Lượt X] Nhập 'Hàng Cột' (VD: 1 1): ")
                if txt.lower() == 'q': return
                r, c = map(int, txt.split())
                if board.make_move(r, c, PLAYER_X): break
                print("Ô không hợp lệ!")
            except: pass

        CaroVisualizer.draw(board, last_move=(r,c))
        CaroVisualizer.print_board(board, last_move=(r,c))

        if board.check_winner() == PLAYER_X:
            print("\nBẠN THẮNG!")
            break
        if board.is_full():
            print("\nHÒA CỜ!")
            break

        # --- AI TURN ---
        print("\nAI đang suy nghĩ...")
        move, scores, logs = ai.get_best_move_explained(board)

        if move:
            board.make_move(move[0], move[1], PLAYER_O)
            CaroVisualizer.draw(board, last_move=move, ai_scores=scores)
            CaroVisualizer.print_board(board, last_move=move)

            print(f"\nBẢNG PHÂN TÍCH (Top 3):")
            print(f"| {'Tọa độ':<8} | {'Điểm số':<10} | {'Đánh giá'}")
            for item in logs[:3]:
                print(f"| {str((item[0], item[1])):<8} | {item[2]:<10} | {item[3]}")

            print(f"AI chọn {move} (Điểm: {logs[0][2]})")

            if board.check_winner() == PLAYER_O:
                print("\nAI THẮNG!")
                break
            if board.is_full():
                print("\nHÒA CỜ!")
                break
        else:
            print("Lỗi AI.")
            break