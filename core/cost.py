"""Hàm chi phí risk_v1."""
from typing import TYPE_CHECKING

from .board import Board, TileType
from .state import GameState

if TYPE_CHECKING:
    from .problem import Action


COST_PROFILE = "risk_v1"


def transition_cost(
    board: Board, state: GameState, action: "Action", next_state: GameState
) -> float:
    """Di chuyển: 1 + 2F + 0.5B; đổi khối: 0.25.
    F: ô yếu, B: ô cầu trong dấu chân cuối bước, gồm cả khối đứng yên.
    Chỉ dùng với bước đi hợp lệ.
    """
    # So sánh chuỗi để tránh import vòng với problem.
    if action == "SWITCH":
        return 0.25

    cells = set(next_state.block.get_occupied_cells())
    fragile_cells = sum(board.grid[r][c] == TileType.FRAGILE for r, c in cells)
    bridge_cells = sum(cell in board.bridge_cell_map for cell in cells)
    return (4 + 8 * fragile_cells + 2 * bridge_cells) / 4
