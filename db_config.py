from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from configparser import ConfigParser
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# CONFIG
config_file_name = 'config.conf'
config_file_location = os.path.join(ROOT_DIR, config_file_name)
config = ConfigParser()
config.read(config_file_location)

connection_string = config['db']['connection_string']
Base = declarative_base()

engine = create_engine(connection_string, echo=True)


def create_all_entities():
    Base.metadata.create_all(engine)


Session = sessionmaker()

local_session = Session(bind=engine)