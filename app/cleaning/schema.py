import pandas as pd

def infer_column_types(df: pd.DataFrame):
    schema = {}

    for col in df.columns:
        series = df[col]

        if pd.api.types.is_numeric_dtype(series):
            schema[col] = "numeric"

        elif pd.api.types.is_datetime64_any_dtype(series):
            schema[col] = "datetime"

        elif series.dtype == object:
            # detect numeric-like text
            sample = series.dropna().astype(str).head(20)
            numeric_ratio = sample.str.match(r"^\d+(\.\d+)?[kKmM]?$").mean()

            if numeric_ratio > 0.6:
                schema[col] = "numeric_text"
            else:
                schema[col] = "categorical"

        else:
            schema[col] = "unknown"

    return schema
