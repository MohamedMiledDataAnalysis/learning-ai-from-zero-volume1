"""Chapter 18 — from sound to a picture of frequencies (a spectrogram).

We make a synthetic sound in numpy (no microphone, no file): 0.5 seconds of a
440 Hz tone, then 0.5 seconds of a 660 Hz tone. A speech model never listens to
the raw wave: it first cuts the sound into short frames and measures how much of
each frequency is present in each frame.
"""

import numpy as np

RATE = 8000                       # samples per second
t = np.arange(RATE) / RATE        # one second of time stamps
wave = np.where(t < 0.5, np.sin(2 * np.pi * 440 * t), np.sin(2 * np.pi * 660 * t))
print(f"Samples: {len(wave)} ({RATE} per second)")
print("First 8 samples:", " ".join(f"{v:+.3f}" for v in wave[:8]))

FRAME = 400                       # 400 samples = 50 milliseconds per frame
window = np.hanning(FRAME)        # soften the frame edges
freqs = np.fft.rfftfreq(FRAME, d=1 / RATE)
print(f"\nFrame length: {FRAME} samples = {FRAME / RATE * 1000:.0f} ms | frequency step: {freqs[1]:.0f} Hz")
print("frame | starts at | strongest frequency")
for i in range(0, len(wave) // FRAME):
    if i not in (0, 4, 9, 10, 15, 19):
        continue
    frame = wave[i * FRAME:(i + 1) * FRAME] * window
    spectrum = np.abs(np.fft.rfft(frame))           # how much of each frequency is in the frame
    print(f"{i:>5} | {i * FRAME / RATE:>6.2f} s  | {freqs[spectrum.argmax()]:.0f} Hz")


def dft_by_hand(x):
    """The discrete Fourier transform written out: compare the signal with each frequency."""
    n = len(x)
    return [abs(sum(x[j] * np.exp(-2j * np.pi * k * j / n) for j in range(n))) for k in range(n // 2 + 1)]


small = np.array([0, 1, 0, -1, 0, 1, 0, -1], dtype=float)    # 2 cycles in 8 samples
print("\nBy hand: signal", small.astype(int).tolist())
print("Strength at 0, 1, 2, 3, 4 cycles per 8 samples:", [round(float(v), 2) for v in dft_by_hand(small)])
