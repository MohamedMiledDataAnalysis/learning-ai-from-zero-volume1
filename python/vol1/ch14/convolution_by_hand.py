"""Chapter 14 — one convolution, computed step by step.

The image is 5x5 pixels: 0 is white, 9 is black. It shows a vertical bar.
The filter (kernel) is 3x3 and responds to 'dark on the right, light on the left'.
"""

import numpy as np

image = np.array([
    [0, 0, 9, 9, 0],
    [0, 0, 9, 9, 0],
    [0, 0, 9, 9, 0],
    [0, 0, 9, 9, 0],
    [0, 0, 9, 9, 0],
])
kernel = np.array([
    [-1, 0, 1],
    [-1, 0, 1],
    [-1, 0, 1],
])


def convolve(img, k):
    """Slide the kernel over every 3x3 window; multiply cell by cell and add up."""
    rows, cols = img.shape[0] - 2, img.shape[1] - 2
    out = np.zeros((rows, cols), dtype=int)
    for r in range(rows):
        for c in range(cols):
            window = img[r:r + 3, c:c + 3]
            out[r, c] = int((window * k).sum())
    return out


if __name__ == "__main__":
    print("Top-left window (rows 1-3, columns 1-3):")
    print(image[0:3, 0:3])
    print("Window x kernel, cell by cell:")
    print(image[0:3, 0:3] * kernel)
    print("Sum =", int((image[0:3, 0:3] * kernel).sum()))
    print()
    print("Feature map (3x3):")
    print(convolve(image, kernel))
