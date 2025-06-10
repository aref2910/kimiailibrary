import numpy as np
from kimiai.processing import compute_energy, compute_power

def test_compute_energy_power():
    fs = 10
    signal = np.array([1, -1, 2, -2, 3, -3], dtype=np.float32) / 3
    t_start = 0
    t_end = 0.5

    energy = compute_energy(signal, fs, t_start, t_end)
    power = compute_power(signal, fs, t_start, t_end)

    expected_energy = sum([abs(x)**2 for x in signal[:6]])
    assert abs(energy - expected_energy) < 1e-6

    expected_power = expected_energy / 6
    assert abs(power - expected_power) < 1e-6

    print("تست انرژی و توان موفقیت‌آمیز بود!")

if __name__ == "__main__":
    test_compute_energy_power()
