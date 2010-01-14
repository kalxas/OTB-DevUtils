SET( CMAKE_BUILD_TYPE "Debug" CACHE STRING "debianDebug" FORCE )
SET( OTB_DIR "/home/otbtesting/OTB/OTB-Binary-Nightly" CACHE STRING "debianDebug" FORCE )
SET( OTB_DATA_ROOT "/home/christop/OTB/trunk/OTB-Data" CACHE STRING "debianDebug" FORCE )
SET( OTB_DATA_USE_LARGEINPUT "ON" CACHE STRING "debianDebug" FORCE )
SET( OTB_DATA_LARGEINPUT_ROOT "/home/christop/OTB/trunk/OTB-Data/LargeInput" CACHE STRING "debianDebug" FORCE )
SET( BUILD_TESTING "ON" CACHE STRING "debianDebug" FORCE )
SET( OTB_USE_VTK "ON" CACHE STRING "debianDebug" FORCE )
SET( CMAKE_C_FLAGS "  -Wall -fprofile-arcs -ftest-coverage" CACHE STRING "debianDebug" FORCE )
SET( CMAKE_CXX_FLAGS " -Wall -Wno-deprecated -fprofile-arcs -ftest-coverage" CACHE STRING "debianDebug" FORCE )
SET( CMAKE_EXE_LINKER "-Wno-deprecated -fprofile-arcs -ftest-coverage" CACHE STRING "debianDebug" FORCE )
SET( MAKECOMMAND "/usr/bin/make -i -k -j 2" CACHE STRING "debianDebug" FORCE )
