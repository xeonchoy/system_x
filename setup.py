from setuptools import setup, find_packages

setup(
    name="system_x",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'Flask',
        'Flask-Login',
        'Flask-SQLAlchemy',
        'Werkzeug'
    ],
)
