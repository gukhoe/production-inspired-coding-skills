"""Local-only synthetic HTTP boundary. No authentication/production claim."""
from http.server import BaseHTTPRequestHandler
import json
import store


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 1024:
                raise ValueError('Invalid length')
            request = json.loads(self.rfile.read(length))
            if not isinstance(request, dict):
                raise ValueError('Object required')
            event_id, amount = request.get('id'), request.get('amount')
            if not isinstance(event_id, str) or not event_id or type(amount) is not int or amount <= 0:
                raise ValueError('Invalid event')
            payload = {'balance': store.apply_event(event_id, amount)}
            status = 200
        except (ValueError, TypeError):
            payload, status = {'error': 'Invalid event'}, 400
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass
