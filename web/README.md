# Cấu trúc giao diện Web

Chạy từ thư mục gốc dự án:

```powershell
python main.py
python main.py --web
```

Máy chủ và các solver tiếp tục dùng thư viện chuẩn Python. Frontend dùng ES modules
trực tiếp trong trình duyệt; không cần Node.js, npm hoặc bước đóng gói.

Three.js r128 được phục vụ từ `static/vendor/`; giao diện dùng phông chữ hệ thống.
Ứng dụng không cần kết nối CDN hoặc Google Fonts khi chạy.

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
    │   ├── legend.css         # Chú giải, biểu tượng và radar
    │   └── completion.css     # Hộp thoại hoàn thành
    ├── images/               # Hình bàn cờ ở màn hình bắt đầu
    ├── vendor/               # Three.js r128 và giấy phép MIT
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
Three.js. Các controller nhận phụ thuộc qua tham số, tránh import vòng. `app.js` xuất `app` và gắn `window.app` để phục vụ quan sát từ DevTools; có thể chờ `app.ready` để biết màn đầu đã nạp xong.

HTML dùng `data-action`, `data-algorithm`, `data-camera`; sự kiện được nối tại
`ui/controls.js`. Khi bổ sung một nút, thêm thuộc tính tương ứng và ánh xạ hành động
tại đây. Các kiểu trình bày nằm trong CSS, thay cho `style` hoặc `onclick` nội tuyến.

`ui/viewport.js` theo dõi kích thước vùng chơi bằng `ResizeObserver`, cập nhật độ
phân giải canvas và tỷ lệ camera. Camera căn theo các ô có sàn và chừa chỗ cho
khối đứng. Bảng điều khiển nằm bên phải trên máy tính, chuyển xuống dưới bàn cờ
khi chiều rộng cửa sổ không quá 900 px.

`render/goal.js` dựng khung và lòng hố đích. `render/dispose.js` giải phóng hình
học và vật liệu riêng khi đổi màn, giữ lại các vật liệu dùng chung. Vùng đổ bóng
được căn theo kích thước bàn cờ; texture dùng lọc anisotropic khi thiết bị hỗ trợ.
Ô đích dùng khung kim loại vát cạnh, đèn xanh ngọc và các dải sáng theo chiều sâu.
Dải sáng nhịp chậm sử dụng cùng đồng hồ với cảnh 3D và đứng yên khi bật giảm chuyển động.

`ui/stage-preview.js` dựng hình xem trước từ dữ liệu màn, lưu kết quả trong bộ nhớ
và tải tối đa ba màn cùng lúc. Hộp chọn màn hỗ trợ tìm theo số, tên và cơ chế;
tìm kiếm tiếng Việt không phân biệt dấu.

`ui/completion.js` hiển thị lời chúc mừng sau chuyển động vào đích, cùng số bước,
chơi lại, sang màn kế tiếp hoặc mở danh sách màn. Màn cuối không có nút chơi tiếp.
Mỗi lần đặt lại màn tăng `state.runId` để bỏ qua chuyển động, yêu cầu giải và các
bước phát lại còn chờ từ lượt trước.

Ô tách chỉ kích hoạt khi khối đứng trên công tắc và có hai vị trí đích trong dữ
liệu màn. Space chỉ đổi khối đang điều khiển sau khi đã tách. Một lượt di chuyển
áp dụng công tắc và trạng thái cầu trước khi kiểm tra nâng đỡ, theo mô hình Python.
Dịch chuyển tới hai ô đích không kích hoạt thêm công tắc ở đó; sau khi ghép, xét
lại công tắc trên dấu chân mới. Các hành vi cầu hỗ trợ `toggle`, `perm_open`,
`perm_close` và bí danh `permanent` cho đặt mở.

`render/victory.js` tạo vòng sáng tại ô đích. `ui/confetti.js` vẽ pháo giấy bằng
Canvas 2D trong tối đa 3,2 giây. Hiệu ứng dừng và giải phóng tài nguyên khi đóng
hộp thoại, đặt lại màn hoặc ẩn tab; không chạy khi bật giảm chuyển động.

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
