from unittest.mock import MagicMock, Mock, patch

import pandas as pd

from src.sprint2_kedro.pipelines.asi.nodes import evaluate_autogluon


@patch("src.sprint2_kedro.pipelines.asi.nodes.wandb")
def test_evaluate_autogluon(mock_wandb):
    """Test sprawdza czy evaluate_autogluon zwraca słownik z metryką w zakresie [0, 1]"""

    mock_run = MagicMock()
    mock_wandb.init.return_value = mock_run

    mock_predictor = Mock()
    mock_predictor.predict.return_value = pd.Series([0, 1, 0, 1])
    mock_predictor.feature_importance.return_value = pd.DataFrame(
        {"importance": [0.5, 0.3, 0.2]}
    )

    X_test = pd.DataFrame({"feat1": [1, 2, 3, 4]})
    y_test = pd.Series([0, 1, 0, 1])
    params = {"eval_metric": "f1"}

    result = evaluate_autogluon(mock_predictor, "test_run", X_test, y_test, params)

    assert isinstance(result, dict), "Wynik powinien być słownikiem"
    assert "f1" in result, "Słownik powinien zawierać klucz 'f1'"
    assert (
        0 <= result["f1"] <= 1
    ), f"F1 score powinien być w [0,1], jest: {result['f1']}"
