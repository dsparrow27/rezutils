# -*- coding: utf-8 -*-
name = "rezutils"
version = "1.1.5"
authors = ["David Sparrow"]
variants = [
    ["platform-windows"]
]
requires = [
    "python",
    "cmake",
    "rez-2+"
]
tools = [
    "rez-package-install",
    "rez-package-install-cmake"
]
build_command = "{root}/bin/rez-package-install-cmake --command build --source_path {root}"
private_build_requires = ["rezutils"]


def commands():
    global env
    env.PYTHONPATH.append("{root}/python")
    env.PATH.append("{root}/bin")
