from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# TODO: Перенести на MongoDB
metadata = MetaData()
Base = declarative_base(metadata=metadata)
Session = sessionmaker()
session = Session()
