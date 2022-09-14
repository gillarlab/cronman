#!/usr/bin/python3

import sys
import signal
import falcon
from wsgiref import simple_server
from cron import Cron
from json import dumps


class CronResource:
    def __init__(self, users: list):
        self.__users = users
        self.__cron = None

    def on_get(self, req, resp, user: str = '', cmd: str = ''):
        resp.content_type = falcon.MEDIA_JSON
        resp.text = None

        if not user:
            resp.status = falcon.HTTP_404
            resp.text = self.__json_dumps(self.__users)
            return
        else:
            try:
                self.__cron = Cron(user)
            except OSError:
                resp.status = falcon.HTTP_404
                return

        if not cmd:
            cmd = 'list'

        if cmd == 'list':
            resp.status = falcon.HTTP_200
            resp.content_type = falcon.MEDIA_JSON
            resp.text = self.__json_dumps(self.__cron.tasks())
        elif cmd == 'enable' or cmd == 'disable':
            try:
                _id = req.get_param('id')
                _id = int(_id)
            except TypeError:
                _id = -1

            if getattr(self.__cron, cmd)(_id):
                resp.status = falcon.HTTP_200
            else:
                resp.status = falcon.HTTP_404
        else:
            resp.status = falcon.HTTP_404

    @staticmethod
    def __json_dumps(data):
        return dumps(data, ensure_ascii=False).encode('utf8')


class WebApp:
    def __init__(self, users: list, port: int = 4321):
        self.__app = falcon.App()

        self.__app.add_route('/cron/', CronResource(users))
        self.__app.add_route('/cron/{user}/{cmd}', CronResource(users))

        self.__httpd = simple_server.make_server('0.0.0.0', port, self.__app)

        signal.signal(signal.SIGINT, WebApp.sigterm_handler)
        signal.signal(signal.SIGTERM, WebApp.sigterm_handler)

    def run(self):
        self.__httpd.serve_forever()

    # noinspection PyUnusedLocal
    @staticmethod
    def sigterm_handler(signum, frame):
        sys.exit(0)


if __name__ == '__main__':
    pass
