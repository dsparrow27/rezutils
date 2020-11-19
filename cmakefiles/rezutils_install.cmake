
# Wrapper macros around rez macro for copying files to handle symlinks.
# On windows(not sure if linux does the same thing) but LOCAL_SYMLINK argument of rez macros
# don't get ignored when releasing so rez tries to symlink to the release repository our main files
# so these macros just add the symlink only on release. Or and probably the reason is cause im doing
# something wrong with rez + cmake
# rezUtils_install_dirs
# rezUtils_install_files
# rezUtils_install_python


include(InstallDirs)
include(InstallFiles)
include(InstallPython)


macro(rezUtils_install_dirs)
    if (${REZ_BUILD_SYMLINK} EQUAL 1 AND ${REZ_BUILD_TYPE} STREQUAL "local")
        rez_install_dirs(${ARGV} LOCAL_SYMLINK)
    else()
        rez_install_dirs(${ARGV})
    endif()
endmacro()

macro(rezUtils_install_files)
    if (${REZ_BUILD_SYMLINK} EQUAL 1 AND ${REZ_BUILD_TYPE} STREQUAL "local")
        rez_install_files(${ARGV} LOCAL_SYMLINK)
    else()
        rez_install_files(${ARGV})
    endif()
endmacro()

macro(rezUtils_install_python)
    if (${REZ_BUILD_SYMLINK} EQUAL 1 AND ${REZ_BUILD_TYPE} STREQUAL "local")
        rez_install_python(${ARGV} LOCAL_SYMLINK)
    else()
        rez_install_python(${ARGV})
    endif()
endmacro()