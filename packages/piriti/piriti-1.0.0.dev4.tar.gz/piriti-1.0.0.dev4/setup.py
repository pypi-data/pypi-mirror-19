from setuptools import setup, find_packages

setup(
    name = "piriti",
    description = "Bridge between HTTP POST messages and WebSockets",
    version = "1.0.0-dev4",
    author = 'Lajos Santa',
    author_email = 'santa.lajos@coldline.hu',
    url = 'https://github.com/voidpp/piriti',
    install_requires = [
        "Flask-uWSGI-WebSocket==0.6",
        "voidpp-tools==1.8",
        "gevent==1.1",
        "querystring-parser==1.2",
        "PyYAML==3.12",
        "six==1.10.0"
    ],
    scripts = [],
    packages = find_packages(),
)
