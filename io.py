import os
import numpy as np
from scipy.io import wavfile

try:
    from pydub import AudioSegment
except ImportError:
    AudioSegment = None

def _convert_mp3_to_wav(mp3_path):
    if AudioSegment is None:
        raise ImportError("برای پشتیبانی از mp3 باید pydub نصب شود:\n pip install pydub")
    audio = AudioSegment.from_file(mp3_path)
    wav_path = mp3_path.rsplit('.', 1)[0] + "_converted.wav"
    audio.export(wav_path, format="wav")
    return wav_path

def load_audio(filepath):
    """
    فایل WAV یا MP3 را می‌خواند و سیگنال تک کانال نرمال شده و نرخ نمونه‌برداری را برمی‌گرداند.

    پارامتر:
        filepath (str): مسیر فایل صوتی (.wav یا .mp3)

    بازگشتی:
        fs (int): نرخ نمونه‌برداری
        signal (np.ndarray): آرایه تک‌کانال float32 نرمال شده در بازه [-1,1]
    """
    ext = filepath.rsplit('.', 1)[-1].lower()
    if ext == 'mp3':
        wav_path = _convert_mp3_to_wav(filepath)
        fs, data = wavfile.read(wav_path)
        os.remove(wav_path)
    elif ext == 'wav':
        fs, data = wavfile.read(filepath)
    else:
        raise ValueError("فرمت فایل فقط WAV و MP3 پشتیبانی می‌شود.")

    if data.dtype == np.int16:
        data = data.astype(np.float32) / 32768.0
    elif data.dtype == np.int32:
        data = data.astype(np.float32) / (2**31)
    if data.ndim == 2:
        data = data[:, 0]
    return fs, data