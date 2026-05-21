"""
Pydantic schemas for API request/response models
"""

from pydantic import BaseModel, Field
from typing import List, Optional

# Request Models

class PasswordRequest(BaseModel):
    password: str = Field(
        ...,
        min_length=1,
        description="Password to analyze"
    )

# Response Models

class PasswordStrength(BaseModel):
    score: int = Field(..., ge=0, le=100)
    entropy: float
    strength: str  # e.g., Weak / Moderate / Strong

class PasswordFeedback(BaseModel):
    suggestions: List[str] = []
    warnings: List[str] = []

class BreachResult(BaseModel):
    breached: bool
    breach_count: Optional[int] = None

class PasswordAnalysisResponse(BaseModel):
    strength: PasswordStrength
    feedback: PasswordFeedback
breached: Optional[BreachResult] = None

# Health Check Response

class HealthResponse(BaseModel):
    status: str = "ok"
