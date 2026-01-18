import argparse
import numpy as np
import matplotlib.pyplot as plt


def default_expression():
    return "x**2 - 2*x + 1"


def parse_args():
    p = argparse.ArgumentParser(description="Plot an equation in x. Use numpy as np in expressions.")
    p.add_argument("--expr", "-e", help="Python expression for y in terms of x (use np for numpy). Example: 'np.sin(x)/x'", default=None)
    p.add_argument("--xmin", type=float, default=-10, help="Minimum x value")
    p.add_argument("--xmax", type=float, default=10, help="Maximum x value")
    p.add_argument("--points", type=int, default=500, help="Number of points")
    return p.parse_args()


def get_expression(args):
    expr = args.expr
    if expr:
        return expr

    try:
        inp = input(f"Enter expression for y in terms of x (press Enter for default {default_expression()}): ")
    except EOFError:
        inp = ""

    if not inp.strip():
        return default_expression()
    return inp


def evaluate_expression(expr, x):
    # Evaluate expression with access to NumPy as np and x as the NumPy array.
    # Limit builtins to reduce risk. This is not perfectly secure but reasonable
    # for local interactive use.
    try:
        y = eval(expr, {"np": np, "__builtins__": None}, {"x": x})
    except Exception as e:
        raise RuntimeError(f"Failed to evaluate expression '{expr}': {e}")
    return y


def main():
    args = parse_args()

    x = np.linspace(args.xmin, args.xmax, args.points)

    expr = get_expression(args)
    y = evaluate_expression(expr, x)

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, linewidth=2)
    plt.grid(True, alpha=0.3)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f'Graph of y = {expr}')
    plt.axhline(y=0, color='k', linewidth=0.5)
    plt.axvline(x=0, color='k', linewidth=0.5)
    plt.show()


if __name__ == '__main__':
    main()