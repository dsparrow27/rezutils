# -*- coding: utf-8 -*-

import subprocess
import sys
import logging
import fnmatch
import os
import os.path
import shutil
import shlex

logging.basicConfig(format="%(module)s - [%(levelname)s] - %(msg)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def callcmake(source_path, destination_path, generator, buildInstallType):
    
    from rezplugins import build_system
    
    cmakePaths = os.getenv("CMAKE_MODULE_PATH", "")
    rezcmakePaths = os.path.join(os.path.dirname(build_system.__file__), "cmake_files")
    print(os.path.exists(rezcmakePaths))
    cmakePaths = os.pathsep.join([cmakePaths, rezcmakePaths])
    
    cmd = ["cmake",
        "-d", source_path, 
        "-DCMAKE_INSTALL_PREFIX={}".format(destination_path),
        '-DCMAKE_MODULE_PATH={}'.format(cmakePaths.replace("\\", "/")),
        "-DCMAKE_BUILD_TYPE=Release",
        "-DREZ_BUILD_TYPE=local",
        "-DREZ_BUILD_INSTALL={}".format(buildInstallType),
        '-G "{}"'.format(generator)
        ]
    print " ".join(cmd)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                 stderr=subprocess.STDOUT)
    while True:
        l = p.stdout.readline()
        if l != "":
            print(l)
        elif p.poll() is not None:
            break
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(p)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

def build(source_path, build_path, install_path, targets, generator):
    buildInstallType = "1" if "install" in targets else "0"
    callcmake(source_path, build_path, generator, buildInstallType)


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
    parser.add_argument("--bs", type=str,
                        default="Visual Studio 15 2017")
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
