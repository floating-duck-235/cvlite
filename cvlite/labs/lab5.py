TITLE = "Image segmentation (Otsu, K-means, Watershed)"
INPUT = "image"
DEFAULT_PATH = "/content/image.jpg"

AIM = "Segment an image into meaningful parts using three automatic methods: Otsu thresholding (intensity), K-means clustering (colour) and the marker-based Watershed algorithm (separating regions along their boundaries). No mouse or GUI input is needed, so it runs safely in Google Colab."

STEPS = [
    "Read the image and shrink it so the longest side is at most 800 px, so it runs quickly.",
    "Otsu thresholding: blur the grayscale image, threshold it with THRESH_OTSU, and keep the original pixels inside the mask with cv2.bitwise_and.",
    "K-means: reshape the image into a list of pixels (N x 3), run cv2.kmeans with K = 3, then replace every pixel with the colour of its cluster centre.",
    "Watershed, part 1 (markers): clean the Otsu mask with opening. Dilate it to get the 'sure background'. Use the distance transform and threshold it at 50% of its maximum to get the 'sure foreground'. The 'unknown' band is sure background minus sure foreground.",
    "Watershed, part 2: label every sure-foreground blob with cv2.connectedComponents, add 1 so the background is 1 instead of 0, set the unknown pixels to 0, and run cv2.watershed. It floods from the markers and marks the boundaries between regions with -1.",
    "Thicken the watershed boundaries with cv2.dilate and draw them in red, show all results in a 2x4 grid, and print the foreground percentages and the number of regions.",
]

THEORY = [
    "Segmentation divides an image into regions that each belong to one object or class.",
    "Thresholding: pixel > T becomes foreground. Otsu chooses T automatically by maximising the between-class variance of the histogram.",
    "K-means clustering: choose K centres, assign each pixel to the nearest centre, move each centre to the mean of its pixels, and repeat until it converges. KMEANS_PP_CENTERS uses smart (k-means++) initialisation.",
    "Watershed: think of the gradient image as a landscape. Water rises from each marker (a 'basin'), and where water from two different markers meets, a dam (boundary, value -1) is built. Markers stop over-segmentation.",
    "Distance transform: each foreground pixel gets its distance to the nearest background pixel. Object centres have the largest values, so thresholding it gives one seed per object even when objects touch.",
    "Why not GrabCut? GrabCut is an interactive (GUI, mouse-driven) algorithm and can loop forever on low-colour images, which freezes the Colab kernel. Watershed is automatic and always finishes.",
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

h, w = img.shape[:2]
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

blur = cv2.GaussianBlur(gray, (5, 5), 0)
otsu_value, otsu_mask = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
otsu_result = cv2.bitwise_and(img, img, mask=otsu_mask)

pixels = img.reshape(-1, 3).astype(np.float32)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
_, labels, centers = cv2.kmeans(pixels, 3, None, criteria, 3, cv2.KMEANS_PP_CENTERS)
kmeans_result = centers.astype(np.uint8)[labels.flatten()].reshape(img.shape)

kernel = np.ones((3, 3), np.uint8)
opening = cv2.morphologyEx(otsu_mask, cv2.MORPH_OPEN, kernel, iterations=2)
sure_bg = cv2.dilate(opening, kernel, iterations=3)
dist = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
_, sure_fg = cv2.threshold(dist, 0.5 * dist.max(), 255, cv2.THRESH_BINARY)
sure_fg = sure_fg.astype(np.uint8)
unknown = cv2.subtract(sure_bg, sure_fg)

count, markers = cv2.connectedComponents(sure_fg)
markers = markers + 1
markers[unknown == 255] = 0
markers = cv2.watershed(img, markers)

boundary = cv2.dilate((markers == -1).astype(np.uint8), kernel, iterations=2)
watershed_result = img.copy()
watershed_result[boundary > 0] = (0, 0, 255)

results = [(img, "Original"), (otsu_mask, "Otsu mask (T = " + str(int(otsu_value)) + ")"),
           (otsu_result, "Otsu segmented"), (kmeans_result, "K-means (K = 3)"),
           (dist, "Distance transform"), (sure_fg, "Sure foreground (seeds)"),
           (markers, "Watershed regions"), (watershed_result, "Watershed boundaries")]
plt.figure(figsize=(20, 10))
for i, (image, name) in enumerate(results):
    plt.subplot(2, 4, i + 1)
    if image is markers:
        plt.imshow(image, cmap="nipy_spectral")
    elif image.ndim == 2:
        plt.imshow(image, cmap="gray")
    else:
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(name)
    plt.axis("off")
plt.tight_layout()
plt.show()

print("Otsu threshold value:", otsu_value)
print("Otsu foreground    :", round(100 * cv2.countNonZero(otsu_mask) / (h * w), 2), "%")
print("Watershed regions (objects found):", count - 1)
print("K-means cluster centres (B, G, R):")
print(centers.astype(int))
'''
