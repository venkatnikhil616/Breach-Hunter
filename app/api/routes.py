#API Routes

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

# Replace this with your real analyzer while running in real world
from app.core.password_analyzer import analyze_password


router = APIRouter()

# Request / Response Schemas

class PasswordRequest(BaseModel):
    password: str = Field(..., min_length=1, example="MySecure@123")

class PasswordResponse(BaseModel):
    score: int
    strength: str
    suggestions: list[str]

# Routes

router.get("/")
def root():
    return {"message": "Password Security API working"}

@router.post("/analyze", response_model=PasswordResponse)
def analyze(req: PasswordRequest):
    try:
        result = analyze_password(req.password)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
def health():
    return {"status": "ok"}
