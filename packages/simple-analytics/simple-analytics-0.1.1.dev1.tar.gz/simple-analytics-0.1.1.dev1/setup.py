from setuptools import setup
from codecs import open
from os import path

setup(
    name='simple-analytics',
    version='0.1.1.dev1',

    description=("A simple python interface for Google's Analytics Reports API" + 
            "(v3)."),

    url="https://github.com/euirim/simple-analytics",
    author="Euirim Choi",
    author_email="euirim@gmail.com",
    license="MIT",

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],

    keywords="simplea google analytics api",
    packages=["simplea"],
    install_requires=["google-api-python-client"],
    extras_require={},
    package_data={},
    data_files=[],
    entry_points={},
)
