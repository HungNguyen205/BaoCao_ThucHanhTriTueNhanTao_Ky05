import heapq
from helper import Node
class AStarSolver:
    def __init__(self, maze):
        self.maze = maze

    def _heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def solve_process(self):
        """
        Generator: Trả về dữ liệu chi tiết để vẽ bảng.
        """
        start_node = Node(self.maze.start)
        goal_node = Node(self.maze.goal)
        start_node.h = self._heuristic(start_node.position, goal_node.position) 
        start_node.f = start_node.g + start_node.h #Khởi tạo và Công thức F = G + H

        open_list = []
        heapq.heappush(open_list, start_node) #Thêm node bắt đầu vào danh sách mở

        closed_set = set() #Tập hợp các node đã duyệt
        g_score = {self.maze.start: 0}

        step_count = 0

        while open_list:
            step_count += 1

            # 1. Lấy node tốt nhất
            current = heapq.heappop(open_list)

            # Danh sách lưu thông tin các hàng xóm để hiển thị bảng
            neighbors_info = []

            # 2. Kiểm tra đích
            if current.position == goal_node.position: # Nếu đã đến đích
                path = self._reconstruct_path(current) # Tạo đường đi từ start đến goal
                # Yield lần cuối
                yield step_count, current, open_list, closed_set, [], path
                return

            closed_set.add(current.position)

            # 3. Duyệt lân cận
            # Duyệt theo thứ tự: Lên, Trái, Xuống, Phải
            for d in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                neighbor_pos = (current.position[0] + d[0], current.position[1] + d[1])

                if not self.maze.is_valid(neighbor_pos): # Nếu không hợp lệ, bỏ qua
                    continue

                if neighbor_pos in closed_set:
                    continue

                new_g = current.g + 1 # Chi phí di chuyển luôn là 1
                h_val = self._heuristic(neighbor_pos, goal_node.position)
                f_val = new_g + h_val

                status = "Mới"

                # Nếu đường đi mới tốt hơn hoặc chưa từng đến
                if neighbor_pos not in g_score or new_g < g_score[neighbor_pos]: # Nếu đường đi tốt hơn
                    if neighbor_pos in g_score: status = "Cập nhật tốt hơn" # Đã từng đến nhưng đường đi tốt hơn

                    g_score[neighbor_pos] = new_g
                    neighbor = Node(neighbor_pos, current)
                    neighbor.g = new_g
                    neighbor.h = h_val
                    neighbor.f = f_val

                    heapq.heappush(open_list, neighbor)
                    neighbors_info.append((neighbor_pos, new_g, h_val, f_val, status))

            # YIELD: Trả về dữ liệu để vẽ
            yield step_count, current, open_list, closed_set, neighbors_info, None

        # Không tìm thấy đường
        yield step_count, None, [], closed_set, [], None

    def _reconstruct_path(self, node): # Tạo đường đi từ start đến goal
        path = []
        while node:
            path.append(node.position)
            node = node.parent
        return path[::-1]
