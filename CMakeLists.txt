cmake_minimum_required(VERSION 3.5)
project(Assem1)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

find_package(ament_cmake REQUIRED)

# Install các thư mục chứa dữ liệu mô hình vào workspace
install(
  DIRECTORY config launch meshes urdf rviz worlds
  DESTINATION share/${PROJECT_NAME}
)

install(FILES
  worlds/map.world
  DESTINATION share/${PROJECT_NAME}/worlds
)

ament_package()