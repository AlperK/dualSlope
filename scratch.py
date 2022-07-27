import numpy as np
from Measurement import _get_slope, _linearize_amplitudes


separations = np.array(
    ([[25, 35], [35, 25]],
     [[25, 35], [35, 25]])
) / 10

amplitudes = np.array((50, 15, 15, 25, 1500, 120, 450, 600)).reshape((2, 2, 2))

phases = np.array(([10, 20], [40, 32], [90, 165], [90, 120])).reshape((2, 2, 2))

print(f'amplitudes: {amplitudes}')

linearized_amplitudes = _linearize_amplitudes(amplitudes, separations)
print(f'linearized_amplitudes: {linearized_amplitudes}')

amplitude_slopes = _get_slope(linearized_amplitudes, separations)
print(f'amplitude_slopes: {amplitude_slopes}')

phase_slopes = _get_slope(phases, separations, average=True)
print(f'phase_slopes: {phase_slopes}')

