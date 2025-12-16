class CSPSolverLogic:
    def __init__(self, graph):
        self.graph = graph

    def suggest_min_colors(self):
        """Gợi ý số màu."""
        nodes = self.graph.get_sorted_nodes()
        temp_asn = {}
        for u in nodes:
            forbidden = {temp_asn[v] for v in self.graph.adj[u] if v in temp_asn}
            c = 0
            while c in forbidden: c += 1
            temp_asn[u] = c
        return max(temp_asn.values()) + 1

    def solve_process(self, limit_colors):
        """Generator: Trả về dữ liệu bảng logic từng bước."""

        # 1. Sắp xếp biến (Heuristic Bậc)
        # Đây là cột "Bậc" trong bảng
        sorted_nodes = self.graph.get_sorted_nodes() # Sắp xếp đỉnh theo bậc giảm dần

        assignment = {} # Biến: Đỉnh -> Màu
        table_history = [] # Lịch sử bảng từng bước
        # Cấu trúc row: [Bước, Đỉnh, Bậc, Màu Cấm, Màu Chọn]

        step = 0

        for u in sorted_nodes:
            step += 1

            # Yield trạng thái TRƯỚC khi quyết định (để hiện dòng đang xét)
            yield step, u, assignment, table_history

            # 2. Tìm ràng buộc (Màu bị cấm)
            degree_u = self.graph.degrees[u] # Bậc của đỉnh u
            forbidden_colors = set() # Tập màu bị cấm

            for v in self.graph.adj[u]: # Duyệt các láng giềng
                if v in assignment and assignment[v] != -1: # Láng giềng đã được gán màu
                    forbidden_colors.add(assignment[v]) # Thêm màu bị cấm

            # Format string màu cấm
            forbidden_str = str(sorted(list(forbidden_colors))).replace('[', '{').replace(']', '}')
            if not forbidden_colors: forbidden_str = "∅" # Rỗng

            # 3. Chọn màu
            chosen_color = -1
            for c in range(limit_colors):
                if c not in forbidden_colors:
                    chosen_color = c
                    break

            assignment[u] = chosen_color

            # Kết quả hiển thị
            res_str = f"Màu {chosen_color}" if chosen_color != -1 else "FAIL"

            # Thêm vào lịch sử bảng
            table_history.append([
                step,
                f"Đỉnh {u}",
                degree_u,
                forbidden_str,
                res_str
            ])
        yield step + 1, None, assignment, table_history