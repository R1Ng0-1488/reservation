
from sqlmodel import Field, SQLModel
from datetime import datetime


class Table(SQLModel, table=True):
	id: int = Field(default=None, primary_key=True)
	name: str
	seats: int
	location: str


class Reservation(SQLModel, table=True):
	id: int = Field(default=None, primary_key=True)
	customer_name: str
	table_id: int = Field(default=None, foreign_key="table.id")
	reservation_time: datetime
	duration_minutes: int
