SET( CMAKE_BUILD_TYPE "Release" CACHE STRING "macSLRelease" FORCE )
SET( BUILD_TESTING ON CACHE BOOL "macSLRelease" FORCE )
SET( BUILD_SHARED_LIBS OFF CACHE BOOL "macSLRelease" FORCE )
SET( BUILD_EXAMPLES ON CACHE BOOL "macSLRelease" FORCE )
SET( OTB_USE_CURL ON CACHE BOOL "macSLRelease" FORCE )
SET( OTB_USE_PQXX OFF CACHE BOOL "macSLRelease" FORCE)
SET( OTB_USE_EXTERNAL_BOOST OFF CACHE BOOL "debianRelease" FORCE )
SET( OTB_USE_EXTERNAL_EXPAT ON CACHE BOOL "debianRelease" FORCE )
SET( USE_FFTWD OFF CACHE BOOL "macSLRelease" FORCE )
SET( USE_FFTWF OFF CACHE BOOL "macSLRelease" FORCE )
SET( OTB_DATA_ROOT "/Users/manuel/Documents/OTB/Src/OTB-Data" CACHE STRING "macSLRelease" FORCE )
SET( OTB_DATA_USE_LARGEINPUT OFF CACHE BOOL "macSLRelease" FORCE )
#SET( OTB_DATA_LARGEINPUT_ROOT "/mnt/sdb1/OTB/trunk/OTB-Data/LargeInput" CACHE STRING "macSLRelease" FORCE )
SET( CMAKE_C_FLAGS " -Wall -fprofile-arcs -ftest-coverage" CACHE STRING "macSLRelease" FORCE )
SET( CMAKE_CXX_FLAGS " -Wall -Wno-deprecated -fprofile-arcs -ftest-coverage" CACHE STRING "macSLRelease" FORCE )
SET( CMAKE_EXE_LINKER "-Wno-deprecated -fprofile-arcs -ftest-coverage" CACHE STRING "macSLRelease" FORCE )
SET( MAKECOMMAND "/usr/bin/make -i -k -j 6" CACHE STRING "macSLRelease" FORCE )
SET( OTB_GL_USE_ACCEL ON CACHE BOOL "macSLRelease" FORCE )
SET( OTB_COMPILE_WITH_FULL_WARNING ON CACHE BOOL "macSLRelease" FORCE )
SET( ITK_USE_REVIEW ON CACHE BOOL "macSLRelease" FORCE )
SET( ITK_USE_OPTIMIZED_REGISTRATION_METHODS ON CACHE BOOL "Multithreaded registration" FORCE )


SET( FLTK_BASE_LIBRARY "/Users/manuel/Documents/Local/fltk-1.3.x-r6960-build/lib/libfltk.a" CACHE STRING "macSLRelease" FORCE )
SET( FLTK_CONFIG_SCRIPT "/Users/manuel/Documents/Local/fltk-1.3.x-r6960-build/bin/fltk-config" CACHE STRING "macSLRelease" FORCE )
SET( FLTK_FLUID_EXECUTABLE "/Users/manuel/Documents/Local/fltk-1.3.x-r6960-build/bin/fluid" CACHE STRING "macSLRelease" FORCE )
SET( FLTK_DIR "/Users/manuel/Documents/Local/fltk-1.3.x-r6960-build" CACHE STRING "macSLRelease" FORCE )
SET( FLTK_FORMS_LIBRARY "/Users/manuel/Documents/Local/fltk-1.3.x-r6960-build/lib/libfltk_forms.a" CACHE STRING "macSLRelease" FORCE )
SET( FLTK_GL_LIBRARY "/Users/manuel/Documents/Local/fltk-1.3.x-r6960-build/lib/libfltk_gl.a" CACHE STRING "macSLRelease" FORCE )
SET( FLTK_IMAGES_LIBRARY "/Users/manuel/Documents/Local/fltk-1.3.x-r6960-build/lib/libfltk_images.a" CACHE STRING "macSLRelease" FORCE )
SET( FLTK_INCLUDE_LIBRARY "/Users/manuel/Documents/Local/fltk-1.3.x-r6960-build/include" CACHE STRING "macSLRelease" FORCE )

SET( ITK_FLTK_RESOURCE mac.H "${FLTK_DIR}/include/FL" CACHE STRING "macSLRelease" FORCE ) 
#SET( OTB_USE_MAPNIK ON CACHE BOOL "Using mapnik" FORCE)
#SET( MAPNIK_INCLUDE_DIR "/home/christop/slash/include" CACHE STRING "mapnik include" FORCE)
#SET( MAPNIK_LIBRARY "/home/christop/slash/lib64/libmapnik.so" CACHE STRING "mapnik lib" FORCE)