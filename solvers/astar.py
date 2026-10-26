"""
======================================================================
THUẬT TOÁN: A* HEURISTIC SEARCH
NGƯỜI PHỤ TRÁCH: QUÂN
======================================================================
Yêu cầu theo đề bài:
1. Sử dụng hàm đánh giá f(n) = g(n) + h(n) với hàng đợi ưu tiên min-heap.
2. Tự thiết kế hàm Heuristic h(n) để ước lượng chi phí còn lại từ trạng
   thái hiện tại đến trạng thái đích.
3. Heuristic cần phù hợp với hàm chi phí g(n) và nên đảm bảo tính
   admissible, tức là không được ước lượng lớn hơn chi phí thực tế.
4. Trạng thái tìm kiếm phải bao gồm vị trí, tư thế của khối và trạng thái
   đóng/mở của các bridge.

Các ý tưởng được sử dụng trong heuristic:
- Khoảng cách Manhattan từ khối đến ô đích, chia cho 2 vì một lần lăn có
  thể làm khối dịch chuyển tối đa hai ô.
- Nếu khối chưa đứng, cộng thêm cận dưới cho việc thay đổi tư thế.
- Nếu màn chơi có Split Switch, sử dụng h(n) = 0 vì teleport có thể đưa
  khối tới vị trí rất xa chỉ trong một bước.
======================================================================
"""
import heapq
from typing import Dict
from .base import BaseSolver, SearchResult
from core.problem import BloxorzProblem, Action
from core.state import GameState, Orientation
from core.board import TileType


class AStarSolver(BaseSolver):
    """
    Bộ giải Bloxorz bằng thuật toán A*.

    A* lựa chọn trạng thái có tổng f(n) nhỏ nhất, trong đó:
    - g(n): chi phí từ trạng thái bắt đầu đến trạng thái hiện tại.
    - h(n): chi phí ước lượng từ trạng thái hiện tại đến đích.
    """

    def __init__(self):
        super().__init__(name="A* Search")

    def heuristic(self, problem: BloxorzProblem, state: GameState) -> float:
        """
        Tính giá trị heuristic h(n) cho một trạng thái.

        Với màn chơi bình thường, tôi dùng khoảng cách Manhattan nhỏ nhất
        giữa các ô mà khối đang chiếm giữ và ô đích. Khoảng cách này được
        chia cho 2 vì một lần lăn có thể dịch chuyển khối tối đa hai ô.

        Khi có Split Switch, khối có thể teleport tới một vị trí xa hơn rất
        nhiều. Khi đó Manhattan không còn là cận dưới an toàn, nên tôi dùng
        h(n) = 0 để giữ tính đúng đắn của A*.
        """
        block = state.block

        # Khi có Split Switch, teleport có thể rút ngắn đường đi rất nhiều.
        # Vì vậy tôi dùng h = 0 để giữ heuristic luôn admissible và consistent.
        if any(
            sw.switch_type == TileType.SPLIT_SWITCH
            for sw in problem.board.switches
        ):
            return 0.0

        goal_r, goal_c = problem.board.goal_pos
        cells = block.get_occupied_cells()

        # Mỗi lần lăn có thể làm một ô của khối dịch chuyển tối đa hai ô.
        # Do đó, Manhattan nhỏ nhất chia cho 2 là một cận dưới hợp lệ.
        min_manhattan = min(
            abs(r - goal_r) + abs(c - goal_c) for r, c in cells
        )
        distance_lower_bound = min_manhattan / 2.0

        # Khối chỉ thắng khi đứng trên goal, nên khối đang nằm hoặc đang tách
        # chắc chắn còn cần ít nhất một thao tác để thay đổi tư thế/trạng thái.
        orientation_lower_bound = (
            1.0 if block.orientation != Orientation.STAND else 0.0
        )

        # Tôi dùng max thay vì cộng vì hai cận dưới có thể đang tính trùng
        # cùng một thao tác lăn. Cộng lại sẽ không còn chắc chắn admissible.
        return max(distance_lower_bound, orientation_lower_bound)

    def _search(self, problem: BloxorzProblem) -> SearchResult:
        """
        Cài đặt quy trình tìm kiếm A*.

        Quy trình xử lý:
        1. Khởi tạo trạng thái bắt đầu và đưa vào min-heap.
        2. Lấy trạng thái có f(n) nhỏ nhất ra khỏi frontier.
        3. Nếu trạng thái hiện tại là đích thì trả về lời giải.
        4. Sinh các trạng thái kế tiếp bằng những hành động hợp lệ.
        5. Chỉ cập nhật một trạng thái khi tìm được chi phí g(n) tốt hơn.
        6. Nếu frontier rỗng mà chưa gặp đích thì bài toán không có lời giải.
        """
        start_state = problem.get_initial_state()
        start_h = self.heuristic(problem, start_state)

        # counter được dùng để phân biệt các phần tử có cùng f-score. Nhờ đó
        # heap không cần phải so sánh trực tiếp hai đối tượng GameState.
        counter = 0
        frontier = [(start_h, counter, 0.0, start_state, [])]
        best_cost: Dict[GameState, float] = {start_state: 0.0}
        expanded_nodes = 0

        while frontier:
            f_score, _, current_cost, current_state, path = heapq.heappop(frontier)

            # Một trạng thái có thể xuất hiện nhiều lần trong heap. Tôi chỉ
            # mở rộng bản ghi có chi phí tốt nhất đã biết.
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
