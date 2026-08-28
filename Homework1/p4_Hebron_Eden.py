"""
Plot an arbitrary function of x entered by the interactive user.

The function expression is given as a string (using the symbol x and,
optionally, the functions from the math module), it is sampled over a
domain interval, tabulated with the format string method, and finally
charted with matplotlib.pyplot.
"""
import math
import matplotlib.pyplot as plt


def plot_function(fun_str, domain, ns):
    xmin, xmax = domain

    # ns sample points evenly dividing the [xmin, xmax] interval
    xs = []
    step = (xmax - xmin) / (ns - 1)
    for i in range(ns):
        xs.append(xmin + i * step)

    # apply the function definition in fun_str for each x in xs
    ys = []
    for x in xs:
        y = eval(fun_str)
        ys.append(y)

    # display a nice table with the xs and ys values
    print()
    print("{:>10}{:>12}".format("x", "y"))
    print("{:>10}{:>12}".format("-" * 8, "-" * 10))
    for x, y in zip(xs, ys):
        print("{:10.4f}{:+12.4f}".format(x, y))

    # display the chart of the function
    plt.figure()
    plt.plot(xs, ys, marker="o")
    plt.axhline(0, color="black", linewidth=0.8)
    plt.axvline(0, color="black", linewidth=0.8)
    plt.title(f"y = {fun_str}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.show()


fun_str = input("Enter function with variable x: ")
ns = int(input("Enter number of samples: "))
xmin = float(input("Enter xmin: "))
xmax = float(input("Enter xmax: "))

plot_function(fun_str, (xmin, xmax), ns)
