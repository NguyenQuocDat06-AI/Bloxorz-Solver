from enum import IntEnum
from typing import Tuple, List, Optional
from dataclasses import dataclass


class Orientation(IntEnum):
    """Tư thế khối; (r, c) là ô trên cùng hoặc bên trái."""
    STAND = 0
    HORIZONTAL = 1
    VERTICAL = 2
    SPLIT = 3


@dataclass(frozen=True)
class BlockState:
    """Trạng thái khối bất biến, dùng làm khóa tìm kiếm."""
    r: int
    c: int
    orientation: Orientation

    # Tọa độ khối thứ hai khi tách.
    r2: Optional[int] = None
    c2: Optional[int] = None
    active_cube: int = 1  # 1 hoặc 2.

    def get_occupied_cells(self) -> List[Tuple[int, int]]:
        """Liệt kê các ô khối đang chiếm."""
        if self.orientation == Orientation.STAND:
            return [(self.r, self.c)]
        elif self.orientation == Orientation.HORIZONTAL:
            return [(self.r, self.c), (self.r, self.c + 1)]
        elif self.orientation == Orientation.VERTICAL:
            return [(self.r, self.c), (self.r + 1, self.c)]
        elif self.orientation == Orientation.SPLIT:
            cells = [(self.r, self.c)]
            if self.r2 is not None and self.c2 is not None:
                cells.append((self.r2, self.c2))
            return cells
        return []

    def is_standing(self) -> bool:
        return self.orientation == Orientation.STAND

    def is_split(self) -> bool:
        return self.orientation == Orientation.SPLIT


@dataclass(frozen=True)
class GameState:
    """Trạng thái khối và các cầu."""
    block: BlockState
    # Sắp theo ID để băm nhất quán.
    bridges: Tuple[Tuple[str, bool], ...] = ()

    def get_bridge_status(self, bridge_id: str) -> bool:
        """True nếu cầu mở; ID không tồn tại trả False."""
        for b_id, state in self.bridges:
            if b_id == bridge_id:
                return state
        return False
