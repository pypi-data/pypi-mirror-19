import argparse
import os
import ssl
import sys
from http.server import HTTPServer

from .server import DEFAULT_PORT, DEFAULT_ROOT_FOLDER, MyHTTPRequestHandler


HERE = os.path.dirname(__file__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--bind', '-b', default='', metavar='ADDRESS',
        help='Specify alternate bind address [default: all interfaces]')
    parser.add_argument(
        '--port', '-p', action='store', default=DEFAULT_PORT, type=int,
        help='Specify alternate port [default: {}]'.format(DEFAULT_PORT))
    parser.add_argument(
        '--root', action='store', default=DEFAULT_ROOT_FOLDER,
        help='Root directory to serve.')
    parser.add_argument(
        '--static', default='js,css,fonts,img', metavar='LIST',
        help='Comma-separated list of folders containing static files. '
        'File not found inside one of these folders will return 404 instead '
        'of the default index page.')
    parser.add_argument(
        '--default-page', default='index.html', metavar='PATH',
        help='Path to the default HTML page to be served for non-existing '
        'paths. Default: index.html. Relative to the root path.')
    parser.add_argument(
        '--ssl', action='store_true', default=False,
        help='Enable SSL')
    args = parser.parse_args()

    server_address = (args.bind, args.port)
    root_folder_path = os.path.abspath(args.root)
    MyHTTPRequestHandler.search_folders = [
        root_folder_path,
    ]
    MyHTTPRequestHandler.default_page = os.path.join(
        root_folder_path, args.default_page)
    MyHTTPRequestHandler.static_folders = args.static.split(',')
    httpd = HTTPServer(server_address, MyHTTPRequestHandler)

    sa = httpd.socket.getsockname()
    print("Serving HTTP on", sa[0], "port", sa[1], "...")
    print('Root directory: {}'.format(os.path.abspath(args.root)))

    if args.ssl:
        print('Enabling SSL (TLSv1)')

        cert_file = os.path.join(HERE, 'server.pem')
        CREATE_CERT_COMMAND = (
            "openssl req -new -x509 -keyout '{0}' -out '{0}' -days 365 -nodes "
            "-subj '/C=XX/ST=Some-State/O=MyOrg'".format(cert_file))
        if not os.path.exists(cert_file):
            print('Certificate not found')
            print('Generate one using the following command:\n\n    {}'
                  .format(CREATE_CERT_COMMAND))
            sys.exit(1)

        httpd.socket = ssl.wrap_socket(
            httpd.socket,
            certfile=cert_file,
            server_side=True,
            ssl_version=ssl.PROTOCOL_TLSv1,
        )

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        httpd.server_close()
