# Cấu trúc giao diện Web

Chạy từ thư mục gốc dự án:

```powershell
python main.py
python main.py --web
```

Máy chủ và các solver tiếp tục dùng thư viện chuẩn Python. Frontend dùng ES modules
trực tiếp trong trình duyệt; không cần Node.js, npm hoặc bước đóng gói.

## Phía Python

| Tệp | Trách nhiệm |
|---|---|
| `server.py` | Điểm khởi chạy, mở trình duyệt, tham số dòng lệnh; giữ import `BloxorzServerHandler` tương thích. |
| `application.py` | Tạo máy chủ và lắp ghép các thành phần; cho phép truyền cổng/thư mục khi kiểm thử. |
| `config.py` | Đường dẫn dự án, thư mục màn và cổng mặc định. |
| `handler.py` | Định tuyến HTTP, mã trạng thái, JSON và tài nguyên tĩnh. |
| `stages.py` | Đọc tệp JSON, giới hạn đường dẫn trong thư mục màn và tạo metadata cho bộ chọn màn. |
| `solver_service.py` | Chọn BFS/DFS/IDS/UCS/A*, gọi mô hình Python và chuyển kết quả thành dữ liệu API. |

`ThreadingHTTPServer` xử lý đồng thời các yêu cầu tài nguyên của trình duyệt. Các lượt
gọi solver được khóa tuần tự vì `tracemalloc` có phạm vi toàn tiến trình. Việc nhập
các mô-đun không tự mở trình duyệt hoặc chiếm cổng.

Các cách chạy trực tiếp vẫn được hỗ trợ:

```powershell
python web/server.py
python -m web.server
python -m web.server --host 127.0.0.1 --port 8081 --no-browser
```

## Phía trình duyệt

```text
web/
├── index.html                 # Cấu trúc HTML và điểm nạp tài nguyên
└── static/
    ├── css/
    │   ├── base.css           # Biến màu, nền và quy tắc chung
    │   ├── start-screen.css   # Màn hình bắt đầu
    │   ├── stages.css         # Hộp thoại và thẻ màn chơi
    │   ├── hud.css            # Bảng điều khiển và nút thao tác
    │   └── legend.css         # Chú giải, biểu tượng và radar
    └── js/
        ├── app.js             # Lắp ghép các thành phần, khởi tạo một ứng dụng
        ├── state.js           # Tạo đối tượng trạng thái trò chơi
        ├── config.js          # Hằng số kích thước, camera và thời gian lăn
        ├── api.js             # Giao tiếp HTTP/JSON
        ├── audio.js           # Âm thanh Web Audio
        ├── game/              # Di chuyển, cầu/công tắc, tách/ghép, kiểm tra trạng thái
        ├── render/            # Scene, vật liệu, ô sàn, khối và vòng lặp vẽ
        └── ui/                # HUD, radar, camera, chọn màn, solver và sự kiện
```

`state` chứa vị trí, tư thế, cấu hình màn và trạng thái cầu; `view` giữ các đối tượng
Three.js. Các controller nhận phụ thuộc qua tham số, tránh import vòng và tránh ghi
biến ứng dụng lên `window`. `app.js` xuất `app` để phục vụ kiểm tra hoặc quan sát từ
DevTools; có thể chờ `app.ready` để biết màn đầu đã nạp xong.

HTML dùng `data-action`, `data-algorithm`, `data-camera`; sự kiện được nối tại
`ui/controls.js`. Khi bổ sung một nút, thêm thuộc tính tương ứng và ánh xạ hành động
tại đây. Các kiểu trình bày nằm trong CSS, thay cho `style` hoặc `onclick` nội tuyến.

## API

Các địa chỉ và trường kết quả được giữ nguyên:

```text
GET /api/stages
GET /stages/stage_01.json
GET /api/solve?stage=stage_01.json&algo=BFS
```

Thuật toán nhận `BFS`, `DFS`, `IDS`, `UCS`, `ASTAR` hoặc `A*`. Kết quả gồm `status`,
`path`, `steps`, `expanded_nodes`, `time_ms`, `memory_kb`, `cost` cùng thông tin màn
và thuật toán. Các thuật toán tìm kiếm vẫn nằm trong `solvers/`.

## Kiểm tra

Kiểm thử Python không cần thư viện bổ sung:

```powershell
python -B -m unittest discover -s web/tests -v
```

Kiểm tra giao diện thật bằng Chromium là tùy chọn, cần Playwright và trình duyệt đã cài:

```powershell
python -B -m web.tests.browser_smoke
```

Nếu đã có bản sao đúng tệp Three.js r128 của CDN, có thể kiểm tra ngoại tuyến:

```powershell
python -B -m web.tests.browser_smoke --three-js <duong-dan-three.r128.min.js>
```

Script kiểm tra thao tác tay, chọn màn, camera, năm nút solver và phát lại A* trên
20 màn. Kết quả nằm trong `scratch/web_refactor/browser/`. Màn 13 giữ kỳ vọng hiện
có là `PLAYING` tại đích Python, do dữ liệu `goal` chưa trùng ô 9; quá trình tách
mô-đun không thay đổi dữ liệu màn hoặc luật chơi.
