import math
import numpy as np
import matplotlib.pyplot as plt

"""
    Gets the optimal angle in radians
"""


def calc_optimal_angle(p_x: int, p_y: int, h_x: int, h_y: int) -> float:
    return math.pi / 4 + math.atan((h_y - p_y) / abs((h_x - p_x)))


def calc_optimal_velocity(
    p_x: int, p_y: int, h_x: int, h_y: int
) -> tuple[float, float]:
    g = 9.81  # m/s^2
    optimal_angle = calc_optimal_angle(p_x, p_y, h_x, h_y)

    # derived from kinematics with known optimal angle & no air resistance
    # v = sqrt(x^2g/(2cos^2\theta(y-xtan\theta)))
    numerator = -((h_x - p_x) ** 2) * g
    denominator = (
        2
        * (math.cos(optimal_angle) ** 2)
        * ((h_y - p_y) - math.tan(optimal_angle) * abs(h_x - p_x))
    )

    v = math.sqrt(numerator / denominator)
    return (
        np.sign(h_x - p_x) * v * math.cos(optimal_angle),
        v * math.sin(optimal_angle),
    )


def calc_actual_angle(points: list[tuple[int, int]]) -> float:
    x0, y0 = points[0]
    x1, y1 = points[1]

    return math.atan2(y1 - y0, x1 - x0)


def calc_actual_velocity(
    points: list[tuple[int, int]], time: float
) -> tuple[float, float]:
    x0, y0 = points[0]
    x1, y1 = points[1]

    return ((x1 - x0) / time, (y1 - y0) / time)


"""
    Given the shot distance, find the area under the curve
"""


# this currently draws a close approximation, but not the exact curve
def area_under_curve(
    p_x: int, p_y: int, h_x: int, h_y: int, m_x: int, m_y: int
) -> float:
    x = np.array(
        [[p_x**2, p_x, 1], [h_x**2, h_x, 1], [m_x**2, m_x, 1]], dtype=np.dtype(float)
    )

    y = np.array([p_y, h_y, m_y], dtype=np.dtype(float))

    a, b, c = np.linalg.solve(x, y)

    print(f"{a} + {b} + {c}")

    plot(a, b, c)
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
