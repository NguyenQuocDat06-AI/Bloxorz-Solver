import time
import tracemalloc
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional
from core.problem import BloxorzProblem


@dataclass
class SearchResult:
    """Kết quả tìm kiếm; bộ nhớ là đỉnh tracemalloc (KiB)."""
    status: str  # FOUND hoặc NOT_FOUND.
    path: List[str] = field(default_factory=list)
    solution_length: int = 0  # Tính cả SWITCH.
    expanded_nodes: int = 0
    search_time_ms: float = 0.0
    memory_peak_kb: float = 0.0
    cost: float = 0.0


class BaseSolver(ABC):
    """Giao diện chung cho các bộ giải."""

    def __init__(self, name: str):
        self.name = name

    def solve(self, problem: BloxorzProblem) -> SearchResult:
        """Đo thời gian và bộ nhớ của _search()."""
        owns_tracer = not tracemalloc.is_tracing()
        if owns_tracer:
            tracemalloc.start()
        try:
            start_time = time.perf_counter()
            result = self._search(problem)
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            # Nếu tracer đã chạy, dùng đỉnh chung và giữ nguyên vòng đời của nó.
            _, peak_bytes = tracemalloc.get_traced_memory()
            result.search_time_ms = round(elapsed_ms, 3)
            result.memory_peak_kb = round(peak_bytes / 1024.0, 2)
            result.solution_length = len(result.path)
            return result
        finally:
            if owns_tracer:
                tracemalloc.stop()

    @abstractmethod
    def _search(self, problem: BloxorzProblem) -> SearchResult:
        pass
