from unittest.mock import MagicMock

from src.load import load_raw


class TestLoad:
    def test_load_raw_calls_to_sql(self):
        df = MagicMock()
        conn = MagicMock()
        load_raw(df, conn, "table")

        df.to_sql.assert_called_once()