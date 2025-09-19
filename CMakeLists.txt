cmake_minimum_required(VERSION 3.6)

include( RezBuild )
include( HoudiniRezCMakeTools )

file(GLOB_RECURSE py_files "src/python/*.py" "src/python/*.yaml" "src/python/*.json")

rez_install_files(
    FILES ${py_files}
    RELATIVE src/python
    DESTINATION python
)

# Handle installing houdini/ files.
file(GLOB_RECURSE houdini_files RELATIVE "${CMAKE_SOURCE_DIR}" "src/houdini/*")

# Filter files to remove things we don't actually want to install. In particular, we want
# to avoid the pythonX.Y libs folders as these are handled more specifically based on
# the Houdini version.
list(FILTER houdini_files EXCLUDE REGEX ".\.pyc|CMakeLists.txt")

# Remove any pythonX.Y libs paths as the specific ones will be handled next.
exclude_all_python_xylibs_dirs( houdini_files )

# Handle the specific pythonX.Ylibs for the target Houdini's Python version.
install_python_xylibs_dir_for_houdini_version( "src/houdini" )


rez_install_files(
    ${houdini_files}
    RELATIVE src/houdini
    DESTINATION houdini
)

add_subdirectory(src/houdini)
