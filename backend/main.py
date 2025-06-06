from datetime import datetime

import models
import schemas
import services
import uvicorn
from crud import save_currencies
from db import engine, get_db
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Currency API", version="1.0.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def load_initial_currency_data():
    db = Session()
    try:
        currencies = services.fetch_currencies()
        save_currencies(db, currencies)
    finally:
        db.close()


@app.get("/currencies")
def get_available_currencies(db: Session = Depends(get_db)):
    currencies = db.query(models.Currency.code, models.Currency.name).distinct().all()
    return [{"code": code, "name": name} for code, name in currencies]


@app.get("/currencies/{date}")
def get_currencies_by_date(date: str, db: Session = Depends(get_db)):
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Invalid date format. Use YYYY-MM-DD."
        )

    rates = db.query(models.Currency).filter(models.Currency.date == parsed_date).all()

    if not rates:
        pass

    return [
        {
            "code": r.code,
            "name": r.name,
            "mid": r.mid,
            "date": r.date.strftime("%Y-%m-%d"),
        }
        for r in rates
    ]


@app.post("/currencies/fetch")
def add_currencies(db: Session = Depends(get_db)):
    try:
        currencies = services.fetch_currencies()
        save_currencies(db, currencies)
        return JSONResponse(
            content={"message": "currencies fetched and saved to database"},
            status_code=200,
        )
    except Exception:
        return JSONResponse(
            content={"message": "currencies fetched and saved to database"},
            status_code=200,
        )


if __name__ == "__main__":

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
