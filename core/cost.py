"""Shared risk_v1 objective for legal Bloxorz transitions (see SPEC-ucs.md §5)."""
from typing import TYPE_CHECKING

from .board import Board, TileType
from .state import GameState

if TYPE_CHECKING:
    from .problem import Action


COST_PROFILE = "risk_v1"


def transition_cost(
    board: Board, state: GameState, action: "Action", next_state: GameState
) -> float:
    """Charge effort plus final-footprint exposure; legality belongs to the engine.

    Every directional move costs 1 + 2 per fragile cell + 0.5 per bridge cell.
    Both cubes contribute after a split move, including the stationary cube.
    Selecting the other cube costs 0.25 without repeating exposure charges.
    These weights express planning preferences, not failure probabilities.
    """
    # Comparing the str enum's value avoids a runtime import cycle with problem.
    if action == "SWITCH":
        return 0.25

    cells = set(next_state.block.get_occupied_cells())
    fragile_cells = sum(board.grid[r][c] == TileType.FRAGILE for r, c in cells)
    bridge_cells = sum(cell in board.bridge_cell_map for cell in cells)
    return (4 + 8 * fragile_cells + 2 * bridge_cells) / 4
