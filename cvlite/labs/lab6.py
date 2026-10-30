TITLE = "Analyse and describe a segmented region"
INPUT = "image"
DEFAULT_PATH = "/content/image.jpg"

AIM = "Segment the main object automatically with marker-controlled Watershed (no GUI, safe in Colab), measure its shape, colour and texture (area, perimeter, centroid, bounding box, aspect ratio, extent, solidity, circularity, orientation, elongation, GLCM texture), save the measurements to a CSV file and write a plain-English description of the region."

STEPS = [
    "Read the image (shrunk to at most 800 px) and blur it slightly.",
    "Segment the main object with marker-controlled Watershed: a thin strip around the image border is labelled 1 (background), a box in the centre is labelled 2 (object), and everything else is 0 (unknown). cv2.watershed grows both labels until they meet at the strongest edge. Pixels labelled 2 form the object mask. If nothing is found, the whole image is used.",
    "Find the contours of the mask and keep the largest one as the region. Redraw it as a filled mask.",
    "Shape measurements: area (cv2.contourArea), perimeter (cv2.arcLength), bounding box (cv2.boundingRect), centroid from image moments (cv2.moments), convex hull (cv2.convexHull).",
    "Derived measurements: aspect ratio = w/h, extent = area / box area, solidity = area / hull area, circularity = 4*pi*area / perimeter^2, equivalent diameter = sqrt(4*area/pi).",
    "Orientation and elongation: run PCA (cv2.PCACompute2) on the region's pixel coordinates. The first eigenvector gives the direction of the major axis; sqrt of the eigenvalues gives the axis lengths.",
    "Colour and texture: mean colour and brightness inside the mask (cv2.mean with mask), and GLCM contrast, homogeneity, energy and correlation (skimage graycomatrix / graycoprops).",
    "Put all measurements in a pandas DataFrame, print it and save it as region_measurements.csv.",
    "Print a written description (size, position, shape, brightness) and draw the contour, hull, box, centroid and major axis on the image.",
]

THEORY = [
    "Marker-controlled Watershed: the markers we place tell the algorithm what is definitely background and definitely object. The flood from each marker stops where the colour changes sharply, so the object boundary follows real edges. It is the automatic, GUI-free replacement for GrabCut's rectangle.",
    "Image moments: m00 = area, m10 and m01 = first moments. Centroid cx = m10/m00, cy = m01/m00.",
    "Circularity = 4*pi*A / P^2 is 1 for a perfect circle and gets smaller for irregular shapes.",
    "Solidity = A / convex hull area: 1 means the region is convex, lower means it has dents or concavities.",
    "Extent = A / (w*h): how much of the bounding box the region fills.",
    "PCA on the (x, y) coordinates: the eigenvector with the largest eigenvalue points along the major axis. Elongation = major / minor axis length.",
    "GLCM (Gray Level Co-occurrence Matrix): counts how often pairs of gray levels appear next to each other (distance 1, angle 0 = horizontal neighbours). Contrast = local intensity variation, Homogeneity = closeness to the diagonal, Energy = uniformity, Correlation = linear dependency of neighbouring gray levels.",
]

