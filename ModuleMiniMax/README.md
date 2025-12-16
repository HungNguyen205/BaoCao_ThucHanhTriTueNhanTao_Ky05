## 1. Thuật toán Minimax

### 1.1. Nguyên lý hoạt động

Minimax là giải thuật đệ quy cơ bản nhất được sử dụng trong lý thuyết trò chơi và trí tuệ nhân tạo để xác định nước đi tốt nhất cho một người chơi, với giả định rằng đối thủ cũng đang chơi một cách tối ưu để bảo vệ lợi ích của họ.

Thuật toán dựa trên tư duy chiến lược "nhìn xa trông rộng": để quyết định nước đi hiện tại, ta phải dự đoán các phản ứng của đối thủ, rồi lại dự đoán phản ứng của mình trước nước đi đó của đối thủ, cứ thế tiếp diễn cho đến khi ván cờ kết thúc hoặc đạt đến giới hạn tính toán.

Trong mô hình này, hai người chơi được gán tên là MAX và MIN:

* **MAX (Máy tính):** Đại diện cho người chơi đang cần tìm nước đi. Mục tiêu của MAX là chọn hành động dẫn đến trạng thái có giá trị hàm lợi ích cao nhất (Maximize).
* **MIN (Đối thủ):** Đại diện cho đối phương. Mục tiêu của MIN là chọn hành động dẫn đến trạng thái có giá trị hàm lợi ích thấp nhất (Minimize), nhằm dìm điểm số của MAX xuống mức thấp nhất có thể.

### 1.2. Công thức toán học



Giá trị Minimax của một trạng thái (node) $s$ bất kỳ được xác định bằng công thức đệ quy sau:

$$Minimax(s) =
\begin{cases}
Utility(s) & \text{nếu } s \text{ là trạng thái kết thúc (Terminal state)} \\
\max_{a \in Actions(s)} Minimax(Result(s, a)) & \text{nếu } Player(s) = MAX \\
\min_{a \in Actions(s)} Minimax(Result(s, a)) & \text{nếu } Player(s) = MIN
\end{cases}$$

**Trong đó:**

* Nếu $s$ là lá, giá trị Minimax chính là điểm số của trạng thái đó.
* Nếu đến lượt MAX, giá trị của $s$ bằng giá trị lớn nhất trong số các giá trị của các nút con (MAX sẽ chọn đi nước tốt nhất cho mình).
* Nếu đến lượt MIN, giá trị của $s$ bằng giá trị nhỏ nhất trong số các giá trị của các nút con (MIN sẽ chọn đi nước tệ nhất cho MAX).

### 1.3. Quy trình thực hiện

Thuật toán Minimax hoạt động theo cơ chế Tìm kiếm theo chiều sâu (Depth-First Search - DFS) và Lan truyền ngược (Back-propagation). Quy trình cụ thể gồm 4 bước:

1.  **Sinh cây trò chơi:** Từ trạng thái hiện tại, thuật toán sinh ra các trạng thái con cho đến độ sâu quy định hoặc đến trạng thái kết thúc.
2.  **Đánh giá tại lá:** Tại các nút lá (leaf nodes), áp dụng hàm lợi ích (hoặc hàm Heuristic) để tính điểm số cho trạng thái đó.
3.  **Lan truyền ngược (Backtracking):** Giá trị từ các nút lá được đẩy ngược lên các nút cha theo quy tắc:
    * Tại tầng của MIN, nút cha nhận giá trị nhỏ nhất của các con.
    * Tại tầng của MAX, nút cha nhận giá trị lớn nhất của các con.
4.  **Ra quyết định:** Khi giá trị được lan truyền ngược về đến nút gốc (Root), MAX sẽ chọn nước đi dẫn đến nút con có giá trị cao nhất.