set(dashboard_model Nightly)
set(OTB_PROJECT OTB)
set(CTEST_DASHBOARD_ROOT "/home/mrashad/dashboard")
set(CTEST_SITE "binpkg.c-s.fr")
set(CTEST_BUILD_CONFIGURATION Release)
set(CTEST_BUILD_NAME "CentOS-5-x86_64-SuperBuild")
set(CTEST_CMAKE_GENERATOR "Unix Makefiles")
set(CTEST_BUILD_COMMAND "/usr/bin/make -k" )
set(CTEST_TEST_ARGS PARALLEL_LEVEL 3)
set(CTEST_TEST_TIMEOUT 500)
set(CTEST_GIT_COMMAND "/usr/bin/git")
set(CTEST_USE_LAUNCHERS ON)

set(CTEST_NIGHTLY_START_TIME "20:00:00 CEST")
set(CTEST_DROP_METHOD "http")
set(CTEST_DROP_SITE "dash.orfeo-toolbox.org")
set(CTEST_DROP_LOCATION "/submit.php?project=OTB")
set(CTEST_DROP_SITE_CDASH TRUE)

set(dashboard_source_name "otb/src/SuperBuild")
set(dashboard_binary_name "otb/build-stable")
set(dashboard_git_url "https://git@git.orfeo-toolbox.org/git/otb.git")
set(dashboard_update_dir ${CTEST_DASHBOARD_ROOT}/otb/src)
set(OTB_INSTALL_PREFIX ${CTEST_DASHBOARD_ROOT}/otb/install-stable)

include(${CTEST_SCRIPT_DIRECTORY}/../config_stable.cmake)

set(CTEST_BUILD_NAME "CentOS-5-x86_64-${dashboard_git_branch}-SuperBuild")

macro(dashboard_hook_init)
set(dashboard_cache "
CMAKE_INSTALL_PREFIX:PATH=${OTB_INSTALL_PREFIX}
CMAKE_BUILD_TYPE:STRING=${CTEST_BUILD_CONFIGURATION}
OTB_DATA_ROOT:PATH=/media/otbnas/otb/DataForTests/OTB-Data
DOWNLOAD_LOCATION:PATH=/media/otbnas/otb/DataForTests/SuperBuild-archives
CTEST_USE_LAUNCHERS:BOOL=${CTEST_USE_LAUNCHERS}
CMAKE_VERBOSE_MAKEFILE:BOOL=OFF
CMAKE_CXX_FLAGS:STRING='-w -fPIC'
CMAKE_C_FLAGS:STRING='-fPIC'
BUILD_TESTING:BOOL=ON

USE_SYSTEM_ZLIB:BOOL=OFF
USE_SYSTEM_PNG:BOOL=OFF
USE_SYSTEM_SQLITE:BOOL=OFF
USE_SYSTEM_JPEG:BOOL=OFF
USE_SYSTEM_TIFF:BOOL=OFF
USE_SYSTEM_GEOTIFF:BOOL=OFF
USE_SYSTEM_GEOS:BOOL=OFF
USE_SYSTEM_PROJ:BOOL=OFF
USE_SYSTEM_GDAL:BOOL=OFF

USE_SYSTEM_BOOST:BOOL=OFF
USE_SYSTEM_EXPAT:BOOL=OFF
OTB_USE_LIBKML:BOOL=ON
USE_SYSTEM_LIBKML:BOOL=OFF

USE_SYSTEM_FFTW:BOOL=OFF
USE_SYSTEM_ITK:BOOL=OFF

USE_SYSTEM_OPENTHREADS:BOOL=OFF
USE_SYSTEM_OSSIM:BOOL=OFF

OTB_USE_LIBSVM:BOOL=ON
USE_SYSTEM_LIBSVM:BOOL=OFF

OTB_USE_OPENCV:BOOL=ON
USE_SYSTEM_OPENCV:BOOL=OFF

USE_SYSTEM_TINYXML:BOOL=OFF

OTB_USE_OPENGL:BOOL=ON
OTB_USE_GLEW:BOOL=ON
OTB_USE_GLFW:BOOL=OFF
OTB_USE_GLUT:BOOL=OFF
USE_SYSTEM_GLUT:BOOL=OFF
USE_SYSTEM_GLFW:BOOL=OFF
USE_SYSTEM_GLEW:BOOL=OFF

OTB_USE_QT4:BOOL=ON
USE_SYSTEM_QT4:BOOL=OFF
USE_SYSTEM_QWT:BOOL=OFF
ENABLE_MONTEVERDI:BOOL=ON

OTB_USE_MUPARSER:BOOL=ON
OTB_USE_MUPARSERX:BOOL=ON

USE_SYSTEM_SWIG:BOOL=ON
USE_SYSTEM_PCRE:BOOL=ON
OTB_WRAP_PYTHON:BOOL=OFF
OTB_WRAP_JAVA:BOOL=OFF

OTB_USE_CURL:BOOL=ON
USE_SYSTEM_CURL:BOOL=OFF
USE_SYSTEM_OPENSSL:BOOL=OFF

OTB_USE_6S:BOOL=ON

OTB_USE_MAPNIK:BOOL=OFF

OTB_USE_OPENJPEG:BOOL=OFF
USE_SYSTEM_OPENJPEG:BOOL=OFF

OTB_USE_SIFTFAST:BOOL=ON

ENABLE_OTB_LARGE_INPUTS:BOOL=OFF
OTB_DATA_LARGEINPUT_ROOT:PATH=${CTEST_DASHBOARD_ROOT}/Data/OTB-LargeInput

GENERATE_PACKAGE:BOOL=OFF
")
endmacro()


# list(APPEND CTEST_TEST_ARGS
#   BUILD ${CTEST_DASHBOARD_ROOT}/${dashboard_binary_name}/OTB/build
# )

macro(dashboard_hook_test)
  set(ENV{LD_LIBRARY_PATH} ${OTB_INSTALL_PREFIX}/lib)
endmacro()

execute_process(COMMAND ${CMAKE_COMMAND} -E remove_directory  ${OTB_INSTALL_PREFIX})

list(APPEND CTEST_NOTES_FILES
  ${CTEST_DASHBOARD_ROOT}/${dashboard_binary_name}/OTB/build/CMakeCache.txt
  ${CTEST_DASHBOARD_ROOT}/${dashboard_binary_name}/OTB/build/otbConfigure.h
)

include(${CTEST_SCRIPT_DIRECTORY}/../otb_common.cmake)
