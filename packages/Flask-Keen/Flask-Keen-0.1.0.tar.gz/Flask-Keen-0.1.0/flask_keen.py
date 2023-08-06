#
# Flask-Keen
#
# Copyright (C) 2017 Boris Raicheff
# All rights reserved
#


import logging

from keen.client import KeenClient


logger = logging.getLogger('Flask-Keen')


class Keen(object):
    """
    Flask-Keen

    Documentation:
    https://flask-keen.readthedocs.io

    API:
    https://keen.io/docs

    :param app: Flask app to initialize with. Defaults to `None`
    """

    client = None

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        project_id = app.config.get('KEEN_PROJECT_ID')
        read_key = app.config.get('KEEN_READ_KEY')
        write_key = app.config.get('KEEN_WRITE_KEY')
        if not all((project_id, read_key, write_key)):
            logger.warning('KEEN credentials not set')
            return
        self.client = KeenClient(
            project_id=project_id,
            read_key=read_key,
            write_key=write_key,
        )

    def __getattr__(self, name):
        return getattr(self.client, name)


# EOF
