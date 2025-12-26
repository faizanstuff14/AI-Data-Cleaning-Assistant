import pandas as pd
from app.cleaning.schema import infer_column_types
from app.cleaning.numeric import safe_numeric
from app.cleaning.text import clean_text
from app.cleaning.missing import handle_missing


def clean_any_dataset(state):
    df = state["df"]
    steps = state["steps"]

    schema = infer_column_types(df)

    for col, col_type in schema.items():
        if col_type in ("numeric", "numeric_text"):
            df[col] = df[col].apply(lambda x: safe_numeric(x, steps, col))
            df[col] = pd.to_numeric(df[col], errors="coerce")

        elif col_type == "categorical":
            df[col] = clean_text(df[col], steps, col)

        df[col] = handle_missing(df[col], steps, col)

    state["df"] = df
    return state
