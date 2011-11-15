SET (ENV{DISPLAY} ":0")
SET (ENV{CC} "/usr/bin/gcc-4.2")
SET (ENV{CPP} "/usr/bin/cpp-4.2")
SET (ENV{CXX} "/usr/bin/g++-4.2")

SET (CTEST_SOURCE_DIRECTORY "/Users/otbval/WWW.ORFEO-TOOLBOX.ORG-CS-NIGHTLY/OTB")
SET (CTEST_BINARY_DIRECTORY "/Users/otbval/OTB-NIGHTLY-VALIDATION/build/OTB-macport")

SET( CTEST_CMAKE_GENERATOR  "Unix Makefiles" )
SET (CTEST_CMAKE_COMMAND "cmake" )
SET (CTEST_BUILD_COMMAND "/usr/bin/make -j6" )
SET (CTEST_SITE "leod.c-s.fr")
SET (CTEST_BUILD_NAME "MacOSX10.5-Release-macport")
SET (CTEST_BUILD_CONFIGURATION "Release")
SET (CTEST_HG_COMMAND "/usr/local/bin/hg")
SET (CTEST_HG_UPDATE_OPTIONS "-C")


SET (CTEST_INITIAL_CACHE "
BUILDNAME:STRING=${CTEST_BUILD_NAME}
SITE:STRING=${CTEST_SITE}
CTEST_USE_LAUNCHERS:BOOL=ON

OTB_DATA_USE_LARGEINPUT:BOOL=ON
OTB_DATA_LARGEINPUT_ROOT:STRING=/media/otbnas/otb/OTB-LargeInput
OTB_DATA_ROOT:STRING=$ENV{HOME}/WWW.ORFEO-TOOLBOX.ORG-CS-NIGHTLY/OTB-Data

CMAKE_C_FLAGS:STRING= -Wall -Wno-uninitialized -Wno-unused-variable -fPIC
CMAKE_CXX_FLAGS:STRING= -Wall -Wno-deprecated -Wno-uninitialized -Wno-unused-variable -fPIC

CMAKE_OSX_ARCHITECTURES:STRING=i386
OPENTHREADS_CONFIG_HAS_BEEN_RUN_BEFORE:BOOL=ON

CMAKE_BUILD_TYPE:STRING=Release
BUILD_TESTING:BOOL=ON
BUILD_EXAMPLES:BOOL=ON
BUILD_APPLICATIONS:BOOL=ON
WRAP_PYTHON:BOOL=ON
WRAP_QT:BOOL=ON
#WRAP_PYQT:BOOL=ON
WRAP_JAVA:BOOL=ON

# Enabling jpeg 2000 creates conflict with macport openjpeg
OTB_USE_JPEG2000:BOOL=OFF

OTB_USE_CURL:BOOL=ON
OTB_USE_PQXX:BOOL=OFF
ITK_USE_PATENTED:BOOL=ON
OTB_USE_PATENTED:BOOL=ON
OTB_USE_EXTERNAL_BOOST:BOOL=ON
OTB_USE_EXTERNAL_EXPAT:BOOL=ON
OTB_USE_EXTERNAL_FLTK:BOOL=OFF
OTB_USE_GETTEXT:BOOL=OFF
USE_FFTWD:BOOL=OFF
USE_FFTWF:BOOL=OFF
OTB_GL_USE_ACCEL:BOOL=OFF
ITK_USE_REVIEW:BOOL=ON 
ITK_USE_OPTIMIZED_REGISTRATION_METHODS:BOOL=ON 
OTB_USE_MAPNIK:BOOL=OFF
CMAKE_INSTALL_PREFIX:STRING=$ENV{HOME}/OTB-NIGHTLY-VALIDATION/install/OTB-macport

GDALCONFIG_EXECUTABLE:FILEPATH=/opt/local/bin/gdal-config
GDAL_CONFIG:FILEPATH=/opt/local/bin/gdal-config
GDAL_INCLUDE_DIR:STRING=/opt/local/include
GDAL_LIBRARY:FILEPATH=/opt/local/lib/libgdal.dylib

GEOTIFF_INCLUDE_DIRS:PATH=/opt/local/include
GEOTIFF_LIBRARY:FILEPATH=/opt/local/lib/libgeotiff.dylib

TIFF_INCLUDE_DIRS:PATH=/opt/local/include
TIFF_LIBRARY:FILEPATH=/opt/local/lib/libtiff.dylib

JPEG_INCLUDE_DIRS:PATH=/opt/local/include
JPEG_INCLUDE_DIR:PATH=/opt/local/include
JPEG_LIBRARY:FILEPATH=/opt/local/lib/libjpeg.dylib

#MAPNIK_INCLUDE_DIR:PATH=/opt/local/include
#MAPNIK_LIBRARY:FILEPATH=/opt/local/lib/libmapnik.dylib
#FREETYPE2_INCLUDE_DIR:PATH=/opt/local/include/freetype2

")

SET( PULL_RESULT_FILE "${CTEST_BINARY_DIRECTORY}/pull_result.txt" )

SET (CTEST_NOTES_FILES
${CTEST_SCRIPT_DIRECTORY}/${CTEST_SCRIPT_NAME}
${PULL_RESULT_FILE}
${CTEST_BINARY_DIRECTORY}/CMakeCache.txt
)

ctest_empty_binary_directory (${CTEST_BINARY_DIRECTORY})

execute_process( COMMAND ${CTEST_HG_COMMAND} pull http://hg.orfeo-toolbox.org/OTB-Nightly
                 WORKING_DIRECTORY "${CTEST_SOURCE_DIRECTORY}"
                 OUTPUT_VARIABLE   PULL_RESULT
                 ERROR_VARIABLE    PULL_RESULT )
file(WRITE ${PULL_RESULT_FILE} ${PULL_RESULT} )

ctest_start(Nightly)
ctest_update(SOURCE "${CTEST_SOURCE_DIRECTORY}")
file(WRITE "${CTEST_BINARY_DIRECTORY}/CMakeCache.txt" ${CTEST_INITIAL_CACHE})
ctest_configure (BUILD "${CTEST_BINARY_DIRECTORY}")
ctest_read_custom_files(${CTEST_BINARY_DIRECTORY})
ctest_build (BUILD "${CTEST_BINARY_DIRECTORY}")
ctest_test (BUILD "${CTEST_BINARY_DIRECTORY}" PARALLEL_LEVEL 4)
ctest_submit ()

