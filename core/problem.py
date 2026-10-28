from enum import Enum
from typing import List, Tuple, Dict, Optional
from .state import Orientation, BlockState, GameState
from .board import Board, TileType, SwitchBehavior, Switch
from .cost import transition_cost


class Action(str, Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    SWITCH_CUBE = "SWITCH"  # Đổi quyền điều khiển giữa 2 khối con khi bị tách


class BloxorzProblem:
    """
    Hình thức hóa bài toán tìm kiếm trạng thái (Search Problem Formulation) cho Bloxorz.
    Bao gồm:
    - Initial State
    - Actions
    - Transition Model
    - Goal Test
    - Step Cost Function
    """

    def __init__(self, board: Board):
        self.board = board

    def get_initial_state(self) -> GameState:
        """Trả về trạng thái ban đầu của bàn cờ và khối."""
        block = BlockState(
            r=self.board.start_pos[0],
            c=self.board.start_pos[1],
            orientation=Orientation.STAND
        )
        bridges = self.board.get_initial_bridges_tuple()
        return GameState(block=block, bridges=bridges)

    def is_goal(self, state: GameState) -> bool:
        """
        Kiểm tra trạng thái đích:
        Chỉ thắng khi khối 1x1x2 ĐỨNG THẲNG trên ô đích (GOAL).
        Khối nằm đè hoặc khối con 1x1x1 không được tính là chiến thắng.
        """
        block = state.block
        if block.orientation == Orientation.STAND:
            return (block.r, block.c) == self.board.goal_pos
        return False

    def is_cell_passable(self, r: int, c: int, state: GameState) -> bool:
        """Kiểm tra một ô có an toàn để nâng đỡ khối hay không (tính cả trạng thái cầu)."""
        if not (0 <= r < self.board.rows and 0 <= c < self.board.cols):
            return False

        tile = self.board.grid[r][c]
        if tile == TileType.VOID:
            return False

        if (r, c) in self.board.bridge_cell_map:
            b_id = self.board.bridge_cell_map[(r, c)]
            return state.get_bridge_status(b_id)

        return True

    def is_valid_state(self, state: GameState) -> bool:
        """
        Kiểm tra tính hợp lệ của trạng thái:
        - Tất cả các phần của khối phải nằm trên sàn hợp lệ (không đè lên void / cầu đóng).
        - Khối KHÔNG ĐƯỢC đứng thẳng trên ô gạch vỡ (FRAGILE).
        """
        block = state.block
        cells = block.get_occupied_cells()

        for r, c in cells:
            if not self.is_cell_passable(r, c, state):
                return False

        # Kiểm tra gạch vỡ (FRAGILE): khối đứng (hoặc khối đơn 1x1x1) sẽ làm sập gạch
        if block.orientation == Orientation.STAND:
            r, c = block.r, block.c
            if self.board.grid[r][c] == TileType.FRAGILE:
                return False
        elif block.orientation == Orientation.SPLIT:
            # Hai khối con 1x1x1 không thể chiếm cùng một ô tọa độ (va chạm vật lý)
            if (block.r, block.c) == (block.r2, block.c2):
                return False
            for r, c in cells:
                if self.board.grid[r][c] == TileType.FRAGILE:
                    return False

        return True

    def get_actions(self, state: GameState) -> List[Action]:
        """Trả về danh sách các hành động có thể thử tại trạng thái hiện tại."""
        actions = [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT]
        if state.block.orientation == Orientation.SPLIT:
            actions.append(Action.SWITCH_CUBE)
        return actions

    def get_successor(self, state: GameState, action: Action) -> Optional[GameState]:
        """
        Mô hình chuyển trạng thái (Transition Model):
        Nhận vào trạng thái hiện tại và hành động, trả về trạng thái kế tiếp nếu hợp lệ,
        ngược lại trả về None nếu bước đi dẫn đến rơi vực / vỡ gạch.
        """
        block = state.block

        # 1. Trường hợp đổi khối con khi đang bị tách
        if action == Action.SWITCH_CUBE:
            if block.orientation != Orientation.SPLIT:
                return None
            next_active = 2 if block.active_cube == 1 else 1
            new_block = BlockState(
                r=block.r, c=block.c, orientation=Orientation.SPLIT,
                r2=block.r2, c2=block.c2, active_cube=next_active
            )
            return GameState(block=new_block, bridges=state.bridges)

        # 2. Trường hợp di chuyển khối
        new_block = self._compute_next_block_state(block, action)
        if new_block is None:
            return None

        # 3. Kích hoạt công tắc & cập nhật trạng thái cầu
        new_bridges = self._apply_switches(new_block, state.bridges, prev_block=block)

        # 4. Kiểm tra xem sau khi dẫm công tắc, có rơi vào ô tách khối SPLIT_SWITCH không
        final_block = self._check_split_switch(new_block)

        next_state = GameState(block=final_block, bridges=new_bridges)

        # 5. Kiểm tra tính hợp lệ (rơi vực / vỡ gạch)
        if not self.is_valid_state(next_state):
            return None

        return next_state

    def _compute_next_block_state(self, block: BlockState, action: Action) -> Optional[BlockState]:
        """Tính tọa độ và tư thế mới của khối sau khi lăn theo một hướng."""
        r, c = block.r, block.c
        orient = block.orientation

        if orient == Orientation.STAND:
            if action == Action.UP:
                return BlockState(r=r - 2, c=c, orientation=Orientation.VERTICAL)
            elif action == Action.DOWN:
                return BlockState(r=r + 1, c=c, orientation=Orientation.VERTICAL)
            elif action == Action.LEFT:
                return BlockState(r=r, c=c - 2, orientation=Orientation.HORIZONTAL)
            elif action == Action.RIGHT:
                return BlockState(r=r, c=c + 1, orientation=Orientation.HORIZONTAL)

        elif orient == Orientation.HORIZONTAL:
            if action == Action.UP:
                return BlockState(r=r - 1, c=c, orientation=Orientation.HORIZONTAL)
            elif action == Action.DOWN:
                return BlockState(r=r + 1, c=c, orientation=Orientation.HORIZONTAL)
            elif action == Action.LEFT:
                return BlockState(r=r, c=c - 1, orientation=Orientation.STAND)
            elif action == Action.RIGHT:
                return BlockState(r=r, c=c + 2, orientation=Orientation.STAND)

        elif orient == Orientation.VERTICAL:
            if action == Action.UP:
                return BlockState(r=r - 1, c=c, orientation=Orientation.STAND)
            elif action == Action.DOWN:
                return BlockState(r=r + 2, c=c, orientation=Orientation.STAND)
            elif action == Action.LEFT:
                return BlockState(r=r, c=c - 1, orientation=Orientation.VERTICAL)
            elif action == Action.RIGHT:
                return BlockState(r=r, c=c + 1, orientation=Orientation.VERTICAL)

        elif orient == Orientation.SPLIT:
            # Di chuyển khối con đang được kích hoạt (active_cube)
            delta = {Action.UP: (-1, 0), Action.DOWN: (1, 0), Action.LEFT: (0, -1), Action.RIGHT: (0, 1)}[action]
            dr, dc = delta

            if block.active_cube == 1:
                nr1, nc1 = r + dr, c + dc
                nr2, nc2 = block.r2, block.c2
            else:
                nr1, nc1 = r, c
                nr2, nc2 = block.r2 + dr, block.c2 + dc

            # Kiểm tra hợp nhất 2 khối con thành 1x1x2 khi đứng cạnh nhau
            merged = self._try_merge_cubes(nr1, nc1, nr2, nc2)
            if merged is not None:
                return merged

            return BlockState(r=nr1, c=nc1, orientation=Orientation.SPLIT, r2=nr2, c2=nc2, active_cube=block.active_cube)

        return None

    def _try_merge_cubes(self, r1: int, c1: int, r2: int, c2: int) -> Optional[BlockState]:
        """Nếu 2 khối 1x1x1 đứng kề nhau, tự động ghép lại thành khối 1x1x2."""
        if r1 == r2:
            if c1 + 1 == c2:
                return BlockState(r=r1, c=c1, orientation=Orientation.HORIZONTAL)
            elif c2 + 1 == c1:
                return BlockState(r=r2, c=c2, orientation=Orientation.HORIZONTAL)
        elif c1 == c2:
            if r1 + 1 == r2:
                return BlockState(r=r1, c=c1, orientation=Orientation.VERTICAL)
            elif r2 + 1 == r1:
                return BlockState(r=r2, c=c2, orientation=Orientation.VERTICAL)
        return None

    def _apply_switches(
        self,
        block: BlockState,
        bridges_state: Tuple[Tuple[str, bool], ...],
        prev_block: Optional[BlockState] = None
    ) -> Tuple[Tuple[str, bool], ...]:
        """Kích hoạt công tắc nếu khối thỏa mãn điều kiện đạp lên."""
        bridge_dict = dict(bridges_state)

        # Nếu đang ở trạng thái SPLIT và vừa di chuyển 1 khối con:
        # Chỉ khối con vừa di chuyển (active_cube của prev_block) mới có khả năng kích hoạt công tắc.
        # Khối con đứng yên không được re-trigger lặp lại.
        if prev_block is not None and prev_block.orientation == Orientation.SPLIT and block.orientation == Orientation.SPLIT:
            if prev_block.active_cube == 1:
                trigger_cells = [(block.r, block.c)]
            else:
                trigger_cells = [(block.r2, block.c2)]
        else:
            trigger_cells = block.get_occupied_cells()

        for r, c in trigger_cells:
            if (r, c) in self.board.switch_map:
                sw = self.board.switch_map[(r, c)]

                # Kiểm tra điều kiện kích hoạt:
                # - SOFT: Đè lên ở bất kỳ tư thế nào (kể cả khối con 1x1x1)
                # - HEAVY: Phải ĐỨNG thẳng (khối 1x1x2) - khối con 1x1x1 không kích hoạt được
                can_trigger = False
                if sw.switch_type == TileType.SOFT_SWITCH:
                    can_trigger = True
                elif sw.switch_type in (TileType.HEAVY_SWITCH, TileType.SPLIT_SWITCH):
                    # Heavy và split switch đều chỉ được kích hoạt khi khối
                    # đứng thẳng. Split switch vẫn phải cập nhật bridge trước
                    # khi khối được dịch chuyển/tách ở bước kế tiếp.
                    can_trigger = (block.orientation == Orientation.STAND)

                if can_trigger:
                    for b_id in sw.linked_bridge_ids:
                        if b_id in bridge_dict:
                            if sw.behavior == SwitchBehavior.TOGGLE:
                                bridge_dict[b_id] = not bridge_dict[b_id]
                            elif sw.behavior in (SwitchBehavior.PERMANENT_OPEN, SwitchBehavior.PERMANENT):
                                bridge_dict[b_id] = True
                            elif sw.behavior == SwitchBehavior.PERMANENT_CLOSE:
                                bridge_dict[b_id] = False

        # Giữ thứ tự sorted để bảo đảm hash nhất quán
        return tuple((k, bridge_dict[k]) for k in sorted(bridge_dict.keys()))

    def _check_split_switch(self, block: BlockState) -> BlockState:
        """Nếu đứng lên công tắc SPLIT_SWITCH, dịch chuyển và tách thành 2 khối 1x1x1."""
        if block.orientation == Orientation.STAND:
            pos = (block.r, block.c)
            if pos in self.board.switch_map:
                sw = self.board.switch_map[pos]
                if sw.switch_type == TileType.SPLIT_SWITCH and sw.split_targets:
                    t1, t2 = sw.split_targets
                    return BlockState(
                        r=t1[0], c=t1[1], orientation=Orientation.SPLIT,
                        r2=t2[0], c2=t2[1], active_cube=1
                    )
        return block

    def get_step_cost(self, state: GameState, action: Action, next_state: GameState) -> float:
        """
        Cost risk_v1 dùng chung cho UCS/A*: di chuyển 1 + 2F + 0.5B,
        đổi cube 0.25. Chỉ gọi với transition hợp lệ; xem SPEC-ucs.md §5.
        """
        return transition_cost(self.board, state, action, next_state)
