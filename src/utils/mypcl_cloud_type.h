/*
 * Coco-LIC: Coco-LIC: Continuous-Time Tightly-Coupled LiDAR-Inertial-Camera
 * Odometry using Non-Uniform B-spline Copyright (C) 2023 Xiaolei Lang
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

#pragma once

#include <cmath>
#include <pcl/filters/voxel_grid.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl/type_traits.h>

#ifndef MACRO_POINTXYZTR
#define MACRO_POINTXYZTR
struct PointXYZTR  //定义点类型结构
{
    PCL_ADD_POINT4D;  // 该点类型有4个元素
    PCL_ADD_INTENSITY;
    double timestamp;
    int ring;
    EIGEN_MAKE_ALIGNED_OPERATOR_NEW  // 确保new操作符对齐操作
} EIGEN_ALIGN16;                     // 强制SSE对齐

// 注册点类型宏
POINT_CLOUD_REGISTER_POINT_STRUCT(PointXYZTR,                     //
                                  (float, x, x)                   //
                                  (float, y, y)                   //
                                  (float, z, z)                   //
                                  (float, intensity, intensity)   //
                                  (double, timestamp, timestamp)  //
                                  (int, ring, ring))
#endif

typedef PointXYZTR PointT;
typedef pcl::PointCloud<PointT> PointCloud;
using PointCloudPtr = PointCloud::Ptr;

using PosPoint     = PointT;
using VPoint       = PointT;
using RTPoint      = PointT;
using RTPointCloud = PointCloud;
using PosCloud     = PointCloud;
using VPointCloud  = PointCloud;

struct PointCloudMsg {
    using Ptr = std::shared_ptr<PointCloudMsg>;
    PointCloud::Ptr cloud_;
    double timestamp_;
};
using PointCloudMsgPtr = PointCloudMsg::Ptr;
