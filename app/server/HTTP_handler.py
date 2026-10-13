import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
from app.db.connection import check_database
from app.utils import db_logger, app_logger

MAX_REQUEST_BODY_BYTES = 1024 * 1024

class RequestError(Exception):
    def __init__(self, status: int, message: dict):
        super().__init__(message)
        self.status = status
        self.message = message

def test(request):
    data = request.read_json()

    if not isinstance(data, dict):
        raise RequestError(400, {"error":"JSON body must be an object"})

    if "name" not in data:
        raise RequestError(400, {"error":"Missing required field: name"})

    if not isinstance(data["name"], str) or not data["name"].strip():
        raise RequestError(400, {"error":"Field 'name' must be a non empty string"})

    return 200, {"message": "valid request", "data": data}


def health(request):

    try:
        check_database()
    except Exception as error:
        db_logger.error(f"Database Health: {error}")
        return 503, {"status":"unhealthy", "database": "unavailable"}
    return 200, {"status": "healthy", "database": "connected"}

def not_found(request):
    return 404, {"error": "Not Found"}

ROUTES = {
    ("GET", "/health"): health,
    ("POST", "/test"): test,
}

class RequestHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def send_response(self, code, message=None):
        self.log_request(code)
        self.send_response_only(code, message)
        self.send_header('Date', self.date_time_string())


    def send_json(self, status: int, data: dict) -> None:
        body = json.dumps(data).encode('utf-8')

        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

        self.wfile.write(body)

    def read_json(self):
        content_type = self.headers.get("Content-Type", "")

        if content_type.split(";")[0].strip().lower() != "application/json":
            raise RequestError(415, {"error":"Content-Type must be application/json"})

        length_header = self.headers.get("Content-Length", None)
        if length_header is None:
            raise RequestError(411, {"error":"Content-Length is required"})

        try:
            length = int(length_header)
        except ValueError:
            raise RequestError(400, {"error":"Invalid Content-Length"})

        if length <= 0:
            raise RequestError(400, {"error":"Request body is required"})

        if length > MAX_REQUEST_BODY_BYTES:
            raise RequestError(400, {"error":"Request body too large"})

        raw_body = self.rfile.read(length)

        if len(raw_body) != length:
            raise RequestError(400, {"error":"Request body is Incomplete"})

        try:
            text = raw_body.decode("utf-8")
        except UnicodeDecodeError:
            raise RequestError(400, {"error":"Body must use UTF-8 encoding"})

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            raise RequestError(400, {"error":"Malformed JSON"})
        

    def handle_request(self, method):
        path = urlparse(self.path).path
        endpoint = ROUTES.get((method, path), not_found)

        try:
            status, data = endpoint(self)
            self.send_json(status, data)
        except RequestError as error:
            self.send_json(error.status, error.message)
        except Exception as unidentified_error:
            app_logger.error(f"Error while sending response: {unidentified_error}")
            self.send_json(500, {"error": "Internal server error"})

    def do_GET(self):
        self.handle_request("GET")

    def do_POST(self):
        self.handle_request("POST")

    def do_PUT(self):
        self.handle_request("PUT")

    def do_PATCH(self):
        self.handle_request("PATCH")

    def do_DELETE(self):
        self.handle_request("DELETE")



