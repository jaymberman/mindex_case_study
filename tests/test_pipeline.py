from unittest.mock import patch

from src.pipeline import pipeline


class TestPipeline:
    def test_pipeline_writes_profiles(self):
        with patch("src.pipeline._write_profile_report") as mock_profile:
            pipeline()
            mock_profile.assert_called_once()