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
4. Hỗ trợ đầy đủ các cơ chế nâng cao:
   - Gạch vỡ (FRAGILE).
   - Cầu đóng/mở & các loại công tắc (SOFT, HEAVY).
   - Công tắc tách khối (SPLIT_SWITCH) & điều khiển phân tách 2 khối đơn 1x1x1 (Action.SWITCH_CUBE)
     cũng như cơ chế tự động hợp nhất (MERGE) thành khối 1x1x2.
=============================================================================
"""
from typing import List, Set, Tuple, Dict, Optional
from .base import BaseSolver, SearchResult
from core.problem import BloxorzProblem, Action
from core.state import GameState, Orientation
from core.board import TileType


class DFSSolver(BaseSolver):
    """
    Bộ giải Bloxorz bằng thuật toán tìm kiếm theo chiều sâu (DFS)
    hoặc tìm kiếm sâu dần (Iterative Deepening Search - IDS).

    Thuộc tính:
        use_ids (bool): Nếu True, sử dụng Iterative Deepening Search (IDS).
                        Nếu False (mặc định), sử dụng Depth-First Search (DFS).
        max_depth (int): Độ sâu tối đa cho phép duyệt (mặc định: 50).
        order_moves (bool): Nếu True, áp dụng kỹ thuật Move Ordering ưu tiên các
                            nước đi hướng về phía ô đích (Goal) hoặc công tắc tách khối (SPLIT),
                            giúp DFS giảm đáng kể số bước đi vòng và tăng tốc độ tìm kiếm.
    """

    def __init__(self, use_ids: bool = False, max_depth: int = 50, order_moves: bool = True):
        name = "Iterative Deepening Search (IDS)" if use_ids else "Depth-First Search (DFS)"
        super().__init__(name=name)
        self.use_ids = use_ids
        self.max_depth = max_depth
        self.order_moves = order_moves

    def _heuristic_distance(self, problem: BloxorzProblem, state: GameState) -> float:
        """
        Khoảng cách định hướng thông minh cho Move Ordering:
        1. Khi khối đang ở trạng thái phân tách (SPLIT):
           - Hai khối con 1x1x1 bắt buộc phải HỢP NHẤT (MERGE) mới có thể chiến thắng ở Goal.
           - Mục tiêu: Khối con cần tiến lại gần nhau (giảm khoảng cách giữa 2 khối) và
             điều khiển khối con gần công tắc mở cầu nhất đi mở các cây cầu đang đóng.
        2. Khi khối chưa tách nhưng trên bản đồ có SPLIT_SWITCH (như Stage 18):
           - Khối ở khu vực xuất phát không thể đến thẳng Goal nếu không qua SPLIT_SWITCH.
           - Mục tiêu: Hướng khối đứng thẳng (STAND) vào ô SPLIT_SWITCH để kích hoạt phân tách.
        3. Trường hợp thông thường:
           - Khoảng cách Manhattan từ khối đến ô Goal.
        """
        block = state.block
        goal_r, goal_c = problem.board.goal_pos

        # 1. Trạng thái phân tách: 2 khối con 1x1x1
        if block.orientation == Orientation.SPLIT:
            r1, c1 = block.r, block.c
            r2, c2 = block.r2, block.c2
            dist_between = abs(r1 - r2) + abs(c1 - c2)

            # Phạt nếu còn cây cầu nào đang đóng mà chưa được mở
            unopened_bridges = [b_id for b_id, is_open in state.bridges if not is_open]
            bridge_penalty = 0.0
            if unopened_bridges:
                for (sr, sc), sw in problem.board.switch_map.items():
                    if any(b in sw.linked_bridge_ids for b in unopened_bridges):
                        cr, cc = (r1, c1) if block.active_cube == 1 else (r2, c2)
                        bridge_penalty = abs(cr - sr) + abs(cc - sc)
                        break

            return dist_between + bridge_penalty * 2.0

        # 2. Chưa phân tách nhưng trên bàn cờ có SPLIT_SWITCH (như Stage 18, 19, 20)
        split_switches = [sw for sw in problem.board.switches if sw.switch_type == TileType.SPLIT_SWITCH]
        if split_switches:
            sw = split_switches[0]
            sr, sc = sw.r, sw.c
            cells = block.get_occupied_cells()
            dist_to_split = min(abs(r - sr) + abs(c - sc) for r, c in cells)
            # Công tắc SPLIT_SWITCH chỉ kích hoạt khi khối ĐỨNG THẲNG (STAND)
            if block.orientation != Orientation.STAND:
                dist_to_split += 1.0
            return dist_to_split

        # 3. Trạng thái thông thường: khoảng cách Manhattan đến đích
        cells = block.get_occupied_cells()
        return min(abs(r - goal_r) + abs(c - goal_c) for r, c in cells)

    def _calculate_path_cost(self, problem: BloxorzProblem, start_state: GameState, path: List[str]) -> float:
        """Tính tổng chi phí đường đi dựa trên hàm get_step_cost của BloxorzProblem (chuẩn risk_v1)."""
        curr = start_state
        total_cost = 0.0
        for action_val in path:
            action = Action(action_val)
            next_state = problem.get_successor(curr, action)
            if next_state is not None:
                total_cost += problem.get_step_cost(curr, action, next_state)
                curr = next_state
        return total_cost

    def _search(self, problem: BloxorzProblem) -> SearchResult:
        """
        Điều hướng thuật toán tìm kiếm dựa theo cấu hình self.use_ids:
        - self.use_ids == True  -> Chạy Iterative Deepening Search (IDS)
        - self.use_ids == False -> Chạy Depth-First Search (DFS)
        """
        if self.use_ids:
            return self._search_ids(problem)
        return self._search_dfs(problem)

    def _search_dfs(self, problem: BloxorzProblem) -> SearchResult:
        """
        Cài đặt thuật toán Depth-First Search (DFS) sử dụng ngăn xếp lặp (Explicit Stack).

        Quy trình xử lý & tối ưu:
        1. Kiểm tra tính hợp lệ của trạng thái khởi đầu.
        2. Dùng visited_depth lưu độ sâu tối thiểu từng ghé thăm mỗi trạng thái.
        3. Early Goal Test: Kiểm tra đích sớm khi sinh successor để kết thúc ngay khi chạm đích.
        4. Move Ordering: Sắp xếp các nước đi hướng về đích/công tắc tách khối trước.
        5. Cắt tỉa nếu đạt max_depth.
        """
        start_state = problem.get_initial_state()
        if not problem.is_valid_state(start_state):
            return SearchResult(status="NOT_FOUND", path=[], expanded_nodes=0, cost=0.0)

        if problem.is_goal(start_state):
            return SearchResult(status="FOUND", path=[], expanded_nodes=0, cost=0.0)

        stack: List[Tuple[GameState, List[str]]] = [(start_state, [])]
        visited_depth: Dict[GameState, int] = {}
        expanded_nodes = 0

        while stack:
            curr_state, path = stack.pop()
            depth = len(path)

            if curr_state in visited_depth and visited_depth[curr_state] <= depth:
                continue
            visited_depth[curr_state] = depth
            expanded_nodes += 1

            if problem.is_goal(curr_state):
                cost = self._calculate_path_cost(problem, start_state, path)
                return SearchResult(
                    status="FOUND",
                    path=path,
                    expanded_nodes=expanded_nodes,
                    cost=cost
                )

            if self.max_depth is not None and depth >= self.max_depth:
                continue

            successors = []
            for action in problem.get_actions(curr_state):
                next_state = problem.get_successor(curr_state, action)
                if next_state is not None:
                    new_path = path + [action.value]

                    # Early Goal Test: kiểm tra đích sớm để dừng ngay lập tức
                    if problem.is_goal(next_state):
                        expanded_nodes += 1
                        cost = self._calculate_path_cost(problem, start_state, new_path)
                        return SearchResult(
                            status="FOUND",
                            path=new_path,
                            expanded_nodes=expanded_nodes,
                            cost=cost
                        )

                    next_depth = depth + 1
                    if next_state not in visited_depth or visited_depth[next_state] > next_depth:
                        if self.order_moves:
                            dist = self._heuristic_distance(problem, next_state)
                            # Phạt nếu thực hiện SWITCH_CUBE liên tiếp 2 lần không di chuyển
                            if action == Action.SWITCH_CUBE and path and path[-1] == Action.SWITCH_CUBE.value:
                                dist += 50.0
                            successors.append((dist, next_state, new_path))
                        else:
                            stack.append((next_state, new_path))

            if self.order_moves and successors:
                # Sắp xếp khoảng cách giảm dần để khi push vào stack LIFO,
                # trạng thái hứa hẹn nhất nằm ở đỉnh stack và được pop duyệt trước
                successors.sort(key=lambda item: item[0], reverse=True)
                for _, n_st, n_path in successors:
                    stack.append((n_st, n_path))

        return SearchResult(
            status="NOT_FOUND",
            path=[],
            expanded_nodes=expanded_nodes,
            cost=0.0
        )

    def _search_ids(self, problem: BloxorzProblem) -> SearchResult:
        """
        Cài đặt thuật toán Iterative Deepening Search (IDS).

        Quy trình xử lý:
        - Tăng dần giới hạn độ sâu limit từ 0 đến max_depth.
        - Ở mỗi vòng lặp, chạy Depth-Limited Search (DLS).
        - Nếu tìm thấy đích: Dừng ngay và trả về đường đi tối ưu (độ dài ngắn nhất như BFS).
        - Nếu không có nhánh nào bị cắt bởi giới hạn độ sâu (any_cutoff == False),
          chứng tỏ đã duyệt kiệt toàn bộ không gian trạng thái liên thông -> Dừng sớm.
        - Cộng dồn số node đã mở rộng qua các vòng lặp để thu thập số liệu thực nghiệm chính xác.
        """
        start_state = problem.get_initial_state()
        if not problem.is_valid_state(start_state):
            return SearchResult(status="NOT_FOUND", path=[], expanded_nodes=0, cost=0.0)

        if problem.is_goal(start_state):
            return SearchResult(status="FOUND", path=[], expanded_nodes=0, cost=0.0)

        total_expanded_nodes = 0
        depth_limit = 0

        while True:
            if self.max_depth is not None and depth_limit > self.max_depth:
                break

            found, path, expanded, any_cutoff = self._dls(problem, start_state, depth_limit)
            total_expanded_nodes += expanded

            if found:
                cost = self._calculate_path_cost(problem, start_state, path)
                return SearchResult(
                    status="FOUND",
                    path=path,
                    expanded_nodes=total_expanded_nodes,
                    cost=cost
                )

            if not any_cutoff:
                break

            depth_limit += 1

        return SearchResult(
            status="NOT_FOUND",
            path=[],
            expanded_nodes=total_expanded_nodes,
            cost=0.0
        )

    def _dls(
        self, problem: BloxorzProblem, start_state: GameState, limit: int
    ) -> Tuple[bool, List[str], int, bool]:
        """
        Depth-Limited Search (DLS) phục vụ cho từng tầng của IDS.

        Args:
            problem: Bài toán Bloxorz.
            start_state: Trạng thái bắt đầu.
            limit: Ngưỡng độ sâu tối đa cho lần tìm kiếm này.

        Returns:
            Tuple[bool, List[str], int, bool]:
                - found (bool): Có tìm thấy đích không.
                - path (List[str]): Đường đi nếu tìm thấy đích.
                - expanded_nodes (int): Số node đã mở rộng trong lần chạy này.
                - any_cutoff (bool): Có nhánh nào bị cắt vì chạm giới hạn độ sâu hay không.
        """
        stack: List[Tuple[GameState, List[str], int]] = [(start_state, [], 0)]
        visited_depth: Dict[GameState, int] = {}
        expanded_nodes = 0
        any_cutoff = False

        while stack:
            curr_state, path, depth = stack.pop()

            if curr_state in visited_depth and visited_depth[curr_state] <= depth:
                continue
            visited_depth[curr_state] = depth
            expanded_nodes += 1

            if problem.is_goal(curr_state):
                return True, path, expanded_nodes, False

            if depth >= limit:
                any_cutoff = True
                continue

            for action in problem.get_actions(curr_state):
                next_state = problem.get_successor(curr_state, action)
                if next_state is not None:
                    next_depth = depth + 1
                    if next_state not in visited_depth or visited_depth[next_state] > next_depth:
                        stack.append((next_state, path + [action.value], next_depth))

        return False, [], expanded_nodes, any_cutoff
