import http.server as hs
import logging
import os
import sys

from urllib.parse import parse_qs

from utils import get_logger, get_database_connection, insert_prompt_into_db

DEFAULT_FILE = "index.html"
STATIC_DIR = "static"

logger = get_logger(__file__)


class web_handler(hs.BaseHTTPRequestHandler):
    def load_file(self, file):
        if not os.path.isfile(file):
            return 404, "404".encode("utf-8")
        else:
            with open(file, 'rb') as fh:
                return 200, fh.read()

    def get_file_type(self, file):
        type_by_extension = {
            "html": "text/html",
            "css": "text/css",
            "js": "application/javascript",
        }
        extension = file.split(".")[-1]
        return type_by_extension.get(extension, "text/html")
    
    def send_the_response(self, status_code, content_type, contests):
        self.send_response(status_code)
        self.send_header("Content-type", content_type)
        self.end_headers()
        self.wfile.write(contests)

    def do_GET(self):
        file = DEFAULT_FILE if self.path == "/" else self.path.replace("/", "", 1)
        status_code, file_contents = self.load_file(f"{os.path.curdir}/{STATIC_DIR}/{file}")
        file_type = self.get_file_type(file)
        self.send_the_response(status_code, file_type, file_contents)

    def do_POST(self):
        logger.info(dir(self.request))
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = parse_qs(self.rfile.read(content_length).decode())
        logger.info(f"Received POST data: {post_data}")
        self.send_the_response(200, "text/plain", str(post_data).encode())
        if 'text' in post_data:
            db_path = os.path.join(os.path.dirname(__file__), 'test_character_maker.db')
            connection = get_database_connection(db_path)
            prompt_text = post_data['text'][0]
            insert_prompt_into_db(connection, prompt_text)
            logger.info(f"Inserted prompt into database: {prompt_text}")
        

class web_server(hs.HTTPServer):
    def __init__(self, handler, address="", port=8000):
        super().__init__((address, port), handler)


def main():
    try:
        ws = web_server(web_handler)
        ws.serve_forever()
    except Exception as ex:
        logger.exception(ex)


if __name__ == "__main__":
    main()