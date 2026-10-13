from app.utils import app_logger
from app.server.HTTP_server import serve



def main():
    app_logger.info("Hello from stories!")
    serve()


if __name__ == "__main__":
    main()
