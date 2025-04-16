import numpy as np
from scipy.optimize import minimize

# 定义三次多项式
def cubic_polynomial(t, a):
    return a[0] * t**3 + a[1] * t**2 + a[2] * t + a[3]

# 定义三次多项式的一阶导数
def cubic_derivative(t, a):
    return 3 * a[0] * t**2 + 2 * a[1] * t + a[2]

# 定义三次多项式的二阶导数
def cubic_second_derivative(t, a):
    return 6 * a[0] * t + 2 * a[1]

# 目标函数：最小化曲线与数据点的误差平方和
def objective(params, data_points):
    a1, a2 = params[:4], params[4:]
    error = 0
    for t, y in data_points:
        if t < 1:
            error += (cubic_polynomial(t, a1) - y)**2
        else:
            error += (cubic_polynomial(t - 1, a2) - y)**2
    return error

# 约束条件：C2 连续
def c2_continuity_constraints(params):
    a1, a2 = params[:4], params[4:]
    # 位置连续
    pos_continuity = cubic_polynomial(1, a1) - cubic_polynomial(0, a2)
    # 一阶导数连续
    first_derivative_continuity = cubic_derivative(1, a1) - cubic_derivative(0, a2)
    # 二阶导数连续
    second_derivative_continuity = cubic_second_derivative(1, a1) - cubic_second_derivative(0, a2)
    return [pos_continuity, first_derivative_continuity, second_derivative_continuity]

# 示例数据点
data_points = [(0, 0), (0.5, 1), (1, 2), (1.5, 3), (2, 7)]

# 初始参数猜测
initial_guess = np.random.rand(8)

# 定义约束条件
constraints = ({'type': 'eq', 'fun': lambda params: c2_continuity_constraints(params)})

# 求解优化问题
result = minimize(objective, initial_guess, args=(data_points,), constraints=constraints)

# 输出结果
print("Optimized parameters:", result.x)