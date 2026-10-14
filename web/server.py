import os
import json
import http.server
import socketserver
import webbrowser
from urllib.parse import parse_qs, urlparse

from core.board import Board
from core.problem import BloxorzProblem
from solvers.bfs import BFSSolver
from solvers.dfs import DFSSolver
from solvers.ucs import UCSSolver
from solvers.astar import AStarSolver

PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
STAGES_DIR = os.path.join(PROJECT_DIR, "stages")


class BloxorzServerHandler(http.server.SimpleHTTPRequestHandler):
    """
    HTTP Request Handler phục vụ cả static files (HTML, CSS, JS)
    lẫn REST API trả về kết quả chạy các thuật toán tìm kiếm.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/api/stages":
            # API: Lấy danh sách các màn chơi có sẵn trong thư mục stages/
            stages = []
            if os.path.exists(STAGES_DIR):
                for f in sorted(os.listdir(STAGES_DIR)):
                    if f.endswith(".json"):
                        stages.append(f)
            self._send_json({"stages": stages})
            return

        elif parsed.path == "/api/solve":
            # API: /api/solve?stage=stage_01.json&algo=BFS
            params = parse_qs(parsed.query)
            stage_file = params.get("stage", ["stage_01.json"])[0]
            algo_name = params.get("algo", ["BFS"])[0].upper()

            stage_path = os.path.join(STAGES_DIR, stage_file)
            if not os.path.exists(stage_path):
                self._send_json({"error": f"Stage {stage_file} not found"}, status=404)
                return

            try:
                board = Board.from_json(stage_path)
                problem = BloxorzProblem(board)

                # Khởi tạo solver tương ứng
                if algo_name == "BFS":
                    solver = BFSSolver()
                elif algo_name == "DFS":
                    solver = DFSSolver()
                elif algo_name == "UCS":
                    solver = UCSSolver()
                elif algo_name == "ASTAR" or algo_name == "A*":
                    solver = AStarSolver()
                else:
                    self._send_json({"error": f"Unknown algorithm: {algo_name}"}, status=400)
                    return

                result = solver.solve(problem)
                self._send_json({
                    "stage": stage_file,
                    "algorithm": solver.name,
                    "status": result.status,
                    "path": result.path,
                    "steps": result.solution_length,
                    "expanded_nodes": result.expanded_nodes,
                    "time_ms": result.search_time_ms,
                    "memory_kb": result.memory_peak_kb,
                    "cost": result.cost
                })
            except NotImplementedError as e:
                self._send_json({
                    "status": "NOT_IMPLEMENTED",
                    "message": str(e)
                })
            except Exception as e:
                self._send_json({"error": str(e)}, status=500)
            return

        # Phục vụ static files (index.html, v.v.)
        super().do_GET()

    def _send_json(self, data: dict, status: int = 200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)


def run():
    with socketserver.TCPServer(("", PORT), BloxorzServerHandler) as httpd:
        url = f"http://localhost:{PORT}/index.html"
        print("=" * 60)
        print(f"🚀 Bloxorz 3D Web Server running at: {url}")
        print("💡 Nhấn Ctrl+C để dừng server.")
        print("=" * 60)
        webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nĐã dừng server.")


if __name__ == "__main__":
    run()
