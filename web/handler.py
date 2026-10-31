"""HTTP routes and response formatting for the local application."""
from http.server import SimpleHTTPRequestHandler
import json
from urllib.parse import parse_qs, unquote, urlparse

from .config import STAGES_DIR, WEB_DIR
from .solver_service import SolverService, UnknownAlgorithmError
from .stages import StageNotFoundError, StageRepository


class BloxorzServerHandler(SimpleHTTPRequestHandler):
    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        ".js": "text/javascript; charset=utf-8",
        ".css": "text/css; charset=utf-8",
    }

    def __init__(self, *args, directory=None, stages=None, solver_service=None, **kwargs):
        self.stages = stages if stages is not None else StageRepository(STAGES_DIR)
        self.solver_service = solver_service or SolverService(self.stages)
        super().__init__(*args, directory=str(directory or WEB_DIR), **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path.startswith("/stages/"):
            self._serve_stage(unquote(parsed.path[len("/stages/"):]))
        elif parsed.path == "/api/stages":
            self._send_json({"stages": self.stages.list_stages()})
        elif parsed.path == "/api/solve":
            self._solve(parse_qs(parsed.query))
        else:
            super().do_GET()

    def _serve_stage(self, name: str):
        try:
            content = self.stages.read(name)
        except StageNotFoundError as error:
            self._send_json({"error": str(error)}, status=404)
            return
        self._send_bytes(content, "application/json; charset=utf-8")

    def _solve(self, params: dict):
        stage = params.get("stage", ["stage_01.json"])[0]
        algorithm = params.get("algo", ["BFS"])[0]
        try:
            self._send_json(self.solver_service.solve(stage, algorithm))
        except StageNotFoundError as error:
            self._send_json({"error": str(error)}, status=404)
        except UnknownAlgorithmError as error:
            self._send_json({"error": str(error)}, status=400)
        except NotImplementedError as error:
            self._send_json({"status": "NOT_IMPLEMENTED", "message": str(error)})
        except Exception as error:
            self._send_json({"error": str(error)}, status=500)

    def _send_json(self, data: dict, status: int = 200):
        self._send_bytes(json.dumps(data).encode("utf-8"), "application/json; charset=utf-8", status)

    def _send_bytes(self, body: bytes, content_type: str, status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)
