# -*- coding: utf-8 -*-

import subprocess
import logging
import os
import os.path
import shlex
from rezplugins import build_system
import inspect
logging.basicConfig(format="%(module)s - [%(levelname)s] - %(msg)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def run(cmd, cwdPath):
    logger.debug("Running cmake command: {}".format(shlex.split(" ".join(cmd))))
    p = subprocess.Popen(shlex.split(" ".join(cmd)), stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, cwd=cwdPath)
    while True:
        l = p.stdout.readline()
        if l:
            print(l.decode())
        elif p.poll() is not None:
            break


def callcmake(source_path, build_path, install_path, generator, buildInstallType, symlink, buildArgs):
    cmakePaths = os.getenv("CMAKE_MODULE_PATH", "")
    rezcmakePaths = os.path.join(os.path.dirname(build_system.__file__), "cmake_files")
    internalPaths = os.path.join(r"D:\dave\code\rez\git\rezutils\cmakefiles")

    cmakePaths = os.pathsep.join([cmakePaths, rezcmakePaths, internalPaths])

    cmd = ["cmake",
           "-d", source_path.replace("\\", "/"),
           "-DCMAKE_INSTALL_PREFIX={}".format(install_path.replace("\\", "/")),
           '-DCMAKE_MODULE_PATH={}'.format(cmakePaths.replace("\\", "/")),
           "-DCMAKE_BUILD_TYPE={}".format(os.getenv("CMAKE_BUILD_TYPE")),
           "-DREZ_BUILD_TYPE={}".format(os.getenv("REZ_BUILD_TYPE")),
           "-DREZ_BUILD_INSTALL={}".format(buildInstallType),
           "-DREZ_BUILD_SYMLINK={}".format(int(not symlink)),
           ]
    cmd += buildArgs
    cmd.append('-G "{}"'.format(generator))
    run(cmd, build_path)
    if buildInstallType == "1":
        cmd = ["cmake", "--build",
               ".", "--target", "install"]
        run(cmd, build_path)


def build(source_path, build_path, install_path, targets, generator, symlink, buildArgs):
    buildInstallType = "1" if "install" in targets else "0"
    callcmake(source_path, build_path, install_path, generator, buildInstallType,
              symlink, buildArgs)


def main():
    import argparse

    parser = argparse.ArgumentParser("rezbuild")
    parser.add_argument("--command")
    parser.add_argument("--source_path", type=str)
    parser.add_argument("--build_path",
                        type=str,
                        default=os.getenv("REZ_BUILD_PATH"))
    parser.add_argument("--install_path",
                        type=str,
                        default=os.getenv("REZ_BUILD_INSTALL_PATH"))
    parser.add_argument("--install", type=bool,
                        default=bool(int(os.getenv("REZ_BUILD_INSTALL"))))
    parser.add_argument("--bs", type=str,
                        default="Visual Studio 15 2017 Win64")
    parser.add_argument("--no_symlink", action="store_true")

    known, unknown = parser.parse_known_args()
    buildSystem = (known.bs.strip().replace("'", ""))
    targets = ["install"] if known.install else []
    logger.debug(str(known))
    build(known.source_path,
          known.build_path,
          known.install_path,
          targets,
          generator=buildSystem,
          symlink=known.no_symlink,
          buildArgs=unknown)


if __name__ == '__main__':
    main()
