"""Select Python solvers and serialize their results independently of HTTP."""
from functools import partial
from threading import Lock

from core.board import Board
from core.problem import BloxorzProblem
from solvers import AStarSolver, BFSSolver, DFSSolver, UCSSolver

from .stages import StageRepository


class UnknownAlgorithmError(ValueError):
    pass


SOLVER_FACTORIES = {
    "BFS": BFSSolver,
    "DFS": DFSSolver,
    "IDS": partial(DFSSolver, use_ids=True),
    "UCS": UCSSolver,
    "ASTAR": AStarSolver,
    "A*": AStarSolver,
}

# tracemalloc is process-wide: HTTP asset requests may run concurrently, but
# separate solver searches must not start/stop each other's measurement scope.
_SEARCH_LOCK = Lock()


class SolverService:
    def __init__(self, stages: StageRepository):
        self.stages = stages

    def solve(self, stage_name: str, algorithm: str) -> dict:
        stage_path = self.stages.resolve(stage_name)
        algorithm = algorithm.upper()
        try:
            factory = SOLVER_FACTORIES[algorithm]
        except KeyError:
            raise UnknownAlgorithmError(f"Unknown algorithm: {algorithm}") from None
        with _SEARCH_LOCK:
            problem = BloxorzProblem(Board.from_json(str(stage_path)))
            solver = factory()
            result = solver.solve(problem)
        return {
            "stage": stage_name,
            "algorithm": solver.name,
            "status": result.status,
            "path": result.path,
            "steps": result.solution_length,
            "expanded_nodes": result.expanded_nodes,
            "time_ms": result.search_time_ms,
            "memory_kb": result.memory_peak_kb,
            "cost": result.cost,
        }
