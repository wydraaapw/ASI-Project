import pandas as pd

from sprint2_kedro.pipelines.asi.nodes import split_data


def test_split_data_simple():
    df = pd.DataFrame(
        {
            "class": [0, 1, 0, 1, 0],
            "feat1": [10, 20, 30, 40, 50],
            "feat2": ["a", "b", "c", "d", "e"],
        }
    )

    test_size = 0.4
    random_state = 42

    X_train, X_test, y_train, y_test = split_data(df, test_size, random_state)

    assert len(X_train) == 3  # noqa: PLR2004
    assert len(X_test) == 2  # noqa: PLR2004
    assert len(y_train) == 3  # noqa: PLR2004
    assert len(y_test) == 2  # noqa: PLR2004

    # brak target leakate
    assert "class" not in X_train.columns
    assert "class" not in X_test.columns
