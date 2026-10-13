import logging


## Logging

app_logger = logging.getLogger("app")
db_logger = logging.getLogger("db")
security_logger = logging.getLogger("security")

db_handler = logging.FileHandler("app/db/logs")
app_handler = logging.FileHandler("app/logs")

db_logger.addHandler(db_handler)
app_logger.addHandler(app_handler)

# app_handler.setLevel(logging.DEBUG)
# db_handler.setLevel(logging.DEBUG)
app_logger.setLevel(logging.DEBUG)
db_logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)

db_handler.setFormatter(formatter)
app_handler.setFormatter(formatter)