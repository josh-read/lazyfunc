import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad
from scipy.interpolate import interp1d

from lazyfunc import LazyFunc


@LazyFunc
def bremsstrahlung_spectrum(energy, /, temperature):
    """The thermal power spectrum (black body).

    Equivalent to the bremsstrahlung power spectrum at high energies.
    """
    return np.exp(- energy / temperature)


@LazyFunc
@np.vectorize
def responsivity(energy):
    """Approximation of the manufacturer's diode responsivity table."""
    threshold = 10e3
    if energy < threshold:
        return 0.25
    else:
        return 0.25 * np.exp(-(energy - threshold)/threshold)


henke_data = np.genfromtxt('data.txt', skip_header=2)
transmission = LazyFunc(interp1d(*henke_data.T, bounds_error=False, fill_value=0.), description='transmission')

impedance = 50


measured_voltage_spectrum = bremsstrahlung_spectrum * transmission * responsivity / impedance
print(measured_voltage_spectrum(1e3, temperature=100))

measured_voltage_spectrum.kwargs = {'temperature': 100}
# measured_voltage = quad(measured_voltage_spectrum, 0, 30e3)
# print(measured_voltage)
#
# fig, ax = plt.subplots()
# x = np.linspace(0, 30e3, 1000)
# ax.plot(x, measured_voltage_spectrum(x))
# plt.show()
