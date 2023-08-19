from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy import func
from datetime import datetime
from fastapi import HTTPException
import json

def convert_result(res):
    return [{c:getattr(r,c) for c in res.keys()}for r in res]

def post_data(db:Session, machine_id, time, history):
    stmt = """
        INSERT INTO public.history(machine_id, "time", history)
        VALUES (:machine_id, :time, :history)
        RETURNING time;
    """
    try:
        res = db.execute(text(stmt), {"machine_id": machine_id, "time": time, "history": json.dumps(history)})
        db.commit()
        result = convert_result(res)
    except Exception as e:
        raise HTTPException(400,"Error inserting data :"+str(e))
    return result[0]

def post_fault(db:Session, time,date,fault_code):
    stmt = """
        INSERT INTO public.fault_history("time",date,fault_code)
        VALUES (:time, :date, :fault_code)
        RETURNING time;
    """
    try:
        res = db.execute(text(stmt), {"time": time, "date": date, "fault_code": fault_code})
        db.commit()
        result = convert_result(res)
    except Exception as e:
        raise HTTPException(400,"Error inserting fault history :"+str(e))
    return result[0]

def get_fault_history(db:Session,start_time: datetime):
    stmt = f"""
        SELECT * FROM fault_history
        JOIN fault_message USING (fault_code)
        WHERE "time" >= '{start_time}'
        ORDER BY date DESC, time DESC;
    """
    try:
        result = db.execute(text(stmt)).mappings().all()
        return result
    except Exception as e:
        raise HTTPException(400,"Error inserting fault history :"+str(e))

def get_history(db: Session,start_time: datetime):
    stmt = f"""
        SELECT * FROM fault_history
        JOIN fault_message USING (fault_code)
        WHERE "time" >= '{start_time}'
        ORDER BY date DESC, time DESC;
    """
    try:
        result = db.execute(text(stmt)).mappings().all()
        return result
    except Exception as e:
        raise HTTPException(400,"Error inserting fault history :"+str(e))





def get_fault_message(db: Session, fault_code: str):
    stmt = """
        SELECT fault_message
        FROM fault_message
        WHERE fault_code = :fault_code;
    """
    try:
        result = db.execute(text(stmt), {"fault_code": fault_code})
        print("stmt",stmt)
        print("result",result)
        row = result.fetchone()
        print("row",row)
        if row:
            fault_message = row[0]
            print(fault_message)
            return fault_message
        else:
            return ""
    except Exception as e:
        raise HTTPException(400, "Error fetching data: " + str(e))

