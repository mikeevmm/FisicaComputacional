#!/usr/bin/env python


def heun(h: float, Dt: float, initial_conditions: tuple, diff_eqs: tuple, return_final_only: bool = True):
    """Integrates a system of equations using the Heun method.

    Arguments:
        `h` - step of integration
        `Dt` - integration length ("integrate for")
        `initial_conditions` - tuple of initial conditions
        `diff_eqs` - tuple of functions `f_i(t, x0, x1, x2, ...) = dx_i/dt`
        `return_final_only` - whether to only return (x0(t0 + Dt), ...) or
            ((x0(t0), ...), (x0(t0 + h), ...), (x0(t0 + 2h), ...), ..., (x0(t0 + Dt), ...))

    Returns:
        Tuple (x0, x1, ...) at time t0 + dt

    Remarks:
        `initial_conditions` tuple should be `t0` + same variable order
        as `diff_eqs` (where `t` is the independent variable), i.e., if
            `diff_eqs = (f_0, f_1, ...)`
        then
            `initial_conditions = (t0, x0(t0), x1(t0), ...)`
    """

    total_steps = int(Dt/h)

    t0 = initial_conditions[0]
    points = list(initial_conditions[1:])
    first_order = points

    total_points = None
    if not return_final_only:
        total_points = [[0 for _ in range(len(diff_eqs))]
                        for _ in range(total_steps)]

    for step in range(total_steps):
        for var in range(len(points)):
            first_order[var] = points[var] + h * \
                diff_eqs[var](t0 + step*h, *points)
        for var in range(len(points)):
            points[var] += h/2*(diff_eqs[var](t0 + step*h, *points) +
                                diff_eqs[var](t0 + (step+1)*h, *first_order))
        for var in range(len(points)):
            total_points[step][var] = points[var]

    if return_final_only:
        return points
    return (initial_conditions[1:],) + tuple(total_points)


if __name__ == '__main__':

    import matplotlib.pyplot as plt
    from Folha11Ex1 import euler

    def diff_eqs_for_params(b, c, m):
        return (
            lambda t, y, z: -(b*y + c*z)/m,
            lambda t, y, z: y
        )

    hs = input('h: ')
    hs = tuple(map(lambda x: float(x), hs.split()))
    m, c = 50.0, 2E4
    for b in (5000, 2500, 1000, 500, 100, 50):
        plt.title('b: {}  c: {}  m:{}'.format(b, c, m))
        for h in hs:
            x_values = tuple(h*i for i in range(int(1/h)+1))
            y_values = tuple(map(lambda x: x[1], heun(
                h, 1, (0, 3, 0.001), diff_eqs_for_params(b, c, m), False)))
            y_euler = tuple(map(lambda x: x[1], euler(
                h, 1, (0, 3, 0.001), diff_eqs_for_params(b, c, m), False)))

            plt.plot(x_values, y_values, label='h = %f' % h)
            plt.plot(x_values, y_euler, label='Euler (h = %f)' % h)
        plt.legend(loc='best')
        plt.show()

    print("""
    There's a big difference between the results yielded by Euler's
    and Heun's integration methods. It's expected that the latter results
    are more trustworthy, and therefore it's relevant to employ it.
    """)

    input('ENTER TO QUIT')