from ..utils import predictor


async def predict(message: str) -> str:
    prediction_result = predictor.rag_predictor.invoke(message)
    return prediction_result