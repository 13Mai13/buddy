from pathlib import Path

APP_DIR = Path.home() / ".onboard_ai"
DB_PATH = APP_DIR / "index.sqlite"

APP_DIR.mkdir(parents=True, exist_ok=True)
