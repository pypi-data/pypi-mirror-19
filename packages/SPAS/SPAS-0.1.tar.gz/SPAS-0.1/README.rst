SPAS - Single Page App Server
#############################

Development server for single-page apps.

For when ``python -m http.server`` is not enough.


Features
========

- Serve single-page apps, that is, serve the same HTML page no matter
  what the requested path.
- Serve static files as well
- Return "normal" 404s if a static file is missing, to avoid returning
  HTML when eg. a script was expected.
- Support SSL. This is mostly handy in case you want to test things
  like browser geolocation API locally using a custom domain (browsers
  only allow geolocation on HTTPS or localhost).


Sample usage
============

This will work nicely to serve the demo app::

    spas --bind 127.0.0.1 --port 8000 --root ./demo-app/ --static js,css,img --default-page index.html

Note that, since most options have acceptable defaults, the following
would do just the same::

    spas --root ./demo-app/


Full command help
=================

::

    usage: spas [-h] [--bind ADDRESS] [--port PORT] [--root ROOT] [--static LIST]
                [--default-page PATH] [--ssl]

    optional arguments:
      -h, --help            show this help message and exit
      --bind ADDRESS, -b ADDRESS
                            Specify alternate bind address [default: all
                            interfaces]
      --port PORT, -p PORT  Specify alternate port [default: 8000]
      --root ROOT           Root directory to serve.
      --static LIST         Comma-separated list of folders containing static
                            files. File not found inside one of these folders will
                            return 404 instead of the default index page.
      --default-page PATH   Path to the default HTML page to be served for non-
                            existing paths. Default: index.html. Relative to the
                            root path.
      --ssl                 Enable SSL
