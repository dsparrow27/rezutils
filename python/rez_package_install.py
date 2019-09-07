# -*- coding: utf-8 -*-

import subprocess
import sys
import logging
import fnmatch
import os
import os.path
import shutil

logging.basicConfig(format="%(module)s - [%(levelname)s] - %(msg)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Include all files from a package, except these
# Think of these as a `.gitignore`
IGNORE = [
    "package.py",
    "rezbuild.py",
    "build",
    ".git",
    "doc*",
    "*.pyc",
    ".cache",
    "__pycache__",
    "*.pyproj",
    "*.sln",
    ".vs",
    ".bez*",
    "build.rxt",
    ".gitignore"
]


def copyBuild(source_path, destination_path, symlink=False):
    for name in os.listdir(source_path):
        if any(fnmatch.fnmatch(name, pat) for pat in IGNORE):
            continue
        src = os.path.join(source_path, name)
        dest = os.path.join(destination_path, name)
        if not os.path.exists(src):
            continue
        if os.path.exists(dest):
            logger.debug("Removing path: {}".format(dest))
            if os.path.isdir(dest):
                shutil.rmtree(dest)
            else:
                os.remove(dest)
        logger.debug("Copying path: {} -> {}".format(src, dest))
        if os.path.isdir(src):
            if symlink:
                subprocess.check_call('mklink /J "{}" "{}"'.format(dest,
                                                                   os.path.normpath(src)), shell=True)
            else:
                shutil.copytree(src, dest)


def build(source_path, build_path, install_path, targets, symlink=False):
    def _build():
        copyBuild(source_path, build_path, symlink)

    def _install():
        copyBuild(source_path, install_path, symlink)

    _build()

    if "install" in (targets or []):
        _install()


def main():
    import argparse

    parser = argparse.ArgumentParser("rezbuild")
    parser.add_argument("--command")
    parser.add_argument("--source_path", type=lambda s: unicode(s, 'utf8'))
    parser.add_argument("--build_path",
                        type=lambda s: unicode(s, 'utf8'),
                        default=os.getenv("REZ_BUILD_PATH"))
    parser.add_argument("--install_path",
                        type=lambda s: unicode(s, 'utf8'),
                        default=os.getenv("REZ_BUILD_INSTALL_PATH"))
    parser.add_argument("--install", type=bool,
                        default=bool(os.getenv("REZ_BUILD_INSTALL")))
    parser.add_argument("--symlink",
                        action="store_true")

    opts = parser.parse_args()

    targets = ["install"] if opts.install else []
    logger.debug(str(opts))
    build(opts.source_path,
          opts.build_path,
          opts.install_path,
          targets,
          symlink=opts.symlink)


if __name__ == '__main__':
    main()
