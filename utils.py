import pandas as pd


def load_dataset(path: str):
    df = pd.read_csv(path)
    return df


def append_case(path: str, case: dict):
    df = pd.read_csv(path)
    df = df.append(case, ignore_index=True)
    df.to_csv(path, index=False)


def normalize_age(age: int):
    # keep age 0–100
    return max(0, min(100, int(age)))
