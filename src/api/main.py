import datetime as dt
import json
import sqlite3
from contextlib import asynccontextmanager

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODEL_PATH: str = "data/06_models/ag_production.pkl"
    DB_NAME: str = "predictions.db"
    MODEL_VERSION: str = "v1-default"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()


class MushroomFeatures(BaseModel):
    cap_shape: str = Field(alias="cap-shape")
    cap_surface: str = Field(alias="cap-surface")
    cap_color: str = Field(alias="cap-color")
    bruises: str
    odor: str
    gill_attachment: str = Field(alias="gill-attachment")
    gill_spacing: str = Field(alias="gill-spacing")
    gill_size: str = Field(alias="gill-size")
    gill_color: str = Field(alias="gill-color")
    stalk_shape: str = Field(alias="stalk-shape")
    stalk_root: str = Field(alias="stalk-root")
    stalk_surface_above_ring: str = Field(alias="stalk-surface-above-ring")
    stalk_surface_below_ring: str = Field(alias="stalk-surface-below-ring")
    stalk_color_above_ring: str = Field(alias="stalk-color-above-ring")
    stalk_color_below_ring: str = Field(alias="stalk-color-below-ring")
    veil_type: str = Field(alias="veil-type")
    veil_color: str = Field(alias="veil-color")
    ring_number: str = Field(alias="ring-number")
    ring_type: str = Field(alias="ring-type")
    spore_print_color: str = Field(alias="spore-print-color")
    population: str
    habitat: str

    class Config:
        populate_by_name = True


class PredictionResponse(BaseModel):
    prediction: str
    model_version: str


ml_models = {}


def init_db():
    with sqlite3.connect(settings.DB_NAME) as con:
        con.execute(
            """
                    CREATE TABLE IF NOT EXISTS predictions
                    (
                        id
                        INTEGER
                        PRIMARY
                        KEY
                        AUTOINCREMENT,
                        timestamp
                        TEXT,
                        payload
                        TEXT,
                        prediction
                        TEXT,
                        model_version
                        TEXT
                    )
                    """
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    try:
        ml_models["production"] = joblib.load(settings.MODEL_PATH)
        ml_models["version"] = settings.MODEL_VERSION
    except Exception:
        ml_models["production"] = None

    yield
    # -- STOP --
    ml_models.clear()


app = FastAPI(title="Mushroom API", lifespan=lifespan)


@app.get("/healthz")
def healthz():
    if not ml_models.get("production"):
        return {"status": "unhealthy", "reason": "Model not loaded"}
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(features: MushroomFeatures):
    model = ml_models.get("production")
    if not model:
        raise HTTPException(status_code=503, detail="Model unavailable")

    input_data = features.dict(by_alias=True)
    df = pd.DataFrame([input_data])

    try:
        pred = model.predict(df)[0]

        result_str = str(pred)

        with sqlite3.connect(settings.DB_NAME) as con:
            con.execute(
                "INSERT INTO predictions (timestamp, payload, prediction, model_version) VALUES (?, ?, ?, ?)",
                (
                    dt.datetime.utcnow().isoformat(),
                    json.dumps(input_data),
                    result_str,
                    ml_models["version"],
                ),
            )

        return {"prediction": result_str, "model_version": ml_models["version"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
