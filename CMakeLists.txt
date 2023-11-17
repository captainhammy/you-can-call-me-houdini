cmake_minimum_required(VERSION 3.6)

include(RezBuild)

file(GLOB_RECURSE py_files "src/python/*.py" "src/python/*.yaml" "src/python/*.json")

rez_install_files(
    FILES ${py_files}
    RELATIVE src/python
    DESTINATION python
)

# Handle installing houdini/ files.
file(GLOB_RECURSE houdini_files RELATIVE "${CMAKE_SOURCE_DIR}" "src/houdini/*")

# Filter files to remove things we don't actually want to install. In particular we want
# to avoid any digital assets and Python bytecode files.
list(FILTER houdini_files EXCLUDE REGEX "src/houdini/python.+libs|.\.pyc|CMakeLists.txt")

rez_install_files(
    ${houdini_files}
    RELATIVE src/houdini
    DESTINATION houdini
)

add_subdirectory(src/houdini)
