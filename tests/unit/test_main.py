from unittest.mock import patch

from main import main


class TestMain:
    def test_main_calls_pipeline_once(self):
        with patch("main.pipeline") as mock_pipeline:
            main()
            mock_pipeline.assert_called_once()