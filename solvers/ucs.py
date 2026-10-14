"""
=============================================================================
THUẬT TOÁN: UNIFORM-COST SEARCH (UCS)
NGƯỜI PHỤ TRÁCH: TRƯỜNG
=============================================================================
Yêu cầu theo đề bài:
1. Sử dụng hàng đợi ưu tiên (heapq / PriorityQueue) sắp xếp theo chi phí g(n).
2. ĐẶC BIỆT QUAN TRỌNG:
   - Đề bài lưu ý: "Nếu mọi bước có cost = 1, UCS sẽ bị thoái hóa thành BFS".
   - Do đó, Trường cần thiết kế một hàm chi phí KHÔNG ĐỒNG NHẤT (non-uniform cost function)
     và giải thích trực giác/lý do hợp lý trong báo cáo để đạt điểm tối đa phần này.
   - Ví dụ gợi ý:
     + Bước đi bình thường trên FLOOR: cost = 1.0
     + Bước đi tiếp xúc ô gạch vỡ FRAGILE: cost = 2.5 (chi phí cao vì nguy hiểm/rủi ro)
     + Bước đi dẫm công tắc kích hoạt cầu: cost = 0.5 (chi phí thấp vì mở đường đi mới)
=============================================================================
"""
import heapq
from typing import Dict, List, Tuple
from .base import BaseSolver, SearchResult
from core.problem import BloxorzProblem, Action
from core.state import GameState, Orientation
from core.board import TileType


class UCSSolver(BaseSolver):
    def __init__(self):
        super().__init__(name="Uniform-Cost Search (UCS)")

    def get_action_cost(self, problem: BloxorzProblem, state: GameState, action: Action, next_state: GameState) -> float:
        """
        TODO (Trường): Định nghĩa hàm chi phí g(n) tại đây.
        
        Gợi ý thiết kế cost:
        - Trường có thể phân loại theo tính chất của ô đích mà khối sắp bước lên:
          cells = next_state.block.get_occupied_cells()
          for r, c in cells:
              if problem.board.grid[r][c] == TileType.FRAGILE:
                  return 2.5  # Phạt nặng ô dễ vỡ
              if (r, c) in problem.board.switch_map:
                  return 0.5  # Khuyến khích dẫm công tắc
          return 1.0          # Bước đi thông thường
        """
        # Mặc định cơ bản (Trường hãy điều chỉnh và giải thích trong Report)
        return 1.0

    def _search(self, problem: BloxorzProblem) -> SearchResult:
        """
        TODO (Trường): Cài đặt thuật toán UCS tại đây.
        
        Gợi ý các bước thực hiện:
        -------------------------
        1. Lấy start_state = problem.get_initial_state()
        2. Khởi tạo hàng đợi ưu tiên min-heap (heapq):
           Mỗi phần tử trong heap có dạng: (cost_so_far, tie_breaker_id, current_state, path)
           pq = []
           heapq.heappush(pq, (0.0, 0, start_state, []))
           
        3. Khởi tạo cấu trúc lưu chi phí thấp nhất đến từng trạng thái:
           best_cost: Dict[GameState, float] = {start_state: 0.0}
           expanded_nodes = 0
           counter = 0

        4. Vòng lặp while pq:
           a. Lấy node có chi phí g nhỏ nhất:
              g_cost, _, curr_state, path = heapq.heappop(pq)
              
           b. Nếu g_cost > best_cost.get(curr_state, float('inf')):
              continue  # Đã tìm được đường đi tốt hơn tới state này trước đó
              
           c. expanded_nodes += 1
           
           d. Kiểm tra nếu problem.is_goal(curr_state):
              -> Trả về SearchResult(
                     status="FOUND",
                     path=path,
                     expanded_nodes=expanded_nodes,
                     cost=g_cost
                 )
                 
           e. Mở rộng các trạng thái kế tiếp:
              for action in problem.get_actions(curr_state):
                  next_state = problem.get_successor(curr_state, action)
                  if next_state is not None:
                      step_cost = self.get_action_cost(problem, curr_state, action, next_state)
                      new_cost = g_cost + step_cost
                      
                      if new_cost < best_cost.get(next_state, float('inf')):
                          best_cost[next_state] = new_cost
                          counter += 1
                          heapq.heappush(pq, (new_cost, counter, next_state, path + [action.value]))
                          
        5. Nếu duyệt hết heap mà không đến được đích:
           -> Trả về SearchResult(status="NOT_FOUND", path=[], expanded_nodes=expanded_nodes)
        """
        # ==================== TRƯỜNG VIẾT CODE TẠI ĐÂY ====================
        raise NotImplementedError("Trường hãy cài đặt thuật toán UCS theo gợi ý ở docstring!")
        # =================================================================
