import pandas as pd
import wandb
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


def load_raw(raw_data: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "class",
        "cap-shape",
        "cap-surface",
        "cap-color",
        "bruises",
        "odor",
        "gill-attachment",
        "gill-spacing",
        "gill-size",
        "gill-color",
        "stalk-shape",
        "stalk-root",
        "stalk-surface-above-ring",
        "stalk-surface-below-ring",
        "stalk-color-above-ring",
        "stalk-color-below-ring",
        "veil-type",
        "veil-color",
        "ring-number",
        "ring-type",
        "spore-print-color",
        "population",
        "habitat",
    ]
    raw_data.columns = columns
    return raw_data


def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna()
    le = LabelEncoder()
    for col in df.columns:
        df[col] = le.fit_transform(df[col])
    return df


def split_data(df: pd.DataFrame, test_size: float, random_state: int):
    X = df.drop("class", axis=1)
    y = df["class"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    return X_train, X_test, y_train, y_test


def train_baseline(X_train, y_train, params):
    wandb.init(project="mushrooms", job_type="train", config=params)
    model = LogisticRegression(max_iter=params.get("max_iter", 1000))
    model.fit(X_train, y_train)
    return model


def evaluate(model, X_test, y_test):
    y_pred = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_pred)
    wandb.log({"roc_auc": auc})
    return {"roc_auc": auc}
