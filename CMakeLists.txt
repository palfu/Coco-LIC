cmake_minimum_required(VERSION 3.0.2)
project(cocolic)

set(CMAKE_BUILD_TYPE "Release")
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -Wall -g -Wno-sign-compare -Wno-unused -Wno-comment -pthread")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -msse4.2")

find_package(OpenMP)
if (OPENMP_FOUND)
    set (CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
endif()

include(cmake/sys_arch.cmake)
include(cmake/find_dependencies.cmake)
include(cmake/Protobuf.cmake)
if(NOT DEFINED DEPENDENCIES_PATH)
    if(EXISTS /dependencies)
        set(DEPENDENCIES_PATH /dependencies/)
    else()
        set(DEPENDENCIES_PATH ${CMAKE_CURRENT_SOURCE_DIR}/dependencies/)
    endif()
    message(STATUS "DEPENDENCIES_PATH not set, use default ${DEPENDENCIES_PATH}")
    message(STATUS "cmake ../  -DDEPENDENCIES_PATH=xxx")
endif()
message(STATUS ${DEPENDENCIES_PATH})
set_dependencies_dir(${DEPENDENCIES_PATH})

find_dependency_package(comm)
find_dependency_package(common)
find_dependency_package(hibag)
find_dependency_package(ipc)
find_dependency_package(log)
find_dependency_package(pos)
find_dependency_package(rte)
find_dependency_package(base)
find_dependency_package(error_relation)
find_dependency_package(easy_profiler)
find_dependency_thirdparty(jsoncpp)
find_dependency_thirdparty(boost)
find_dependency_thirdparty(pangolin)
find_dependency_thirdparty(eigen3)
find_dependency_thirdparty(gtsam)
find_dependency_thirdparty(pcl)
find_dependency_thirdparty(gtest)
find_dependency_thirdparty(opencv)
find_dependency_thirdparty(ffmpeg)
find_dependency_thirdparty(bdb)
find_dependency_thirdparty(zmq)
find_dependency_thirdparty(protobuf)
find_dependency_thirdparty(glog)
find_dependency_thirdparty(gflags)
find_dependency_thirdparty(class_loader)
find_dependency_thirdparty(vsomeip)
find_dependency_thirdparty(yamlcpp)
include_directories(
    ${jsoncpp_INCLUDE_DIRS}
    ${boost_INCLUDE_DIRS}
    ${gtsam_INCLUDE_DIRS}
    ${parking_slam_proto_INCLUDE_DIRS}
    ${pangolin_INCLUDE_DIRS}
    ${opencv_INCLUDE_DIRS}
    ${protobuf_INCLUDE_DIRS}
    ${pcl_INCLUDE_DIRS}
    ${glog_INCLUDE_DIRS}
    ${gflags_INCLUDE_DIRS}
    ${gtest_INCLUDE_DIRS}
    ${log_INCLUDE_DIRS}
    ${pos_INCLUDE_DIRS}
    ${comm_INCLUDE_DIRS}
    ${hibag_INCLUDE_DIRS}
    ${ipc_INCLUDE_DIRS}
    ${base_INCLUDE_DIRS}
    ${common_INCLUDE_DIRS}
    ${ffmpeg_INCLUDE_DIRS}
    ${yamlcpp_INCLUDE_DIRS}
    ${class_loader_INCLUDE_DIRS}
)
link_directories(
    ${jsoncpp_LIB_DIRS}
    ${boost_LIB_DIRS}
    ${gtsam_LIB_DIRS}
    ${parking_slam_proto_LIB_DIRS}
    ${pangolin_LIB_DIRS}
    ${opencv_LIB_DIRS}
    ${protobuf_LIB_DIRS}
    ${pcl_LIB_DIRS}
    ${glog_LIB_DIRS}
    ${gflags_LIB_DIRS}
    ${gtest_LIB_DIRS}
    ${log_LIB_DIRS}
    ${zmq_LIB_DIRS}
    ${pos_LIB_DIRS}
    ${comm_LIB_DIRS}
    ${hibag_LIB_DIRS}
    ${ipc_LIB_DIRS}
    ${rte_LIB_DIRS}
    ${base_LIB_DIRS}
    ${common_LIB_DIRS}
    ${ffmpeg_LIB_DIRS}
    ${class_loader_LIB_DIRS}
    ${easy_profiler_LIB_DIRS}
)
message("easy ${easy_profiler_LIB_DIRS}")
set(LIBS ${common_LIBS} ${hibag_LIBS} ${log_LIBS} 
  ${pos_LIBS} ${error_relation_LIBS} ${base_LIBS} ${protobuf_LIBS} 
  ${boost_LIBS} ${opencv_LIBS} ${easy_profiler_LIBS} ${jsoncpp_LIBS} 
  ${ffmpeg_LIBS} ${pcl_LIBS} ${glog_LIBS} ${gtest_LIBS})

## Specify additional locations of header files
## Your package locations should be listed before o `ther locations
include_directories(
  ${CMAKE_CURRENT_SOURCE_DIR}/src
  ${CMAKE_CURRENT_SOURCE_DIR}/src/camera
  ${CMAKE_CURRENT_SOURCE_DIR}/src/camera/loam/include
  ${CMAKE_CURRENT_SOURCE_DIR}/src/camera/tools/
  ${CMAKE_CURRENT_SOURCE_DIR}/src/camera/rgb_map
)

add_library(spline_lib SHARED src/spline/trajectory.cpp)
target_link_libraries(spline_lib ${LIBS})

file(GLOB lidar_files
    "src/lidar/lidar_handler.cpp"
    "src/lidar/velodyne_feature_extraction.cpp",
    "src/lidar/livox_feature_extraction.cpp"
)
add_library(lidar_lib SHARED ${lidar_files})
target_link_libraries(lidar_lib spline_lib ${LIBS})

file(GLOB r3live_files
    "src/camera/loam/*.cpp"
    "src/camera/optical_flow/*.cpp"
    "src/camera/rgb_map/*.cpp"
    "src/camera/*.cpp"
)
add_library(r3live_lib SHARED ${r3live_files})
target_link_libraries(r3live_lib ${LIBS})

file(GLOB imu_files
    src/imu/imu_state_estimator.cpp
    src/imu/imu_initializer.cpp)

add_library(imu_lib SHARED ${imu_files})
target_link_libraries(imu_lib ${LIBS})


file(GLOB odom_files
   src/odom/trajectory_manager.cpp
   src/odom/trajectory_estimator.cpp
   src/odom/odometry_manager.cpp
   src/odom/factor/analytic_diff/marginalization_factor.cpp
)

add_library(odom_libs SHARED ${odom_files})
target_link_libraries(odom_libs ${LIBS})


# add_executable(odometry_node 
#    src/odometry_node.cpp
#    src/imu/imu_state_estimator.cpp
#    src/imu/imu_initializer.cpp
#    src/odom/msg_manager.cpp
#    src/odom/trajectory_manager.cpp
#    src/odom/trajectory_estimator.cpp
#    src/odom/odometry_manager.cpp
#    src/odom/factor/analytic_diff/marginalization_factor.cpp
#    src/utils/parameter_struct.cpp
# )

# target_link_libraries(odometry_node 
#    spline_lib 
#    lidar_lib 
#    r3live_lib
#    ${LIBS}
# )