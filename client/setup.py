import os
from setuptools import setup

with open("./openapi_client_README.md", "r") as f:
    long_description = f.read()

setup(
    name="passerine_client",
    version="0.0.1",
    description="The API client for the antipoaching platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Zixuan James Li",
    author_email="p359101898@gmail.com",
    packages=["openapi_client"],
    install_requires=["urllib3 >= 1.25.3", "python-dateutil"],
)
