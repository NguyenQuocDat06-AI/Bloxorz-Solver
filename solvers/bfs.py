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
        """
        TODO (Phúc): Cài đặt thuật toán BFS tại đây.
        
        Gợi ý các bước thực hiện:
        -------------------------
        1. Lấy trạng thái bắt đầu: start_state = problem.get_initial_state()
        2. Kiểm tra nếu start_state đã là đích (problem.is_goal(start_state)):
           -> Trả về SearchResult(status="FOUND", path=[], expanded_nodes=0)
           
        3. Khởi tạo hàng đợi FIFO (deque):
           Mỗi phần tử trong hàng đợi có thể lưu dạng tuple: (current_state, path_so_far)
           queue = deque([(start_state, [])])
           
        4. Khởi tạo tập đã thăm (visited set) để chống lặp:
           visited: Set[GameState] = {start_state}
           expanded_nodes = 0

        5. Vòng lặp while queue:
           a. Lấy node đầu tiên ra khỏi hàng đợi:
              curr_state, path = queue.popleft()
              expanded_nodes += 1
              
           b. Duyệt qua tất cả các hành động hợp lệ:
              for action in problem.get_actions(curr_state):
                  next_state = problem.get_successor(curr_state, action)
                  
                  if next_state is not None and next_state not in visited:
                      # Kiểm tra điều kiện đích sớm (hoặc kiểm tra khi pop)
                      if problem.is_goal(next_state):
                          return SearchResult(
                              status="FOUND",
                              path=path + [action.value],
                              expanded_nodes=expanded_nodes
                          )
                      visited.add(next_state)
                      queue.append((next_state, path + [action.value]))
                      
        6. Nếu duyệt hết queue mà không thấy đường đi:
           -> Trả về SearchResult(status="NOT_FOUND", path=[], expanded_nodes=expanded_nodes)
        """
        # ==================== PHÚC VIẾT CODE TẠI ĐÂY ====================
        raise NotImplementedError("Phúc hãy cài đặt thuật toán BFS theo gợi ý ở docstring!")
        # ===============================================================
