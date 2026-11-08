"""Practical task (chapter 18): replace the two tones by a single 1,000 Hz tone lasting one second.
What strongest frequency does frame 0 show, in Hz?"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
from part3_checker import check

t = np.arange(8000) / 8000
frame = np.sin(2 * np.pi * 1000 * t)[:400] * np.hanning(400)
check(float(np.fft.rfftfreq(400, 1 / 8000)[np.abs(np.fft.rfft(frame)).argmax()]), 0, "§ 18.3", " Hz")
