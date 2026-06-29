from unittest.mock import MagicMock, patch

from src.db.init_db import init_db


class TestAnalytics:
    @patch("src.db.init_db.open")
    def test_init_db(self, mock_open):
        conn = MagicMock()

        init_db(conn)

        mock_open.assert_called_once_with("src/db/ddls.sql")
        conn.executescript.assert_called_once()
