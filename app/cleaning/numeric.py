import re
import pandas as pd

def safe_numeric(value, steps, col):
    if isinstance(value, str):
        v = value.strip().lower()

        if re.match(r"^\d+(\.\d+)?$", v):
            return float(v)

        if re.match(r"^\d+(\.\d+)?k$", v):
            num = float(v[:-1]) * 1_000
            steps.append(f"[{col}] converted '{value}' → {int(num)}")
            return int(num)

        if re.match(r"^\d+(\.\d+)?m$", v):
            num = float(v[:-1]) * 1_000_000
            steps.append(f"[{col}] converted '{value}' → {int(num)}")
            return int(num)

    return value
