import time
import tracemalloc
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional
from core.problem import BloxorzProblem


@dataclass
class SearchResult:
    """
    Kết quả chuẩn trả về sau khi thực thi thuật toán tìm kiếm.
    Đáp ứng đầy đủ 4 tiêu chí đo đạc thực nghiệm của đề bài:
    1. search_time_ms: Thời gian tìm kiếm (ms).
    2. memory_peak_kb: Dung lượng RAM đỉnh tiêu thụ (KB).
    3. expanded_nodes: Tổng số node đã được mở rộng.
    4. solution_length: Số bước của đường đi tìm được.
    """
    status: str                         # "FOUND" hoặc "NOT_FOUND"
    path: List[str] = field(default_factory=list)  # Danh sách nước đi ['RIGHT', 'DOWN', ...]
    solution_length: int = 0            # Số bước di chuyển
    expanded_nodes: int = 0             # Số node được lấy ra từ Frontier để duyệt
    search_time_ms: float = 0.0         # Thời gian tìm kiếm
    memory_peak_kb: float = 0.0         # Bộ nhớ đỉnh tiêu thụ
    cost: float = 0.0                   # Tổng chi phí đường đi (quan trọng với UCS và A*)


class BaseSolver(ABC):
    """
    Lớp cơ sở trừu tượng cho tất cả các thuật toán tìm kiếm.
    Mọi thành viên (Phúc, Đức, Trường, Quân) đều kế thừa lớp này.
    """

    def __init__(self, name: str):
        self.name = name

    def solve(self, problem: BloxorzProblem) -> SearchResult:
        """
        Bọc việc đo lường bộ nhớ (tracemalloc) và thời gian thực thi (time.perf_counter),
        sau đó gọi hàm _search() do từng thành viên tự code.
        """
        owns_tracer = not tracemalloc.is_tracing()
        if owns_tracer:
            tracemalloc.start()
        try:
            start_time = time.perf_counter()
            result = self._search(problem)
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            # With a caller-owned tracer, this is its process-wide peak; do not
            # reset it or stop tracing allocations on the caller's behalf.
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
        """
        Phương thức trừu tượng - Thành viên được phân công PHẢI tự viết code tại đây.
        """
        pass
