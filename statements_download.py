import pandas as pd
from zipfile import ZipFile
import wget
import os
from datetime import date
from codes.get_statements import *
from sqlite3 import *

conn = connect('statements/statements.db')

current_year = int(date.today().year)
get_statements(begin = 2011,end = current_year, database = conn)