cmake_minimum_required(VERSION 3.0.0)
project(App VERSION 0.0.1 LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Wpedantic -Weffc++ -Wno-sign-compare -Wconversion -Wsign-conversion -pedantic-errors")

# IMPORTANT: Generate COMPILE_COMMANDS.JSON file
set(CMAKE_EXPORT_COMPILE_COMMANDS ON CACHE INTERNAL "")

# Application library
add_subdirectory(lib)

# Application Executable
add_subdirectory(app)

# Platform specific actions
# if(WIN32)
#     message(STATUS "WINDOWS")
# elseif(APPLE)
#     message(STATUS "APPLE")
# elseif(UNIX AND NOT APPLE)
#     message(STATUS "LINUX")
# else()
#     message(STATUS "UNKNOWN OS")
# endif()
