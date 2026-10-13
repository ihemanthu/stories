from http.server import HTTPServer
from .HTTP_handler import RequestHandler
from app.utils import app_logger
from app.config import settings

def serve() -> None:
    server = HTTPServer(("127.0.0.1", 8000), RequestHandler)

    app_logger.info(f"HTTP server listening on {settings.HTTP_PROTOCOL}://127.0.0.1:8000")

    try:
        server.serve_forever()

    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

    

