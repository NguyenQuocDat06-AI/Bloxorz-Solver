"""Tìm kiếm A*."""
import heapq
from typing import Dict
from .base import BaseSolver, SearchResult
from core.problem import BloxorzProblem, Action
from core.state import GameState, Orientation
from core.board import TileType


class AStarSolver(BaseSolver):
    def __init__(self):
        super().__init__(name="A* Search")

    def heuristic(self, problem: BloxorzProblem, state: GameState) -> float:
        """Ước lượng cận dưới chi phí còn lại."""
        block = state.block

        # Dịch chuyển làm mất cận dưới Manhattan; dùng h = 0.
        if any(
            sw.switch_type == TileType.SPLIT_SWITCH
            for sw in problem.board.switches
        ):
            return 0.0

        goal_r, goal_c = problem.board.goal_pos
        cells = block.get_occupied_cells()

        # Một lần lăn dịch chuyển tối đa hai ô.
        min_manhattan = min(
            abs(r - goal_r) + abs(c - goal_c) for r, c in cells
        )
        distance_lower_bound = min_manhattan / 2.0

        orientation_lower_bound = (
            1.0 if block.orientation != Orientation.STAND else 0.0
        )

        # Dùng max để không đếm trùng thao tác giữa hai cận dưới.
        return max(distance_lower_bound, orientation_lower_bound)

    def _search(self, problem: BloxorzProblem) -> SearchResult:
        start_state = problem.get_initial_state()
        start_h = self.heuristic(problem, start_state)

        # counter tránh so sánh GameState khi f bằng nhau.
        counter = 0
        frontier = [(start_h, counter, 0.0, start_state, [])]
        best_cost: Dict[GameState, float] = {start_state: 0.0}
        expanded_nodes = 0

        while frontier:
            f_score, _, current_cost, current_state, path = heapq.heappop(frontier)

            # Bỏ bản ghi có chi phí lớn hơn mức tốt nhất đã biết.
            if current_cost > best_cost.get(current_state, float("inf")):
                continue

            expanded_nodes += 1
            if problem.is_goal(current_state):
                return SearchResult(
                    status="FOUND",
                    path=path,
                    expanded_nodes=expanded_nodes,
                    cost=current_cost,
                )

            for action in problem.get_actions(current_state):
                next_state = problem.get_successor(current_state, action)
                if next_state is None:
                    continue

                step_cost = problem.get_step_cost(
                    current_state, action, next_state
                )
                new_cost = current_cost + step_cost

                if new_cost >= best_cost.get(next_state, float("inf")):
                    continue

                best_cost[next_state] = new_cost
                counter += 1
                new_f_score = new_cost + self.heuristic(problem, next_state)
                heapq.heappush(
                    frontier,
                    (
                        new_f_score,
                        counter,
                        new_cost,
                        next_state,
                        path + [action.value],
                    ),
                )

        return SearchResult(
            status="NOT_FOUND",
            path=[],
            expanded_nodes=expanded_nodes,
            cost=0.0,
        )
