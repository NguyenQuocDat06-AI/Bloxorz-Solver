# BẢNG PHÂN CHIA NHIỆM VỤ ĐỒ ÁN 1: BLOXORZ SOLVER
**Môn học**: CSC14003 - Nhập môn Trí tuệ Nhân tạo  
**Khoa Công nghệ Thông tin - Trường ĐH Khoa học Tự nhiên, ĐHQG-HCM**

---

## 1. THÀNH VIÊN & PHÂN CÔNG CÔNG VIỆC

| Thành viên | Vai trò | Nhiệm vụ chính | File đảm nhiệm | Đánh giá đóng góp dự kiến |
| :--- | :--- | :--- | :--- | :---: |
| **Trưởng nhóm** | Lead / Architecture & GUI | - Xây dựng kiến trúc dự án, mô hình trạng thái (State & Problem Formulation).<br>- Phát triển giao diện Web 3D (Three.js) trực quan hóa game và quá trình chạy solver.<br>- Thiết kế cấu trúc đọc map (JSON format).<br>- Tích hợp hệ thống, viết Benchmark runner & tổng hợp báo cáo. | `core/*`<br>`web/*`<br>`main.py`<br>`benchmark.py` | 100% |
| **Phúc** | Solver Developer | - Nghiên cứu và tự cài đặt thuật toán **BFS (Breadth-First Search)**.<br>- Đảm bảo cơ chế kiểm tra `visited` chống lặp trạng thái.<br>- Thu thập 4 thông số: Search Time, Memory, Expanded Nodes, Solution Length.<br>- Viết phần lý thuyết & phân tích kết quả BFS trong báo cáo. | `solvers/bfs.py` | 100% |
| **Đức** | Solver Developer | - Nghiên cứu và tự cài đặt thuật toán **DFS (Depth-First Search)** hoặc **IDS (Iterative Deepening Search)**.<br>- Xử lý triệt để bài toán tránh chu trình lặp (Cycle avoidance).<br>- Thu thập 4 thông số đo lường hiệu năng của DFS/IDS.<br>- Viết phần lý thuyết & phân tích ưu/nhược điểm DFS trong báo cáo. | `solvers/dfs.py` | 100% |
| **Trường** | Solver Developer | - Nghiên cứu và tự cài đặt thuật toán **UCS (Uniform-Cost Search)**.<br>- Sử dụng cấu trúc hàng đợi ưu tiên (Priority Queue / Min-heap).<br>- **Đặc biệt**: Thiết kế và bảo vệ hàm chi phí không đồng nhất ($c \neq 1$) có ý nghĩa thực tế (giải thích tại sao đi trên ô dễ vỡ tốn nhiều cost hơn, v.v.).<br>- Viết phần lý thuyết & phân tích UCS trong báo cáo. | `solvers/ucs.py` | 100% |
| **Quân** | Solver Developer | - Nghiên cứu và tự cài đặt thuật toán **A\* Search**.<br>- **Đặc biệt**: Thiết kế ít nhất một hàm Heuristic $h(n)$ xấp xỉ khoảng cách tới đích.<br>- Chứng minh tính **Admissible** ($h(n) \le h^*(n)$) và tính **Consistent** tương ứng với hàm cost của UCS.<br>- Viết phần lý thuyết, chứng minh toán học & phân tích A\* trong báo cáo. | `solvers/astar.py` | 100% |

---

## 2. QUY CHUẨN ĐẦU VÀO / ĐẦU RA CHO CÁC SOLVER

Mọi thành viên **bắt buộc** phải kế thừa từ lớp trừu tượng `BaseSolver` trong `solvers/base.py` và triển khai hàm:

```python
def solve(self, problem: BloxorzProblem) -> SearchResult:
    """
    Thực hiện thuật toán tìm kiếm đường đi từ trạng thái bắt đầu đến đích.
    
    Returns:
        SearchResult: Chứa đường đi, thời gian chạy, ram tiêu thụ, số node mở rộng.
    """
```

### Quy chuẩn kết quả trả về (`SearchResult`):
- `status`: `"FOUND"` nếu tìm thấy đích, `"NOT_FOUND"` nếu duyệt hết không gian mà không có đường đi.
- `path`: Danh sách các hành động từ đầu đến đích, ví dụ: `['RIGHT', 'DOWN', 'RIGHT', ...]`
- `solution_length`: Số bước di chuyển (độ dài mảng `path`).
- `expanded_nodes`: Tổng số node được pop ra khỏi Frontier để mở rộng.
- `search_time_ms`: Thời gian thực thi thuật toán (tính bằng mili-giây).
- `memory_peak_kb`: Lượng bộ nhớ RAM đỉnh tiêu thụ (sử dụng module `tracemalloc`).

---

## 3. TIẾN ĐỘ THỰC HIỆN DỰ KIẾN (3 TUẦN)

- **Tuần 1**:
  - Trưởng nhóm hoàn thành `core/` (Game mechanics, State transitions, Board loader) và giao diện Web cơ bản.
  - Các thành viên đọc kỹ luật Bloxorz, nắm chắc không gian trạng thái `(r, c, orientation, bridge_states)`.
- **Tuần 2**:
  - Phúc, Đức, Trường, Quân hoàn thiện code thuật toán trong các file `solvers/`.
  - Chạy thử nghiệm trên các màn chơi mẫu ở thư mục `stages/`.
  - Kiểm tra tính đúng đắn của đường đi và giải quyết các trường hợp bế tắc.
- **Tuần 3**:
  - Chạy `benchmark.py` để lấy số liệu thực nghiệm toàn bộ các màn chơi.
  - Vẽ biểu đồ so sánh thời gian, bộ nhớ, số node mở rộng giữa 4 thuật toán.
  - Viết hoàn thiện file Báo cáo học thuật `Report.pdf`.
  - Quay video demo giao diện và quá trình giải đưa lên YouTube. Đóng gói nộp bài.
