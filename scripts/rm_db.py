from pathlib import Path

DB_PATH = Path("output") / "dw.db"

if DB_PATH.exists():
    DB_PATH.unlink()