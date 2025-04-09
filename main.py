from typing import Annotated

from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, select, create_engine
from fastapi import Depends, FastAPI, HTTPException, Query

from models import Table, Reservation

app = FastAPI()

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get('/tables')
def read_tables(
	session: SessionDep, 
	offset: int = 0,
	limit: Annotated[int, Query(le=100)] = 100
) -> list[Table]:
	tables = session.exec(select(Table).offset(offset).limit(limit)).all()
	return tables

@app.post('/tables')
def create_tables(table: Table, session: SessionDep) -> Table:
	session.add(table)
	session.commit()
	session.refresh(table)
	return table

@app.delete('/tables/{table_id}')
def delete_tables(table_id: int, session: SessionDep):
	table = session.get(Table, table_id)
	if not table:
		raise HTTPException(status_code=404, detail="Table not found")
	session.delete(table)
	session.commit()
	return {"ok": True}

@app.get('/reservations')
def read_reservations(
	session: SessionDep, 
	offset: int = 0,
	limit: Annotated[int, Query(le=100)] = 100
) -> list[Reservation]:
	resevations = session.exec(select(Reservation).offset(offset).limit(limit)).all()
	return resevations 

@app.post('/reservations')
def create_reservations(reservation: Reservation, session: SessionDep) -> Reservation:
	session.add(reservation)
	session.commit()
	session.refresh(reservation)
	return reservation

@app.delete('/reservations/{reservation_id}')
def delete_reservations(reservation_id: int, session: SessionDep):
	reservation = session.get(Reservation, reservation_id)
	if not reservation:
		raise HTTPException(status_code=404, detail="Reservation not found")
	session.delete(reservation)
	session.commit()
	return {"ok": True}