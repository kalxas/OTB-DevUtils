# Client maintainer: julien.malik@c-s.fr
set(OTB_PROJECT OTB) # OTB / Monteverdi / Monteverdi2
set(OTB_ARCH x86) # x86 / amd64
set(CTEST_BUILD_CONFIGURATION RelWithDebInfo)
set(CTEST_BUILD_TARGET INSTALL)
include(${CTEST_SCRIPT_DIRECTORY}/raoul_common.cmake)

macro(dashboard_hook_init)
  set(dashboard_cache "${dashboard_cache}
  
CMAKE_INSTALL_PREFIX:PATH=${CTEST_DASHBOARD_ROOT}/install/${OTB_PROJECT}-vc10-${OTB_ARCH}-${CTEST_BUILD_CONFIGURATION}

BUILD_TESTING:BOOL=ON
BUILD_EXAMPLES:BOOL=ON
BUILD_APPLICATIONS:BOOL=ON
OTB_WRAP_PYTHON:BOOL=ON
OTB_WRAP_QT:BOOL=ON

OTB_DATA_ROOT:STRING=${CTEST_DASHBOARD_ROOT}/src/OTB-Data
OTB_DATA_USE_LARGEINPUT:BOOL=ON
OTB_DATA_LARGEINPUT_ROOT:PATH=${CTEST_DASHBOARD_ROOT}/src/OTB-LargeInput

OTB_USE_CURL:BOOL=ON
OTB_USE_EXTERNAL_EXPAT:BOOL=ON
OTB_USE_EXTERNAL_FLTK:BOOL=OFF
OTB_USE_EXTERNAL_OSSIM:BOOL=ON
OTB_USE_LIBLAS:BOOL=ON
OTB_USE_EXTERNAL_LIBLAS:BOOL=ON
OTB_USE_GETTEXT:BOOL=OFF
OTB_USE_JPEG2000:BOOL=ON

OTB_USE_OPENCV:BOOL=ON
OpenCV_DIR:PATH=${OSGEO4W_ROOT}/share/OpenCV

OTB_USE_EXTERNAL_ITK:BOOL=ON
ITK_DIR:PATH=${CTEST_DASHBOARD_ROOT}/build/ITK-x86-RelDeb

SWIG_EXECUTABLE:FILEPATH=${OSGEO4W_ROOT}/apps/swigwin/swig.exe

PYTHON_EXECUTABLE:FILEPATH=${OSGEO4W_ROOT}/bin/python.exe
PYTHON_INCLUDE_DIR:PATH=${OSGEO4W_ROOT}/apps/Python27/include
PYTHON_LIBRARY:FILEPATH=${OSGEO4W_ROOT}/apps/Python27/libs/python27.lib

    ")
endmacro()

#remove install dir
execute_process(COMMAND ${CTEST_CMAKE_COMMAND} -E remove_directory ${CTEST_DASHBOARD_ROOT}/install/${OTB_PROJECT}-vc10-${OTB_ARCH}-${CTEST_BUILD_CONFIGURATION})

include(${CTEST_SCRIPT_DIRECTORY}/../otb_common.cmake)
