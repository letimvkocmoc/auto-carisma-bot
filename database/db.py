import datetime

from sqlalchemy import create_engine, MetaData, Table, String, Integer, Column, DateTime, Boolean, Float

# from database.config import Config, load_config

# config: Config = load_config()
engine = create_engine('sqlite:///../database/main.db')
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

users = Table(
    'users',
    metadata,
    Column('id', Integer(), unique=True, primary_key=True),
    Column('user_id', String(100), unique=True, nullable=False),
    Column('username', String(100), nullable=True),
    Column('first_name', String(100)),
    Column('last_name', String(100)),
    Column('created', DateTime(), default=datetime.datetime.now())
)


orders = Table(
    'orders',
    metadata,
    Column('id', Integer(), unique=True, primary_key=True),
    Column('client_id', String(100), nullable=False),
    Column('client_first_name', String(100)),
    Column('client_last_name', String(100)),
    Column('client_phonenubmer', String(100)),
    Column('model_auto', String(100)),
    Column('rating', String(100)),
    Column('price', Integer()),
    Column('status', String(100)),
    Column('picture', String(100)),
    Column('link', String(100)),
    Column('is_paid', Boolean(), default=False)
)

metadata.create_all(engine)
