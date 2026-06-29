from unittest.mock import MagicMock, patch

from src.cleanse import clean_gold, clean_silver


class TestCleanse:
    @patch("src.cleanse.open")
    def test_clean_silver(self, mock_open):
        conn = MagicMock()

        clean_silver(conn)

        mock_open.assert_called_once_with("src/db/silver.sql", "r", encoding="utf-8")
        conn.executescript.assert_called_once()


    @patch("src.cleanse.open")
    def test_clean_gold(self, mock_open):
        conn = MagicMock()

        clean_gold(conn)

        mock_open.assert_called_once_with("src/db/gold.sql", "r", encoding="utf-8")
        conn.executescript.assert_called_once()