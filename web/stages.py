"""Load stage files and build the stage selector's metadata."""
import json
from pathlib import Path
from typing import Dict, List, Union


class StageNotFoundError(FileNotFoundError):
    """The requested name does not identify a stage in the configured directory."""

    def __init__(self, name: str):
        super().__init__(f"Stage {name} not found")


class StageRepository:
    def __init__(self, directory: Union[str, Path]):
        self.directory = Path(directory).resolve()

    def resolve(self, name: str) -> Path:
        """Accept JSON filenames from this directory, including for solve requests."""
        if (
            not name.endswith(".json")
            or Path(name).name != name
            or any(character in name for character in ("/", "\\", ":", "\x00"))
        ):
            raise StageNotFoundError(name)
        path = self.directory / name
        if path.resolve().parent != self.directory or not path.is_file():
            raise StageNotFoundError(name)
        return path

    def read(self, name: str) -> bytes:
        return self.resolve(name).read_bytes()

    def list_stages(self) -> List[Dict]:
        if not self.directory.is_dir():
            return []
        stages = []
        for path in sorted(self.directory.iterdir()):
            if not path.name.endswith(".json"):
                continue
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                stages.append(self._metadata(path.name, data))
            except (OSError, ValueError, TypeError, KeyError, IndexError, AttributeError):
                stages.append({
                    "id": path.name,
                    "name": path.name.replace(".json", "").title(),
                    "diff": "medium",
                    "mech": "Cơ bản",
                    "rows": 10,
                    "cols": 10,
                })
        return stages

    @staticmethod
    def _metadata(name: str, data: dict) -> dict:
        grid = data.get("grid", [])
        tiles = {tile for row in grid for tile in row} if grid else set()
        mechanisms = []
        if 2 in tiles:
            mechanisms.append("Gạch vỡ")
        if 3 in tiles or data.get("bridges"):
            mechanisms.append("Cầu nối")
        if 4 in tiles or 5 in tiles or data.get("switches"):
            mechanisms.append("Công tắc")
        if 6 in tiles:
            mechanisms.append("Tách khối")
        return {
            "id": name,
            "name": data.get("name", name.replace(".json", "").replace("_", " ").title()),
            "diff": str(data.get("difficulty", "medium")).lower(),
            "mech": " + ".join(mechanisms) if mechanisms else "Cơ bản",
            "rows": len(grid),
            "cols": len(grid[0]) if grid else 0,
        }
