"""
=============================================================================
THUẬT TOÁN: A* HEURISTIC SEARCH
NGƯỜI PHỤ TRÁCH: QUÂN
=============================================================================
Yêu cầu theo đề bài:
1. Sử dụng hàm đánh giá f(n) = g(n) + h(n) với hàng đợi ưu tiên min-heap.
2. ĐẶC BIỆT QUAN TRỌNG:
   - Quân phải tự thiết kế hàm Heuristic h(n) ước lượng chi phí còn lại từ trạng thái hiện tại đến đích.
   - Trong Báo cáo (Report.pdf), Quân phải trình bày lập luận và CHỨNG MINH tính:
     + Chấp nhận được (Admissible): h(n) <= h*(n) (không bao giờ ước lượng vượt quá chi phí thực tế).
     + Nhất quán (Consistent / Monotonic): h(n) <= c(n, a, n') + h(n').
   - Lưu ý: h(n) phải tương thích với hàm chi phí g(n) do Trường thiết kế ở bài UCS.
3. Các ý tưởng Heuristic gợi ý từ giảng viên (có thể kết hợp):
   - Ý tưởng 1: Khoảng cách Manhattan từ khối đến ô đích chia 2:
     dist = (|r - goal_r| + |c - goal_c|) / 2.0 (vì mỗi bước lăn khối đi được tối đa 2 ô).
   - Ý tưởng 2: Phạt tư thế (Orientation Penalty): Nếu khối không đứng (Orientation != STAND),
     nó bắt buộc phải tốn thêm ít nhất 1 bước lật để dựng đứng vào lỗ đích (+1 penalty).
   - Ý tưởng 3: Khoảng cách bài toán nới lỏng (Relaxed problem distance).
=============================================================================
"""
import heapq
from typing import Dict, List, Tuple
from .base import BaseSolver, SearchResult
from core.problem import BloxorzProblem, Action
from core.state import GameState, Orientation


class AStarSolver(BaseSolver):
    def __init__(self):
        super().__init__(name="A* Search")

    def heuristic(self, problem: BloxorzProblem, state: GameState) -> float:
        """
        TODO (Quân): Thiết kế hàm heuristic h(n) tại đây.
        
        Gợi ý cài đặt:
        --------------
        block = state.block
        goal_r, goal_c = problem.board.goal_pos
        
        # 1. Tính khoảng cách Manhattan từ khối đến đích
        # (Nếu khối nằm, có thể lấy trung bình cộng tọa độ hoặc tọa độ ô gần nhất)
        cells = block.get_occupied_cells()
        min_manhattan = min(abs(r - goal_r) + abs(c - goal_c) for r, c in cells)
        
        # Vì mỗi bước lăn khối có thể dịch chuyển tối đa 2 ô, nên chia 2 là một lower bound hợp lệ:
        h = min_manhattan / 2.0
        
        # 2. Phạt tư thế: Nếu chưa đứng thẳng, chắc chắn cần thêm ít nhất 1 bước lật để đứng vào đích
        if block.orientation != Orientation.STAND:
            h += 1.0
            
        return h
        """
        # ==================== QUÂN VIẾT HEURISTIC TẠI ĐÂY ====================
        raise NotImplementedError("Quân hãy thiết kế và cài đặt hàm heuristic h(n)!")
        # =====================================================================

    def _search(self, problem: BloxorzProblem) -> SearchResult:
        """
        TODO (Quân): Cài đặt thuật toán A* Search tại đây.
        
        Gợi ý các bước thực hiện:
        -------------------------
        1. Lấy start_state = problem.get_initial_state()
        2. Khởi tạo hàng đợi ưu tiên pq:
           Mỗi phần tử trong heap lưu: (f_score, tie_breaker_id, g_score, current_state, path)
           
           h_start = self.heuristic(problem, start_state)
           f_start = 0.0 + h_start
           pq = []
           heapq.heappush(pq, (f_start, 0, 0.0, start_state, []))
           
        3. Khởi tạo g_score_map lưu chi phí g tốt nhất đã biết đến từng state:
           g_scores: Dict[GameState, float] = {start_state: 0.0}
           expanded_nodes = 0
           counter = 0

        4. Vòng lặp while pq:
           a. Lấy node có f_score nhỏ nhất:
              f, _, g, curr_state, path = heapq.heappop(pq)
              
           b. Nếu g > g_scores.get(curr_state, float('inf')):
              continue  # Đã có đường đi g ngắn hơn đến node này
              
           c. expanded_nodes += 1
           
           d. Kiểm tra nếu problem.is_goal(curr_state):
              -> Trả về SearchResult(
                     status="FOUND",
                     path=path,
                     expanded_nodes=expanded_nodes,
                     cost=g
                 )
                 
           e. Mở rộng các trạng thái kế tiếp:
              for action in problem.get_actions(curr_state):
                  next_state = problem.get_successor(curr_state, action)
                  if next_state is not None:
                      step_cost = problem.get_step_cost(curr_state, action, next_state)
                      tentative_g = g + step_cost
                      
                      if tentative_g < g_scores.get(next_state, float('inf')):
                          g_scores[next_state] = tentative_g
                          h = self.heuristic(problem, next_state)
                          f = tentative_g + h
                          counter += 1
                          heapq.heappush(pq, (f, counter, tentative_g, next_state, path + [action.value]))
                          
        5. Nếu không tìm thấy đường đi:
           -> Trả về SearchResult(status="NOT_FOUND", path=[], expanded_nodes=expanded_nodes)
        """
        # ==================== QUÂN VIẾT THUẬT TOÁN A* TẠI ĐÂY ====================
        raise NotImplementedError("Quân hãy cài đặt thuật toán A* theo gợi ý ở docstring!")
        # ========================================================================
