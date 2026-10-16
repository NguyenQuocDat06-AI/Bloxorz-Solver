import json
from enum import Enum, IntEnum
from typing import List, Tuple, Dict, Optional, Any
from dataclasses import dataclass


class TileType(IntEnum):
    """Phân loại các ô trên mặt sàn theo đề bài Project 1."""
    VOID = 0           # Khoảng trống / Vực thẳm (rơi = thua)
    FLOOR = 1          # Ô bình thường, chịu được khối ở mọi tư thế
    FRAGILE = 2        # Gạch vỡ màu cam (chỉ chịu được khi khối nằm, đứng lên sẽ vỡ)
    BRIDGE = 3         # Ô cầu nối (mở thì là FLOOR, đóng thì là VOID)
    SOFT_SWITCH = 4    # Công tắc mềm (hình tròn/bát giác): kích hoạt khi đè lên ở bất kỳ tư thế nào
    HEAVY_SWITCH = 5   # Công tắc nặng (hình chữ X): chỉ kích hoạt khi khối ĐỨNG thẳng lên
    SPLIT_SWITCH = 6   # Công tắc tách khối: chỉ kích hoạt khi khối ĐỨNG thẳng lên
    GOAL = 9           # Ô đích (chỉ thắng khi khối ĐỨNG thẳng lên ô này)


class SwitchBehavior(str, Enum):
    """Hành vi của công tắc khi được kích hoạt."""
    TOGGLE = "toggle"             # Đảo trạng thái cầu (Đóng <-> Mở)
    PERMANENT_OPEN = "perm_open"   # Luôn mở cầu sau khi kích hoạt
    PERMANENT_CLOSE = "perm_close" # Luôn đóng cầu sau khi kích hoạt


@dataclass
class Bridge:
    """Đại diện một cây cầu được điều khiển bởi công tắc."""
    bridge_id: str
    cells: List[Tuple[int, int]]
    initial_open: bool = False


@dataclass
class Switch:
    """Đại diện một công tắc kích hoạt trên bản đồ."""
    r: int
    c: int
    switch_type: TileType
    behavior: SwitchBehavior
    linked_bridge_ids: List[str]
    # Tọa độ dịch chuyển khi rơi vào SPLIT_SWITCH: ((r1, c1), (r2, c2))
    split_targets: Optional[Tuple[Tuple[int, int], Tuple[int, int]]] = None


class Board:
    """
    Biểu diễn bàn cờ Bloxorz đọc từ file JSON / cấu hình.
    """
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

        # Tra cứu nhanh công tắc theo tọa độ
        self.switch_map: Dict[Tuple[int, int], Switch] = {
            (sw.r, sw.c): sw for sw in self.switches
        }

        # Tra cứu nhanh ô nào thuộc cầu nào
        self.bridge_cell_map: Dict[Tuple[int, int], str] = {}
        for b_id, bridge in self.bridges.items():
            for cell in bridge.cells:
                self.bridge_cell_map[tuple(cell)] = b_id

    @classmethod
    def from_json(cls, file_path: str) -> "Board":
        """Đọc và khởi tạo bàn cờ từ file JSON chuẩn."""
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
                behavior = SwitchBehavior(sw_info.get("behavior", "toggle"))
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
        """Tạo tuple trạng thái cầu ban đầu (được sắp xếp theo ID) để khởi tạo GameState."""
        states = [(b_id, bridge.initial_open) for b_id, bridge in sorted(self.bridges.items())]
        return tuple(states)
