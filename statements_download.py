import pandas as pd
from zipfile import ZipFile
import wget
import os
from datetime import date
from codes.get_statements import *
from sqlalchemy import create_engine

engine = create_engine('sqlite:///statements_database.db', echo = True)
conn = engine.connect()

current_year = int(date.today().year)
get_statements(begin = 2011,end = 2019, database = conn)