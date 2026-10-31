"""UCS fragile_v1 objective, exposed through the shared problem cost API."""
from typing import TYPE_CHECKING

from .board import Board, TileType
from .state import GameState

if TYPE_CHECKING:
    from .problem import Action


COST_PROFILE = "fragile_v1"


def transition_cost(
    board: Board, state: GameState, action: "Action", next_state: GameState
) -> float:
    """Charge 3 for a fragile landing, 1 for other rolls, 0.25 for control.

    The fragile surcharge applies once per roll, even over two fragile cells.
    Bridges and switch activation have no surcharge or discount. These are
    planning preferences, not failure probabilities. Only legal edges qualify.
    """
    # Comparing the str enum's value avoids a runtime import cycle with problem.
    if action == "SWITCH":
        return 0.25

    if any(board.grid[r][c] == TileType.FRAGILE
           for r, c in next_state.block.get_occupied_cells()):
        return 3.0
    return 1.0
