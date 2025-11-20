import os


def test_project_structure():
    assert os.path.exists("conf/base/parameters.yml")
    assert os.path.exists("data/06_models/ag_production.pkl")
