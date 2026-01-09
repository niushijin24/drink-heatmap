from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import router

app = FastAPI(title="Drink Heatmap API")

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Drink Heatmap API is running"}
