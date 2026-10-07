from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = "127.0.0.1"
PORT = 8765


class DemoHandler(BaseHTTPRequestHandler):
    sys_version = ""

    def version_string(self) -> str:
        if self.path.startswith("/insecure"):
            return "Apache/2.4.58"
        return "ExampleServer"

    def do_GET(self) -> None:  # noqa: N802
        if self.path.startswith("/secure"):
            self._secure()
        elif self.path.startswith("/insecure"):
            self._insecure()
        else:
            self.send_response(302)
            self.send_header("Location", "/insecure")
            self.end_headers()

    def _insecure(self) -> None:
        body = b"<html><body><h1>Insecure demo target</h1></body></html>"
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("X-Powered-By", "DemoFramework/1.0")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Set-Cookie", "MoodleSession=demo-insecure; Path=/; HttpOnly")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _secure(self) -> None:
        body = b"<html><body><h1>Hardened demo target</h1></body></html>"
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Security-Policy", "default-src 'self'; frame-ancestors 'none'")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        self.send_header("Set-Cookie", "MoodleSession=demo-secure; Path=/; Secure; HttpOnly; SameSite=Lax")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args) -> None:
        print(f"[demo] {self.address_string()} - {fmt % args}")


def run() -> None:
    server = ThreadingHTTPServer((HOST, PORT), DemoHandler)
    print("CyberQuality demo server is running")
    print(f"  Insecure target: http://{HOST}:{PORT}/insecure")
    print(f"  Hardened target: http://{HOST}:{PORT}/secure")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping demo server...")
    finally:
        server.server_close()


if __name__ == "__main__":
    run()
