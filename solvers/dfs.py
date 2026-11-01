"""DFS giới hạn độ sâu và IDS."""
from typing import List, Set, Tuple, Dict, Optional
from .base import BaseSolver, SearchResult
from core.problem import BloxorzProblem, Action
from core.state import GameState, Orientation
from core.board import TileType


class DFSSolver(BaseSolver):
    """use_ids chọn IDS; order_moves bật ưu tiên nước đi."""

    def __init__(self, use_ids: bool = False, max_depth: int = 50, order_moves: bool = False):
        name = "Iterative Deepening Search (IDS)" if use_ids else "Depth-First Search (DFS)"
        super().__init__(name=name)
        self.use_ids = use_ids
        self.max_depth = max_depth
        self.order_moves = order_moves

    def _heuristic_distance(self, problem: BloxorzProblem, state: GameState) -> float:
        """Xếp nước đi theo khoảng cách đến đích, ô tách hoặc công tắc cầu."""
        block = state.block
        goal_r, goal_c = problem.board.goal_pos

        if block.orientation == Orientation.SPLIT:
            r1, c1 = block.r, block.c
            r2, c2 = block.r2, block.c2
            dist_between = abs(r1 - r2) + abs(c1 - c2)

            # Ưu tiên công tắc điều khiển cầu còn đóng.
            unopened_bridges = [b_id for b_id, is_open in state.bridges if not is_open]
            bridge_penalty = 0.0
            if unopened_bridges:
                for (sr, sc), sw in problem.board.switch_map.items():
                    if any(b in sw.linked_bridge_ids for b in unopened_bridges):
                        cr, cc = (r1, c1) if block.active_cube == 1 else (r2, c2)
                        bridge_penalty = abs(cr - sr) + abs(cc - sc)
                        break

            return dist_between + bridge_penalty * 2.0

        split_switches = [sw for sw in problem.board.switches if sw.switch_type == TileType.SPLIT_SWITCH]
        if split_switches:
            sw = split_switches[0]
            sr, sc = sw.r, sw.c
            cells = block.get_occupied_cells()
            dist_to_split = min(abs(r - sr) + abs(c - sc) for r, c in cells)
            # Cần đổi tư thế để kích hoạt ô tách.
            if block.orientation != Orientation.STAND:
                dist_to_split += 1.0
            return dist_to_split

        cells = block.get_occupied_cells()
        return min(abs(r - goal_r) + abs(c - goal_c) for r, c in cells)

    def _calculate_path_cost(self, problem: BloxorzProblem, start_state: GameState, path: List[str]) -> float:
        """Phát lại đường đi để tính tổng chi phí."""
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
        if self.use_ids:
            return self._search_ids(problem)
        return self._search_dfs(problem)

    def _search_dfs(self, problem: BloxorzProblem) -> SearchResult:
        """DFS dùng ngăn xếp, cắt nhánh theo độ sâu nhỏ nhất đã gặp."""
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

                    # DFS tính cả đích vừa sinh vào expanded_nodes.
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
                            # Giảm ưu tiên đổi khối liên tiếp.
                            if action == Action.SWITCH_CUBE and path and path[-1] == Action.SWITCH_CUBE.value:
                                dist += 50.0
                            successors.append((dist, next_state, new_path))
                        else:
                            stack.append((next_state, new_path))

            if self.order_moves and successors:
                # Đẩy nước đi gần mục tiêu nhất vào sau để lấy ra trước.
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
        """Tăng giới hạn sâu đến max_depth; dừng khi gặp đích hoặc hết nhánh."""
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
        """Trả (found, path, expanded_nodes, any_cutoff)."""
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
