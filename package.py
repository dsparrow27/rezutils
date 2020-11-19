# -*- coding: utf-8 -*-
name = "rezutils"
version = "1.1.1"
authors = ["David Sparrow"]
variants = [
    ["platform-windows", "python"]
]
requires = [
    "python",
    "cmake",
    "rez"
]
tools = [
    "rez-package-install",
    "rez-package-install-cmake"
]
build_command = "{root}/bin/rez-package-install-cmake --command build --source_path {root}"


def commands():
    global env
    env.PYTHONPATH.append("{root}/python")
    env.PATH.append("{root}/bin")
    env.CMAKE_MODULE_PATH.append("{ROOT}/cmakefiles")
