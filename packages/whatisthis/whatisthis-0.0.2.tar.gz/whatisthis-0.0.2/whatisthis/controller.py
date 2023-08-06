import os
from jinja2 import Template
from mimetypes import MimeTypes
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler

class RequestHandler(BaseHTTPRequestHandler):

    def __init__(self, emitter, images, categories, *args):
        self.images = images
        self.emitter = emitter
        self.categories = categories
        BaseHTTPRequestHandler.__init__(self, *args)

    def send_file(self, request, path):
        try:
            with open(path, 'r') as index:
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                template = Template(index.read())
                data = template.render(
                    categories=self.categories,
                    title='whatisthis'
                )
                self.wfile.write(bytes(data, 'utf8'))
        except FileNotFoundError as e:
            self.send_error(404)
        return

    def handle_image_service(self, request):
        parameters = parse_qs(request.query)
        if 'prev' in parameters:
            tag = parameters['tag'][0]
            previous = int(parameters['prev'][0])
            index = (previous + 1) % len(self.images)
            previous_path = self.images[index]
            self.emitter(previous_path, tag)
        else:
            previous_path = self.images[0]
        try:
            with open(previous_path, 'rb') as previous_image:
                mime = MimeTypes()
                mime_type = mime.guess_type(previous_path)
                self.send_response(200)
                self.send_header('Content-type', mime_type[0])
                self.end_headers()
                self.wfile.write(previous_image.read())
        except FileNotFoundError as e:
            self.send_error(404)
        return

    def do_GET(self):
        request = urlparse(self.path)

        if 'image' in request.path:
            return self.handle_image_service(request)

        index = os.path.join(os.path.dirname(__file__), 'index.html')
        self.send_file(request, index)
