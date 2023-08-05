# -*- coding: utf-8 -*-
import os
import requests
import jinja2
import exceptions
import urls


def enum(**enums):
    # support enum type
    return type('Enum', (), enums)


PWD = os.path.dirname(os.path.realpath(__file__))
APP_TYPES = enum(SIMPLE=1, LARGE=2)


def get_file_map(app_type):
    '''
    - dirs
    Enter the name of the folder to be created.

    - remote_files
    The first argument enter the filename to be used in the project.
    Enter the URL to download as the second argument.

    - local_files
    The first argument is the name of the file in the flask generator project.
    In the second argument, enter the filename to be used in the project.
    '''

    if app_type == APP_TYPES.SIMPLE:
        file_map = {
            'dirs': [
                'templates',
                'static/css',
                'static/js',
                'static/img'
            ],
            'remote_files': [
                ('static/css/bootstrap.min.css', urls.BOOTSTRAP_CSS),
                ('static/js/bootstrap.min.js', urls.BOOTSTRAP_JS),
                ('static/js/jquery.min.js', urls.JQUERY_JS)
            ],
            'local_files': [
                ('README.md', 'templates/README.md.j2'),
                ('.gitignore', 'templates/.gitignore'),
                ('config.py', 'config/prod.py.j2'),
                ('app.py', 'templates/app_simple.py'),
                ('__init__.py', 'templates/__init__.py'),
                ('requirements.txt', 'templates/requirements.txt'),
                ('templates/layout.html', 'templates/html/layout.html'),
                ('templates/index.html', 'templates/html/index.html')
            ]
        }
    elif app_type == APP_TYPES.LARGE:
        file_map = {
            'dirs': [
                'config',
                'bin',
                'app/templates',
                'app/static/css',
                'app/static/js',
                'app/static/img',
                'app/models',
                'app/views'
            ],
            'remote_files': [
                ('app/static/css/bootstrap.min.css', urls.BOOTSTRAP_CSS),
                ('app/static/js/bootstrap.min.js', urls.BOOTSTRAP_JS),
                ('app/static/js/jquery.min.js', urls.JQUERY_JS)
            ],
            'local_files': [
                ('README.md', 'templates/README.md.j2'),
                ('.gitignore', 'templates/.gitignore'),
                ('config/__init__.py', 'templates/__init__.py'),
                ('config/prod.py', 'config/prod.py.j2'),
                ('config/dev.py', 'config/dev.py.j2'),
                ('manage.py', 'templates/manage.py'),
                ('requirements.txt', 'templates/requirements.txt'),
                ('__init__.py', 'templates/__init__.py'),
                ('app/__init__.py', 'templates/__init__.py'),
                ('app/app.py', 'templates/app_large.py'),
                ('app/templates/layout.html', 'templates/html/layout.html'),
                ('app/templates/index.html', 'templates/html/index.html'),
                ('app/views/__init__.py', 'templates/views/__init__.py'),
                ('app/views/index.py', 'templates/views/index.py')
            ]
        }
    else:
        raise exceptions.NotSupportAppTypeException(
            'not support app_type: %s' % app_type)
    return file_map


def generate_random_hex():
    return os.urandom(24).encode('hex')


def download_file(dest, url):
    r = requests.get(url, stream=True)
    with open(dest, 'wb') as fp:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                fp.write(chunk)


def create_virtualenv():
    # After creating the virtual environment, install the library
    command = 'virtualenv venv'
    os.system(command)


def install_lib_with_virtualenv():
    command = 'source venv/bin/activate;' \
              'pip install -r requirements.txt'
    os.system(command)


def configure_git(github_user, github_repo, is_git_push=True):
    git_url = 'https://github.com/' + github_user + '/' + github_repo + '.git'
    os.system('git init')
    os.system('git remote add origin %s' % git_url)
    os.system('git add --all')
    os.system('git commit -m "project initialize"')
    if is_git_push:
        os.system('git push origin master')


def render(filename, context):
    loader = jinja2.FileSystemLoader(PWD)
    env = jinja2.Environment(loader=loader)
    template = env.get_template(filename)
    return template.render(context)


def load_file_data(file_path):
    with open(file_path, 'r') as fp:
        file_data = fp.read()
    return file_data


class AppGenerator(object):
    def __init__(self, app_type, app_name):
        self.app_type = app_type
        self.app_name = app_name
        self.destination_path = PWD
        self.install_path = os.getcwd()

    def init_app(self):
        os.mkdir(self.app_name)
        os.chdir(self.app_name)
        create_virtualenv()

    def build_app(self):
        file_map = get_file_map(self.app_type)

        # create dirs
        for d in file_map['dirs']:
            os.makedirs(d)

        # create local_files
        for lf in file_map['local_files']:
            file_ext = os.path.splitext(lf[1])[1]
            if file_ext == '.j2':
                # if it is a .j2 file, render it as jinja2
                context = {
                    'SECRET_KEY': generate_random_hex(),
                    'APP_NAME': self.app_name
                }
                data = render(lf[1], context)
            else:
                path = os.path.join(self.destination_path, lf[1])
                data = load_file_data(path)
            with open(lf[0], 'w') as fp:
                fp.write(data)

        # create remote_files
        for rf in file_map['remote_files']:
            # print rf
            dest = os.path.join(self.install_path, self.app_name, rf[0])
            url = rf[1]
            download_file(dest, url)

        # install lib
        install_lib_with_virtualenv()


if __name__ == '__main__':
    gen = AppGenerator(APP_TYPES.SIMPLE, 'app')
    gen.init_app()
    gen.build_app()
