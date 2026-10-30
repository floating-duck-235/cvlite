TITLE = "Region of interest (ROI) identification"
INPUT = "image"
DEFAULT_PATH = "/content/image.jpg"

AIM = "Automatically find the three largest regions of interest in an image using Otsu thresholding, morphological cleaning and contours, draw boxes around them and crop them out."

STEPS = [
    "Read the image and shrink it so the longest side is at most 800 px, so the kernel sizes behave the same on every image.",
    "Convert to grayscale and blur it to remove noise.",
    "Threshold with Otsu's method. THRESH_BINARY_INV makes the dark objects white (foreground).",
    "Clean the mask with morphological opening (removes small white specks) and closing (fills small black holes).",
    "Find the outer contours, sort them by area and keep the three largest.",
    "For each contour: get its bounding box, draw it with a label, crop the ROI and print its position and size.",
    "Show the threshold, the cleaned mask and the boxes, then show each cropped ROI.",
]

THEORY = [
    "ROI (region of interest): the part of an image that we want to analyse further.",
    "Otsu's method picks the threshold automatically by minimising the within-class variance (equivalently, maximising the between-class variance) of foreground and background.",
    "Erosion shrinks white regions, dilation grows them. Opening = erosion then dilation (removes noise). Closing = dilation then erosion (fills holes).",
    "A contour is the curve joining all continuous boundary points of a region. RETR_EXTERNAL keeps only outer contours. CHAIN_APPROX_SIMPLE stores only the corner points of straight segments.",
    "Bounding box (x, y, w, h): the smallest upright rectangle containing the contour. Cropping uses NumPy slicing img[y:y+h, x:x+w] (rows first, then columns).",
]

CODE = r'''import cv2
import numpy as np
import matplotlib.pyplot as plt

image_path = __PATH__

img = cv2.imread(image_path)
if img is None:
    raise FileNotFoundError("Could not read the image at " + image_path)

scale = 800 / max(img.shape[:2])
if scale < 1:
    img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)

_, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

kernel = np.ones((9, 9), np.uint8)
clean = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
clean = cv2.morphologyEx(clean, cv2.MORPH_CLOSE, kernel)

contours, _ = cv2.findContours(clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:3]

output = img.copy()
colours = [(0, 255, 0), (255, 0, 0), (0, 0, 255)]
rois = []
for i, contour in enumerate(contours):
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(output, (x, y), (x + w, y + h), colours[i], 3)
    cv2.putText(output, "ROI " + str(i + 1), (x + 5, y + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, colours[i], 2)
    rois.append(img[y:y + h, x:x + w])
    print("ROI", i + 1, ": x =", x, "y =", y, "width =", w, "height =", h, "area =", cv2.contourArea(contour))

plt.figure(figsize=(14, 10))
plt.subplot(2, 2, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title("Original")
plt.axis("off")
plt.subplot(2, 2, 2)
plt.imshow(thresh, cmap="gray")
plt.title("Otsu threshold")
plt.axis("off")
plt.subplot(2, 2, 3)
plt.imshow(clean, cmap="gray")
plt.title("After opening and closing")
plt.axis("off")
plt.subplot(2, 2, 4)
plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
plt.title("Detected ROIs")
plt.axis("off")
plt.tight_layout()
plt.show()

if len(rois) == 0:
    print("No regions were found")
else:
    plt.figure(figsize=(5 * len(rois), 5))
    for i, roi in enumerate(rois):
        plt.subplot(1, len(rois), i + 1)
        plt.imshow(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))
        plt.title("ROI " + str(i + 1))
        plt.axis("off")
    plt.tight_layout()
    plt.show()
'''
