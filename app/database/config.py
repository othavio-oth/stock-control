import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = 'postgresql://strategy_db_inventory:kbkhwbveuibhv92@localhost:5433/postgre'