#!/usr/bin/env python

import os
import posixpath
import sys
import urllib
from http.client import NOT_FOUND, OK
from http.server import SimpleHTTPRequestHandler

VERSION = '0.1'
VENDOR_STRING = 'SPAS/{}'.format(VERSION)

ENABLE_COLORS = True

DEFAULT_ROOT_FOLDER = './dist'
DEFAULT_PORT = 8000


def _c(s, c):
    if not ENABLE_COLORS:
        return s
    return '\x1b[{}m{}\x1b[0m'.format(c, s)


class MyHTTPRequestHandler(SimpleHTTPRequestHandler):

    server_version = ' '.join((
        VENDOR_STRING,
        SimpleHTTPRequestHandler.server_version))
    static_folders = ['js', 'css', 'fonts', 'img']
    default_page = 'index.html'
    search_folders = None

    def _get_parsed_path(self):
        # Drop query string and fragment
        path = self.path.split('?', 1)[0].split('#', 1)[0]
        parts = path.split('/')
        return tuple(filter(None, parts))

    def send_head(self):
        path_parts = self._get_parsed_path()

        full_path = self._find_file(self.path)
        if full_path:
            return self._serve_static_file(full_path)

        if len(path_parts) and path_parts[0] in self.static_folders:
            # This will make sure we get a 404 trying to get a
            # non-existing static file
            self._send_404()
            return None

        return self._serve_default_page()

    def _find_file(self, file_path):
        for folder in self.search_folders:
            candidate = self.translate_path(self.path, root=folder)
            if os.path.isfile(candidate):
                return candidate

    def _serve_default_page(self):
        return self._serve_static_file(self.default_page, ctype='text/html')

    def _serve_static_file(self, path, ctype=None):
        if ctype is None:
            ctype = self.guess_type(path)

        try:
            f = open(path, 'rb')
        except OSError:
            self._send_404()
            return None

        try:
            self.send_response(OK)
            self.send_header("Content-type", ctype)
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified",
                             self.date_time_string(fs.st_mtime))
            self.end_headers()
            return f
        except:
            f.close()
            raise

    def _send_404(self):
        self.send_error(NOT_FOUND, "File not found")

    def log_message(self, fmtstr, *args):
        msg = fmtstr % args
        sys.stderr.write(
            '{address} - - [{datestamp}] {msg}\n'
            .format(
                address=_c(self.address_string(), '35'),
                datestamp=_c(self.log_date_time_string(), '36'),
                msg=msg))

    def log_request(self, code='-', size='-'):

        def _get_code_color():
            if code < 200:
                return '33'
            if code < 300:
                return '32'
            if code < 400:
                return '33'
            return '31'

        self.log_message(
            '%s', '"{reqline}" {code} {size}'
            .format(reqline=self._colorize_requestline(self.requestline),
                    code=_c(code, _get_code_color()),
                    size=_c(size, '34')))

    def _colorize_requestline(self, rqline):
        def _get_method_color(method):
            if method in ['GET', 'HEAD', 'OPTIONS']:
                return '1;32'
            return '1;31'

        method, rest = rqline.split(None, 1)
        path, http = rest.rsplit(None, 1)
        return '{method} {path} {http}'.format(
            method=_c(method, _get_method_color(method)),
            path=_c(path, '1'), http=_c(http, '34'))

    def translate_path(self, path, root=None):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        # abandon query parameters
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        # Don't forget explicit trailing slash when normalizing. Issue17324
        trailing_slash = path.rstrip().endswith('/')
        try:
            path = urllib.parse.unquote(path, errors='surrogatepass')
        except UnicodeDecodeError:
            path = urllib.parse.unquote(path)
        path = posixpath.normpath(path)
        words = path.split('/')
        words = filter(None, words)
        path = root or os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)
        if trailing_slash:
            path += '/'
        return path
