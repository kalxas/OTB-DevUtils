# -----------------------------------------------------------------------------
# Nightly script for OpenJPEG trunk
# This will retrieve/compile/run tests/upload to cdash OpenJPEG
# Results will be available at: http://my.cdash.org/index.php?project=OPENJPEG
# ctest -S leod_openJPEG_trunk_nightly.cmake -V
# Author: mickael.savinaud@c-s.fr
# Date: 2011-06-17
# -----------------------------------------------------------------------------

cmake_minimum_required(VERSION 2.8)
SET (ENV{DISPLAY} ":0.0")

# Set where to find srr and test data and where to build binaries.
SET (CTEST_SOURCE_DIRECTORY       "$ENV{HOME}/OpenJPEG/src/trunk")
SET (CTEST_BINARY_DIRECTORY       "$ENV{HOME}/OpenJPEG/build/OpenJPEG_v1")
SET (CTEST_SOURCE_DATA_DIRECTORY  "$ENV{HOME}/OpenJPEG/src/opj-data")

# User inputs:
SET( CTEST_CMAKE_GENERATOR      "Unix Makefiles" )    # What is your compilation apps ?
SET( CTEST_CMAKE_COMMAND        "cmake" )
SET( CTEST_BUILD_COMMAND        "/usr/bin/make -j6" )
SET( CTEST_SITE                 "leod.c-s.fr" )       # Generally the output of hostname
SET( CTEST_BUILD_CONFIGURATION  Debug)                # What type of build do you want ?
SET( CTEST_BUILD_NAME           "MacOSX10.5-32bits-trunk-${CTEST_BUILD_CONFIGURATION}") # Build Name
SET( ENV{CFLAGS} "-Wall" )                            # All warnings ...

set( CACHE_CONTENTS "
CMAKE_BUILD_TYPE:STRING=${CTEST_BUILD_CONFIGURATION}

BUILD_TESTING:BOOL=TRUE
BUILD_EXAMPLES:BOOL=TRUE

JPEG2000_CONFORMANCE_DATA_ROOT:PATH=${CTEST_SOURCE_DATA_DIRECTORY}

BUILD_THIRDPARTY:BOOL=ON

" )

# Update method 
# repository: http://openjpeg.googlecode.com/branches/v2
# need to use https for CS machine
set( CTEST_UPDATE_COMMAND   "/usr/bin/svn")

# 3. cmake specific:
#set( CTEST_NOTES_FILES      "${CTEST_SCRIPT_DIRECTORY}/${CTEST_SCRIPT_NAME}")

ctest_empty_binary_directory( "${CTEST_BINARY_DIRECTORY}" )
file(WRITE "${CTEST_BINARY_DIRECTORY}/CMakeCache.txt" "${CACHE_CONTENTS}")

# Perform the Nightly build
ctest_start(Nightly TRACK Nightly-trunk)
ctest_update(SOURCE "${CTEST_SOURCE_DIRECTORY}")
ctest_configure(BUILD "${CTEST_BINARY_DIRECTORY}")
ctest_build(BUILD "${CTEST_BINARY_DIRECTORY}")
ctest_test(BUILD "${CTEST_BINARY_DIRECTORY}")
ctest_submit()

