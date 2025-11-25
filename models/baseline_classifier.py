import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from typing import Dict

# Paths
DATAFILE = "data/small_labeled.csv"
MODEL_PATH = "models/baseline.pkl"

# Ensure directories exist
os.makedirs("models", exist_ok=True)
os.makedirs("data", exist_ok=True)


def make_tiny_dataset() -> None:
    """
    Create a tiny toy labeled dataset (CSV).
    Each row is (text, label) where label 0 = real/credible, 1 = fake/sensational.
    """
    rows = [
        ("The government confirmed new policy today", 0),
        ("Celebrity endorses miracle cure — click to buy!", 1),
        ("Research shows improved results in trials", 0),
        ("Shocking: vaccine causes instant harm!", 1),
    ]
    df = pd.DataFrame(rows, columns=["text", "label"])
    df.to_csv(DATAFILE, index=False)
    print("Tiny dataset saved to", DATAFILE)


def train() -> None:
    """
    Train a TF-IDF + LogisticRegression baseline on the CSV at DATAFILE
    and save the vectorizer + model as a joblib file.
    """
    if not os.path.exists(DATAFILE):
        make_tiny_dataset()

    df = pd.read_csv(DATAFILE)
    vec = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X = vec.fit_transform(df["text"].astype(str))  # learn vocab and transform

    clf = LogisticRegression(max_iter=1000)
    clf.fit(X, df["label"])

    # Save both vectorizer and classifier so we can load them for inference
    joblib.dump((vec, clf), MODEL_PATH, compress=3)
    print("Trained & saved model to", MODEL_PATH)


# ----------------------
# Load-once helper (recommended for servers)
# ----------------------
_model_cache = None  # will hold (vec, clf) after first load


def _load_model_once():
    global _model_cache
    if _model_cache is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Run train() first.")
        _model_cache = joblib.load(MODEL_PATH)
    return _model_cache


def predict(text: str, threshold: float = 0.5) -> Dict[str, object]:
    """
    Predict whether `text` is fake.
    Returns dict: {"label": 0/1, "fake_probability": 0.0-1.0}
    Uses a load-once model for speed (good for FastAPI).
    """
    vec, clf = _load_model_once()
    X = vec.transform([text])                # X is a 1xN sparse matrix
    probs = clf.predict_proba(X)[0]         # [prob_class_0, prob_class_1]
    fake_prob = float(probs[1])
    label = int(fake_prob >= threshold)
    return {"label": label, "fake_probability": fake_prob}


if __name__ == "__main__":
    # Train a model (if needed) and test a quick prediction
    train()
    print(predict("This miracle pill cures all diseases!"))
