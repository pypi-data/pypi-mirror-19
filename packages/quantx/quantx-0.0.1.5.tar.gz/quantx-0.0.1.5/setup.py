# coding=utf-8

import setuptools
from setuptools import find_packages
import quantx

setuptools.setup(
    name="quantx",
    packages=find_packages(exclude=["examples", "docs", "csquant", "tests"]),
    version=quantx.__version__,
    description="",
    author="chinascope",
    license="BSD",
    author_email="it@chinascope.com",
    url="http://chinascope.com",
    # download_url=download_url,
    install_requires=["pandas", "odo", "click", "tqdm", "requests"],
    entry_points={
        "console_scripts": [
            "quantx = quantx.cli:main",
        ]
    },
    keywords=("backtest", "stock", "quant", "chinascope"),
    classifiers=[
        # How mature is this project? Common values are
        # 3 - Alpha
        "Development Status :: 4 - Beta",
        # 5 - Production/Stable
        # "Development Status :: 5 - Production/Stable",

        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent",

        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: BSD License",

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3.5"
    ],
    long_description=""
)
