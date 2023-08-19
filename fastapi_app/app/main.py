from fastapi import Depends,FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from . import crud, schemas
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from typing import Union,List
import datetime as dt
from .crud import get_fault_message
from fastapi import HTTPException

origins=["*"]

app = FastAPI()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:  
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MachineHistory(BaseModel):
    machine_id:int
    time: dt.time
    history: dict

class FaultHistory(BaseModel):
    time: dt.datetime
    date: dt.datetime
    fault_code: str

class AlarmData(BaseModel):
    timestamp: Union[str, dt.time]
    alarmCode:str

class TableData(BaseModel):
    date:dt.date
    time:dt.time
    fault_code: str
    fault_message:str



@app.post("/data")
async def post_data(json_input: MachineHistory, db: Session = Depends(get_db)):
    json = crud.post_data(db, json_input.machine_id, json_input.time, json_input.history)
    return json

@app.post("/faultdata")
async def post_data(json_input: FaultHistory, db: Session = Depends(get_db)):
    json = crud.post_fault(db, json_input.time, json_input.date, json_input.fault_code)
    return json

@app.get("/process_alarm_data",response_model=List[TableData])
async def process_alarm_data(start_time:dt.datetime,db:Session = Depends(get_db)):
    
    try:
        table_data = crud.get_fault_history(db,start_time=start_time)
        return table_data
    except Exception as e:
        raise HTTPException(500,"Error processing alarm"+ str(e))
    

@app.get("/get_history",response_model=List[TableData])
async def get_history(start_time:dt.datetime,db:Session = Depends(get_db)):
    table_data = crud.get_history(db,start_time=start_time)
    return table_data