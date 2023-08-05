# -*- coding: utf-8 -*-
from flask_script import Manager, Shell
from app.app import create_app


def main():
    manager = Manager(create_app)
    manager.add_option('-c', '--config', dest='config_name', required=False,
                       default='config.prod')
    manager.add_command('shell', Shell())
    manager.run()


if __name__ == '__main__':
    main()
