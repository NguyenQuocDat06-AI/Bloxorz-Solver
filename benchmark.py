"""Đo BFS, IDS, UCS và A* trên các màn JSON."""
import os
import sys
import csv

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from typing import List
from core.board import Board
from core.cost import COST_PROFILE
from core.problem import Action, BloxorzProblem
from solvers.bfs import BFSSolver
from solvers.dfs import DFSSolver
from solvers.ucs import UCSSolver
from solvers.astar import AStarSolver

STAGES_DIR = "stages"
OUTPUT_CSV = "benchmark_results.csv"


def _solution_cost(problem: BloxorzProblem, path: List[str]) -> float:
    """Tính chi phí chung ngoài thời gian tìm kiếm."""
    state = problem.get_initial_state()
    if not problem.is_valid_state(state):
        raise ValueError("Invalid initial state during benchmark replay")
    total = 0.0
    for value in path:
        action = Action(value)
        successor = problem.get_successor(state, action)
        if successor is None:
            raise ValueError(f"Illegal benchmark path action: {value}")
        total += problem.get_step_cost(state, action, successor)
        state = successor
    if not problem.is_goal(state):
        raise ValueError("Benchmark path does not reach the goal")
    return total


def run_benchmark():
    if not os.path.exists(STAGES_DIR):
        print(f"Không tìm thấy thư mục: {STAGES_DIR}.")
        return

    stage_files = sorted([f for f in os.listdir(STAGES_DIR) if f.endswith(".json")])
    if not stage_files:
        print("Không có màn chơi JSON nào trong thư mục stages/.")
        return

    solvers = [
        ("BFS (Phúc)", BFSSolver()),
        ("IDS (Đức)", DFSSolver(use_ids=True)),
        ("UCS (Trường)", UCSSolver()),
        ("A* (Quân)", AStarSolver()),
    ]

    results = []

    print("=" * 85)
    print(f"{'STAGE':<18} | {'SOLVER':<16} | {'STATUS':<9} | {'STEPS':<6} | {'NODES':<8} | {'TIME(ms)':<9} | {'PEAK(KiB)'} | COST")
    print("=" * 85)

    for stage_file in stage_files:
        stage_path = os.path.join(STAGES_DIR, stage_file)
        board = Board.from_json(stage_path)
        problem = BloxorzProblem(board)

        for solver_label, solver in solvers:
            try:
                res = solver.solve(problem)
                cost = _solution_cost(problem, res.path) if res.status == "FOUND" else ""
                row = {
                    "stage": stage_file,
                    "solver": solver_label,
                    "status": res.status,
                    "steps": res.solution_length,
                    "nodes": res.expanded_nodes,
                    "time_ms": res.search_time_ms,
                    "ram_kb": res.memory_peak_kb,
                    "cost": cost,
                    "cost_profile": COST_PROFILE,
                }
                results.append(row)
                print(f"{stage_file:<18} | {solver_label:<16} | {res.status:<9} | {res.solution_length:<6} | {res.expanded_nodes:<8} | {res.search_time_ms:<9.2f} | {res.memory_peak_kb:.1f} | {cost if cost != '' else '--'}")
            except NotImplementedError:
                print(f"{stage_file:<18} | {solver_label:<16} | {'NOT IMPL':<9} | {'--':<6} | {'--':<8} | {'--':<9} | --")
            except Exception as e:
                print(f"{stage_file:<18} | {solver_label:<16} | {'ERROR':<9} | {str(e)[:30]}")

    print("=" * 85)

    if results:
        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["stage", "solver", "status", "steps", "nodes", "time_ms", "ram_kb", "cost", "cost_profile"])
            writer.writeheader()
            writer.writerows(results)
        print(f"Đã lưu kết quả: {OUTPUT_CSV}.")


if __name__ == "__main__":
    run_benchmark()
