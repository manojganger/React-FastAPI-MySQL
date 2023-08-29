from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
import asyncio
from fastapi.responses import StreamingResponse

import json
import random

app = FastAPI()

# Set up CORS
origins = ["http://localhost:8000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DATABASE_URL = "mysql://root:-----@localhost/mysql"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class UserCreate(BaseModel):
    name: str

@app.post("/api/users/")
def create_user(user: UserCreate):
    db = SessionLocal()
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user

@app.get("/api/users/")
def read_users(skip: int = 0, limit: int = 10):
    db = SessionLocal()
    users = db.query(User).offset(skip).limit(limit).all()
    db.close()
    return users

def sse_response(event):
    return f"data: {event}\n\n"

@app.get("/api/events")
async def events():
    async def event_generator():
        fname=['john','jerry','tom','Sherry','Adam','steve','jim','joe','eden','cathy']
        lname=['smith','johnson','brown','miller','lopaz','taylor','moore','martin','clark','young']
        rn=0
        while True:
            # Simulate inserting a new record into the database
            rn=rn+1
            sse_data = json.dumps({"id": rn, "name": random.choice(fname)+' '+random.choice(lname)})
            
            
            yield f"data: {sse_data}\n\n"
            await asyncio.sleep(5)  # Wait for 5 seconds before sending next event

    return StreamingResponse(event_generator(), media_type="text/event-stream")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
