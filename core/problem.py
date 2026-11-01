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
    SWITCH_CUBE = "SWITCH"


class BloxorzProblem:
    """Luật chuyển trạng thái và điều kiện đích."""

    def __init__(self, board: Board):
        self.board = board

    def get_initial_state(self) -> GameState:
        block = BlockState(
            r=self.board.start_pos[0],
            c=self.board.start_pos[1],
            orientation=Orientation.STAND
        )
        bridges = self.board.get_initial_bridges_tuple()
        return GameState(block=block, bridges=bridges)

    def is_goal(self, state: GameState) -> bool:
        """Chỉ khối đứng trên đích mới được tính thắng."""
        block = state.block
        if block.orientation == Orientation.STAND:
            return (block.r, block.c) == self.board.goal_pos
        return False

    def is_cell_passable(self, r: int, c: int, state: GameState) -> bool:
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
        """Các ô phải đỡ được khối; ô yếu chỉ đỡ khối nằm."""
        block = state.block
        cells = block.get_occupied_cells()

        for r, c in cells:
            if not self.is_cell_passable(r, c, state):
                return False

        if block.orientation == Orientation.STAND:
            r, c = block.r, block.c
            if self.board.grid[r][c] == TileType.FRAGILE:
                return False
        elif block.orientation == Orientation.SPLIT:
            if (block.r, block.c) == (block.r2, block.c2):
                return False
            for r, c in cells:
                if self.board.grid[r][c] == TileType.FRAGILE:
                    return False

        return True

    def get_actions(self, state: GameState) -> List[Action]:
        actions = [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT]
        if state.block.orientation == Orientation.SPLIT:
            actions.append(Action.SWITCH_CUBE)
        return actions

    def get_successor(self, state: GameState, action: Action) -> Optional[GameState]:
        """Trả trạng thái hợp lệ sau hành động, hoặc None."""
        block = state.block

        if action == Action.SWITCH_CUBE:
            if block.orientation != Orientation.SPLIT:
                return None
            next_active = 2 if block.active_cube == 1 else 1
            new_block = BlockState(
                r=block.r, c=block.c, orientation=Orientation.SPLIT,
                r2=block.r2, c2=block.c2, active_cube=next_active
            )
            return GameState(block=new_block, bridges=state.bridges)

        new_block = self._compute_next_block_state(block, action)
        if new_block is None:
            return None

        # Cập nhật cầu trước khi tách và kiểm tra ô đỡ.
        new_bridges = self._apply_switches(new_block, state.bridges, prev_block=block)

        final_block = self._check_split_switch(new_block)

        next_state = GameState(block=final_block, bridges=new_bridges)

        if not self.is_valid_state(next_state):
            return None

        return next_state

    def _compute_next_block_state(self, block: BlockState, action: Action) -> Optional[BlockState]:
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
            delta = {Action.UP: (-1, 0), Action.DOWN: (1, 0), Action.LEFT: (0, -1), Action.RIGHT: (0, 1)}[action]
            dr, dc = delta

            if block.active_cube == 1:
                nr1, nc1 = r + dr, c + dc
                nr2, nc2 = block.r2, block.c2
            else:
                nr1, nc1 = r, c
                nr2, nc2 = block.r2 + dr, block.c2 + dc

            merged = self._try_merge_cubes(nr1, nc1, nr2, nc2)
            if merged is not None:
                return merged

            return BlockState(r=nr1, c=nc1, orientation=Orientation.SPLIT, r2=nr2, c2=nc2, active_cube=block.active_cube)

        return None

    def _try_merge_cubes(self, r1: int, c1: int, r2: int, c2: int) -> Optional[BlockState]:
        """Ghép hai khối đơn khi kề cạnh."""
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
        """Cập nhật cầu theo các công tắc vừa chạm."""
        bridge_dict = dict(bridges_state)

        # Khi tách, chỉ khối vừa di chuyển kích hoạt công tắc.
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

                can_trigger = False
                if sw.switch_type == TileType.SOFT_SWITCH:
                    can_trigger = True
                elif sw.switch_type in (TileType.HEAVY_SWITCH, TileType.SPLIT_SWITCH):
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

        # Sắp theo ID để băm nhất quán.
        return tuple((k, bridge_dict[k]) for k in sorted(bridge_dict.keys()))

    def _check_split_switch(self, block: BlockState) -> BlockState:
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
        return transition_cost(self.board, state, action, next_state)
