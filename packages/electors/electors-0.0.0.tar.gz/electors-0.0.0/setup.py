
from setuptools import setup
from setuptools import find_packages

setup(
    name="electors",
    author="Anthony Pizzimenti",
    author_email="pizzimentianthony@gmail.com",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["electors=electors.electors:main"]
    }
)
