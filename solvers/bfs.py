"""BFS tìm đường đi ít hành động nhất."""
from collections import deque
from typing import List, Set
from .base import BaseSolver, SearchResult
from core.problem import BloxorzProblem
from core.state import GameState


class BFSSolver(BaseSolver):
    def __init__(self):
        super().__init__(name="Breadth-First Search (BFS)")

    def _search(self, problem: BloxorzProblem) -> SearchResult:
        start_state = problem.get_initial_state()

        if not problem.is_valid_state(start_state):
            return SearchResult(
                status="NOT_FOUND",
                path=[],
                solution_length=0,
                expanded_nodes=0,
                cost=0.0
            )

        if problem.is_goal(start_state):
            return SearchResult(
                status="FOUND",
                path=[],
                solution_length=0,
                expanded_nodes=0,
                cost=0.0
            )

        queue = deque([(start_state, [])])

        visited: Set[GameState] = {start_state}
        expanded_nodes = 0

        while queue:
            curr_state, path = queue.popleft()
            expanded_nodes += 1

            for action in problem.get_actions(curr_state):
                next_state = problem.get_successor(curr_state, action)

                if next_state is not None and next_state not in visited:
                    new_path = path + [action.value]

                    # Kiểm tra đích khi sinh; không tính đích vào expanded_nodes.
                    if problem.is_goal(next_state):
                        return SearchResult(
                            status="FOUND",
                            path=new_path,
                            solution_length=len(new_path),
                            expanded_nodes=expanded_nodes,
                            cost=float(len(new_path))
                        )

                    visited.add(next_state)
                    queue.append((next_state, new_path))

        return SearchResult(
            status="NOT_FOUND",
            path=[],
            solution_length=0,
            expanded_nodes=expanded_nodes,
            cost=0.0
        )
