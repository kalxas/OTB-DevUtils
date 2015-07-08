# Client maintainer: julien.malik@c-s.fr
set(dashboard_model Nightly)
set(CTEST_DASHBOARD_ROOT "/home/otbval/Dashboard")
set(CTEST_SITE "hulk.c-s.fr")
set(CTEST_BUILD_CONFIGURATION Release)
set(CTEST_BUILD_NAME "Ubuntu14.04-64bits-${CTEST_BUILD_CONFIGURATION}")
set(CTEST_CMAKE_GENERATOR "Unix Makefiles")
set(CTEST_BUILD_COMMAND "/usr/bin/make -j10 -i -k install" )
set(CTEST_TEST_ARGS PARALLEL_LEVEL 6)
set(CTEST_TEST_TIMEOUT 500)
set(CTEST_USE_LAUNCHERS ON)
set(CTEST_GIT_COMMAND "/usr/bin/git")

set(dashboard_root_name "tests")
set(dashboard_source_name "src/Monteverdi")
set(dashboard_binary_name "build/Monteverdi")

set(MVD_INSTALL_PREFIX ${CTEST_DASHBOARD_ROOT}/install/Monteverdi)

#set(dashboard_fresh_source_checkout OFF)
set(dashboard_git_url "https://git@git.orfeo-toolbox.org/git/monteverdi.git")

macro(dashboard_hook_init)
  set(dashboard_cache "${dashboard_cache}

BUILDNAME:STRING=${CTEST_BUILD_NAME}
SITE:STRING=${CTEST_SITE}
CTEST_USE_LAUNCHERS:BOOL=ON

CMAKE_INSTALL_PREFIX:STRING=${MVD_INSTALL_PREFIX}
CMAKE_BUILD_TYPE:STRING=${CTEST_BUILD_CONFIGURATION}
BUILD_TESTING:BOOL=ON

CMAKE_C_FLAGS:STRING= -Wall -Wno-uninitialized -Wno-unused-variable
CMAKE_CXX_FLAGS:STRING= -Wall -Wno-deprecated -Wno-uninitialized -Wno-unused-variable

OTB_DATA_USE_LARGEINPUT:BOOL=ON
OTB_DATA_LARGEINPUT_ROOT:STRING=$ENV{HOME}/Data/OTB-LargeInput
OTB_DATA_ROOT:STRING=$ENV{HOME}/Dashboard/src/OTB-Data

OTB_DIR:STRING=$ENV{HOME}/Dashboard/build/OTB-RelWithDebInfo
OpenCV_DIR:PATH=/usr/share/OpenCV
")
endmacro()

execute_process(COMMAND ${CTEST_CMAKE_COMMAND} -E remove_directory ${MVD_INSTALL_PREFIX})
execute_process(COMMAND ${CTEST_CMAKE_COMMAND} -E make_directory ${MVD_INSTALL_PREFIX})

include(${CTEST_SCRIPT_DIRECTORY}/../otb_common.cmake)
