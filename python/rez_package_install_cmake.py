# -*- coding: utf-8 -*-

import subprocess
import logging
import os
import os.path
import shlex

logging.basicConfig(format="%(module)s - [%(levelname)s] - %(msg)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def run(cmd, cwdPath):
    p = subprocess.Popen(shlex.split(" ".join(cmd)), stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, cwd=cwdPath)
    while True:
        l = p.stdout.readline()
        if l != "":
            print(l)
        elif p.poll() is not None:
            break


def callcmake(source_path, build_path, install_path, generator, buildInstallType):
    from rezplugins import build_system

    cmakePaths = os.getenv("CMAKE_MODULE_PATH", "")
    rezcmakePaths = os.path.join(os.path.dirname(build_system.__file__), "cmake_files")

    cmakePaths = os.pathsep.join([cmakePaths, rezcmakePaths])
    cmd = ["cmake",
           "-d", source_path.replace("\\", "/"),
           "-DCMAKE_INSTALL_PREFIX={}".format(install_path.replace("\\", "/")),
           '-DCMAKE_MODULE_PATH={}'.format(cmakePaths.replace("\\", "/")),
           "-DCMAKE_BUILD_TYPE=Release",
           "-DREZ_BUILD_TYPE=local",
           "-DREZ_BUILD_INSTALL={}".format(buildInstallType),
           '-G "{}"'.format(generator)
           ]
    run(cmd, build_path)
    if buildInstallType == "1":
        print("running cmake --build {}".format(os.getcwd()))
        cmd = ["cmake", "--build",
               ".", "--target", "install"]
        run(cmd, build_path)


def build(source_path, build_path, install_path, targets, generator):
    buildInstallType = "1" if "install" in targets else "0"
    callcmake(source_path, build_path, install_path, generator, buildInstallType)


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
                        default=bool(os.getenv("REZ_BUILD_INSTALL")))
    parser.add_argument("--bs", type=str,
                        default="Visual Studio 15 2017 Win64")
    opts = parser.parse_args()

    targets = ["install"] if opts.install else []
    logger.debug(str(opts))

    build(opts.source_path,
          opts.build_path,
          opts.install_path,
          targets,
          generator=opts.bs)


if __name__ == '__main__':
    main()
