from enum import IntEnum
from typing import Tuple, List, Optional
from dataclasses import dataclass


class Orientation(IntEnum):
    """
    Ba tư thế cơ bản của khối 1x1x2 và trạng thái tách khối:
    - STAND (0): Đứng thẳng trên 1 ô (r, c).
    - HORIZONTAL (1): Nằm ngang trên 2 ô kề nhau theo hàng ngang (r, c) và (r, c + 1).
    - VERTICAL (2): Nằm dọc trên 2 ô kề nhau theo cột dọc (r, c) và (r + 1, c).
    - SPLIT (3): Bị tách thành 2 khối đơn 1x1x1 độc lập.
    """
    STAND = 0
    HORIZONTAL = 1
    VERTICAL = 2
    SPLIT = 3


@dataclass(frozen=True)
class BlockState:
    """
    Biểu diễn vị trí và hình thể của khối tại một thời điểm.
    Lớp này bất biến (immutable) và hashable để làm key trong visited set / dictionary.
    """
    # Khối chính (hoặc khối 1 khi bị tách)
    r: int
    c: int
    orientation: Orientation

    # Trường dùng riêng khi khối bị tách thành 2 khối 1x1x1 (SPLIT)
    r2: Optional[int] = None
    c2: Optional[int] = None
    active_cube: int = 1  # 1 hoặc 2: khối con nào đang được điều khiển

    def get_occupied_cells(self) -> List[Tuple[int, int]]:
        """Trả về danh sách tọa độ các ô trên sàn mà khối đang chiếm giữ."""
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
        """Kiểm tra khối có đang đứng thẳng dạng 1x1x2 hay không."""
        return self.orientation == Orientation.STAND

    def is_split(self) -> bool:
        """Kiểm tra khối có đang ở trạng thái phân tách thành 2 khối con hay không."""
        return self.orientation == Orientation.SPLIT


@dataclass(frozen=True)
class GameState:
    """
    Trạng thái toàn cục đầy đủ của trò chơi Bloxorz:
    - block: Vị trí & tư thế khối.
    - bridges: Bộ tuple bất biến lưu trạng thái đóng (False) hoặc mở (True) của từng cây cầu.
    """
    block: BlockState
    # Tuple dạng (("bridge_1", True), ("bridge_2", False), ...) sắp xếp theo tên để hash đồng nhất
    bridges: Tuple[Tuple[str, bool], ...] = ()

    def get_bridge_status(self, bridge_id: str) -> bool:
        """Kiểm tra trạng thái cầu: True là mở (đi được), False là đóng (khoảng trống)."""
        for b_id, state in self.bridges:
            if b_id == bridge_id:
                return state
        return False
