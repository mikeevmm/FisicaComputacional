#!/usr/bin/env python


def euler(h: float, Dt: float, initial_conditions: tuple, diff_eqs: tuple, return_final_only: bool = True):
    """Integrates a system of equations using the Euler method.

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
    import threading
    from threading import Barrier, Thread

    # Validity checks
    if len(initial_conditions) != len(diff_eqs) + 1:
        raise ValueError(
            "Length of `initial_conditions` must be length of `diff_eqs` + 1.")

    diff_eq_count = len(diff_eqs)

    iteration_done = Barrier(diff_eq_count)
    value_updates = Barrier(diff_eq_count)
    all_done = Barrier(diff_eq_count + 1)

    integrated_values = list(initial_conditions[1:])
    start_t = initial_conditions[0]
    total_steps = abs(round(Dt/h))

    steps = []
    if not return_final_only:
        for _ in range(total_steps):
            steps.append([0 for _ in range(diff_eq_count)])

    def thread_integration(var_index):
        local = threading.local()  # Thread local data
        local.t = start_t
        local.x = integrated_values[var_index]
        diff_eq = diff_eqs[var_index]
        local.step = 0
        while local.step < total_steps:
            local.x += h * diff_eq(local.t, *integrated_values)

            i = iteration_done.wait()
            if i == 0:
                iteration_done.reset()

            integrated_values[var_index] = local.x
            if not return_final_only:
                steps[local.step][var_index] = local.x

            i = value_updates.wait()
            if i == 0:
                value_updates.reset()
                steps[local.step] = tuple(steps[local.step])

            local.t += h
            local.step += 1

    class DoThread (Thread):
        def __init__(self, var_index):
            Thread.__init__(self)
            self.var_index = var_index

        def run(self):
            thread_integration(self.var_index)
            all_done.wait()

    for var_index in range(diff_eq_count):
        thread = DoThread(var_index)
        thread.start()
    all_done.wait()

    if return_final_only:
        return tuple(integrated_values)
    else:
        return (initial_conditions[1:],) + tuple(steps)


if __name__ == '__main__':

    from threading import Barrier, Thread
    import matplotlib.pyplot as plt

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
            y_values = tuple(map(lambda x: x[1], euler(
                h, 1, (0, 3, 0.001), diff_eqs_for_params(b, c, m), False)))

            plt.plot(x_values, y_values, label='h = %f' % h)
        plt.legend(loc='best')
        plt.show()

    print("""
    There's significant difference between integrations
    of different step size; it's expected that Heun might
    yield more consistent results by mitigating the
    effect of rapidly varying slope (which occurs especially
    for non-dampening solutions).
    """)

    input('ENTER TO QUIT')