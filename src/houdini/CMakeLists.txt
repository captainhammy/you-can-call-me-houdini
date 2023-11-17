# Handle installing Python files living in pythonX.Ylibs for the target Houdini Python version.

# The path to collapse/copy digital assets to.
set( PYTHON_LIBS_DIR "$ENV{REZ_BUILD_PATH}/houdini/python$ENV{HOUDINI_PYTHON_VERSION}libs" )

file( MAKE_DIRECTORY ${PYTHON_LIBS_DIR} )

# Find all digital asset files.
file( GLOB_RECURSE python_files "python$ENV{HOUDINI_PYTHON_VERSION}libs/*.py" )

foreach( python_file ${python_files} )
	configure_file( ${python_file} ${PYTHON_LIBS_DIR} COPYONLY )
endforeach()

# Install the collapsed or copied files.
rez_install_dirs( ${PYTHON_LIBS_DIR} DESTINATION houdini )
