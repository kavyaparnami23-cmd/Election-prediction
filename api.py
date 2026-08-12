"""
Author      : Kavya Parnami
Project     : ElectionPulse AI
Description : FastAPI Backend — REST prediction API
              Serves at http://localhost:8000

Run:
    uvicorn api:app --reload --port 8000
"""

import sys
import os
from typing import Literal
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# ── Force cwd to project root so Config.ROOT_DIR resolves correctly ──────────
# This ensures artifacts/models/best_model.pkl is always found,
# regardless of which directory uvicorn was launched from.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_ROOT)
sys.path.insert(0, PROJECT_ROOT)

from src.pipeline.prediction_pipeline import PredictionPipeline
from src.components.prediction import KNOWN_STATES

# ─────────────────────────────────────────────────────────────
# Startup: preload the pipeline so /api/health shows true
# ─────────────────────────────────────────────────────────────

_pipeline: PredictionPipeline | None = None
_load_error: str | None = None


def get_pipeline() -> PredictionPipeline:
    global _pipeline, _load_error
    if _pipeline is None:
        try:
            _pipeline = PredictionPipeline()
        except Exception as e:
            _load_error = str(e)
            raise HTTPException(status_code=503, detail=f"Model not loaded. Error: {e}")
    return _pipeline


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the ML pipeline once at server startup."""
    global _pipeline, _load_error
    model_path = os.path.join(PROJECT_ROOT, "artifacts", "models", "best_model.pkl")
    print(f"[ElectionPulse] Loading model from: {model_path}")
    try:
        _pipeline = PredictionPipeline()
        print("[ElectionPulse] SUCCESS: Model loaded!")
    except FileNotFoundError as e:
        _load_error = str(e)
        print(f"[ElectionPulse] ERROR - Model not found: {e}")
        print("[ElectionPulse] Run the training pipeline first to generate artifacts/models/best_model.pkl")
    except Exception as e:
        _load_error = str(e)
        print(f"[ElectionPulse] ERROR loading model: {e}")
    yield
    # Cleanup on shutdown (nothing needed)


# ─────────────────────────────────────────────────────────────
# App
# ─────────────────────────────────────────────────────────────

app = FastAPI(
    title="ElectionPulse AI — Prediction API",
    description="Lok Sabha election winner prediction using Random Forest + XGBoost",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Allow React dev server (port 3000) to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────────────────────
# Schemas
# ─────────────────────────────────────────────────────────────

class CandidateRequest(BaseModel):
    year:              int   = Field(2019,   ge=1951, le=2035, description="Election year")
    st_name:           str   = Field("Maharashtra",            description="State / UT name")
    constituency_name: str | None = Field(None,                description="Constituency name")
    pc_no:             int   = Field(24,     ge=1, le=543,     description="Constituency number")
    pc_type:           str   = Field("GEN",                    description="GEN | SC | ST")
    cand_sex: Literal["M", "F", "O"] = Field("M",     description="Candidate gender")
    electors:          int   = Field(150000, ge=100,           description="Total registered electors")
    party:             str | None = Field("BJP",               description="Political party name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "year": 2019,
                "st_name": "Maharashtra",
                "constituency_name": "Mumbai South",
                "pc_no": 24,
                "pc_type": "GEN",
                "cand_sex": "M",
                "electors": 150000,
                "party": "BJP",
            }
        }
    }


class PredictionResponse(BaseModel):
    prediction:      int
    label:           str
    win_prob:        float
    predicted_votes: int | None = None
    party:           str | None = None


class LokSabhaPartyRequest(BaseModel):
    year:              int = Field(2029, ge=1951, le=2035, description="Election year")
    st_name:           str = Field("Maharashtra",          description="State / UT name")
    constituency_name: str | None = Field(None,            description="Constituency name")
    pc_no:             int = Field(24, ge=1, le=543,       description="Constituency number")
    pc_type:           str = Field("GEN",                  description="GEN | SC | ST")
    electors:          int = Field(150000, ge=1000,        description="Total registered electors")
    party1:            str = Field("BJP",                  description="First political party")
    party2:            str = Field("Congress",             description="Second political party")


# ─────────────────────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    return {"message": "ElectionPulse AI API is running 🗳️", "docs": "/docs"}


@app.get("/api/health", tags=["Health"])
def health():
    """Check API and model status."""
    model_path = os.path.join(PROJECT_ROOT, "artifacts", "models", "best_model.pkl")
    return {
        "status": "ok",
        "model_loaded": _pipeline is not None,
        "model_path": model_path,
        "model_file_exists": os.path.exists(model_path),
        "load_error": _load_error,
        "cwd": os.getcwd(),
    }


@app.get("/api/states", tags=["Data"])
def get_states():
    """Return the deduplicated sorted list of known Indian states / UTs."""
    seen, unique = set(), []
    for s in KNOWN_STATES:
        if s not in seen:
            seen.add(s)
            unique.append(s)
    return {"states": sorted(unique)}


@app.post("/api/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict(candidate: CandidateRequest):
    """
    Predict whether a Lok Sabha candidate will win their constituency.
    Returns prediction (0/1), win probability, label, and optional vote estimate.
    """
    pipe = get_pipeline()
    try:
        data = candidate.model_dump()
        result = pipe.predict_single(data)
        if candidate.party:
            result["party"] = candidate.party
        return PredictionResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/predict/constituency", tags=["Prediction"])
def predict_constituency(candidates: list[CandidateRequest]):
    """
    Given all candidates in a constituency, predict the winner.
    Returns the winner's index and win probability.
    """
    pipe = get_pipeline()
    try:
        result = pipe.predict_constituency([c.model_dump() for c in candidates])
        return {
            "winner_index": result["winner_index"],
            "winner_data":  result["winner_data"],
            "win_prob":     result["win_prob"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/predict/loksabha-party", tags=["Prediction"])
def predict_loksabha_party(req: LokSabhaPartyRequest):
    """
    Predict head-to-head Lok Sabha party winner for a constituency.
    """
    pipe = get_pipeline()
    try:
        result = pipe.predict_party_contest(req.model_dump())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
