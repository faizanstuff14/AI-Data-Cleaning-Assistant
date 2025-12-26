def clean_text(series, steps, col):
    before = series.copy()
    series = series.astype(str).str.strip().str.lower()

    if not before.equals(series):
        steps.append(f"[{col}] normalized text (trim + lowercase)")

    return series
