from setuptools import setup, find_packages

setup(
    name="flask_app",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "flask==2.0.1",
        "gunicorn==20.1.0",
        "pytest==6.2.5",
        "python-dotenv==0.19.0"
    ],
) 