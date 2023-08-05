try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages
from pip.req import parse_requirements
from src.flask_app_generator import __version__

install_reqs = parse_requirements('requirements.txt', session='hack')
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='flask_app_generator',
    version=__version__,
    packages=find_packages(exclude=['*.pyc']),
    install_requires=reqs,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'flask-app-generator=src.flask_app_generator.run:main'],
    },
    author='ClaudeSeo',
    author_email='ehdaudtj@gmail.com',
    url='https://github.com/SeoDongMyeong/flask-app-generator',
    description='Flask Project Generator',
    keywords=['flask', 'flask-project', 'flask-generator'],
    license='MIT License'
)
