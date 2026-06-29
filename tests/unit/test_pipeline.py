from unittest.mock import patch

from src.pipeline import pipeline


class TestPipeline:
    @patch("src.pipeline.export_report")
    @patch("src.pipeline.refresh_views")
    @patch("src.pipeline.clean_gold")
    @patch("src.pipeline.clean_silver")
    @patch("src.pipeline.load_raw")
    @patch("src.pipeline.init_db")
    @patch("src.pipeline.sqlite3.connect")
    @patch("src.pipeline._write_profile_report")
    @patch("src.pipeline.pd.read_csv")
    def test_pipeline(self, mock_read_csv, mock_profile, mock_conn, mock_init_db, mock_load_raw, mock_clean_silver, mock_clean_gold, mock_refresh_views, mock_export_report):
        pipeline()

        assert mock_read_csv.call_count == 3

        mock_profile.assert_called_once()

        mock_conn.assert_called_once()

        mock_init_db.assert_called_once()

        assert mock_load_raw.call_count == 3

        mock_clean_silver.assert_called_once()

        mock_clean_gold.assert_called_once()

        mock_refresh_views.assert_called_once()

        mock_export_report.assert_called_once()

