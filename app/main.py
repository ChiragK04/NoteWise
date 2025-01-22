from fastapi import FastAPI
from app.routers.api_router import router as audio_router
import uvicorn
app = FastAPI()

# Register routers
app.include_router(audio_router, prefix="/audio", tags=["Audio"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Audio Processing API!"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", host="0.0.0.0", port=8000, log_level="info", reload=True
    )