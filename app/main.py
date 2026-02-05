from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from app.api.routes import auth, predictor

app = FastAPI(
    title="AI Disease Predictor",
    description="Non-diagnostic disease prediction using LLMs",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth.router)
app.include_router(predictor.router)
