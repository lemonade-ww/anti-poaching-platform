import os

DEBUG = bool(os.environ.get("DJANGO_DEBUG", True))

from server.config.common import *

if DEBUG:
    from server.config.development import *
