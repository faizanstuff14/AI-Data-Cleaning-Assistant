import pandas as pd

def handle_missing(series, steps, col):
    if series.isna().sum() == 0:
        return series

    if pd.api.types.is_numeric_dtype(series):
        fill = series.median()
        series = series.fillna(fill)
        steps.append(f"[{col}] filled missing values with median ({fill})")

    else:
        series = series.fillna("unknown")
        steps.append(f"[{col}] filled missing values with 'unknown'")

    return series
