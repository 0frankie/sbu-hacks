import math

import matplotlib.pyplot as plt
import numpy as np

"""
    Gets the optimal angle in radians
"""


# optimal angle calculation derived here: https://livingstones.thetreeoflife.us/ShootingAngle.pdf
def calc_optimal_angle(p_x: int, p_y: int, h_x: int, h_y: int) -> float:
    return math.pi / 4 + math.atan2(abs(p_y - h_y), abs((h_x - p_x)))


def calc_optimal_velocity(
    p_x: int, p_y: int, h_x: int, h_y: int, px_per_meter: float
) -> tuple[float, float]:
    g = 9.81 * px_per_meter  # m/s^2
    optimal_angle = calc_optimal_angle(p_x, p_y, h_x, h_y)

    # derived from kinematics with known optimal angle & no air resistance
    # v = sqrt(x^2g/(2cos^2\theta(y-xtan\theta)))
    numerator = -((h_x - p_x) ** 2) * g
    denominator = (
        2
        * (math.cos(optimal_angle) ** 2)
        * (abs(p_y - h_y) - math.tan(optimal_angle) * abs(h_x - p_x))
    )

    v = math.sqrt(numerator / denominator)
    return (
        np.sign(h_x - p_x) * v * math.cos(optimal_angle),
        -v * math.sin(optimal_angle),
    )


def calc_actual_angle(points: list[tuple[int, int]]) -> float:
    x0, y0 = points[0]
    x1, y1 = points[1]

    return math.atan2(y1 - y0, x1 - x0)


def calc_actual_velocity(
    points: list[tuple[int, int]], dt: float, px_per_meter: float
) -> tuple[float, float]:
    g = 9.81 * px_per_meter  # m/s^2
    num_points = math.floor(len(points) * 0.9)
    vx = 0
    vy = 0
    time = dt
    for i in range(num_points):
        y0 = points[0][1]
        y1 = points[i + 1][1]
        vy += (y1 - y0 - 0.5 * g * time * time) / time
        time += dt
    for i in range(math.floor(len(points) * 0.1), num_points):
        xi = points[i][0]
        x1 = points[i + 1][0]
        vx += (x1 - xi) / dt
    vx /= num_points
    vy /= num_points

    all_x = []
    all_y = []
    for i in range(0, len(points), 3):
        all_x.append(points[i][0])
        all_y.append(points[i][1])
    # area_under_curve(all_x, all_y)
    return (vx, vy)


def calc_diff(a, b) -> float:
    return abs(a - b) / ((a + b) / 2.0)


"""
    Given the shot distance, find the area under the curve
"""


def angle_diff(p_x: int, p_y: int, h_x: int, h_y: int, angle: float) -> float:
    return calc_diff(calc_optimal_angle(p_x, p_y, h_x, h_y), angle)


def speed_diff(
    p_x: int, p_y: int, h_x: int, h_y: int, velocity: tuple[float, float]
) -> float:
    return calc_diff(calc_optimal_velocity(p_x, p_y, h_x, h_y), velocity)


def check_is_in_basket(
    points: list[tuple[int, int]], h_center: tuple[float, float]
) -> bool:
    for pt in points:
        if (
            math.sqrt(pt[0] ** 2 + h_center[0] ** 2) < 100
            and math.sqrt(pt[1] ** 2 + h_center[1] ** 2) < 100
        ):
            return True
    return False


def check_is_overshot(
    points: list[tuple[int, int]], h_bbox: tuple[float, float, float, float]
) -> bool:
    for pt in points:
        if math.sqrt(pt[0] ** 2 + (h_bbox[0] + h_bbox[2] // 2) ** 2) < 100:
            if np.sign(pt[1] - (h_bbox[1] + h_bbox[3] // 2)) > 0:
                return True
            else:
                return False
    return False


# this currently draws a close approximation, but not the exact curve
def area_under_curve(all_x: list[int], all_y: list[int]) -> float:
    # for x in all_x:

    xs = np.eye(len(all_x), dtype=np.dtype(float))

    for i, x in enumerate(all_x):
        for j in reversed(range(len(all_x))):
            xs[i][len(all_x) - 1 - j] = x**j
        # print(xs.shape)
    ys = np.array([all_y], dtype=np.dtype(float))
    ys = np.transpose(ys)

    # print(ys.shape)
    solutions = np.linalg.solve(xs, ys)

    # print(solutions.shape)

    x_axis = np.linspace(0, 400, 100)
    y_axis = 0
    for i in reversed(range(len(solutions))):
        print(solutions[len(solutions) - 1 - i][0])
        y_axis += solutions[len(solutions) - 1 - i][0] * x_axis**i
        # print(y_axis)
    test_plot()
    plt.fill_between(x_axis, y_axis)
    plt.plot(x_axis, y_axis)
    plt.show()

    return 1.1


def area_under_ideal_curve(v: float, p_x: int, p_y: int, h_x: int, h_y: int) -> float:
    # the angle must be that the equation allows the ball to
    # reach (h_y - p_y) after d (h_x - p_x)
    return 1.1


def plot(a: float, b: float, c: float) -> None:
    xs = np.linspace(-10, 10, 10)
    ys = a * xs**2 + b * xs + c

    plt.fill_between(xs, ys)

    plt.plot(xs, ys)
    plt.show()


def test_plot():
    xs = np.linspace(0, 10, 10)
    ys = 2 * xs**2 + 2 * xs + 10

    plt.plot(xs, ys)
    plt.show()


def main():
    area_under_curve(-3, 2, 5, 16, 13, 2)
    test_plot()


if __name__ == "__main__":
    main()
