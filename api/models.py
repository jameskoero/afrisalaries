from pydantic import BaseModel, Field
from typing import List

class PredictRequest(BaseModel):
    description: str = Field(
       ...,
        min_length=20,
        max_length=5000,
        description="Full job description text",
        examples=["Senior Python Developer with 5+ years Django, AWS. Remote. Nairobi."]
    )
    country: str = Field(
       ...,
        min_length=2,
        max_length=2,
        description="ISO 3166-1 alpha-2 country code",
        examples=["KE", "NG", "ZA"]
    )
    currency: str = Field(
        default="USD",
        min_length=3,
        max_length=3,
        description="ISO 4217 currency code",
        examples=["USD", "KES", "NGN"]
    )

class PredictResponse(BaseModel):
    salary_low: int = Field(..., description="Lower bound of salary estimate")
    salary_mid: int = Field(..., description="Median salary estimate")
    salary_high: int = Field(..., description="Upper bound of salary estimate")
    currency: str = Field(..., description="Currency of salary values")
    confidence: float = Field(..., ge=0, le=1, description="Model confidence 0-1")
    top_factors: List[str] = Field(..., description="Top SHAP features driving prediction")

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
