# -*- coding: utf-8 -*-
name = "rezutils"
version = "1.0.0"
authors = ["David Sparrow"]
variants = [
    ["platform-windows", "python-2.7"]
]


def commands():
    global env
    env["PYTHONPATH"].prepend("{root}/python")
