from kedro.pipeline import Pipeline, node

from .nodes import (
    basic_clean,
    evaluate_autogluon,
    load_raw,
    split_data,
    train_autogluon,
)


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(load_raw, "raw_data", "loaded_data", name="load_raw"),
            node(basic_clean, "loaded_data", "clean_data", name="basic_clean"),
            node(
                split_data,
                ["clean_data", "params:split.test_size", "params:split.random_state"],
                ["X_train", "X_test", "y_train", "y_test"],
                name="split_data",
            ),
            # Sprint 2 zakomentowane bo teraz używamy auto gluon
            # node(
            #     train_baseline,
            #     ["X_train", "y_train", "params:model"],
            #     ["model_baseline", "wandb_run_id_baseline"],
            #     name="train_baseline",
            # ),
            # node(
            #     evaluate,
            #     ["model_baseline", "wandb_run_id_baseline", "X_test", "y_test"],
            #     "metrics_baseline",
            #     name="evaluate_baseline",
            # ),
            #  Sprint 3
            node(
                train_autogluon,
                ["X_train", "y_train", "params:autogluon"],
                ["ag_model", "wandb_run_id_ag"],
                name="train_autogluon",
            ),
            node(
                evaluate_autogluon,
                ["ag_model", "wandb_run_id_ag", "X_test", "y_test", "params:autogluon"],
                "ag_metrics",
                name="evaluate_autogluon",
            ),
        ]
    )
