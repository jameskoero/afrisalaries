from fastapi import FastAPI, HTTPException
from api.models import PredictRequest, PredictResponse, HealthResponse
import joblib
import pandas as pd
import shap
import os
from contextlib import asynccontextmanager

model = None
vectorizer = None
explainer = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, vectorizer, explainer
    model_path = os.getenv("MODEL_PATH", "models/model.pkl")
    vectorizer_path = os.getenv("VECTORIZER_PATH", "models/vectorizer.pkl")
    
    try:
        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)
        explainer = shap.TreeExplainer(model)
        print("Model and vectorizer loaded successfully")
    except Exception as e:
        print(f"Error loading model: {e}")
    
    yield
    print("Shutting down API")

app = FastAPI(
    title="AfriSalaries API",
    description="Predict tech salaries across Africa from job descriptions",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/health", response_model=HealthResponse)
async def health():
    if model is None or vectorizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return HealthResponse(status="healthy", model_loaded=True)

@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    if model is None or vectorizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        text_features = vectorizer.transform([request.description])
        
        country_features = pd.DataFrame({
            'country_KE': [1 if request.country == 'KE' else 0],
            'country_NG': [1 if request.country == 'NG' else 0],
            'country_ZA': [1 if request.country == 'ZA' else 0],
        })
        
        X = pd.concat([pd.DataFrame(text_features.toarray()), country_features], axis=1)
        X.columns = X.columns.astype(str)
        
        salary_pred = model.predict(X)[0]
        salary_low = int(salary_pred * 0.85)
        salary_mid = int(salary_pred)
        salary_high = int(salary_pred * 1.15)
        
        shap_values = explainer.shap_values(X)
        feature_names = X.columns.tolist()
        feature_importance = list(zip(feature_names, shap_values[0]))
        feature_importance.sort(key=lambda x: x[1], reverse=True)
        top_factors = [f"{name}: +{val:.0%}" for name, val in feature_importance[:3] if val > 0]
        
        confidence = min(0.95, max(0.60, 1 - abs(shap_values[0].std()) / abs(salary_pred) * 100))
        
        return PredictResponse(
            salary_low=salary_low,
            salary_mid=salary_mid,
            salary_high=salary_high,
            currency=request.currency,
            confidence=round(confidence, 2),
            top_factors=top_factors if top_factors else ["Base rate"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/")
async def root():
    return {"message": "AfriSalaries API. See /docs for usage."}
