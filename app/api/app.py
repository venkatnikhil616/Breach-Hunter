"""
FastAPI app factory
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

# Import routes
from app.api.routes import router as api_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="Password Security Platform",
        description="API for password strength analysis and breach detection",
        version="1.0.0"
    )
    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # change in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # Routes
    app.include_router(api_router, prefix="/api")
    # Root Redirect
    @app.get("/", include_in_schema=False)
    async def root():
        return RedirectResponse(url="/docs")
    # Health Check
    @app.get("/health")
    def health_check():
        return {"status": "ok"}
    return app
