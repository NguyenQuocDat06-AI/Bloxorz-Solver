"""Đường dẫn và cấu hình mặc định của máy chủ."""
from pathlib import Path

WEB_DIR = Path(__file__).resolve().parent
PROJECT_DIR = WEB_DIR.parent
STAGES_DIR = PROJECT_DIR / "stages"
PORT = 8080
