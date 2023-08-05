import os
import io
import re
from setuptools import setup

def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(	name="bklv2",
        version=find_version( "bklv2", "__init__.py" ),
        url="https://github.com/etecor/bklv2",
        description="Backlog API v2 library",
        author="etecor",
        license="MIT",
        packages=["bklv2"],
        install_requires=["rfc6266", "requests"],
        classifiers=[
            #"Development Status :: 1 - Planning",
            "Development Status :: 2 - Pre-Alpha",
            #"Development Status :: 3 - Alpha",
            #"Development Status :: 4 - Beta",
            #"Development Status :: 5 - Production/Stable",
            #"Development Status :: 6 - Mature",
            #"Development Status :: 7 - Inactive",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
        ],
    )
