from kedro.pipeline import Pipeline, node

from .nodes import (
    basic_clean,
    evaluate,
    evaluate_autogluon,
    load_raw,
    save_best_model,
    split_data,
    train_autogluon,
    train_baseline,
)


def create_pipeline(**kwargs):
    return Pipeline(
        [
            # baseline pipeline
            node(load_raw, "raw_data", "loaded_data"),
            node(basic_clean, "loaded_data", "clean_data"),
            node(
                split_data,
                ["clean_data", "params:split.test_size", "params:split.random_state"],
                ["X_train", "X_test", "y_train", "y_test"],
            ),
            node(
                train_baseline, ["X_train", "y_train", "params:model"], "model_baseline"
            ),
            node(evaluate, ["model_baseline", "X_test", "y_test"], "metrics_baseline"),
            # autogluon pipeline
            node(
                train_autogluon, ["X_train", "y_train", "params:autogluon"], "ag_model"
            ),
            node(
                evaluate_autogluon,
                ["ag_model", "X_test", "y_test", "params:autogluon"],
                "ag_metrics",
            ),
            node(save_best_model, "ag_model", "ag_model_production"),
        ]
    )
