from fastapi import APIRouter, UploadFile,HTTPException
from ..services import ingest

router = APIRouter()

@router.post('/files')
async def upload(file: UploadFile):
    if not file:
        raise HTTPException(status_code=400, detail="bad request")
    else:
        try:
            ingest.upload(file)
            return {"message": "successfully upload file"}
        except:
            raise HTTPException(status_code=500, detail="Internal error")