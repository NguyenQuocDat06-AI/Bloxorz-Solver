"""
=============================================================================
THUẬT TOÁN: BREADTH-FIRST SEARCH (BFS)
NGƯỜI PHỤ TRÁCH: PHÚC
=============================================================================
Yêu cầu theo đề bài:
1. Sử dụng hàng đợi FIFO (collections.deque) để duyệt không gian trạng thái theo chiều rộng.
2. Đảm bảo tìm ra đường đi ngắn nhất theo số lượng bước đi.
3. Sử dụng tập visited (set) để lưu vết các GameState đã duyệt, tránh lặp vô hạn.
4. Đếm chính xác số node đã mở rộng (expanded_nodes) mỗi khi pop một node ra khỏi hàng đợi.
=============================================================================
"""
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

        # Kiểm tra nếu trạng thái bắt đầu đã là đích
        if problem.is_goal(start_state):
            return SearchResult(
                status="FOUND",
                path=[],
                solution_length=0,
                expanded_nodes=0,
                cost=0.0
            )

        # Hàng đợi FIFO lưu tuple: (current_state, path)
        queue = deque([(start_state, [])])

        # Tập visited lưu các trạng thái đã ghé thăm nhằm tránh lặp vô tận
        visited: Set[GameState] = {start_state}
        expanded_nodes = 0

        while queue:
            curr_state, path = queue.popleft()
            expanded_nodes += 1

            for action in problem.get_actions(curr_state):
                next_state = problem.get_successor(curr_state, action)

                if next_state is not None and next_state not in visited:
                    new_path = path + [action.value]

                    # Early goal test theo chuẩn AIMA để tối ưu số node mở rộng
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

        # Nếu duyệt hết không gian trạng thái mà không tìm thấy đường đi tới đích
        return SearchResult(
            status="NOT_FOUND",
            path=[],
            solution_length=0,
            expanded_nodes=expanded_nodes,
            cost=0.0
        )
