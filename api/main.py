"""
AfriSalaries v3 — FastAPI Application
Two-stage: Band Classifier + Empirical Salary Distribution
Author: James Koero | May 2026
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pathlib import Path
from pydantic import BaseModel
from typing import List, Optional
import joblib
import pandas as pd
import numpy as np
from scipy.sparse import hstack, csr_matrix
import re
import os

# ── Globals ──────────────────────────────────────────────────
clf           = None
vectorizer    = None
band_thresholds = None
country_cols  = None
num_cols      = None

# ── Absolute model directory (works in Docker at /app) ───────
MODEL_DIR = Path(__file__).parent.parent / "models"

# ── Feature engineering constants ────────────────────────────
SENIORITY_MAP = {
    'Intern':0.0,'Junior':0.3,'Mid-Level':0.6,
    'Senior':0.85,'Lead':1.0
}
COUNTRY_BASELINE = {
    'ZA':42,'NG':28,'KE':25,'GH':18,
    'ET':12,'UG':13,'TZ':14,'RW':15
}
HIGH_VALUE_SKILLS = [
    'AWS','GCP','Azure','Kubernetes','Docker',
    'PyTorch','TensorFlow','Spark','React',
    'TypeScript','Go','Rust','Blockchain',
    'LLM','Terraform','Databricks','Snowflake',
]
FINTECH_TERMS = ['fintech','payments','banking','finance',
                 'crypto','blockchain','mpesa','flutterwave']
MGMT_TERMS    = ['manager','director','head of','vp ',
                 'lead','principal','architect','cto','chief']
BAND_LABELS   = {0:'LOW', 1:'MEDIUM', 2:'HIGH'}


# ── Pydantic models ──────────────────────────────────────────
class PredictRequest(BaseModel):
    description: str
    country:     str
    currency:    Optional[str] = "USD"

class PredictResponse(BaseModel):
    band:         str
    band_meaning: str
    salary_low:   int
    salary_mid:   int
    salary_high:  int
    currency:     str
    confidence:   float
    country_median: Optional[int] = None
    top_factors:  List[str]
    disclaimer:   str

class HealthResponse(BaseModel):
    status:       str
    model_loaded: bool
    model_version: str
    training_rows: int


# ── Feature extraction ───────────────────────────────────────
def extract_features(df_in: pd.DataFrame) -> pd.DataFrame:
    f = pd.DataFrame(index=df_in.index)
    f['seniority']    = df_in['description'].apply(
        lambda d: next((v for k,v in SENIORITY_MAP.items() if k in d), 0.5))
    f['years_exp']    = df_in['description'].apply(
        lambda d: min(float(re.search(r'(\d+)\+?\s*years?',d).group(1))
                      if re.search(r'(\d+)\+?\s*years?',d) else 3.0, 30.0))
    f['is_remote']    = df_in['description'].str.contains(
        'Remote', case=False).astype(float)
    f['hv_skills']    = df_in['description'].apply(
        lambda d: float(sum(1 for s in HIGH_VALUE_SKILLS if s.lower() in d.lower())))
    f['country_base'] = df_in['country'].map(COUNTRY_BASELINE).fillna(20.0)
    f['desc_len']     = df_in['description'].str.len() / 200.0
    f['is_fintech']   = df_in['description'].apply(
        lambda d: float(any(t in d.lower() for t in FINTECH_TERMS)))
    f['is_mgmt']      = df_in['description'].apply(
        lambda d: float(any(t in d.lower() for t in MGMT_TERMS)))
    return f


def build_features(description: str, country: str):
    """Build full feature matrix for one row — matches training pipeline exactly."""
    X_t = vectorizer.transform([description])

    cd  = pd.get_dummies(pd.Series([country]), prefix='c')
    for col in country_cols:
        if col not in cd.columns:
            cd[col] = 0
    X_c = csr_matrix(cd[country_cols].values.astype(float))

    row_df = pd.DataFrame({'description': [description], 'country': [country]})
    X_n    = csr_matrix(extract_features(row_df).values.astype(float))

    return hstack([X_t, X_c, X_n])


def get_top_factors(description: str, country: str) -> List[str]:
    """Return human-readable top salary drivers."""
    factors = []
    desc_lower = description.lower()

    for k, v in SENIORITY_MAP.items():
        if k in description:
            factors.append(f"Seniority: {k} (+{int(v*100)}%)")
            break

    hv = [s for s in HIGH_VALUE_SKILLS if s.lower() in desc_lower]
    if hv:
        factors.append(f"High-value skills: {', '.join(hv[:3])}")

    if any(t in desc_lower for t in FINTECH_TERMS):
        factors.append("Industry: Fintech premium")

    if any(t in desc_lower for t in MGMT_TERMS):
        factors.append("Role: Management/Leadership premium")

    if 'remote' in desc_lower:
        factors.append("Remote work premium")

    m = re.search(r'(\d+)\+?\s*years?', description)
    if m:
        factors.append(f"Experience: {m.group(1)}+ years")

    baseline = COUNTRY_BASELINE.get(country, 20)
    factors.append(f"Country baseline: {country} (~${baseline}k median)")

    return factors[:5] if factors else ["Insufficient description detail"]


# ── Lifespan (load models on startup) ────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    global clf, vectorizer, band_thresholds, country_cols, num_cols
    try:
        clf             = joblib.load(MODEL_DIR / "band_classifier.pkl")
        vectorizer      = joblib.load(MODEL_DIR / "vectorizer.pkl")
        band_thresholds = joblib.load(MODEL_DIR / "band_thresholds.pkl")
        country_cols    = joblib.load(MODEL_DIR / "country_columns.pkl")
        num_cols        = joblib.load(MODEL_DIR / "numerical_features.pkl")
        print(f"✅ All models loaded from {MODEL_DIR}")
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        print(f"   MODEL_DIR={MODEL_DIR}")
        print(f"   Files present: {list(MODEL_DIR.glob('*')) if MODEL_DIR.exists() else 'DIR NOT FOUND'}")
    yield


# ── App ───────────────────────────────────────────────────────
app = FastAPI(
    title="AfriSalaries API",
    description="ML-powered salary band prediction for African tech roles. "
                "Stack Overflow data 2022–2025 | CC BY-SA 4.0",
    version="3.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Routes ────────────────────────────────────────────────────
@app.get("/")
def root():
    return {
        "message": "AfriSalaries API v3.0.0",
        "docs":    "/docs",
        "health":  "/health",
        "predict": "POST /predict",
    }


@app.get("/health", response_model=HealthResponse)
def health():
    loaded = clf is not None and vectorizer is not None
    if not loaded:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded — check Render logs for startup errors."
        )
    metrics_path = MODEL_DIR / "metrics.json"
    training_rows = 1526
    try:
        import json
        with open(metrics_path) as f:
            m = json.load(f)
        training_rows = m.get("training_rows", 1526)
    except:
        pass
    return HealthResponse(
        status="healthy",
        model_loaded=True,
        model_version="xgboost_v3.0.0",
        training_rows=training_rows,
    )


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    if clf is None or vectorizer is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded — check Render logs for startup errors."
        )
    try:
        X        = build_features(request.description, request.country)
        band_id  = int(clf.predict(X)[0])
        proba    = clf.predict_proba(X)[0]
        confidence = float(proba[band_id])
        band_label = BAND_LABELS[band_id]

        # Salary from empirical distribution
        stats = band_thresholds["salary_stats"][band_label]
        country_median = stats["country_medians"].get(request.country)
        salary_mid  = country_median if country_median else stats["median"]
        salary_low  = stats["p25"]
        salary_high = stats["p75"]

        MEANINGS = {
            "LOW":    "Below market median — strong grounds to negotiate upward.",
            "MEDIUM": "At market rate — negotiate on specific skills and experience.",
            "HIGH":   "Above market median — evaluate total compensation carefully.",
        }

        return PredictResponse(
            band=band_label,
            band_meaning=MEANINGS[band_label],
            salary_low=salary_low,
            salary_mid=salary_mid,
            salary_high=salary_high,
            currency="USD",
            confidence=round(confidence, 3),
            country_median=country_median,
            top_factors=get_top_factors(request.description, request.country),
            disclaimer=(
                "Statistical estimate only. Based on Stack Overflow Survey 2022–2025 "
                "(CC BY-SA 4.0). Excludes equity, bonuses, benefits. Not a legal instrument."
            )
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
