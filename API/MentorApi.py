from fastapi import FastAPI
from fastapi import HTTPException

from config.config import mentorSheet

app = FastAPI()


#crud
@app.get("/getAllMentor")
async def getAllMentor():
    try:
        records =  mentorSheet.get_all_records()
        return records
    except:
        raise HTTPException(status_code=401, detail="Error ")
