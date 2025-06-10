def compute_energy(signal, fs, t_start, t_end):
    """
    انرژی سیگنال را در بازه زمانی مشخص به صورت دستی حساب می‌کند.

    پارامترها:
        signal (np.ndarray): سیگنال تک کانال
        fs (int): نرخ نمونه‌برداری
        t_start (float): زمان شروع (ثانیه)
        t_end (float): زمان پایان (ثانیه)

    بازگشتی:
        energy (float): انرژی محاسبه شده
    """
    if t_start < 0:
        t_start = 0
    if t_end > len(signal) / fs:
        t_end = len(signal) / fs
    if t_end <= t_start:
        raise ValueError("t_end باید بزرگ‌تر از t_start باشد.")

    n1 = int(t_start * fs)
    n2 = int(t_end * fs)
    segment = signal[n1 : n2 + 1]

    energy = 0.0
    for sample in segment:
        val = sample if sample >= 0 else -sample
        energy += val * val
    return energy

def compute_power(signal, fs, t_start, t_end):
    """
    توان سیگنال را در بازه زمانی مشخص به صورت دستی حساب می‌کند.

    پارامترها:
        signal (np.ndarray): سیگنال تک کانال
        fs (int): نرخ نمونه‌برداری
        t_start (float): زمان شروع (ثانیه)
        t_end (float): زمان پایان (ثانیه)

    بازگشتی:
        power (float): توان محاسبه شده
    """
    energy = compute_energy(signal, fs, t_start, t_end)
    n1 = int(t_start * fs)
    n2 = int(t_end * fs)
    N = n2 - n1 + 1
    if N <= 0:
        return 0
    power = energy / N
    return power