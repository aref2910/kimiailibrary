import numpy as np
from scipy.io import wavfile
from PIL import Image, ImageDraw
from typing import Optional, Tuple

class SignalAnalyzer:
    """
    ابزار تحلیل و رسم سیگنال صوتی WAV بدون استفاده از matplotlib
    امکانات:
    - انتخاب کانال
    - انتخاب بازه زمانی
    - رسم سیگنال و طیف فرکانسی
    - ذخیره با فرمت دلخواه
    """

    def __init__(self, file_path: str):
        self.fs, self.signal = wavfile.read(file_path)
        self.file_path = file_path
        if self.signal.ndim > 1:
            self.channels = self.signal.shape[1]
        else:
            self.channels = 1
        self.signal = self.signal.astype(np.float32)
        self.signal /= np.max(np.abs(self.signal))

    def draw_signal(self, 
                    output_path: str = "signal.png", 
                    width: int = 1000, 
                    height: int = 400, 
                    channel: int = 0, 
                    time_range: Optional[Tuple[float, float]] = None):
        if self.channels > 1:
            sig = self.signal[:, channel]
        else:
            sig = self.signal

        t = np.arange(len(sig)) / self.fs
        if time_range:
            start, end = time_range
            idx = (t >= start) & (t <= end)
            t = t[idx]
            sig = sig[idx]

        if len(sig) < 2:
            print("⛔ سیگنال خیلی کوتاه است.")
            return

        samples = len(sig)
        step = max(1, samples // width)

        img = Image.new("RGB", (width, height), "black")
        draw = ImageDraw.Draw(img)
        mid_y = height // 2
        scale_y = (height // 2) * 0.9

        # رسم نمودار سیگنال
        prev_x = 0
        prev_y = mid_y - int(sig[0] * scale_y)
        for x in range(1, width):
            idx = x * step
            if idx >= samples:
                break
            y = mid_y - int(sig[idx] * scale_y)
            draw.line((prev_x, prev_y, x, y), fill="lime")
            prev_x, prev_y = x, y

        # رسم گرید و برچسب ثانیه
        duration = t[-1] if len(t) > 0 else len(sig) / self.fs
        for sec in range(int(duration) + 1):
            x = int(sec / duration * width) if duration > 0 else 0
            draw.line((x, 0, x, height), fill=(60, 60, 60))
            draw.text((x + 2, height - 18), str(sec), fill="white")

        img.save(output_path)
        print(f"✅ تصویر سیگنال در «{output_path}» ذخیره شد.")

    def draw_spectrum(self, 
                      output_path: str = "spectrum.png", 
                      width: int = 1000, 
                      height: int = 400, 
                      channel: int = 0, 
                      time_range: Optional[Tuple[float, float]] = None):
        if self.channels > 1:
            sig = self.signal[:, channel]
        else:
            sig = self.signal

        t = np.arange(len(sig)) / self.fs
        if time_range:
            start, end = time_range
            idx = (t >= start) & (t <= end)
            sig = sig[idx]

        N = len(sig)
        if N < 2:
            print("⛔ سیگنال خیلی کوتاه است.")
            return

        freqs = np.fft.rfftfreq(N, d=1/self.fs)
        spectrum = np.abs(np.fft.rfft(sig))
        spectrum /= np.max(spectrum) if np.max(spectrum) > 0 else 1

        img = Image.new("RGB", (width, height), "black")
        draw = ImageDraw.Draw(img)
        max_freq = self.fs // 2

        for x in range(width):
            freq = x / width * max_freq
            idx = np.searchsorted(freqs, freq)
            if idx >= len(spectrum):
                break
            y_val = spectrum[idx]
            y = int((1 - y_val) * (height - 40)) + 20
            draw.line((x, height - 20, x, y), fill="orange")

        # رسم محور فرکانس و گرید
        for f in range(0, max_freq + 1, 1000):
            x = int(f / max_freq * width)
            draw.line((x, 0, x, height), fill=(60, 60, 60))
            draw.text((x + 2, height - 18), f"{f // 1000}k", fill="white")

        img.save(output_path)
        print(f"✅ تصویر طیف در «{output_path}» ذخیره شد.")


