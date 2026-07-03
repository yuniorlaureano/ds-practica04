from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    CON_STRING = os.getenv("CON_STRING")


config = Config()