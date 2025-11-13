from kedro.pipeline import Pipeline, node

from .nodes import basic_clean, evaluate, load_raw, split_data, train_baseline


def create_pipeline(**kwargs):
    return Pipeline(
        [
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
        ]
    )
