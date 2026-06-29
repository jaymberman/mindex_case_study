from unittest.mock import MagicMock, patch

from src.export import export_report


class TestExport:
    @patch("src.export.open")
    @patch('src.export.json.dump')
    @patch('src.export.sqlite3')
    def test_export_report(self, mock_sqlite3, mock_dump, mock_open):
        conn = MagicMock()
        cursor = MagicMock()
        conn.cursor.return_value = cursor

        export_report(conn)

        assert cursor.execute.call_count == 5
        mock_dump.assert_called_once()