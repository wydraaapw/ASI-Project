import random

import numpy as np
import pandas as pd
from autogluon.tabular import TabularPredictor
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

import wandb


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
    y_pred = model.predict(X_test)
    f1 = f1_score(y_test, y_pred)
    wandb.log({"f1": f1})
    return {"f1": f1}


def train_autogluon(X_train: pd.DataFrame, y_train: pd.Series, params: dict):

    wandb.init(project="mushrooms", job_type="ag-train", config=params)

    train_data = pd.concat([X_train, y_train], axis=1)

    seed = params.get("seed", 42)
    random.seed(seed)
    np.random.seed(seed)

    predictor = TabularPredictor(
        label=params["label"],
        eval_metric=params["eval_metric"],
        problem_type=params["problem_type"],
    ).fit(
        train_data=train_data,
        time_limit=params["time_limit"],
        presets=params["presets"],
    )

    wandb.finish()
    return predictor


def evaluate_autogluon(
    predictor, X_test: pd.DataFrame, y_test: pd.Series, params: dict
):
    wandb.init(project="mushrooms", job_type="ag-eval", config=params)

    y_pred = predictor.predict(X_test)
    metric_name = params.get("eval_metric", "f1")

    if metric_name == "f1":
        from sklearn.metrics import f1_score

        score = f1_score(y_test, y_pred)
    elif metric_name == "accuracy":
        from sklearn.metrics import accuracy_score

        score = accuracy_score(y_test, y_pred)
    else:
        score = None

    wandb.log({metric_name: score})

    try:
        fi = predictor.feature_importance(X_test)
        fi_path = "data/09_tracking/ag_feature_importance.csv"
        fi.to_csv(fi_path)
        wandb.log({"feature_importance": wandb.Table(dataframe=fi)})
    except Exception:
        pass

    wandb.finish()
    return {metric_name: score}


def save_best_model(predictor):
    return predictor
