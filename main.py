"""
=============================================================================
BLOXORZ SOLVER - MAIN ENTRY POINT
CSC14003 - Nhập môn Trí tuệ Nhân tạo - Project 1
=============================================================================
"""
import argparse
import sys
import os

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from core.board import Board
from core.problem import BloxorzProblem
from solvers.bfs import BFSSolver
from solvers.dfs import DFSSolver
from solvers.ucs import UCSSolver
from solvers.astar import AStarSolver


def run_cli_solve(stage_file: str, algo_name: str):
    """Chạy giải thuật toán trên console."""
    if not os.path.exists(stage_file):
        print(f"❌ Lỗi: File màn chơi {stage_file} không tồn tại!")
        return

    print(f"\n🎮 Đang đọc bàn cờ từ: {stage_file}")
    board = Board.from_json(stage_file)
    problem = BloxorzProblem(board)

    solvers = {
        "BFS": BFSSolver,
        "DFS": DFSSolver,
        "UCS": UCSSolver,
        "ASTAR": AStarSolver,
        "A*": AStarSolver
    }

    algo_key = algo_name.upper()
    if algo_key not in solvers:
        print(f"❌ Thuật toán không hợp lệ: {algo_name}. Hãy chọn: BFS, DFS, UCS, ASTAR.")
        return

    solver = solvers[algo_key]()
    print(f"⚡ Đang thực thi thuật toán: {solver.name}...")

    try:
        result = solver.solve(problem)
        print("\n" + "=" * 50)
        print(f"📊 KẾT QUẢ TÌM KIẾM ({solver.name})")
        print("=" * 50)
        print(f"Trạng thái      : {result.status}")
        print(f"Độ dài đường đi : {result.solution_length} bước")
        print(f"Số node mở rộng : {result.expanded_nodes}")
        print(f"Thời gian chạy  : {result.search_time_ms:.2f} ms")
        print(f"Bộ nhớ tiêu thụ : {result.memory_peak_kb:.2f} KB")
        if result.cost > 0:
            print(f"Tổng chi phí    : {result.cost:.2f}")
        print("\nCác bước đi chi tiết:")
        print(" -> ".join(result.path) if result.path else "(Không có đường đi)")
        print("=" * 50)
    except NotImplementedError as e:
        print(f"\n⚠️  {e}")


def main():
    parser = argparse.ArgumentParser(description="Bloxorz AI Solver & 3D Web Studio")
    parser.add_argument("--web", action="store_true", help="Khởi động giao diện Web 3D Studio")
    parser.add_argument("--solve", action="store_true", help="Chạy chế độ tìm kiếm giải bằng CLI")
    parser.add_argument("--stage", type=str, default="stages/stage_01.json", help="Đường dẫn file stage JSON")
    parser.add_argument("--algo", type=str, default="BFS", help="Thuật toán (BFS, DFS, UCS, ASTAR)")
    parser.add_argument("--benchmark", action="store_true", help="Chạy toàn bộ benchmark trên các màn chơi")

    args = parser.parse_args()

    if args.benchmark:
        from benchmark import run_benchmark
        run_benchmark()
    elif args.solve:
        run_cli_solve(args.stage, args.algo)
    else:
        # Mặc định khởi động Web Studio
        from web.server import run as run_web_server
        run_web_server()


if __name__ == "__main__":
    main()
