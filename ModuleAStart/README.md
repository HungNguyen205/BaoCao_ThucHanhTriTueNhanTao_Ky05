## 1. Giới thiệu bài toán
Bài toán tìm đường đi trong mê cung (Maze Pathfinding) là một ví dụ điển hình của bài toán tìm kiếm trên đồ thị.
* **Không gian trạng thái:** Một lưới $N \times N$ các ô vuông.
* **Trạng thái:** Tọa độ $(x, y)$ của ô hiện tại.
* **Hành động:** Di chuyển sang các ô lân cận (Lên, Xuống, Trái, Phải) nếu không bị chặn bởi tường.
* **Mục tiêu:** Tìm lộ trình ngắn nhất từ điểm bắt đầu (**Start**) đến điểm đích (**Goal**).

## 2. Cơ sở lý thuyết thuật toán A*
**A* (A-Star)** là giải thuật tìm kiếm có thông tin (Informed Search), kết hợp ưu điểm của *Dijkstra* (tìm đường ngắn nhất thực tế) và *Greedy Best-First Search* (hướng đích nhanh nhất).

### 2.1. Hàm đánh giá (Evaluation Function)
A* lựa chọn nút tiếp theo để duyệt dựa trên hàm chi phí:
$$f(n) = g(n) + h(n)$$

Trong đó:
* $g(n)$: **Chi phí thực tế** từ điểm bắt đầu ($Start$) đến nút hiện tại $n$. Trong mê cung lưới, mỗi bước đi thường có chi phí là 1.
* $h(n)$: **Chi phí ước lượng (Heuristic)** từ nút hiện tại $n$ đến đích ($Goal$).
* $f(n)$: Tổng chi phí ước lượng của đường đi qua nút $n$.

### 2.2. Hàm Heuristic trong không gian lưới
Để đảm bảo A* tìm được đường đi tối ưu (Optimal), hàm $h(n)$ phải là hàm **chấp nhận được (Admissible)**, nghĩa là không bao giờ đánh giá cao hơn chi phí thực tế.
Với bài toán mê cung chỉ cho phép đi 4 hướng (không đi chéo), ta sử dụng **Khoảng cách Manhattan**:

$$h(n) = |x_{current} - x_{goal}| + |y_{current} - y_{goal}|$$

### 2.3. Các bước thực hiện
1.  **Khởi tạo:**
    * `Open List` (Hàng đợi ưu tiên): Chứa $Start$ với $f(Start) = h(Start)$.
    * `Closed List` (Tập đã duyệt): Rỗng.
2.  **Lặp:** Khi `Open List` không rỗng:
    * Lấy nút $n$ có giá trị $f(n)$ nhỏ nhất từ `Open List`.
    * Nếu $n$ là $Goal$: **Dừng và truy vết đường đi.**
    * Thêm $n$ vào `Closed List`.
    * Xét các nút lân cận $m$ của $n$:
        * Nếu $m$ là tường hoặc đã trong `Closed List`: Bỏ qua.
        * Tính $g(m) = g(n) + 1$.
        * Nếu $m$ chưa trong `Open List` hoặc $g(m)$ mới nhỏ hơn $g(m)$ cũ:
            * Cập nhật $g(m)$, $h(m)$, $f(m)$.
            * Đặt cha của $m$ là $n$ (để truy vết).
            * Thêm $m$ vào `Open List`.
3.  **Kết thúc:** Nếu `Open List` rỗng mà chưa tới đích $\rightarrow$ Không có đường đi.