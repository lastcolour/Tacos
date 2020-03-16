project(TestProject)

if(PRINT_MESSAGE)
    add_definitions(-DPRINT_MESSAGE="${PRINT_MESSAGE}")
endif()

add_executable(${PROJECT_NAME} ${CMAKE_CURRENT_SOURCE_DIR}/main.cpp)