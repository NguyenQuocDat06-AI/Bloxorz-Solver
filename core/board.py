import json
from enum import Enum, IntEnum
from typing import List, Tuple, Dict, Optional, Any
from dataclasses import dataclass


class TileType(IntEnum):
    """Mã các loại ô trong JSON."""
    VOID = 0  # Khoảng trống.
    FLOOR = 1  # Sàn thường.
    FRAGILE = 2  # Chỉ đỡ khối nằm.
    BRIDGE = 3  # Chỉ đi được khi cầu mở.
    SOFT_SWITCH = 4  # Nhận mọi tư thế, kể cả khối đơn.
    HEAVY_SWITCH = 5  # Chỉ nhận khối đứng.
    SPLIT_SWITCH = 6  # Tách khi khối đứng.
    GOAL = 9  # Thắng khi khối đứng.


class SwitchBehavior(str, Enum):
    TOGGLE = "toggle"
    PERMANENT_OPEN = "perm_open"
    PERMANENT_CLOSE = "perm_close"
    PERMANENT = "permanent"  # Bí danh của perm_open.


@dataclass
class Bridge:
    bridge_id: str
    cells: List[Tuple[int, int]]
    initial_open: bool = False


@dataclass
class Switch:
    r: int
    c: int
    switch_type: TileType
    behavior: SwitchBehavior
    linked_bridge_ids: List[str]
    # Hai vị trí sau khi tách.
    split_targets: Optional[Tuple[Tuple[int, int], Tuple[int, int]]] = None


class Board:
    """Bàn cờ, cầu và công tắc."""
    def __init__(
        self,
        grid: List[List[int]],
        start_pos: Tuple[int, int],
        goal_pos: Tuple[int, int],
        bridges: Optional[Dict[str, Bridge]] = None,
        switches: Optional[List[Switch]] = None
    ):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0
        self.start_pos = start_pos
        self.goal_pos = goal_pos
        self.bridges = bridges or {}
        self.switches = switches or []

        self.switch_map: Dict[Tuple[int, int], Switch] = {
            (sw.r, sw.c): sw for sw in self.switches
        }

        self.bridge_cell_map: Dict[Tuple[int, int], str] = {}
        for b_id, bridge in self.bridges.items():
            for cell in bridge.cells:
                self.bridge_cell_map[tuple(cell)] = b_id

    @classmethod
    def from_json(cls, file_path: str) -> "Board":
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        grid = data["grid"]
        start_pos = (data["start"][0], data["start"][1])
        goal_pos = (data["goal"][0], data["goal"][1])

        bridges: Dict[str, Bridge] = {}
        if "bridges" in data:
            for b_id, b_info in data["bridges"].items():
                cells = [(c[0], c[1]) for c in b_info["cells"]]
                init_state = b_info.get("initial_open", False)
                bridges[b_id] = Bridge(bridge_id=b_id, cells=cells, initial_open=init_state)

        switches: List[Switch] = []
        if "switches" in data:
            for sw_info in data["switches"]:
                sw_type = TileType[sw_info["type"].upper()]
                raw_beh = sw_info.get("behavior", "toggle").lower()
                if raw_beh == "permanent":
                    behavior = SwitchBehavior.PERMANENT
                else:
                    behavior = SwitchBehavior(raw_beh)
                linked = sw_info.get("linked_bridges", [])
                targets = None
                if "split_targets" in sw_info:
                    st = sw_info["split_targets"]
                    targets = ((st[0][0], st[0][1]), (st[1][0], st[1][1]))
                switches.append(
                    Switch(
                        r=sw_info["pos"][0],
                        c=sw_info["pos"][1],
                        switch_type=sw_type,
                        behavior=behavior,
                        linked_bridge_ids=linked,
                        split_targets=targets
                    )
                )

        return cls(grid, start_pos, goal_pos, bridges, switches)

    def get_initial_bridges_tuple(self) -> Tuple[Tuple[str, bool], ...]:
        """Trạng thái cầu sắp theo ID để băm nhất quán."""
        states = [(b_id, bridge.initial_open) for b_id, bridge in sorted(self.bridges.items())]
        return tuple(states)
