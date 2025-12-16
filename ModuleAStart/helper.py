import os
import random # Thư viện để tạo số ngẫu nhiên
import numpy as np
import matplotlib.colors as mcolors # Để tạo ra các bảng màu tùy chỉnh
import matplotlib.pyplot as plt # Thư viện để vẽ đồ thị và biểu đồ
import matplotlib.patches as mpatches # Để vẽ các miếng vá màu (như các ô vuông màu trong chú thích)
from matplotlib.lines import Line2D # Để vẽ các đường thẳng hoặc biểu tượng trong phần chú thích
class Node:
    """Đại diện cho một ô."""
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        # Ưu tiên F nhỏ, nếu bằng thì ưu tiên H nhỏ
        return self.f < other.f or (self.f == other.f and self.h < other.h)

    def __repr__(self):
        return f"{self.position}"

class Maze:
    """Quản lý dữ liệu mê cung."""
    def __init__(self, size):
        self.size = size
        self.grid = np.zeros((size, size)) # 0: Đường, 1: Tường
        self.start = None
        self.goal = None

    def generate_obstacles(self, prob):
        self.grid = np.zeros((self.size, self.size))
        for r in range(self.size):
            for c in range(self.size):
                if random.random() < prob:
                    self.grid[r][c] = 1

    def set_points(self, start, goal):
        self.start = start
        self.goal = goal
        self.grid[start] = 0
        self.grid[goal] = 0

    def is_valid(self, pos):
        r, c = pos
        return (0 <= r < self.size) and (0 <= c < self.size) and (self.grid[r][c] == 0)

class MazeVisualizer:
    """Class vẽ Mê cung, Bảng tính và Chú thích."""

    @staticmethod
    def show_step_with_legend(step, maze, current_node, open_list, closed_set, neighbors_info, path=None, result_dir=None):
        """
        Vẽ đầy đủ: Mê cung, Lưới, Chú thích màu, Bảng Heuristic.
        """
        # 1. SETUP MÀU SẮC
        # 0:Trắng, 1:Đen, 2:Xám, 3:Cam, 4:Tím, 5:Xanh
        color_grid = maze.grid.copy()

        for r, c in closed_set:
            color_grid[r][c] = 2 # Closed
        for node in open_list:
            color_grid[node.position[0]][node.position[1]] = 3 # Open
        if current_node:
            color_grid[current_node.position[0]][current_node.position[1]] = 4 # Current

        # Định nghĩa bảng màu
        colors = ['white', 'black', '#d3d3d3', '#ffa500', '#800080', '#0000ff']
        cmap = mcolors.ListedColormap(colors)
        bounds = [0, 1, 2, 3, 4, 5, 6]
        norm = mcolors.BoundaryNorm(bounds, cmap.N)

        # 2. KHỞI TẠO KHUNG HÌNH (SUBPLOTS)
        fig, (ax_map, ax_table) = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={'width_ratios': [1.2, 0.8]})

        # --- A. VẼ MÊ CUNG (TRÁI) ---
        ax_map.imshow(color_grid, cmap=cmap, norm=norm)

        # Kẻ lưới và đánh số
        ax_map.set_xticks(np.arange(-0.5, maze.size, 1), minor=True)
        ax_map.set_yticks(np.arange(-0.5, maze.size, 1), minor=True)
        ax_map.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)
        ax_map.xaxis.tick_top() # Số cột nằm trên

        # Vẽ Start/Goal
        ax_map.scatter(maze.start[1], maze.start[0], c='lime', s=180, edgecolors='k', zorder=10, label='Start')
        ax_map.scatter(maze.goal[1], maze.goal[0], c='red', marker='*', s=250, edgecolors='k', zorder=10, label='Goal')

        if path:
            ys, xs = zip(*path)
            ax_map.plot(xs, ys, c='blue', linewidth=4, zorder=5)
            ax_map.set_title(f"BƯỚC {step}: HOÀN THÀNH (Chi phí {len(path)})", fontweight='bold', pad=15)
        else:
            title_txt = f"Start" if current_node is None else f"{current_node.position}"
            ax_map.set_title(f"BƯỚC {step}: Đang xét {title_txt}", fontweight='bold', pad=15)

        # --- B. TẠO CHÚ THÍCH ---
        # Tạo các miếng vá màu (Patches) giả lập cho legend
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor='lime', markersize=10, markeredgecolor='k', label='Start'),
            Line2D([0], [0], marker='*', color='w', markerfacecolor='red', markersize=13, markeredgecolor='k', label='Goal'),
            mpatches.Patch(facecolor='white', edgecolor='gray', label='Đường đi'),
            mpatches.Patch(color='black', label='Tường'),
            mpatches.Patch(color='#d3d3d3', label='Đã duyệt (Closed)'),
            mpatches.Patch(color='#ffa500', label='Đang chờ (Open)'),
            mpatches.Patch(color='#800080', label='Đang xét (Current)'),
            mpatches.Patch(color='#0000ff', label='Đường đi kết quả')
        ]

        # Đặt chú thích bên dưới bản đồ
        ax_map.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.05),
                      fancybox=True, shadow=True, ncol=4, fontsize=9)

        # --- C. VẼ BẢNG TÍNH (PHẢI) ---
        ax_table.axis('off')
        ax_table.set_title("BẢNG TÍNH HEURISTIC (F = G + H)", fontweight='bold', pad=10)

        table_data = []
        if current_node:
            table_data.append([str(current_node.position), current_node.g, f"{current_node.h:.1f}", f"{current_node.f:.1f}", "Current"])

        for n_info in neighbors_info:
            # n_info: (pos, g, h, f, status)
            table_data.append([str(n_info[0]), n_info[1], f"{n_info[2]:.1f}", f"{n_info[3]:.1f}", n_info[4]])

        col_labels = ["Tọa độ", "G (Thực)", "H (Ước lượng)", "F (Tổng)", "Ghi chú"]

        if table_data:
            # Màu nền cho bảng để dễ nhìn
            cell_colors = []
            for i in range(len(table_data)):
                if i == 0 and current_node: cell_colors.append(["#f0f0f0"] * 5) # Dòng đầu xám nhạt
                else: cell_colors.append(["#ffffff"] * 5)

            table = ax_table.table(cellText=table_data, colLabels=col_labels,
                                   cellColours=cell_colors,
                                   loc='center', cellLoc='center', bbox=[0, 0, 1, 1])
            table.auto_set_font_size(False)
            table.set_fontsize(10)
        else:
            ax_table.text(0.5, 0.5, "Đang khởi tạo...", ha='center', style='italic')

        plt.tight_layout()
        if result_dir:
            plt.savefig(os.path.join(result_dir, f"step_{step}.png"), bbox_inches='tight')
        else:
            plt.show()
        plt.close(fig)

