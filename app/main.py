# Python standard library imports
import logging

# Project specific imports
from app.database.table_definitions import create_tables
from app.services.parser_service import persist_orders, get_is_successful_persist
from app.database.db_engine import DBEngine

# Third-party imports
from fastapi import FastAPI, status
import uvicorn


app = FastAPI()
_DB_ENGINE = None


def init():
    global _DB_ENGINE
    try:
        _DB_ENGINE = DBEngine().get_engine()
        create_tables(_DB_ENGINE)
    except Exception as e:
        logging.error(f"Can't reach to a running PostgreSQL server, {e}")
init()


@app.get("/")
def home():
    return "This is home.", status.HTTP_200_OK


@app.post("/ingest_file")
def ingest_file(filename: str = "dataset"):
    if "csv" in filename:
        return "Please do not provide file extension.", status.HTTP_400_BAD_REQUEST
    if not _DB_ENGINE:
        return "The service couldn't create a DB engine.", status.HTTP_500_INTERNAL_SERVER_ERROR
    persist_orders(_DB_ENGINE, filename)
    if get_is_successful_persist():
        return f"The orders from {filename} have been persisted successfully!", status.HTTP_200_OK
    else:
        return "Some entries could not be persisted, speak to the support team.", status.HTTP_500_INTERNAL_SERVER_ERROR


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5000)
