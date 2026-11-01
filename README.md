# Bloxorz Solver

Đồ án 1 — CSC14003, Nhập môn Trí tuệ nhân tạo. Ứng dụng gồm mô hình trò chơi và các
bộ giải Python, máy chủ HTTP cục bộ và giao diện Bloxorz 3D trên trình duyệt.

## Thành viên

| MSSV | Họ và tên | Phần phụ trách | Hoàn thành |
|---|---|---|---|
| 24120282 | Nguyễn Quốc Đạt | Mô hình, giao diện, tích hợp, thực nghiệm | 100% |
| 24120486 | Trần Nhật Trường | UCS và hàm chi phí | 100% |
| 24120215 | Nguyễn Ngọc Phúc | BFS | 100% |
| 24120040 | Dương Hoài Đức | DFS/IDS | 100% |
| 24120218 | Nguyễn Đức Quân | A* và heuristic | 100% |

## Chạy ứng dụng

Đã kiểm tra với **Python 3.12**. Chạy tại thư mục chứa `main.py`.

```powershell
python main.py
```

Trình duyệt mở tại `http://localhost:8080/index.html`. Ứng dụng dùng thư viện chuẩn
Python; `requirements.txt` không có gói bắt buộc. Three.js và giấy phép được đóng
gói trong `web/static/vendor/`, không cần tải CDN hoặc dùng Node.js/npm.

Để chọn cổng và không tự mở trình duyệt:

```powershell
python -m web.server --host 127.0.0.1 --port 8081 --no-browser
```

Sau đó mở `http://localhost:8081/index.html`. Dùng `Ctrl+C` để dừng máy chủ.

## Điều khiển

- Mũi tên hoặc WASD: lăn khối.
- R hoặc nút Đặt lại màn: bắt đầu lại màn hiện tại.
- Space: đổi khối đang điều khiển sau khi đã tách.
- Ô tách chỉ kích hoạt khi khối đứng trên công tắc. Hai cube ghép lại khi nằm kề nhau.
- Chọn màn, đổi góc nhìn hoặc chạy BFS, DFS/IDS, UCS, A* bằng các nút trên giao diện.

## Chạy bộ giải và thực nghiệm

```powershell
python main.py --solve --stage stages/stage_01.json --algo BFS
python main.py --solve --stage stages/stage_13.json --algo ASTAR
python main.py --solve --stage stages/stage_18.json --algo IDS
python main.py --benchmark
```

Các tên thuật toán được hỗ trợ: `BFS`, `DFS`, `IDS`, `UCS`, `ASTAR` và `A*`.
Lệnh benchmark chạy BFS, IDS, UCS, A* trên 20 màn và tạo `benchmark_results.csv`.

UCS/A* dùng chi phí `risk_v1`: mỗi lần di chuyển tính `1 + 2F + 0.5B`, với F, B là
số ô yếu và ô cầu trong dấu chân cuối bước; đổi cube tính `0.25`. Báo cáo phát lại
đường đi của mọi bộ giải để so sánh theo cùng hàm chi phí.

Số hành động của lời giải bao gồm SWITCH; số bước chơi tay chỉ đếm di chuyển.
Bộ nhớ được đo bằng `tracemalloc`, quy đổi sang KiB; giao diện hiện ghi nhãn KB.

## Tổ chức mã nguồn

```text
main.py             Điểm chạy GUI, CLI và benchmark
benchmark.py        Đo các bộ giải và xuất CSV
core/               Trạng thái, bàn cờ, luật chuyển và hàm chi phí
solvers/            BFS, DFS/IDS, UCS, A* và lớp kết quả chung
stages/             20 màn JSON cùng script sinh/định dạng
web/                Máy chủ Python, HTML, CSS, JavaScript và kiểm thử
requirements.txt    Phụ thuộc chạy ứng dụng
```

Các ô JSON dùng mã: `0` khoảng trống, `1` sàn, `2` ô yếu, `3` cầu, `4` công tắc
mềm, `5` công tắc nặng, `6` công tắc tách và `9` đích. Màn 13 dùng đích `(6,7)`;
JSON và script sinh đều đã thống nhất tọa độ này.

## Video minh họa

[Video demo Bloxorz 3D](https://youtu.be/p2pHJUaProk).
