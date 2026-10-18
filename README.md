# 🎮 Bloxorz AI Solver & 3D Web Studio

> **Đồ án 1: Trò chơi Bloxorz và Thuật toán Tìm kiếm Không gian Trạng thái**  
> **Môn học**: CSC14003 - Nhập môn Trí tuệ Nhân tạo  
> **Khoa Công nghệ Thông tin - Trường ĐH Khoa học Tự nhiên, ĐHQG-HCM**

---

## 👥 1. Danh sách Thành viên & Phân công Nhiệm vụ

Dự án được xây dựng theo mô hình phân tách module độc lập (Modular Architecture). Chi tiết tiêu chí đánh giá đóng góp được trình bày trong [TASK_ASSIGNMENT.md](file:///c:/Users/Mr.Dat09/Documents/python/Bloxorz-Solver/TASK_ASSIGNMENT.md).

| Họ và Tên | Vai trò | Phụ trách kỹ thuật | File đảm nhiệm |
| :--- | :--- | :--- | :--- |
| **Trưởng nhóm** | Lead / Architecture | Xây dựng cấu trúc State, Problem, Map Loader, 3D Web GUI, Benchmark | `core/*`, `web/*`, `main.py`, `benchmark.py` |
| **Phúc** | Solver Developer | Thuật toán tìm kiếm theo chiều rộng (**BFS**) | `solvers/bfs.py` |
| **Đức** | Solver Developer | Thuật toán tìm kiếm theo chiều sâu (**DFS / IDS**) | `solvers/dfs.py` |
| **Trường** | Solver Developer | Thuật toán tìm kiếm chi phí đồng nhất (**UCS**) & Hàm Cost không đồng nhất | `solvers/ucs.py` |
| **Quân** | Solver Developer | Thuật toán tìm kiếm **A\*** & Thiết kế hàm Heuristic $h(n)$ (Admissible & Consistent) | `solvers/astar.py` |

---

## 📁 2. Cấu trúc Dự án

```text
Bloxorz-Solver/
├── core/                       # Lõi Game Engine & Hình thức hóa bài toán
│   ├── __init__.py
│   ├── state.py                # Định nghĩa Orientation, BlockState, GameState (bất biến, hashable)
│   ├── board.py                # Mô hình hóa bàn cờ, gạch vỡ, công tắc, cầu nối, đọc file JSON
│   └── problem.py              # Hình thức hóa Search Problem (actions, transitions, goal test, cost)
│
├── solvers/                    # Module chứa các thuật toán tìm kiếm do thành viên code tay
│   ├── __init__.py
│   ├── base.py                 # Abstract BaseSolver & SearchResult (đo Time, RAM, Nodes, Steps)
│   ├── bfs.py                  # [Phúc] Cài đặt Breadth-First Search
│   ├── dfs.py                  # [Đức] Cài đặt Depth-First Search / Iterative Deepening Search
│   ├── ucs.py                  # [Trường] Cài đặt Uniform-Cost Search & Non-uniform Cost Function
│   └── astar.py                # [Quân] Cài đặt A* Search & Admissible Heuristic
│
├── stages/                     # Bộ dữ liệu các màn chơi định dạng JSON
│   ├── stage_01.json           # Màn chơi cơ bản (gốc)
│   └── stage_02.json           # Màn chơi có gạch vỡ (Fragile)
│
├── web/                        # Giao diện đồ họa Web 3D (Three.js Studio)
│   ├── index.html              # 3D WebGL Canvas, Procedural PBR Shading, Web Audio, Glassmorphism HUD
│   └── server.py               # Local server kết nối REST API giữa trình duyệt và Python Solvers
│
├── .gitignore                  # Bỏ qua bytecode, môi trường ảo và file tạm
├── benchmark.py                # Script chạy tự động đo đạc 4 thuật toán và xuất ra benchmark_results.csv
├── main.py                     # Entry point chính của dự án (CLI / Web / Benchmark)
├── README.md                   # Hướng dẫn chi tiết dự án
├── requirements.txt            # Danh sách thư viện phụ trợ
└── TASK_ASSIGNMENT.md          # Bảng phân công công việc chi tiết cho từng thành viên
```

---

## 🚀 3. Hướng dẫn Cài đặt & Chạy chương trình

### 3.1. Cài đặt môi trường
Dự án được tối ưu hóa để sử dụng **thư viện chuẩn của Python** (Standard Library), không phụ thuộc vào các thư viện bên ngoài phức tạp, đảm bảo chạy ổn định trên mọi máy chấm của Giảng viên và Trợ giảng.

```bash
# Clone repository về máy
git clone <repository_url>
cd Bloxorz-Solver

# (Khuyến nghị) Tạo môi trường ảo
python -m venv venv
venv\Scripts\activate      # Trên Windows
# source venv/bin/activate  # Trên Linux / macOS

# Cài đặt requirements (nếu có)
pip install -r requirements.txt
```

---

### 3.2. Chế độ 1: Giao diện Web 3D Studio (Mặc định)
Khởi động giao diện 3D trực quan, chơi tay và cho phép gọi các thuật toán tự động diễn hoạt bước giải:

```bash
python main.py
# hoặc
python main.py --web
```
Trình duyệt sẽ tự động mở trang: `http://localhost:8080/index.html`.

---

### 3.3. Chế độ 2: Chạy Solver qua Dòng lệnh (CLI Mode)
Cho phép chạy từng thuật toán trên một màn chơi cụ thể và in chi tiết các thông số đo đạc:

```bash
# Chạy giải thuật toán BFS trên màn chơi 1
python main.py --solve --stage stages/stage_01.json --algo BFS

# Chạy giải thuật toán A* trên màn chơi 2
python main.py --solve --stage stages/stage_02.json --algo ASTAR

# Các tùy chọn algo: BFS, DFS, UCS, ASTAR
```

---

### 3.4. Chế độ 3: Chạy Benchmark Thực nghiệm toàn diện
Chạy tự động tất cả 4 thuật toán trên toàn bộ các màn chơi trong thư mục `stages/`, in bảng so sánh hiệu năng lên terminal và xuất file `benchmark_results.csv`:

```bash
python main.py --benchmark
# hoặc
python benchmark.py
```

---

## 🗺️ 4. Định dạng Màn chơi (Stage JSON Format)

Mỗi màn chơi được cấu hình độc lập trong file JSON để dễ dàng mở rộng và chia sẻ:

```json
{
  "name": "Stage 01 - The Beginning",
  "difficulty": "Easy",
  "start": [1, 1],
  "goal": [4, 7],
  "grid": [
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, 1, 9, 1, 1],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 0]
  ]
}
```

*Ký hiệu các loại ô (`TileType`):*
- `0`: Vực thẳm (`VOID`) - Rơi xuống là thua.
- `1`: Sàn bình thường (`FLOOR`) - Đi an toàn ở mọi tư thế.
- `2`: Gạch vỡ (`FRAGILE`) - Chỉ chịu được khi khối nằm, đứng lên sẽ vỡ và rơi.
- `3`: Cầu nối (`BRIDGE`) - Trạng thái đi được do công tắc điều khiển.
- `4`: Công tắc mềm (`SOFT_SWITCH`) - Đè lên ở bất kỳ tư thế nào cũng kích hoạt.
- `5`: Công tắc nặng (`HEAVY_SWITCH`) - Chỉ kích hoạt khi khối đứng thẳng lên trên.
- `6`: Công tắc phân tách (`SPLIT_SWITCH`) - Tách khối 1x1x2 thành hai khối đơn 1x1x1.
- `9`: Lỗ đích (`GOAL`) - Chỉ chiến thắng khi khối đứng thẳng vào ô này.

---

## 📊 5. Đo đạc Thực nghiệm (Benchmarking Metrics)

Theo yêu cầu của đề tài, mỗi thuật toán đều được thu thập tự động 4 chỉ số:
1. **Search Time (ms)**: Đo bằng `time.perf_counter()`.
2. **Memory Usage (KB)**: Bộ nhớ RAM đỉnh đo bằng thư viện chuẩn `tracemalloc`.
3. **Expanded Nodes**: Số lượng trạng thái được lấy ra khỏi Frontier để mở rộng.
4. **Solution Length**: Số bước di chuyển trong lời giải tìm được.

---

## 📺 6. Video Demo & Báo cáo
- **Video Demo YouTube**: `[Link YouTube công khai của nhóm sẽ được bổ sung tại đây]`
- **Báo cáo chi tiết**: Đọc file [Report.pdf](Report.pdf) trong thư mục gốc.

## 7. UCS — phần triển khai của Trường

UCS đã được cài trong `solvers/ucs.py`: min-heap, cập nhật best-cost, bỏ entry lỗi thời, phá hòa bằng counter và truy vết bằng parent. Solver tối ưu tổng cost, có thể chọn nhiều bước hơn để giảm exposure. State giữ đầy đủ tư thế, cầu và cube đang điều khiển.

Cost mặc định dùng chung qua `BloxorzProblem.get_step_cost()` và `core/cost.py`, profile **risk_v1**:

- Di chuyển: `1 + 2F + 0.5B`; F/B là số ô fragile/cầu thuộc footprint cuối, gồm cả cube đứng yên khi split.
- Đổi cube (`SWITCH`): `0.25`, không tính lại exposure.
- Void, cầu đóng, đứng trên fragile vẫn là bước bất hợp lệ do engine loại bỏ. Không dùng cost để cho phép bước sai luật.

Đây là mục tiêu công sức/exposure, không phải xác suất rơi đo được. Các trọng số và chứng minh được trình bày trong [đặc tả](SPEC-ucs.md); [kế hoạch](tasks/plan.md), [tiến độ](tasks/todo.md) và [bằng chứng test](tasks/verification.md) đi kèm.

Chạy từ thư mục gốc repo, không cần cài dependency test:

```bash
python -B -m unittest discover -s tests -p 'test_*.py' -v
python -B main.py --solve --stage stages/stage_01.json --algo UCS
python -B main.py --solve --stage tests/fixtures/ucs/weighted_detour.json --algo UCS
python -B main.py --solve --stage tests/fixtures/ucs/split_switch.json --algo UCS
```

Fixture weighted detour: lời giải ít bước nhất có 4 bước nhưng cost 12; UCS chọn 8 bước cost 8. Fixture split buộc đổi cube, mở cầu rồi ghép khối: 9 action, cost 8.75. `solution_length` tính mọi action, gồm cả `SWITCH`.

Benchmark CSV có thêm `cost` và `cost_profile`; cost được tính lại từ path hợp lệ cho mọi solver để cùng mục tiêu so sánh. `NOT_FOUND` có ô cost trống. `expanded_nodes` của UCS đếm pop hợp lệ, kể cả goal, bỏ stale. Peak memory là cấp phát Python do `tracemalloc` trace, không phải RAM/RSS toàn hệ thống; nếu caller đã bật tracer, peak thuộc session tracer của caller.

BFS/DFS/A* hiện vẫn là skeleton của các thành viên khác. Quân cần dùng hook cost chung khi triển khai A* và chứng minh heuristic đối với cost đó; `h=0` là baseline an toàn kể cả teleport. GUI hiện chưa replay đầy đủ split/SWITCH. Stage 02 có goal metadata không khớp tile 9 và topology hiện không giải được; bản UCS không tự sửa stage hay luật engine. Các contract nâng cao còn mở được ghi rõ trong đặc tả và bảng traceability.
