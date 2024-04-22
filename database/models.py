import datetime

from sqlalchemy import create_engine, MetaData, Table, String, Integer, Column, DateTime, Boolean, Float

from database.config import Config, load_config

config: Config = load_config()
engine = create_engine('sqlite:///database/main.db')
engine.connect()
metadata = MetaData()

currency = Table(
    'currency',
    metadata,
    Column('id', Integer(), unique=True, primary_key=True),
    Column('name', String(100), unique=True, nullable=False),
    Column('rate', Float(10), nullable=True, default=0),
    Column('updated', DateTime()),
    Column('last_request', DateTime(), default=datetime.datetime.now())
)

metadata.create_all(engine)
