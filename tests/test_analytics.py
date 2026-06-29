from unittest.mock import MagicMock, patch

from src.analytics import refresh_views


class TestAnalytics:
    @patch("src.analytics.open")
    def test_refresh_views(self, mock_open):
        conn = MagicMock()

        refresh_views(conn)

        mock_open.assert_called_once_with("src/db/analytics.sql", "r", encoding="utf-8")
        conn.executescript.assert_called_once()
