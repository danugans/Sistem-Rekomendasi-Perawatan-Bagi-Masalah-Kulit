import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import OneHotEncoder


class CBRSystem:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy().reset_index(drop=True)
        self.feature_cols = [
            "age", "gender", "skin_type",
            "acne", "blackheads", "dryness",
            "redness", "dark_spots", "aging"
        ]
        self._prepare_model()

    def _prepare_model(self):
        # Prepare feature matrix
        X = self._build_feature_matrix(self.df)
        self.nn = NearestNeighbors(n_neighbors=5, metric='cosine')
        self.nn.fit(X)
        self.X = X

    def _build_feature_matrix(self, df):
        # Normalize age 0-1
        age = df["age"].astype(float).clip(0, 100).values.reshape(-1, 1) / 100.0

        # Encode gender & skin type
        cat = df[["gender", "skin_type"]].astype(str)
        self.ohe = OneHotEncoder(sparse=False, handle_unknown="ignore")
        cat_enc = self.ohe.fit_transform(cat)

        # Numeric symptoms
        symp = df[[
            "acne", "blackheads", "dryness",
            "redness", "dark_spots", "aging"
        ]].astype(float).values

        X = np.hstack([age, cat_enc, symp])
        return X

    def retrieve(self, query: dict, k=3):
        q_df = pd.DataFrame([query])

        q_age = q_df["age"].astype(float).clip(0, 100).values.reshape(-1, 1) / 100.0
        cat = q_df[["gender", "skin_type"]].astype(str)
        cat_enc = self.ohe.transform(cat)
        symp = q_df[[
            "acne", "blackheads", "dryness",
            "redness", "dark_spots", "aging"
        ]].astype(float).values

        qX = np.hstack([q_age, cat_enc, symp])

        dists, idxs = self.nn.kneighbors(qX, n_neighbors=min(k, len(self.df)))

        results = []
        for dist, i in zip(dists[0], idxs[0]):
            case = self.df.loc[i].to_dict()
            results.append((case, float(dist)))

        return results

    def reuse(self, case: dict):
        # default: return solution of most similar case
        return case.get("solution", "")

    def next_id(self):
        if "id" in self.df.columns and not self.df["id"].isnull().all():
            return int(self.df["id"].max()) + 1
        return len(self.df) + 1
