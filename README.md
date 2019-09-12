Adapted from 
https://github.com/mottosso/rez-for-projects

but trimmed down and supports windows junction points during build


example usage in package.py

..code-block:: python

    build_command = "rez-package-install --command build --source_path {root}"
    private_build_requires = ["rezutils"]