TITLE = "Colour models and colour maps"
INPUT = "image"
DEFAULT_PATH = "/content/image.jpg"

AIM = "Convert an image into different colour models (RGB, Grayscale, HSV, LAB, YCrCb, CMY, CMYK), look at every channel separately, and apply pseudo-colour maps (JET, TURBO, BONE, HOT) to the grayscale image."

STEPS = [
    "Read the image with OpenCV. OpenCV stores colour images in BGR order, not RGB.",
    "Convert BGR to RGB, Grayscale, HSV, LAB and YCrCb with cv2.cvtColor.",
    "Compute CMY as 255 - RGB (the subtractive complement of each channel).",
    "Compute CMYK by hand: normalise RGB to 0-1, K = 1 - max(R, G, B), then C = (1 - R - K) / (1 - K), and the same for M and Y.",
    "Show all colour models side by side.",
    "Split every model into its channels with cv2.split and show each channel as a grayscale image.",
    "Apply colour maps to the grayscale image with cv2.applyColorMap (pseudo-colouring).",
    "Print the image size and the mean value of each channel.",
]

THEORY = [
    "RGB: additive model used by screens. Each pixel = Red, Green, Blue intensities (0-255).",
    "Grayscale: Y = 0.299 R + 0.587 G + 0.114 B (single intensity channel).",
    "HSV: Hue (colour type, 0-179 in OpenCV), Saturation (purity of colour), Value (brightness). Good for colour-based segmentation because colour is separated from brightness.",
    "LAB: L = lightness, A = green to red axis, B = blue to yellow axis. Designed to be perceptually uniform.",
    "YCrCb: Y = luma (brightness), Cr = red difference, Cb = blue difference. Used in JPEG/video compression and skin detection.",
    "CMY: subtractive model used by printers. C = 1 - R, M = 1 - G, Y = 1 - B.",
    "CMYK: adds a separate black (K) channel so printers use less colour ink. K = 1 - max(R, G, B).",
    "Colour maps (pseudo-colour): map each gray level to a colour so small intensity differences are easier to see. JET/TURBO go blue to red, BONE is a bluish-white map, HOT goes black-red-yellow-white.",
]

CODE = r'''import cv2
import numpy as np
import matplotlib.pyplot as plt

image_path = __PATH__

img = cv2.imread(image_path)
if img is None:
    raise FileNotFoundError("Could not read the image at " + image_path)

rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
cmy = 255 - rgb

rgb_norm = rgb.astype(np.float64) / 255.0
k = 1 - np.max(rgb_norm, axis=2)
c = (1 - rgb_norm[:, :, 0] - k) / (1 - k + 1e-8)
m = (1 - rgb_norm[:, :, 1] - k) / (1 - k + 1e-8)
y = (1 - rgb_norm[:, :, 2] - k) / (1 - k + 1e-8)

models = [(rgb, "RGB"), (gray, "Grayscale"), (hsv, "HSV"), (lab, "LAB"), (ycrcb, "YCrCb"), (cmy, "CMY")]
plt.figure(figsize=(15, 8))
for i, (image, name) in enumerate(models):
    plt.subplot(2, 3, i + 1)
    plt.imshow(image, cmap="gray")
    plt.title(name)
    plt.axis("off")
plt.tight_layout()
plt.show()

r, g, b = cv2.split(rgb)
h, s, v = cv2.split(hsv)
l_ch, a_ch, b_ch = cv2.split(lab)
y_ch, cr_ch, cb_ch = cv2.split(ycrcb)

channels = [(r, "R (Red)"), (g, "G (Green)"), (b, "B (Blue)"), (h, "H (Hue)"),
            (s, "S (Saturation)"), (v, "V (Value)"), (l_ch, "L (Lightness)"), (a_ch, "A (green-red)"),
            (b_ch, "B (blue-yellow)"), (y_ch, "Y (Luma)"), (cr_ch, "Cr (red difference)"), (cb_ch, "Cb (blue difference)"),
            (c, "C (Cyan)"), (m, "M (Magenta)"), (y, "Y (Yellow)"), (k, "K (Black)")]
plt.figure(figsize=(16, 14))
for i, (channel, name) in enumerate(channels):
    plt.subplot(4, 4, i + 1)
    plt.imshow(channel, cmap="gray")
    plt.title(name)
    plt.axis("off")
plt.tight_layout()
plt.show()

colour_maps = [(cv2.COLORMAP_JET, "JET"), (cv2.COLORMAP_TURBO, "TURBO"), (cv2.COLORMAP_BONE, "BONE"), (cv2.COLORMAP_HOT, "HOT")]
plt.figure(figsize=(16, 4))
for i, (colour_map, name) in enumerate(colour_maps):
    mapped = cv2.applyColorMap(gray, colour_map)
    plt.subplot(1, 4, i + 1)
    plt.imshow(cv2.cvtColor(mapped, cv2.COLOR_BGR2RGB))
    plt.title(name)
    plt.axis("off")
plt.tight_layout()
plt.show()

print("Image size (height, width, channels):", img.shape)
print("Mean R, G, B:", np.mean(r), np.mean(g), np.mean(b))
print("Mean H, S, V:", np.mean(h), np.mean(s), np.mean(v))
print("Mean C, M, Y, K:", np.mean(c), np.mean(m), np.mean(y), np.mean(k))
'''
