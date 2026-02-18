from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.connection import MongoDBConnection
from app.routes import (
    website_survey_router
)

app = FastAPI(
    title="Survey Microservices",
    description="Backend API for managing website survey, tag survey, custom survey template and custom survey responses.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    MongoDBConnection.connect()
    print("Survey Microservices started successfully.")

@app.on_event("shutdown")
async def shutdown_event():
    MongoDBConnection.close()
    print("Survey Microservices stopped successfully.")

@app.get("/", tags=["Health"])
async def root():
    return {
        "message": "Survey Microservices",
        "statusCode": "running",
        "version": "1.0.0",
        "docs": "/docs",
    }

@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "database": "connected"
    }

app.include_router(website_survey_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
