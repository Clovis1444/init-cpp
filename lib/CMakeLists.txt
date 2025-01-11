cmake_minimum_required(VERSION 3.0.0)

# Note: library is declared static
add_library(AppLib STATIC
${CMAKE_CURRENT_SOURCE_DIR}/include/App/App.h
${CMAKE_CURRENT_SOURCE_DIR}/src/App.cpp
)

# Note: use PUBLIC to propagate include dir to the parent
target_include_directories(AppLib PUBLIC include)
