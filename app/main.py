from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import trades
from app.config import settings

app = FastAPI(
    title="Crypto Derivatives Trade Tracker",
    description="A mock crypto derivatives trading system backend",
    version="1.0.0",
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(trades.router)

@app.get("/")
async def root():
    return {"message": "Crypto Derivatives Trade Tracker API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "environment": settings.ENVIRONMENT}

@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup (if database is available)"""
    try:
        from app.database import engine, Base
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"⚠️  Database not available: {e}")
        print("   API will work for margin simulation, but database operations will fail")