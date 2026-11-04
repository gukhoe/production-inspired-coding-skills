"""Exercise actual loopback HTTP and state change, shutting down in all cases."""
from http.server import HTTPServer
import json
import threading
from client import send
from gateway import Handler


def main():
    server = HTTPServer(('127.0.0.1', 0), Handler)
    server.timeout = 3
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    url = f'http://127.0.0.1:{server.server_port}/events'
    try:
        first = send(url, {'id': 'event-1', 'amount': 10})
        repeated = send(url, {'id': 'event-1', 'amount': 10})
        rejected = send(url, {'id': 'bad', 'amount': -7})
        adjacent = send(url, {'id': 'event-2', 'amount': 5})
        checks = {'normal': first == (200, {'balance':110}),
                  'duplicate_replay': repeated == (200, {'balance':110}),
                  'invalid_amount_rejected': rejected[0] == 400,
                  'adjacent_valid_event': adjacent == (200, {'balance':115})}
        print(json.dumps({'checks': checks, 'observed_duplicate_balance': repeated[1]['balance'],
                          'expected_duplicate_balance':110, 'transport':'actual loopback HTTP',
                          'scope':'single process, single-threaded receiver, no persistence/restart/TLS/auth testing'}, sort_keys=True))
        return 0 if all(checks.values()) else 1
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=3)
        if worker.is_alive():
            raise RuntimeError('Demo server did not stop')


if __name__ == '__main__':
    raise SystemExit(main())
