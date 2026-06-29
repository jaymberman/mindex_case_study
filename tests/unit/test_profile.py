import pandas as pd

from src.profile import profile


class TestProfile:
    def test_profile_edge_cases(self):
        df = pd.read_csv("tests/data/empty_df.csv")
        audit = profile(df, "name")

        assert audit["name"]["shape"]["rows"] == 0
        assert audit["name"]["shape"]["columns"] == 3


    def test_profile_logic(self):
        df = pd.read_csv("tests/data/test_profile.csv", parse_dates=["e"])
        audit = profile(df, "name")

        assert audit["name"]["shape"]["rows"] == 10
        assert audit["name"]["shape"]["columns"] == 5

        assert audit["name"]["duplicates"]["duplicate_rows_count"] == 5
        assert audit["name"]["duplicates"]["duplicate_groups_count"] == 3

        assert audit["name"]["nulls"]["by_row_stats"]["rows_with_any_nulls"] == 6
        assert audit["name"]["nulls"]["by_row_stats"]["rows_all_null"] == 2
        assert audit["name"]["nulls"]["by_row_stats"]["max"] == 5
        assert audit["name"]["nulls"]["by_row_stats"]["min"] == 0
        assert audit["name"]["nulls"]["by_row_stats"]["mean"] == 1.4

        assert audit["name"]["nulls"]["by_column_stats"]["a"]["null_count"] == 3
        assert audit["name"]["nulls"]["by_column_stats"]["a"]["non_null_count"] == 7
        assert audit["name"]["nulls"]["by_column_stats"]["a"]["null_percentage"] == 0.3

        assert audit["name"]["nulls"]["by_column_stats"]["b"]["null_count"] == 2
        assert audit["name"]["nulls"]["by_column_stats"]["b"]["non_null_count"] == 8
        assert audit["name"]["nulls"]["by_column_stats"]["b"]["null_percentage"] == 0.2

        assert audit["name"]["nulls"]["by_column_stats"]["c"]["null_count"] == 2
        assert audit["name"]["nulls"]["by_column_stats"]["c"]["non_null_count"] == 8
        assert audit["name"]["nulls"]["by_column_stats"]["c"]["null_percentage"] == 0.2

        assert audit["name"]["nulls"]["by_column_stats"]["d"]["null_count"] == 3
        assert audit["name"]["nulls"]["by_column_stats"]["d"]["non_null_count"] == 7
        assert audit["name"]["nulls"]["by_column_stats"]["d"]["null_percentage"] == 0.3

        assert audit["name"]["nulls"]["by_column_stats"]["e"]["null_count"] == 4
        assert audit["name"]["nulls"]["by_column_stats"]["e"]["non_null_count"] == 6
        assert audit["name"]["nulls"]["by_column_stats"]["e"]["null_percentage"] == 0.4

        assert audit["name"]["numeric"]["a"]["min"] == 1.0
        assert audit["name"]["numeric"]["a"]["max"] == 5.0
        assert audit["name"]["numeric"]["a"]["mean"] == 2.7
        assert audit["name"]["numeric"]["a"]["std"] == 1.4
        assert audit["name"]["numeric"]["a"]["zeros"] == 0
        assert audit["name"]["numeric"]["a"]["negatives"] == 0

        assert audit["name"]["numeric"]["b"]["min"] == -4.1
        assert audit["name"]["numeric"]["b"]["max"] == 10.5
        assert audit["name"]["numeric"]["b"]["mean"] == 0.1
        assert audit["name"]["numeric"]["b"]["std"] == 5.3
        assert audit["name"]["numeric"]["b"]["zeros"] == 0
        assert audit["name"]["numeric"]["b"]["negatives"] == 4

        assert audit["name"]["numeric"]["d"]["min"] == 0.0
        assert audit["name"]["numeric"]["d"]["max"] == 6.0
        assert audit["name"]["numeric"]["d"]["mean"] == 4.0
        assert audit["name"]["numeric"]["d"]["std"] == 2.6
        assert audit["name"]["numeric"]["d"]["zeros"] == 1
        assert audit["name"]["numeric"]["d"]["negatives"] == 0

        assert audit["name"]["string"]["c"]["unique_values"] == 4

        assert audit["name"]["date"]["e"]["min"] == "2026-01-01"
        assert audit["name"]["date"]["e"]["max"] == "2028-01-01"
        assert audit["name"]["date"]["e"]["future_count"] == 1