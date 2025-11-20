import random
import shutil

import numpy as np
import pandas as pd
from autogluon.tabular import TabularPredictor
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

import wandb


# Sprint 2
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

    run = wandb.init(
        project="mushrooms",
        job_type="train",
        config=params,
        reinit=True,
        name="Baseline_LogReg",
    )
    run_id = run.id

    model = LogisticRegression(max_iter=params.get("max_iter", 1000))
    model.fit(X_train, y_train)

    run.finish()
    return model, run_id


def evaluate(model, run_id, X_test, y_test):
    # Loguowanie F1
    run = wandb.init(project="mushrooms", id=run_id, resume="must", reinit=True)

    y_pred = model.predict(X_test)
    f1 = f1_score(y_test, y_pred, average="weighted")

    wandb.log({"f1_baseline": f1})

    run.finish()
    return {"f1": f1}


# Sprint 3


def train_autogluon(X_train: pd.DataFrame, y_train: pd.Series, params: dict):

    preset_name = params.get("presets", "default")
    run_name = f"AutoGluon_{preset_name}"

    # 1. Start Runu
    run = wandb.init(
        project="mushrooms",
        job_type="ag-train",
        config=params,
        reinit=True,
        name=run_name,
    )
    run_id = run.id

    train_data = pd.concat([X_train, y_train], axis=1)

    seed = params.get("seed", 42)
    random.seed(seed)
    np.random.seed(seed)

    ag_path = "data/06_models/ag_tmp_run"
    try:
        shutil.rmtree(ag_path)
    except FileNotFoundError:
        pass

    predictor = TabularPredictor(
        label=params["label"],
        eval_metric=params["eval_metric"],
        problem_type=params["problem_type"],
        path=ag_path,
    ).fit(
        train_data=train_data,
        time_limit=params["time_limit"],
        presets=params["presets"],
    )

    art = wandb.Artifact(name=f"ag_model_{run.id}", type="model")
    art.add_dir(ag_path)

    # oznaczamy jako candidate
    run.log_artifact(art, aliases=["candidate"])

    run.finish()
    return predictor, run_id


def evaluate_autogluon(
    predictor, run_id: str, X_test: pd.DataFrame, y_test: pd.Series, params: dict
):
    run = wandb.init(project="mushrooms", id=run_id, resume="must", reinit=True)

    y_pred = predictor.predict(X_test)
    metric_name = params.get("eval_metric", "f1")

    score = 0
    if "f1" in metric_name:
        score = f1_score(y_test, y_pred, average="weighted")
    elif "acc" in metric_name:
        score = accuracy_score(y_test, y_pred)

    wandb.log({metric_name: score})

    test_data = pd.concat([X_test, y_test], axis=1)
    fi = predictor.feature_importance(data=test_data)

    wandb.log({"feature_importance": wandb.Table(dataframe=fi.reset_index())})
    fi.to_csv("data/09_tracking/ag_feature_importance.csv")

    run.finish()
    return {metric_name: score}
