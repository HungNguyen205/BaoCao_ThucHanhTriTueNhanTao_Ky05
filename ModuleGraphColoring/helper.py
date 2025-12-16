import random
import networkx as nx # Thư viện để tạo và thao tác với đồ thị
import matplotlib.pyplot as plt # Thư viện để vẽ đồ thị và biểu đồ
import matplotlib.patches as mpatches # Để vẽ các miếng vá màu
import sys
import os
from core import CSPSolverLogic
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
class GraphCSP:
    """Quản lý dữ liệu đồ thị."""
    def __init__(self, num_vertices):
        self.n = num_vertices
        self.adj = {i: [] for i in range(num_vertices)}
        self.edges = []
        self.degrees = {}

    def add_constraint(self, u, v):
        if u != v and v not in self.adj[u]:
            self.adj[u].append(v)
            self.adj[v].append(u)
            self.edges.append((u, v))

    def generate_random_constraints(self, prob=0.4):
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if random.random() < prob:
                    self.add_constraint(i, j)
        # Lưu bậc của đỉnh để dùng cho Heuristic
        self.degrees = {i: len(self.adj[i]) for i in range(self.n)}

    def get_sorted_nodes(self):
        """Sắp xếp đỉnh theo bậc giảm dần."""
        return sorted(self.degrees.keys(), key=lambda x: self.degrees[x], reverse=True)

class CSPVisualizer:
    """Hiển thị đồ thị và Bảng logic chi tiết."""

    @staticmethod
    def show_step_with_logic_table(step, graph, current_node, assignment, table_data, max_colors):
        """
        Vẽ đồ thị và Bảng logic: Đỉnh -> Bậc -> Cấm -> Chọn.
        """
        # 1. SETUP ĐỒ THỊ
        G = nx.Graph()
        G.add_nodes_from(range(graph.n))
        G.add_edges_from(graph.edges)
        pos = nx.spring_layout(G, seed=99)

        cmap = plt.cm.tab20 # Bảng màu

        node_colors = []
        node_sizes = []
        edge_colors = []
        node_labels = {}

        for i in range(graph.n):
            node_labels[i] = str(i)
            if i == current_node:
                # Đỉnh đang xét: Vàng viền Đỏ
                node_colors.append('yellow')
                node_sizes.append(900)
                edge_colors.append('red')
            elif i in assignment:
                # Đỉnh đã tô
                color_idx = assignment[i]
                if color_idx == -1:
                    node_colors.append('black') # Fail
                else:
                    node_colors.append(cmap(color_idx % 20))
                node_sizes.append(700)
                edge_colors.append('black')
            else:
                # Chưa tô
                node_colors.append('lightgray')
                node_sizes.append(700)
                edge_colors.append('gray')

        # 2. VẼ SUBPLOTS (Trái: Graph, Phải: Table)
        fig, (ax_graph, ax_table) = plt.subplots(1, 2, figsize=(15, 6), gridspec_kw={'width_ratios': [1, 1]})

        # --- VẼ GRAPH ---
        nx.draw_networkx_nodes(G, pos, ax=ax_graph, node_color=node_colors, node_size=node_sizes, edgecolors=edge_colors, linewidths=2)
        nx.draw_networkx_edges(G, pos, ax=ax_graph, edge_color='gray', alpha=0.5)
        nx.draw_networkx_labels(G, pos, labels=node_labels, ax=ax_graph, font_weight='bold')

        title_info = f"Đang xét Đỉnh {current_node}" if current_node is not None else "Hoàn tất"
        ax_graph.set_title(f"BƯỚC {step}: {title_info}", fontsize=12, fontweight='bold')
        ax_graph.axis('off')

        # Legend màu
        patches = []
        unique_colors = sorted(list(set(val for val in assignment.values() if val != -1)))
        for c in unique_colors:
            patches.append(mpatches.Patch(color=cmap(c%20), label=f'Màu {c}'))
        if -1 in assignment.values():
            patches.append(mpatches.Patch(color='black', label='Lỗi'))

        if patches:
            ax_graph.legend(handles=patches, loc='lower center', ncol=4, bbox_to_anchor=(0.5, -0.15), fontsize=9)

        # --- VẼ BẢNG LOGIC ---
        ax_table.axis('off')
        ax_table.set_title(f"BẢNG PHÂN TÍCH CHỌN MÀU (Max: {max_colors})", fontweight='bold', pad=10)

        # Định nghĩa cột theo đúng yêu cầu
        col_labels = ["Bước", "Đỉnh", "Bậc", "Màu Bị Cấm (Hàng xóm)", "Màu Được Tô"]

        if table_data:
            # Hiển thị tối đa 16 dòng cuối
            visible_data = table_data[-16:]

            table = ax_table.table(cellText=visible_data, colLabels=col_labels,
                                   loc='center', cellLoc='center', bbox=[0, 0, 1, 1])

            table.auto_set_font_size(False)
            table.set_fontsize(9)

            # Format bảng đẹp hơn
            for (row, col), cell in table.get_celld().items():
                if row == 0: # Header
                    cell.set_facecolor('#404040')
                    cell.set_text_props(weight='bold', color='white')
                elif row == len(visible_data): # Dòng mới nhất (đang xét)
                    cell.set_facecolor('#fffacd') # Vàng nhạt
                    cell.set_text_props(weight='bold')

                if col == 3:
                    cell.set_text_props(size=8)

        else:
            ax_table.text(0.5, 0.5, "Đang khởi tạo...", ha='center')

        plt.tight_layout()
        plt.savefig(os.path.join(os.path.dirname(__file__), "result", f"step_{step}.png"))
        plt.close()

def run_csp():
    print("="*60)
    print("TÔ MÀU ĐỒ THỊ")
    print("="*60)

    # 1. Input
    while True:
        try:
            n = int(input("1. Nhập số đỉnh: "))
            if 3 <= n <= 25: break
            print("Nhập từ 3-25.")
        except: pass

    # 2. Tạo đồ thị
    graph = GraphCSP(n)
    graph.generate_random_constraints(prob=0.3)

    # 3. Gợi ý
    solver = CSPSolverLogic(graph)
    min_k = solver.suggest_min_colors()
    print(f"\nGỢI Ý: Đồ thị này cần tối thiểu {min_k} màu.")

    while True:
        try:
            user_k = int(input(f"2. Bạn muốn dùng bao nhiêu màu? (Nhập {min_k} để vừa đủ): "))
            if user_k >= 1: break
        except: pass

    print(f"\nĐang chạy mô phỏng với {user_k} màu...\n")

    # Vẽ đồ thị ban đầu
    CSPVisualizer.show_step_with_logic_table(0, graph, None, {}, [], user_k)
    print(f"Đã lưu kết quả bước 0 vào result/step_0.png")

    # 4. Loop vẽ
    prev_step = -1
    for step, curr, assign, history in solver.solve_process(limit_colors=user_k):
        if step != prev_step:
            CSPVisualizer.show_step_with_logic_table(step, graph, curr, assign, history, user_k)
            print(f"Đã lưu kết quả bước {step} vào result/step_{step}.png")
            prev_step = step

    print("\nHoàn tất quá trình tô màu.")