CODE = r'''import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage.feature import graycomatrix, graycoprops

image_path = __PATH__

img = cv2.imread(image_path)
if img is None:
    raise FileNotFoundError("Could not read the image at " + image_path)

scale = 800 / max(img.shape[:2])
if scale < 1:
    img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

h, w = img.shape[:2]
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

smooth = cv2.GaussianBlur(img, (5, 5), 0)
markers = np.zeros((h, w), np.int32)
border = max(1, min(h, w) // 20)
markers[:border, :] = 1
markers[-border:, :] = 1
markers[:, :border] = 1
markers[:, -border:] = 1
markers[int(h * 0.35):int(h * 0.65), int(w * 0.35):int(w * 0.65)] = 2
markers = cv2.watershed(smooth, markers)
mask2 = np.where(markers == 2, 255, 0).astype(np.uint8)
if cv2.countNonZero(mask2) == 0:
    mask2[:, :] = 255

contours, _ = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
c = max(contours, key=cv2.contourArea)
region_mask = np.zeros_like(mask2)
cv2.drawContours(region_mask, [c], -1, 255, -1)

area = cv2.contourArea(c)
perimeter = cv2.arcLength(c, True)
bx, by, bw, bh = cv2.boundingRect(c)
M = cv2.moments(c)
if M["m00"] != 0:
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
else:
    cx, cy = bx + bw // 2, by + bh // 2
hull = cv2.convexHull(c)
hull_area = cv2.contourArea(hull)

aspect_ratio = bw / bh
extent = area / (bw * bh)
solidity = area / hull_area if hull_area > 0 else 0
circularity = 4 * np.pi * area / (perimeter ** 2) if perimeter > 0 else 0
equivalent_diameter = np.sqrt(4 * area / np.pi)

ys, xs = np.where(region_mask > 0)
points = np.column_stack((xs, ys)).astype(np.float64)
mean, eigenvectors, eigenvalues = cv2.PCACompute2(points, mean=np.empty((0)))
major_axis = 4 * np.sqrt(max(eigenvalues[0, 0], 0))
minor_axis = 4 * np.sqrt(max(eigenvalues[-1, 0], 0))
orientation = np.degrees(np.arctan2(eigenvectors[0, 1], eigenvectors[0, 0]))
elongation = major_axis / minor_axis if minor_axis > 0 else 0

mean_colour = cv2.mean(img, mask=region_mask)
brightness = cv2.mean(gray, mask=region_mask)[0]
roi = cv2.bitwise_and(gray, gray, mask=region_mask)[by:by + bh, bx:bx + bw]
glcm = graycomatrix(roi, distances=[1], angles=[0], levels=256, symmetric=True, normed=True)
texture_contrast = graycoprops(glcm, "contrast")[0, 0]
texture_homogeneity = graycoprops(glcm, "homogeneity")[0, 0]
texture_energy = graycoprops(glcm, "energy")[0, 0]
texture_correlation = graycoprops(glcm, "correlation")[0, 0]
percent = area / (h * w) * 100

measurements = {
    "Area (px)": area,
    "Perimeter (px)": perimeter,
    "Centroid X": cx,
    "Centroid Y": cy,
    "Bounding box X": bx,
    "Bounding box Y": by,
    "Bounding box width": bw,
    "Bounding box height": bh,
    "Aspect ratio": aspect_ratio,
    "Extent": extent,
    "Solidity": solidity,
    "Circularity": circularity,
    "Equivalent diameter": equivalent_diameter,
    "Major axis length": major_axis,
    "Minor axis length": minor_axis,
    "Orientation (deg)": orientation,
    "Elongation": elongation,
    "Mean blue": mean_colour[0],
    "Mean green": mean_colour[1],
    "Mean red": mean_colour[2],
    "Brightness": brightness,
    "Texture contrast": texture_contrast,
    "Texture homogeneity": texture_homogeneity,
    "Texture energy": texture_energy,
    "Texture correlation": texture_correlation,
    "Image coverage (%)": percent,
}
df = pd.DataFrame(list(measurements.items()), columns=["Measurement", "Value"])
print(df.to_string(index=False))
df.to_csv("region_measurements.csv", index=False)
print("Saved region_measurements.csv")

print("\nDescription:")
print("The segmented region covers", round(percent, 1), "% of the image.")
if cx < w / 3:
    print("It is on the left side of the image.")
elif cx > 2 * w / 3:
    print("It is on the right side of the image.")
else:
    print("It is in the centre of the image.")
if aspect_ratio < 1:
    print("It is taller than it is wide.")
else:
    print("It is wider than it is tall.")
if circularity > 0.7:
    print("Its shape is round.")
else:
    print("Its shape is irregular (not round).")
if solidity > 0.9:
    print("It is convex (has almost no dents).")
else:
    print("It has concave parts (dents).")
if brightness > 127:
    print("The region is bright.")
else:
    print("The region is dark.")
print("Its major axis points at", round(orientation, 1), "degrees and it is", round(elongation, 2), "times longer than it is wide.")

output = img.copy()
cv2.drawContours(output, [c], -1, (0, 255, 0), 3)
cv2.drawContours(output, [hull], -1, (255, 0, 255), 2)
cv2.rectangle(output, (bx, by), (bx + bw, by + bh), (255, 0, 0), 3)
cv2.circle(output, (cx, cy), 8, (0, 0, 255), -1)
centre = (int(mean[0, 0]), int(mean[0, 1]))
end_point = (int(centre[0] + major_axis / 2 * eigenvectors[0, 0]), int(centre[1] + major_axis / 2 * eigenvectors[0, 1]))
cv2.line(output, centre, end_point, (0, 255, 255), 3)

plt.figure(figsize=(16, 6))
plt.subplot(1, 3, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title("Original")
plt.axis("off")
plt.subplot(1, 3, 2)
plt.imshow(region_mask, cmap="gray")
plt.title("Segmented region")
plt.axis("off")
plt.subplot(1, 3, 3)
plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
plt.title("Contour, hull, box, centroid and major axis")
plt.axis("off")
plt.tight_layout()
plt.show()
'''
