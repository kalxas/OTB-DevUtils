
# add the remotes modules from input_dir to the output_list
macro(get_remote_modules input_dir output_list)
  file(GLOB _remote_files "${input_dir}/*.remote.cmake")
  foreach(_remote_f ${_remote_files})
    file(STRINGS ${_remote_f} _mod_line REGEX "otb_fetch_module")
    string(REGEX REPLACE "otb_fetch_module\\( *([a-zA-Z0-9]+)" "\\1" _mod_name ${_mod_line})
    list(APPEND ${output_list} ${_mod_name})
  endforeach()
endmacro()

macro(get_module_enable_cache module_list output_cache)
  foreach(mod ${${module_list}})
    set(${output_cache} "${${output_cache}}
Module_${mod}:BOOL=ON")
  endforeach()
endmacro()

macro(get_module_disable_cache module_list output_cache)
  foreach(mod ${${module_list}})
    set(${output_cache} "${${output_cache}}
Module_${mod}:BOOL=OFF")
  endforeach()
endmacro()

macro(enable_official_remote_modules otb_src_dir output_cache)
  set(${output_cache})
  get_remote_modules(${otb_src_dir}/Modules/Remote _output_list)
  get_module_enable_cache(_output_list output_cache)
endmacro()

# set the git update command to checkout the given branch (using CTEST_GIT_COMMAND)
# the macro looks for the git_updater scrip, and modifies CTEST_GIT_UPDATE_CUSTOM
macro(set_git_update_command _branch)
  if((NOT _git_updater_script) OR (NOT EXISTS "${_git_updater_script}"))
    if(EXISTS ${CTEST_SCRIPT_DIRECTORY}/git_updater.cmake)
      set(_git_updater_script ${CTEST_SCRIPT_DIRECTORY}/git_updater.cmake)
    elseif(EXISTS ${CTEST_SCRIPT_DIRECTORY}/../git_updater.cmake)
      set(_git_updater_script ${CTEST_SCRIPT_DIRECTORY}/../git_updater.cmake)
    elseif(EXISTS ${CTEST_SCRIPT_DIRECTORY}/../../git_updater.cmake)
      set(_git_updater_script ${CTEST_SCRIPT_DIRECTORY}/../../git_updater.cmake)
    endif()
  endif()
  set(CTEST_GIT_UPDATE_CUSTOM ${CMAKE_COMMAND} -D GIT_COMMAND:PATH=${CTEST_GIT_COMMAND} -D TESTED_BRANCH:STRING=${_branch} -P ${_git_updater_script})
endmacro()

macro(clean_directories)
  foreach(dir ${ARGV})
    if(IS_DIRECTORY ${dir})
      file(REMOVE_RECURSE ${dir})
      file(MAKE_DIRECTORY ${dir})
    endif()
  endforeach()
endmacro()
