import numpy as np
import math   # Thư viện chứa các hàm toán học cơ bản

# Hằng số
EMPTY = 0
PLAYER_X = 1 # Người chơi
PLAYER_O = 2 # AI
class CaroAI:
    """
    Lớp AI (Solver) sử dụng thuật toán Minimax kết hợp cắt tỉa Alpha-Beta.
    """
    def __init__(self, depth=3):
        """
        Khởi tạo AI.

        Args:
            depth (int): Độ sâu tối đa của cây tìm kiếm (mặc định = 3).
        """
        self.depth = depth
        self.max_player = PLAYER_O
        self.min_player = PLAYER_X

    def evaluate_window(self, window, player, win_k): # Đánh giá một cửa sổ (window) trên bàn cờ
        score = 0
        opp = self.min_player if player == self.max_player else self.max_player # Đối thủ

        my_cnt = np.count_nonzero(window == player) # Đếm số quân của người chơi trong cửa sổ
        opp_cnt = np.count_nonzero(window == opp) # Đếm số quân của đối thủ trong cửa sổ

        if my_cnt > 0 and opp_cnt > 0: return 0

        if my_cnt == win_k: score += 1000000
        elif my_cnt == win_k - 1: score += 50000
        elif my_cnt == win_k - 2: score += 1000
        elif my_cnt == win_k - 3: score += 100
        return score

    def evaluate_board(self, board): # Đánh giá toàn bộ bàn cờ
        winner = board.check_winner()
        if winner == self.max_player: return 100000000
        if winner == self.min_player: return -100000000

        score = 0
        k = board.win_k
        grid = board.grid

        # Ngang
        for r in range(board.rows): # Duyệt từng hàng
            for c in range(board.cols - k + 1): 
                w = grid[r, c:c+k] 
                score += self.evaluate_window(w, self.max_player, k) 
                score -= self.evaluate_window(w, self.min_player, k) * 1.5
        # Dọc
        for c in range(board.cols): # Duyệt từng cột
            for r in range(board.rows - k + 1):
                w = grid[r:r+k, c]
                score += self.evaluate_window(w, self.max_player, k)
                score -= self.evaluate_window(w, self.min_player, k) * 1.5
        return score

    def minimax(self, board, depth, alpha, beta, is_max):
        if depth == 0 or board.is_full() or board.check_winner(): # Điều kiện dừng
            return self.evaluate_board(board)

        candidates = board.get_nearby_empty_cells() # Lấy các ô trống gần các quân đã đánh
        if is_max:
            max_eval = -math.inf # Khởi tạo giá trị lớn nhất
            for r, c in candidates:
                board.grid[r][c] = self.max_player 
                ev = self.minimax(board, depth-1, alpha, beta, False) # Đệ quy
                board.grid[r][c] = EMPTY
                max_eval = max(max_eval, ev)
                alpha = max(alpha, ev)
                if beta <= alpha: break # Cắt tỉa
            return max_eval
        else:
            min_eval = math.inf
            for r, c in candidates:
                board.grid[r][c] = self.min_player 
                ev = self.minimax(board, depth-1, alpha, beta, True) 
                board.grid[r][c] = EMPTY
                min_eval = min(min_eval, ev)
                beta = min(beta, ev)
                if beta <= alpha: break
            return min_eval

    def get_best_move_explained(self, board): # Lấy nước đi tốt nhất
        best_score = -math.inf
        best_move = None
        logs = [] 
        score_map = {}

        candidates = board.get_nearby_empty_cells()
        if not candidates: # Nếu bàn cờ trống, đánh ở giữa
            return (board.rows//2, board.cols//2), {}, [] 

        for r, c in candidates: 
            board.grid[r][c] = self.max_player
            score = self.minimax(board, self.depth-1, -math.inf, math.inf, False)
            board.grid[r][c] = EMPTY

            score_map[(r, c)] = score
            note = "Thủ/Công"
            if score >= 50000: note = "Sắp thắng/Chặn thua"
            elif score >= 1000: note = "Tạo thế công"
            elif score <= -50000: note = "Nguy hiểm"

            logs.append((r, c, score, note))
            if score > best_score:
                best_score = score
                best_move = (r, c)

        logs.sort(key=lambda x: x[2], reverse=True)
        return best_move, score_map, logs

__all__ = ['EMPTY', 'PLAYER_X', 'PLAYER_O', 'CaroAI']