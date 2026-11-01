"""Điểm chạy GUI, CLI và benchmark."""
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
    """Chạy bộ giải từ dòng lệnh."""
    if not os.path.exists(stage_file):
        print(f"Không tìm thấy tệp màn chơi: {stage_file}.")
        return

    print(f"\nMàn chơi: {stage_file}")
    board = Board.from_json(stage_file)
    problem = BloxorzProblem(board)

    solvers = {
        "BFS": BFSSolver,
        "DFS": DFSSolver,
        "IDS": lambda: DFSSolver(use_ids=True),
        "UCS": UCSSolver,
        "ASTAR": AStarSolver,
        "A*": AStarSolver
    }

    algo_key = algo_name.upper()
    if algo_key not in solvers:
        print(f"Thuật toán không hợp lệ: {algo_name}. Chọn BFS, DFS, IDS, UCS hoặc ASTAR.")
        return

    solver = solvers[algo_key]()
    print(f"Thuật toán: {solver.name}")

    try:
        result = solver.solve(problem)
        print("\nKết quả:")
        print(f"Trạng thái      : {result.status}")
        print(f"Độ dài đường đi : {result.solution_length} bước")
        print(f"Số nút mở rộng  : {result.expanded_nodes}")
        print(f"Thời gian chạy  : {result.search_time_ms:.2f} ms")
        print(f"Bộ nhớ đỉnh     : {result.memory_peak_kb:.2f} KiB")
        if result.cost > 0:
            print(f"Tổng chi phí    : {result.cost:.2f}")
        print("\nLời giải:")
        print(" -> ".join(result.path) if result.path else "Không có hành động.")
    except NotImplementedError as e:
        print(f"\nChưa hỗ trợ: {e}")


def main():
    parser = argparse.ArgumentParser(description="Bloxorz Solver")
    parser.add_argument("--web", action="store_true", help="Mở giao diện web")
    parser.add_argument("--solve", action="store_true", help="Giải một màn từ dòng lệnh")
    parser.add_argument("--stage", type=str, default="stages/stage_01.json", help="Tệp màn chơi JSON")
    parser.add_argument("--algo", type=str, default="BFS", help="Thuật toán (BFS, DFS, IDS, UCS, ASTAR)")
    parser.add_argument("--benchmark", action="store_true", help="So sánh các bộ giải trên tất cả màn chơi")

    args = parser.parse_args()

    if args.benchmark:
        from benchmark import run_benchmark
        run_benchmark()
    elif args.solve:
        run_cli_solve(args.stage, args.algo)
    else:
        from web.server import run as run_web_server
        run_web_server()


if __name__ == "__main__":
    main()
