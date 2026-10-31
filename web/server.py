"""Entrypoint for python main.py, python -m web.server and python web/server.py."""
from pathlib import Path
import argparse
import sys
import webbrowser

# Direct script execution needs the project root before importing the web package.
if __package__ in (None, ""):
    project_root = str(Path(__file__).resolve().parent.parent)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

from web.application import create_server
from web.config import PORT, PROJECT_DIR as _PROJECT_DIR, STAGES_DIR as _STAGES_DIR, WEB_DIR
from web.handler import BloxorzServerHandler

# Preserve the existing handler import and path constants for local integrations.
BASE_DIR = str(WEB_DIR)
PROJECT_DIR = str(_PROJECT_DIR)
STAGES_DIR = str(_STAGES_DIR)


def run(host: str = "", port: int = PORT, *, open_browser: bool = True):
    if sys.platform == "win32":
        for stream in (sys.stdout, sys.stderr):
            if hasattr(stream, "reconfigure"):
                try:
                    stream.reconfigure(encoding="utf-8")
                except (OSError, ValueError):
                    pass
    with create_server(host, port) as server:
        url = f"http://localhost:{server.server_address[1]}/index.html"
        print("=" * 60)
        print(f"🚀 Bloxorz 3D Web Server running at: {url}")
        print("💡 Nhấn Ctrl+C để dừng server.")
        print("=" * 60)
        if open_browser:
            webbrowser.open(url)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nĐã dừng server.")


def main():
    parser = argparse.ArgumentParser(description="Bloxorz local web server")
    parser.add_argument("--host", default="", help="Bind address (default: all local interfaces)")
    parser.add_argument("--port", type=int, default=PORT, help="HTTP port (default: 8080)")
    parser.add_argument("--no-browser", action="store_true", help="Start without opening a browser")
    args = parser.parse_args()
    run(args.host, args.port, open_browser=not args.no_browser)


if __name__ == "__main__":
    main()
