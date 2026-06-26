from typing import Optional

import numpy as np
import pandas as pd


def profile(df: pd.DataFrame, name: Optional[str] = None) -> dict:
    audit = {}

    audit["shape"] = {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1])
    }

    audit["duplicates"] = {
        "duplicate_rows_count": int(df.duplicated().sum()),
        "duplicate_groups_count": int((df.groupby(list(df.columns), dropna=False).size() > 1).sum())
    }

    null_by_col = df.isna().sum()
    null_by_row = df.isna().sum(axis=1)
    total_rows = len(df)
    if not null_by_col.empty:
        by_column_stats = {
            col: {
                "null_count": int(count),
                "non_null_count": int(total_rows - count),
                "null_percentage": float(count / total_rows) if total_rows > 0 else 0.0
            }
            for col, count in null_by_col.items()
        }
    else:
        by_column_stats = None

    if not null_by_row.empty:
        by_row_stats= {
            "max": int(null_by_row.max()),
            "min": int(null_by_row.min()),
            "mean": float(null_by_row.mean()),
            "rows_with_any_nulls": int((null_by_row > 0).sum()),
            "rows_all_null": int((null_by_row == df.shape[1]).sum())
        }
    else:
        by_row_stats = None
    audit["nulls"] = {"by_column_stats": by_column_stats, "by_row_stats": by_row_stats}

    numeric = df.select_dtypes(include=[np.number])
    if not numeric.empty:
        audit["numeric"] = {}
        for col in numeric.columns:
            series = numeric[col]
            audit["numeric"][col] = {
                "min": float(series.min()),
                "max": float(series.max()),
                "mean": round(float(series.mean()),1),
                "std": round(float(series.std()),1),
                "zeros": int((series == 0).sum()),
                "negatives": int((series < 0).sum())
            }

    string = df.select_dtypes(include=["str"])
    if not string.empty:
        audit["string"] = {
            col: {
                "unique_values": int(string[col].nunique(dropna=True)),
            }
            for col in string.columns
        }

    date_cols = df.select_dtypes(include=["datetime64[ns]", "datetimetz"]).columns.tolist()
    if len(date_cols) > 0:
        today = pd.Timestamp.today().normalize()
        audit["date"] = {
            col: {
                "min": (df[col].min()).strftime("%Y-%m-%d"),
                "max": (df[col].max()).strftime("%Y-%m-%d"),
                "future_count": int((df[col] > today).sum())
            }
            for col in date_cols
        }

    if name is not None:
        return {name: audit}

    return audit