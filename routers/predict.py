from fastapi import APIRouter
from ..serializer import predict
from ..services import predict as service

router = APIRouter()

@router.post("/predicts")
async def predict(req: predict.PredictRequest):
    result = await service.predict(req.content)
    return {"result": result}