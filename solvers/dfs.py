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
from typing import List, Set, Tuple, Dict, Optional
from .base import BaseSolver, SearchResult
from core.problem import BloxorzProblem
from core.state import GameState


class DFSSolver(BaseSolver):
    """
    Bộ giải Bloxorz bằng thuật toán tìm kiếm theo chiều sâu (DFS)
    hoặc tìm kiếm sâu dần (Iterative Deepening Search - IDS).

    Thuộc tính:
        use_ids (bool): Nếu True, sử dụng Iterative Deepening Search (IDS).
                        Nếu False (mặc định), sử dụng Depth-First Search (DFS).
        max_depth (int): Độ sâu tối đa cho phép duyệt (mặc định: 50).
    """

    def __init__(self, use_ids: bool = False, max_depth: int = 50):
        name = "Iterative Deepening Search (IDS)" if use_ids else "Depth-First Search (DFS)"
        super().__init__(name=name)
        self.use_ids = use_ids
        self.max_depth = max_depth

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

        Quy trình xử lý:
        1. Khởi tạo ngăn xếp stack với trạng thái bắt đầu.
        2. Dùng tập visited để lưu vết các trạng thái đã mở rộng, triệt tiêu chu trình lặp vô hạn.
        3. Kiểm tra điều kiện đích và giới hạn độ sâu (max_depth) để ngăn duyệt quá sâu.
        4. Trả về kết quả chuẩn SearchResult chứa đường đi và số node đã mở rộng.
        """
        start_state = problem.get_initial_state()
        if problem.is_goal(start_state):
            return SearchResult(status="FOUND", path=[], expanded_nodes=0, cost=0.0)

        # Ngăn xếp LIFO: mỗi phần tử gồm (current_state, path_so_far)
        stack: List[Tuple[GameState, List[str]]] = [(start_state, [])]
        visited: Set[GameState] = set()
        expanded_nodes = 0

        while stack:
            curr_state, path = stack.pop()

            # Nếu trạng thái đã được mở rộng trước đó, bỏ qua để tránh chu trình
            if curr_state in visited:
                continue
            visited.add(curr_state)
            expanded_nodes += 1

            # Kiểm tra trạng thái đích
            if problem.is_goal(curr_state):
                return SearchResult(
                    status="FOUND",
                    path=path,
                    expanded_nodes=expanded_nodes,
                    cost=float(len(path))
                )

            # Cắt tỉa nếu đạt tới giới hạn độ sâu tối đa
            if self.max_depth is not None and len(path) >= self.max_depth:
                continue

            # Mở rộng các trạng thái kế tiếp
            for action in problem.get_actions(curr_state):
                next_state = problem.get_successor(curr_state, action)
                if next_state is not None and next_state not in visited:
                    stack.append((next_state, path + [action.value]))

        # Đã duyệt hết không gian trạng thái mà không tìm thấy đích
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
                return SearchResult(
                    status="FOUND",
                    path=path,
                    expanded_nodes=total_expanded_nodes,
                    cost=float(len(path))
                )

            # Toàn bộ không gian liên thông đã được duyệt hết mà không bị cắt tỉa độ sâu
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
        # visited_depth lưu độ sâu nhỏ nhất đã đến từng trạng thái trong lần chạy DLS này
        visited_depth: Dict[GameState, int] = {}
        expanded_nodes = 0
        any_cutoff = False

        while stack:
            curr_state, path, depth = stack.pop()

            # Nếu đã từng đến trạng thái này ở độ sâu nhỏ hơn hoặc bằng, bỏ qua
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
