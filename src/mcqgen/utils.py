from dotenv import load_dotenv
import os


load_dotenv()


def read_file():
    return os.getenv("TEXT")

def get_table_data():
    return "table created"