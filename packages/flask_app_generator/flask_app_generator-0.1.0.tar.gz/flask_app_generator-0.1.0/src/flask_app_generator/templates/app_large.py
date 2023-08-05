# -*- coding: utf-8 -*-
from flask import Flask
from views import register_blueprint


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)
    register_blueprint(app)
    return app


if __name__ == '__main__':
    create_app('config')
