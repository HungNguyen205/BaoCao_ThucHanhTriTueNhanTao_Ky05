# MODULE 3: TÔ MÀU ĐỒ THỊ (GRAPH COLORING)
## PHẦN 1: TỔNG QUAN (INTRODUCTION)

### 1.1. Đặt vấn đề

Trong khoa học máy tính và toán học ứng dụng, việc tìm kiếm lời giải tối ưu cho các hệ thống phức tạp luôn là một thách thức lớn. Một lớp bài toán quan trọng trong số đó là **Bài toán thỏa mãn ràng buộc (Constraint Satisfaction Problems - CSP)**. Khác với các bài toán tìm kiếm thông thường, CSP yêu cầu lời giải phải tuân thủ nghiêm ngặt một tập hợp các quy tắc định trước.

**Bài toán Tô màu đồ thị (Graph Coloring)** là một đại diện kinh điển của CSP. Việc giải quyết bài toán này có ý nghĩa to lớn trong thực tiễn, từ việc lập lịch biểu, phân chia tần số vô tuyến đến tối ưu hóa thanh ghi trong máy tính. Tuy nhiên, việc tìm ra số màu tối thiểu (sắc số) cho một đồ thị tổng quát thuộc lớp bài toán NP-Hard, đòi hỏi các phương pháp tiếp cận thông minh hơn là vét cạn.

### 1.2. Mục tiêu báo cáo

Báo cáo này hướng tới các mục tiêu cụ thể sau:

1.  Hệ thống hóa cơ sở lý thuyết về CSP và bài toán tô màu đồ thị.
2.  Phân tích thuật toán tô màu tối ưu sử dụng phương pháp heuristic dựa trên bậc của đỉnh (Degree-based Heuristic).
3.  Đưa ra thiết kế chi tiết để xây dựng chương trình giải quyết bài toán, bao gồm định nghĩa dữ liệu và giải thuật.

## PHẦN 2: CƠ SỞ LÝ THUYẾT (THEORETICAL BACKGROUND)

### 2.1. Lý thuyết về Bài toán Thỏa mãn ràng buộc (CSP)

**Định nghĩa:** Một bài toán CSP được xác định bởi bộ ba $(X, D, C)$:

  * **$X = \{X_1, X_2, \dots, X_n\}$**: Là tập hợp hữu hạn các biến cần tìm giá trị.
  * **$D = \{D_1, D_2, \dots, D_n\}$**: Là tập hợp các miền giá trị, trong đó mỗi biến $X_i$ nhận giá trị thuộc $D_i$.
  * **$C$**: Là tập hợp hữu hạn các ràng buộc. Ràng buộc là một quan hệ trên một tập con các biến, giới hạn các tổ hợp giá trị mà các biến đó có thể nhận đồng thời.

**Ràng buộc có thể biểu diễn bằng:**

  * Một biểu thức toán học/logic (Ví dụ: $X_i \neq X_j$).
  * Một bảng liệt kê (Table enumeration) các phép gán giá trị hợp lệ.

**Lời giải:** Một lời giải thỏa mãn ràng buộc là một phép gán đầy đủ giá trị cho tất cả các biến trong $X$ sao cho không vi phạm bất kỳ ràng buộc nào trong $C$.

### 2.2. Bài toán Tô màu đồ thị (Graph Coloring)

**Phát biểu bài toán:**
Cho một đồ thị vô hướng $G = (V, E)$, trong đó $V$ là tập đỉnh và $E$ là tập cạnh.

  * **Biến:** Mỗi đỉnh $v \in V$ là một biến.
  * **Miền giá trị:** Tập hợp các màu $K = \{1, 2, \dots, m\}$.
  * **Ràng buộc:** Hai đỉnh kề nhau không được tô cùng màu.
    $$\forall (u, v) \in E \Rightarrow Color(u) \neq Color(v)$$

**Mục tiêu tối ưu:** Tìm giá trị $m$ nhỏ nhất (gọi là Sắc số - Chromatic Number, ký hiệu $\chi(G)$) sao cho tồn tại phép gán màu hợp lệ.

**Nhận định lý thuyết:**
Do tính chất NP-Hard, thời gian tính toán lời giải chính xác tăng theo hàm mũ đối với số đỉnh. Do đó, các thuật toán Heuristic bằng phương pháp dựa trên bậc đỉnh như tô màu đồ thịthường được ưu tiên sử dụng để tìm lời giải gần tối ưu hoặc tối ưu trong thời gian đa thức.

## PHẦN 3: THUẬT TOÁN GIẢI QUYẾT (ALGORITHM)

### 3.1. Nguyên lý hoạt động

Thuật toán dựa trên nhận định: *Đỉnh có bậc càng cao thì càng khó tô màu do bị ràng buộc bởi nhiều láng giềng. Cần ưu tiên giải quyết đỉnh này sớm nhất.* Sau khi tô màu xong, đỉnh đó coi như "đã được giải quyết", do đó ta có thể "loại bỏ" nó khỏi đồ thị xét duyệt bằng cách hạ bậc các đỉnh lân cận.

### 3.2. Các bước của thuật toán

Quy trình lặp lại cho đến khi tất cả các đỉnh đều được tô màu:

  * **Bước 1: Lựa chọn đỉnh (Selection)**

      * Trong số các đỉnh chưa được tô màu, chọn đỉnh $v$ có **bậc hiện tại lớn nhất**.
      * Nếu có nhiều đỉnh có cùng bậc lớn nhất, chọn đỉnh có chỉ số nhỏ nhất (hoặc ngẫu nhiên).
      * Gán cho đỉnh $v$ một màu $i$ nhỏ nhất có thể trong tập màu, sao cho màu $i$ không trùng với màu của bất kỳ đỉnh lân cận nào đã được tô trước đó (không nằm trong danh sách cấm).

  * **Bước 2: Hạ bậc (Degree Reduction)**

      * Đánh dấu đỉnh $v$ là **Đã tô màu** (Gán bậc của $v = 0$ hoặc loại khỏi danh sách xét).
      * Với mọi đỉnh $u$ kề với $v$ và chưa được tô màu: Thực hiện giảm bậc của $u$ đi 1 ($Degree[u] := Degree[u] - 1$).
      * *Ý nghĩa:* Việc giảm bậc phản ánh rằng đỉnh $u$ giờ đây có ít hơn một "láng giềng chưa được giải quyết", thay đổi độ ưu tiên của $u$ trong các bước lặp sau.

  * **Bước 3: Lan truyền ràng buộc (Constraint Propagation)**

      * Cập nhật thông tin cho các đỉnh lân cận: Đánh dấu màu $i$ (màu vừa tô cho $v$) là "Cấm" đối với các đỉnh $u$ kề $v$.
      * Khi đến lượt tô màu đỉnh $u$, thuật toán sẽ bỏ qua các màu bị cấm này.