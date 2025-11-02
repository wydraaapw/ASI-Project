from typing import Dict
from kedro.pipeline import Pipeline
from sprint2_kedro.pipelines.asi.pipeline import create_pipeline


def register_pipelines() -> Dict[str, Pipeline]:
    asi_pipeline = create_pipeline()

    return {
        "__default__": asi_pipeline,
        "asi": asi_pipeline,
    }
