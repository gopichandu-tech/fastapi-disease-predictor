from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user
from app.db.session import AsyncSessionLocal
from app.db.models import DiseasePrediction
from app.schemas.predictor import PredictionRequest, PredictionResponse
from app.core.llm import predict_disease

router = APIRouter(prefix="/predict", tags=["Disease Predictor"])

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db

@router.post("/", response_model=PredictionResponse)
async def predict(
    payload: PredictionRequest,
    user_email: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    prediction = await predict_disease(payload.symptoms)

    record = DiseasePrediction(
        user_name=payload.user_name,
        email=user_email,
        symptoms=payload.symptoms,
        predicted_disease=prediction
    )
    db.add(record)
    await db.commit()

    return {"prediction": prediction}
