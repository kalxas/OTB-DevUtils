SET (CTEST_SOURCE_DIRECTORY "C:/ORFEO/OTB-Applications")
SET (CTEST_BINARY_DIRECTORY "C:/ORFEO/otb-build/OTB-Applications/debug")

SET (CTEST_CMAKE_GENERATOR  "Visual Studio 10" )
SET (CTEST_CMAKE_COMMAND "C:/Program Files/CMake 2.8/bin/cmake.exe")
SET (CTEST_SITE "PO9450.c-s.fr" )
SET (CTEST_BUILD_NAME "Win7-Visual2010-Debug-Static")
SET (CTEST_BUILD_CONFIGURATION "Debug")
SET (CTEST_HG_COMMAND "C:/Program Files/TortoiseHg/hg.exe")
SET (CTEST_HG_UPDATE_OPTIONS "-C")


SET (OTB_INITIAL_CACHE "
BUILDNAME:STRING=${CTEST_BUILD_NAME}
SITE:STRING=${CTEST_SITE}

BUILD_TESTING:BOOL=ON
OTB_USE_CPACK:BOOL=ON

OTB_DATA_ROOT:STRING=C:/ORFEO/OTB-Data
OTB_DATA_USE_LARGEINPUT:BOOL=ON
OTB_DATA_LARGEINPUT_ROOT:PATH=C:/PartageVM/OTB-LargeInput

GDAL_INCLUDE_DIR:PATH=C:/OSGeo4W/apps/gdal-17/include
GDAL_LIBRARY:FILEPATH=C:/OSGeo4W/apps/gdal-17/lib/gdal_i.lib

OTB_DIR:PATH=C:/ORFEO/otb-build/OTB/debug
OTB_USE_CPACK:BOOL=ON

EXPAT_INCLUDE_DIR:PATH=C:/OSGeo4W/include
EXPAT_LIBRARY:FILEPATH=C:/OSGeo4W/lib/libexpat.lib

LIBLAS_INCLUDE_DIR:PATH=C:/OSGeo4W/include
LIBLAS_LIBRARY:FILEPATH=C:/OSGeo4W/lib/liblas_c.lib

OTB_USE_QT:BOOL=ON
OTB_USE_QGIS:BOOL=ON
QGIS_INCLUDE_DIRS:PATH=C:/OSGeo4W/apps/qgis/include
QGIS_LIBRARY:FILEPATH=C:/OSGeo4W/apps/qgis/lib/qgis_core.lib

# OTB Test driver to launch the tests
OTB_TEST_DRIVER:FILEPATH=C:/ORFEO/otb-build/OTB/bin/Debug/otbTestDriver.exe

")

ctest_empty_binary_directory (${CTEST_BINARY_DIRECTORY})

SET( OTB_PULL_RESULT_FILE "${CTEST_BINARY_DIRECTORY}/pull_result.txt" )
execute_process( COMMAND ${CTEST_HG_COMMAND} pull http://hg.orfeo-toolbox.org/OTB-Applications-Nightly
                 WORKING_DIRECTORY "${CTEST_SOURCE_DIRECTORY}"
                 OUTPUT_VARIABLE   OTB_PULL_RESULT
                 ERROR_VARIABLE    OTB_PULL_RESULT )
file(WRITE ${OTB_PULL_RESULT_FILE} ${OTB_PULL_RESULT} )

SET (CTEST_NOTES_FILES
${CTEST_SCRIPT_DIRECTORY}/${CTEST_SCRIPT_NAME}
${CTEST_BINARY_DIRECTORY}/CMakeCache.txt
${OTB_PULL_RESULT_FILE}
)


ctest_start(Nightly TRACK "Nightly Applications")
ctest_update(SOURCE "${CTEST_SOURCE_DIRECTORY}")
file(WRITE "${CTEST_BINARY_DIRECTORY}/CMakeCache.txt" ${OTB_INITIAL_CACHE})
ctest_configure (BUILD "${CTEST_BINARY_DIRECTORY}")
ctest_submit (PARTS Start Update Configure)
ctest_build (BUILD "${CTEST_BINARY_DIRECTORY}")
ctest_submit (PARTS Build)
ctest_test (BUILD "${CTEST_BINARY_DIRECTORY}" PARALLEL_LEVEL 4)
ctest_submit ()
