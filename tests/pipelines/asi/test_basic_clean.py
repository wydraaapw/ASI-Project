import pandas as pd

from sprint2_kedro.pipelines.asi.nodes import basic_clean, load_raw


def test_no_missing_values_after_clean():
    raw_data = pd.read_csv("data/01_raw/mushrooms.csv", header=None)

    loaded = load_raw(raw_data)
    cleaned = basic_clean(loaded)

    assert (
        cleaned.isna().sum().sum() == 0
    ), "Znaleziono brakujące wartości po czyszczeniu"
