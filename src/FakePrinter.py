"""
Copyright 2020 Luc Rubio <luc@loociano.com>
Plugin is licensed under the GNU Lesser General Public License v3.0.
"""
import logging
import re
import socketserver
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Timer
from time import sleep

from typing import Tuple

WELCOME_MESSAGE = """
<html>
<body>
<h1>Monoprice Select Mini V2 API Mock</h1>
<h2>Supported Commands</h2>
<ul>
  <li>Get printer status: <a href="/inquiry">GET /inquiry</a></li>
  <li>Print cached model: <a href="/set?cmd=%7BP:M%7D">GET /set?cmd=%7BP:M%7D</a></li>
  <li>Cancel print: <a href="/set?cmd=%7BP:X%7D">GET /set?cmd=%7BP:X%7D</a></li>
  <li>Set hot-end target temperature: <a href="/set?cmd=%7BC:T0250%7D">GET /set?cmd=%7BC:T0250%7D</a></li>
  <li>Set bed target temperature: <a href="/set?cmd=%7BC:P060%7D">GET /set?cmd=%7BC:P060%7D</a></li>
  <li>Send arbitrary gcode command: <a href="/set?code=M563%20S5">GET /set?code=M563%20S5</a></li>
  <li>Upload a model. POST /upload</li>
</ul>
</body>
</html>
"""

# pylint:disable=relative-beyond-top-level
from .PrinterModel import PrinterModel


class FakePrinter:
  """Emulates the Monoprice Select Mini V2 HTTP REST API."""

  def __init__(self):
    self._logger = logging.getLogger('FakePrinter')
    logging.basicConfig(level=logging.INFO)

  class Handler(BaseHTTPRequestHandler):
    """Handles HTTP requests."""
    printer = None

    def __init__(self, request: bytes, client_address: Tuple[str, int],
                 server: socketserver.BaseServer) -> None:
      """Constructor."""
      self._logger = logging.getLogger('FakePrinterHandler')
      super().__init__(request, client_address, server)

    # pylint:disable=invalid-name
    def do_GET(self) -> None:
      """Handles HTTP GET requests."""
      self.printer.tick()
      response = 'OK'
      if self.path == '/inquiry':
        response = 'T{}/{}P{}/{}/{}{}'.format(
            self.printer.hotend,
            self.printer.target_hotend_temperature,
            self.printer.bed,
            self.printer.target_bed_temperature,
            self.printer.progress,
            'I' if self.printer.state == 'idle' else 'P')
      elif self.path == '/set?cmd=%7BP:M%7D':  # print cached model
        Timer(2, self.printer.set_printer_state, ['printing']).start()
      elif self.path == '/set?cmd=%7BP:X%7D':  # cancel print
        Timer(2, self.printer.set_printer_state, ['idle']).start()
      elif self.path == '/set?cmd=%7BP:P%7D':  # Pause print.
        pass
      elif self.path == '/set?cmd=%7BP:R%7D':  # Resume print.
        pass
      elif self.path.startswith('/set?cmd=%7BC:T'):  # set target hotend temp
        match = re.match(r"^/set\?cmd=%7BC:T0(\d{3})%7D$", self.path)
        if match is not None:
          Timer(2, self.printer.set_target_hotend_temperature,
                [int(match.group(1))]).start()
      elif self.path.startswith('/set?cmd=%7BC:P'):  # set target bed temp
        match = re.match(r"^/set\?cmd=%7BC:P0(\d{2})%7D$", self.path)
        if match is not None:
          Timer(2, self.printer.set_target_bed_temperature,
                [int(match.group(1))]).start()
      elif self.path.startswith('/set?code='):  # any gcode
        pass
      else:
        # No command was specified, display help page.
        self._send_success_headers()
        self.wfile.write(WELCOME_MESSAGE.encode('utf-8'))
        return
      self._send_success_headers()
      self._logger.info('Response: %s', response)
      self.wfile.write(response.encode('utf-8'))

    def do_POST(self) -> None:
      """Handles HTTP POST requests."""
      if self.path == '/upload':
        self._simulateUpload()
      else:
        self._send_not_found_headers()
        self.wfile.write('Not Found'.encode('utf-8'))

    def _simulateUpload(self) -> None:
      """Simulates receiving an upload request."""
      self._send_success_headers()
      content_length = int(self.headers['Content-Length'])
      while content_length > 0:
        # ~8Mbps, faster than the real printer for testing.
        chunk = 10000 if content_length > 10000 else content_length
        content_length -= chunk
        self.rfile.read(chunk)
        sleep(0.01)
      self.wfile.write('OK'.encode('utf-8'))

    def _send_success_headers(self):
      """Sends HTTP OK."""
      self.send_response(200)
      self.send_header('Content-type', 'text/html')
      self.end_headers()

    def _send_not_found_headers(self):
      """Sends HTTP Not Found."""
      self.send_response(404)
      self.send_header('Content-type', 'text/html')
      self.end_headers()

  def run(self, server_class=HTTPServer, handler_class=Handler) -> None:
    """Runs the fake printer."""
    server_address = ('', 80)
    self._logger.info('Starting fake printer on http://localhost:80')
    handler_class.printer = PrinterModel()
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
  try:
    FakePrinter().run()
  except OSError:
    print(
        'On Windows: try disabling World Wide Web Publishing Service to use '
        'port 80.')
