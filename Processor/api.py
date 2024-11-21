import http.server as srv
import json


# run a api with the given functions
def run_api(get, post, port=8000):
    class RequestHandler(srv.BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            if self.path != "/results":
                self.respond("Not Found".encode("utf-8"), code=404)
                return

            self.respond(get(0))

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

            code, msg = post(data)

            self.respond(msg.encode("utf-8"), code=code)

        def respond(self, body: bytes, code=200, content_type="text/plain"):
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.end_headers()
            self.wfile.write(body)

    get = get
    server = srv.HTTPServer(("localhost", port), RequestHandler)
    print("Server running on http://localhost:" + str(port))
    server.serve_forever()
