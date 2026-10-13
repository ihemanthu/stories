import logging


## Logging

app_logger = logging.getLogger("app")
db_logger = logging.getLogger("db")
security_logger = logging.getLogger("security")

db_handler = logging.FileHandler("db.logs")
app_handler = logging.FileHandler("logs")

db_logger.addHandler(db_handler)
app_logger.addHandler(app_handler)
