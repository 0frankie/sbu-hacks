import math
import numpy as np
import matplotlib.pyplot as plt

"""
    Gets the optimal angle in radians
"""


def calc_optimal_angle(p_x: int, p_y: int, h_x: int, h_y: int) -> float:
    return math.pi / 4 + math.atan(abs((p_y - h_y)) / abs((p_x - h_x)))


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
