name = "rezutils"
version = "1.0.0"
requires = [
    "python-2.7",
]

_category = "int"


def commands():
    global env
    env["PYTHONPATH"].prepend("{root}/python")
