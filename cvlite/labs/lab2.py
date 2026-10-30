TITLE = "Histogram equalization"
INPUT = "image"
DEFAULT_PATH = "/content/image.jpg"

AIM = "Improve the contrast of an image using global histogram equalization and CLAHE, compare their histograms and CDFs, and equalize a colour image without changing its colours."

STEPS = [
    "Read the image and convert it to grayscale.",
    "Apply global histogram equalization with cv2.equalizeHist.",
    "Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) with cv2.createCLAHE and .apply.",
    "Show the original, equalized and CLAHE images side by side.",
    "Plot the original, equalized and CLAHE histograms. On each one, draw the CDF (cv2.calcHist then cumsum, scaled to the histogram's height) in red. The equalized histogram is spread over 0-255 and its CDF is almost a straight line.",
    "For a colour result: convert to YCrCb, equalize only the Y (brightness) channel, merge the channels back and convert to BGR. Plot the Y-channel histogram before and after equalization.",
    "Print the standard deviation (a simple measure of contrast) before and after.",
]

THEORY = [
    "Histogram: a count of how many pixels have each intensity value (0-255).",
    "Low-contrast images have a narrow histogram. Equalization spreads it out over the full 0-255 range.",
    "Global equalization maps each intensity through the normalised CDF: new = round((L - 1) * CDF(old)), with L = 256. After equalization the CDF is close to a straight line.",
    "CLAHE splits the image into tiles (tileGridSize), equalizes each tile separately, and clips the histogram at clipLimit so noise is not over-amplified. Tiles are blended with bilinear interpolation.",
    "Equalizing R, G and B separately changes the colours, so for colour images only the brightness channel (Y in YCrCb, or V in HSV) is equalized.",
]

CODE = r'''import cv2
import numpy as np
import matplotlib.pyplot as plt

image_path = __PATH__

img = cv2.imread(image_path)
if img is None:
    raise FileNotFoundError("Could not read the image at " + image_path)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

equalized = cv2.equalizeHist(gray)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
clahe_img = clahe.apply(gray)

results = [(gray, "Original"), (equalized, "Equalized"), (clahe_img, "CLAHE")]

plt.figure(figsize=(16, 5))
for i, (image, name) in enumerate(results):
    plt.subplot(1, 3, i + 1)
    plt.imshow(image, cmap="gray", vmin=0, vmax=255)
    plt.title(name + " image")
    plt.axis("off")
plt.tight_layout()
plt.show()

plt.figure(figsize=(18, 5))
for i, (image, name) in enumerate(results):
    hist = cv2.calcHist([image], [0], None, [256], [0, 256]).ravel()
    cdf = hist.cumsum()
    plt.subplot(1, 3, i + 1)
    plt.hist(image.ravel(), bins=256, range=(0, 256), color="gray", label="Histogram")
    plt.plot(cdf * hist.max() / cdf[-1], color="red", label="CDF (scaled)")
    plt.xlim(0, 256)
    plt.title(name + " histogram")
    plt.xlabel("Pixel intensity")
    plt.ylabel("Number of pixels")
    plt.legend()
plt.tight_layout()
plt.show()

ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
y, cr, cb = cv2.split(ycrcb)
y_equalized = cv2.equalizeHist(y)
colour_equalized = cv2.cvtColor(cv2.merge([y_equalized, cr, cb]), cv2.COLOR_YCrCb2BGR)

plt.figure(figsize=(14, 10))
plt.subplot(2, 2, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title("Original colour image")
plt.axis("off")
plt.subplot(2, 2, 2)
plt.imshow(cv2.cvtColor(colour_equalized, cv2.COLOR_BGR2RGB))
plt.title("Colour image equalized on the Y channel")
plt.axis("off")
plt.subplot(2, 2, 3)
plt.hist(y.ravel(), bins=256, range=(0, 256), color="gray")
plt.xlim(0, 256)
plt.title("Original Y-channel histogram")
plt.xlabel("Pixel intensity")
plt.ylabel("Number of pixels")
plt.subplot(2, 2, 4)
plt.hist(y_equalized.ravel(), bins=256, range=(0, 256), color="gray")
plt.xlim(0, 256)
plt.title("Equalized Y-channel histogram")
plt.xlabel("Pixel intensity")
plt.ylabel("Number of pixels")
plt.tight_layout()
plt.show()

print("Contrast (standard deviation) of original :", np.std(gray))
print("Contrast (standard deviation) of equalized:", np.std(equalized))
print("Contrast (standard deviation) of CLAHE    :", np.std(clahe_img))
'''
