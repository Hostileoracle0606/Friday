from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .routes import auth, task, journal, sync

app = FastAPI(
    title="Friday API",
    description="Personal Assistant App API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(task.router, prefix=settings.API_V1_PREFIX)
app.include_router(journal.router, prefix=settings.API_V1_PREFIX)
app.include_router(sync.router, prefix=settings.API_V1_PREFIX)


@app.get("/")
def root():
    return {"message": "Friday API", "version": "0.1.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}

