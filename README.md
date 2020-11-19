Adapted from 
https://github.com/mottosso/rez-for-projects

but trimmed down and supports windows junction points during build and cmake on windows.


example usage in package.py

..code-block:: python

    build_command = "rez-package-install --command build --source_path {root}"
    private_build_requires = ["rezutils"]

example usage of cmake

::note: Requires cmake as a rez package and visual studio installed

..code-block:: python

    build_command = "rez-package-install-cmake --command build --source_path {root}"
    private_build_requires = ["rezutils"]

By default we build local builds with symlinks enabled but you can turn that off with the below.
::note: Ultimately this really does nothing if you dont handle symlinks in your cmakelists, we embed the variable
`REZ_BUILD_SYMLINK` which will be set to either 1 for creating symlinks or 0 for no symlinks

..code-block:: shell
    rez build --install --clean -- --no_symlink

Now lets pass a build argument to cmake

..code-block:: shell
    >> rez build --install --clean -- -MYBUILD_ARG 0


..todo::
    - cmake macro for handling symlinks
