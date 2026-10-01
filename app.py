import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from fastapi import FastAPI, responses, requests
from pydantic import BaseModel, Field


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
Base = declarative_base()

db = Base.metadata.create_all(bind=engine)

app = FastAPI(title="Contact_Form")




class Form(Base):
    __tablename__ = "forms"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    message = Column(String)

class ContactUpdate(BaseModel):
    id : int
    name : str = Field(min_length=3, max_length=50)
    email : str
    message : str = Field(min_length=3, max_length=500)

class ContactResponse(BaseModel):
    name: str
    email : str
    message : str


@app.post("/contact-form", response_model= ContactResponse)
def submit_form(FormData: ContactUpdate):
    db_form = Form(name = FormData.name, email = FormData.email, message = FormData.message)
    db.add(db_form)
    db.commit()
    db.refresh(db_form)
    return db_form  










if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app.py", host="0.0.0.0", port=8000)

    

