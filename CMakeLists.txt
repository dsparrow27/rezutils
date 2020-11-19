cmake_minimum_required(VERSION 2.8)
include(RezBuild)
include(rezutils_install)
rez_project()

file(GLOB_RECURSE py_files "python/*.py")
file(GLOB_RECURSE bin_files "bin/*")
file(GLOB_RECURSE cmake_files "cmakefiles/*")

rezUtils_install_python(py
        FILES ${py_files}
        DESTINATION .
    )
rezUtils_install_files(
    ${bin_files}
    DESTINATION .
    EXECUTABLE
)
rezUtils_install_files(
    ${cmake_files}
    DESTINATION .
    EXECUTABLE
)
