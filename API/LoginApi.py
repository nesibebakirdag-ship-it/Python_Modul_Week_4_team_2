from fastapi import FastAPI
from fastapi import HTTPException
from .models.LoginModel import LoginModel
from .config.config import sheet

app = FastAPI()



@app.post("/login")
async def login(data: LoginModel):
    records =  sheet.get_all_records()
    for record in records:
        if data.username == record['kullanici']:
            if data.password == record['parola']:
                return record
            else:
                raise HTTPException(status_code=401, detail="Invalid password")


    raise HTTPException(status_code=401, detail="User not found")

@app.get("/getalluser")
def getuser():
    record = sheet.get_all_records()
    return record
