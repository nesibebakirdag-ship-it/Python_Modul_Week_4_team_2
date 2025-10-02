from fastapi import FastAPI
from fastapi import HTTPException
from config.config import interviewsSheet

app = FastAPI()



@app.get("/interviews")
async def getAllInterviews():
    try:
        records =  interviewsSheet.get_all_records()
        return records
    except:
        raise HTTPException(status_code=401, detail="Error ")
