from setuptools import setup, find_packages


def get_version():
    with open("./openapi_client/__init__.py") as f:
        return [
            eval(l.split("=")[1]) for l in f.readlines() if l.startswith("__version__")
        ][0]


with open("./openapi_client_README.md", "r") as f:
    long_description = f.read()

setup(
    name="passerine_client",
    version=get_version(),
    description="The API client for the antipoaching platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Zixuan James Li",
    author_email="p359101898@gmail.com",
    packages=find_packages("."),
    install_requires=["urllib3 >= 1.25.3", "python-dateutil"],
)
