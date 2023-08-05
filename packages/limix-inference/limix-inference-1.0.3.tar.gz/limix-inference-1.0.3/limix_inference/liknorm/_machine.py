from ._ffi import lib, ffi

from numpy import ascontiguousarray
from numpy import ndarray

def ptr(a):
    return ffi.cast("double *", a.ctypes.data)

class LikNormMachine(object):
    def __init__(self, npoints=500):
        self._machine = lib.create_machine(npoints)

    def finish(self):
        lib.destroy_machine(self._machine)

    def moments(self, likname, y, eta, tau, log_zeroth, mean, variance):
        lik = getattr(lib, likname.upper())

        tau = ascontiguousarray(tau, float)
        eta = ascontiguousarray(eta, float)
        log_zeroth = ascontiguousarray(log_zeroth, float)
        mean = ascontiguousarray(mean, float)
        variance = ascontiguousarray(variance, float)

        size = len(log_zeroth)

        tau = ptr(tau)
        eta = ptr(eta)
        log_zeroth = ptr(log_zeroth)
        mean = ptr(mean)
        variance = ptr(variance)

        y = [ptr(yi) for yi in y]

        if likname.lower() == 'binomial':
            lib.apply2d(self._machine, lik, y[0], y[1], tau, eta, size,
                        log_zeroth, mean, variance)
        else:
            lib.apply1d(self._machine, lik, y[0], tau, eta, size, log_zeroth,
                        mean, variance)
