"""Uniform-cost graph search — Trường's contribution.

The problem owns the objective shared with A*. The default fragile_v1 objective
is documented in core/cost.py; custom nonnegative costs work
without changing the search algorithm. No heuristic is used.
"""
import heapq
import math
from itertools import count
from typing import Dict, Tuple

from .base import BaseSolver, SearchResult
from core.problem import Action, BloxorzProblem
from core.state import GameState


class UCSSolver(BaseSolver):
    def __init__(self):
        super().__init__(name="Uniform-Cost Search (UCS)")

    def get_action_cost(
        self, problem: BloxorzProblem, state: GameState,
        action: Action, next_state: GameState,
    ) -> float:
        """Delegate to the shared problem cost, including custom objectives."""
        return problem.get_step_cost(state, action, next_state)

    @staticmethod
    def _validate_cost(cost: float, action: Action) -> None:
        # Integers are always finite; converting a large int to float can overflow.
        if isinstance(cost, bool) or not isinstance(cost, (int, float)):
            raise TypeError(f"Invalid cost for {action.value}: expected int/float, got {cost!r}")
        if cost < 0 or (isinstance(cost, float) and not math.isfinite(cost)):
            raise ValueError(f"Invalid cost for {action.value}: expected finite nonnegative cost, got {cost!r}")

    def _search(self, problem: BloxorzProblem) -> SearchResult:
        """Return the minimum-cost legal plan, or exhaust the finite graph.

        expanded_nodes counts valid heap pops, including the goal, but not stale
        entries. Optimality assumes every reachable edge has nonnegative cost;
        runtime validation only inspects edges that are actually considered.
        """
        start = problem.get_initial_state()
        if not problem.is_valid_state(start):
            raise ValueError("Initial state is not valid for this problem")

        counter = count()
        frontier = [(0, next(counter), start)]
        best_cost: Dict[GameState, float] = {start: 0}
        parent: Dict[GameState, Tuple[GameState, str]] = {}
        expanded_nodes = 0

        while frontier:
            current_cost, _, state = heapq.heappop(frontier)
            if current_cost > best_cost[state]:
                continue

            expanded_nodes += 1
            # A generated goal can still have an expensive, nonfinal label.
            if problem.is_goal(state):
                path = []
                cursor = state
                while cursor != start:
                    cursor, action_value = parent[cursor]
                    path.append(action_value)
                path.reverse()
                return SearchResult(
                    status="FOUND", path=path, cost=current_cost,
                    expanded_nodes=expanded_nodes,
                )

            for action in problem.get_actions(state):
                successor = problem.get_successor(state, action)
                if successor is None:
                    continue
                step_cost = self.get_action_cost(problem, state, action, successor)
                self._validate_cost(step_cost, action)
                try:
                    candidate_cost = current_cost + step_cost
                except OverflowError as error:
                    raise ValueError(f"Accumulated cost overflow for {action.value}") from error
                self._validate_cost(candidate_cost, action)

                # Strict improvement also prevents repeated zero-cost cycles.
                if candidate_cost < best_cost.get(successor, math.inf):
                    best_cost[successor] = candidate_cost
                    parent[successor] = (state, action.value)
                    # Unique insertion IDs prevent comparisons between GameStates.
                    heapq.heappush(frontier, (candidate_cost, next(counter), successor))

        return SearchResult(status="NOT_FOUND", expanded_nodes=expanded_nodes)
