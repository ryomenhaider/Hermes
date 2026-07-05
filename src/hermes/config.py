from dotenv import load_dotenv
import os


load_dotenv()

FRED_API = os.getenv('FRED_API')
DB_URL = os.getenv('DATABASE_URL')