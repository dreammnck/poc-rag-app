from pydantic import BaseModel

class PredictRequest(BaseModel):
    content: str