def get_maze_config():
    print("Mẹo: Nhập '8 30' để tạo bản đồ 8x8, mật độ 30%")
    try:
        raw_cfg = input(">> Nhập [Size] [Mật độ %]: ").split()
        if len(raw_cfg) < 2: n, prob = 8, 0.3 # Mặc định
        else: n, prob = int(raw_cfg[0]), int(raw_cfg[1])/100.0
    except:
        n, prob = 8, 0.3
        print("Lỗi nhập liệu -> Dùng mặc định 8x8, 30%")
    return n, prob

def get_start_goal(maze):
    while True:
        try:
            print("Nhập tọa độ dạng: Hàng Cột (VD: 0 0)")
            s_in = input(">> Start: ").split()
            g_in = input(">> Goal : ").split()

            start = (int(s_in[0]), int(s_in[1]))
            goal = (int(g_in[0]), int(g_in[1]))

            if maze.is_valid(start) and maze.is_valid(goal):
                return start, goal
            else:
                print("Tọa độ trùng Tường hoặc ngoài MAP! Nhập lại.")
        except:
            print("Sai định dạng số!")

def run_astar():
    from core import AStarSolver
    print("=== A* ===")

    # 1. Nhập cấu hình
    n, prob = get_maze_config()

    result_dir = os.path.join(os.path.dirname(__file__), "result")
    os.makedirs(result_dir, exist_ok=True)

    # Tạo & Hiển thị map trống
    maze = Maze(n)
    maze.generate_obstacles(prob)

    print(f"\n[MAP {n}x{n}]")
    plt.figure(figsize=(4, 4))
    plt.imshow(maze.grid, cmap='binary')
    plt.grid(color='gray', linestyle='-', linewidth=0.5)
    plt.title("Nhìn bản đồ này để chọn tọa độ")
    plt.savefig(os.path.join(result_dir, "map_empty.png"), bbox_inches='tight')
    plt.close()

    # 2. Nhập tọa độ Start/Goal
    start, goal = get_start_goal(maze)

    maze.set_points(start, goal)

    # 3. Chạy thuật toán
    solver = AStarSolver(maze)
    print("\n" + "="*50)
    print(f"BẮT ĐẦU DUYỆT TỪ {start} --> {goal}")
    print("="*50)

    for step, curr, opens, closeds, neighbors, path in solver.solve_process():
        # Gọi hàm hiển thị
        MazeVisualizer.show_step_with_legend(step, maze, curr, opens, closeds, neighbors, path, result_dir)

        if path:
            print(f"\nĐÃ TÌM THẤY ĐÍCH SAU {step} BƯỚC!")
            break
        if curr is None and not path:
            print("\nKHÔNG TÌM THẤY ĐƯỜNG ĐI!")
            break
