import http.server as srv
import json
from urllib.parse import urlparse, parse_qs
from detector import Detector, Resulter

JSON = "application/json"


# run a api
def run(detector: Detector, resulter: Resulter, port=8000):
    class RequestHandler(srv.BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            url = urlparse(self.path)
            offset = 0
            if url.path != "/results":
                self.respond("Not Found".encode("utf-8"), code=404)
                return

            try:
                offset = int(parse_qs(url.query)["offset"][0])
            except Exception:
                pass

            print(url.params)
            print(offset)

            response = json.dumps(
                list(map(lambda h: h.to_dict(), resulter.get_hits(offset)))
            )

            self.respond(response.encode("utf-8"), content_type=JSON)

        def do_POST(self) -> None:
            if self.path != "/img":
                self.respond("Not Found".encode("utf-8"), code=404)
                return

            data = None
            try:
                # read json from body to table
                content_length = int(self.headers.get("Content-Length", 0))
                post_data = self.rfile.read(content_length)

                data = json.loads(post_data.decode("utf-8"))
            except Exception as e:
                print(f"An error occurred: {e}")
                self.respond("Invalid Request".encode("utf-8"), code=400)

            print(data)

        def respond(self, body: bytes, code=200, content_type="text/plain"):
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.end_headers()
            self.wfile.write(body)

    server = srv.HTTPServer(("localhost", port), RequestHandler)
    print("Server running on http://localhost:" + str(port))
    server.serve_forever()
