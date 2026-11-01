"""Tạo máy chủ HTTP và các dịch vụ."""
from functools import partial
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Union

from .config import PORT, STAGES_DIR, WEB_DIR
from .handler import BloxorzServerHandler
from .solver_service import SolverService
from .stages import StageRepository


def create_server(
    host: str = "", port: int = PORT, *,
    web_dir: Union[str, Path] = WEB_DIR, stages_dir: Union[str, Path] = STAGES_DIR,
) -> ThreadingHTTPServer:
    stages = StageRepository(stages_dir)
    handler = partial(
        BloxorzServerHandler, directory=web_dir,
        stages=stages, solver_service=SolverService(stages),
    )
    return ThreadingHTTPServer((host, port), handler)
