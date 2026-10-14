"""
=============================================================================
THUẬT TOÁN: DEPTH-FIRST SEARCH (DFS) / ITERATIVE DEEPENING SEARCH (IDS)
NGƯỜI PHỤ TRÁCH: ĐỨC
=============================================================================
Yêu cầu theo đề bài:
1. Duyệt không gian trạng thái theo chiều sâu.
2. Xử lý triệt để bài toán lặp chu trình (Cycles / Repeated states):
   - Bloxorz có nhiều hành động đảo ngược (lăn L rồi R, U rồi D sẽ quay về trạng thái cũ).
   - Nếu không kiểm tra visited hoặc độ sâu, DFS sẽ rơi vào vòng lặp vô tận hoặc tràn bộ nhớ stack.
3. Có thể dùng DFS có giới hạn độ sâu (Depth-Limited Search) kết hợp lặp (IDS - Iterative Deepening Search).
   Nếu dùng IDS, Đức cần nêu rõ trong báo cáo vì IDS kết hợp được ưu điểm tiết kiệm bộ nhớ của DFS
   và tính tối ưu bước đi của BFS.
=============================================================================
"""
from typing import List, Set, Optional
from .base import BaseSolver, SearchResult
from core.problem import BloxorzProblem
from core.state import GameState


class DFSSolver(BaseSolver):
    def __init__(self, use_ids: bool = False, max_depth: int = 50):
        name = "Iterative Deepening Search (IDS)" if use_ids else "Depth-First Search (DFS)"
        super().__init__(name=name)
        self.use_ids = use_ids
        self.max_depth = max_depth

    def _search(self, problem: BloxorzProblem) -> SearchResult:
        """
        TODO (Đức): Cài đặt thuật toán DFS (hoặc IDS) tại đây.
        
        Gợi ý cách 1: DFS dùng Ngăn xếp lặp (Iterative Stack) - Tránh lỗi RecursionError của Python
        -----------------------------------------------------------------------------------------
        1. Lấy start_state = problem.get_initial_state()
        2. Khởi tạo stack:
           stack = [(start_state, [])] # (state, path_so_far)
           
        3. Khởi tạo tập đã thăm (visited set):
           visited: Set[GameState] = set()
           expanded_nodes = 0

        4. Vòng lặp while stack:
           a. Lấy node trên đỉnh ngăn xếp:
              curr_state, path = stack.pop()
              
           b. Nếu curr_state in visited -> Bỏ qua (continue)
           c. visited.add(curr_state)
              expanded_nodes += 1
              
           d. Kiểm tra nếu problem.is_goal(curr_state):
              -> Trả về SearchResult(status="FOUND", path=path, expanded_nodes=expanded_nodes)
              
           e. Giới hạn độ sâu (nếu cần): len(path) < max_depth
           f. Duyệt các actions:
              for action in problem.get_actions(curr_state):
                  next_state = problem.get_successor(curr_state, action)
                  if next_state is not None and next_state not in visited:
                      stack.append((next_state, path + [action.value]))
                      
        Gợi ý cách 2: Nếu Đức chọn làm IDS (Iterative Deepening Search):
        ----------------------------------------------------------------
        - Cho một vòng lặp depth_limit từ 1 tăng dần lên:
          Chạy Depth-Limited Search với độ sâu depth_limit.
          Nếu tìm thấy đích -> Dừng và trả về kết quả ngay.
        """
        # ==================== ĐỨC VIẾT CODE TẠI ĐÂY ====================
        raise NotImplementedError("Đức hãy cài đặt thuật toán DFS/IDS theo gợi ý ở docstring!")
        # ===============================================================
