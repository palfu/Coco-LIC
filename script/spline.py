import numpy as np

# 三次 B 样条基本矩阵
M = (1/6) * np.array([
    [-1, 3, -3, 1],
    [3, -6, 3, 0],
    [-3, 0, 3, 0],
    [1, 4, 1, 0]
])

# catmul
def compute_basis_matrix(t):
    return np.array([
        [-t, 2-t, t-2, t],
        [2*t, t-3, 3-2*t, -t],
        [-t, 0, t, 0],
        [0, 1, 0, 0]
    ])


N = compute_basis_matrix(0.8)

# 计算曲线点
def compute_curve_point(t, control_points):
    U = np.array([t**3, t**2, t, 1])
    # return np.dot(U, np.dot(M, control_points))
    return np.dot(U, np.dot(N, control_points))

# 计算一阶导数
def compute_first_derivative(t, control_points):
    U_prime = np.array([3*t**2, 2*t, 1, 0])
    return np.dot(U_prime, np.dot(N, control_points))

# 计算二阶导数
def compute_second_derivative(t, control_points):
    U_double_prime = np.array([6*t, 2, 0, 0])
    return np.dot(U_double_prime, np.dot(N, control_points))

# 示例控制点
control_points_1 = np.array([
    [0, 0],
    [1, 2],
    [2, 2],
    [3, 0]
])

control_points_2 = np.array([
    [3, 0],
    [4, -2],
    [5, -2],
    [6, 0]
])

# 检查 C0 连续性
end_point_1 = compute_curve_point(1, control_points_1)
start_point_2 = compute_curve_point(0, control_points_2)
print("C0 continuity:", np.allclose(end_point_1, start_point_2))
print("{}, {}\n".format(end_point_1, start_point_2))

# 检查 C1 连续性
end_derivative_1 = compute_first_derivative(1, control_points_1)
start_derivative_2 = compute_first_derivative(0, control_points_2)
print("C1 continuity:", np.allclose(end_derivative_1, start_derivative_2))
print("{}, {}\n".format(end_derivative_1, start_derivative_2))

# 检查 C2 连续性
end_second_derivative_1 = compute_second_derivative(1, control_points_1)
start_second_derivative_2 = compute_second_derivative(0, control_points_2)
print("C2 continuity:", np.allclose(end_second_derivative_1, start_second_derivative_2))
print("{}, {}\n".format(end_second_derivative_1, start_second_derivative_2))