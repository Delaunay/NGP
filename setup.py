#!/usr/bin/env python
from pathlib import Path

from setuptools import setup

with open("ngp/core/__init__.py") as file:
    for line in file.readlines():
        if "version" in line:
            version = line.split("=")[1].strip().replace('"', "")
            break

extra_requires = {"plugins": ["importlib_resources"]}
extra_requires["all"] = sorted(set(sum(extra_requires.values(), [])))

if __name__ == "__main__":
    setup(
        name="ngp",
        version=version,
        extras_require=extra_requires,
        description="Neural Geometry Processing",
        long_description=(Path(__file__).parent / "README.rst").read_text(),
        author="Delaunay",
        author_email="anony@mous.com",
        license="BSD 3-Clause License",
        url="https://ngp.readthedocs.io",
        classifiers=[
            "License :: OSI Approved :: BSD License",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Operating System :: OS Independent",
        ],
        packages=[
            "ngp.core",
            "ngp.dataset",
            "ngp.model",
            "ngp.task",
            "ngp.plugins.example",
        ],
        setup_requires=["setuptools"],
        install_requires=[
            "importlib_resources",
            "assimp-py",
            "requests",
            "vtk"
        ],
        package_data={
            "ngp.data": [
                "ngp/data",
            ],
        },
    )
