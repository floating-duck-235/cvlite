TITLE = "Edge detection (Sobel, Prewitt, Roberts, Laplacian, Canny)"
INPUT = "image"
DEFAULT_PATH = "/content/image.jpg"

AIM = "Detect edges in an image with first-order gradient operators (Sobel, Prewitt, Roberts), a second-order operator (Laplacian) and the Canny edge detector, and compare the results."

STEPS = [
    "Read the image, convert it to grayscale and smooth it with a Gaussian blur to reduce noise (noise creates false edges).",
    "Sobel: compute the gradient in x and y with cv2.Sobel, then the magnitude sqrt(Gx^2 + Gy^2).",
    "Prewitt: build the two 3x3 Prewitt kernels with np.array and convolve them with cv2.filter2D, then take the magnitude.",
    "Roberts: build the two 2x2 diagonal Roberts kernels and convolve them with cv2.filter2D, then take the magnitude.",
    "Laplacian: second derivative with cv2.Laplacian, take the absolute value.",
    "Canny: cv2.Canny with a low and a high threshold.",
    "Clip every result to 0-255, convert to uint8 and show everything in a 3x3 grid.",
    "Print how many edge pixels Canny found.",
]

THEORY = [
    "An edge is a place where intensity changes sharply, so edges are found with derivatives.",
    "Sobel kernels: Gx = [[-1,0,1],[-2,0,2],[-1,0,1]], Gy = its transpose. The centre row/column has weight 2, which gives extra smoothing.",
    "Prewitt kernels: Gx = [[-1,0,1],[-1,0,1],[-1,0,1]], Gy = [[1,1,1],[0,0,0],[-1,-1,-1]]. Same idea as Sobel without the extra weight.",
    "Roberts cross kernels: [[1,0],[0,-1]] and [[0,1],[-1,0]]. 2x2 diagonal differences: fast but sensitive to noise.",
    "Gradient magnitude = sqrt(Gx^2 + Gy^2), gradient direction = atan2(Gy, Gx).",
    "Laplacian = d2I/dx2 + d2I/dy2, kernel [[0,1,0],[1,-4,1],[0,1,0]]. Edges are at zero crossings. It does not give a direction and is very sensitive to noise.",
    "Canny steps: 1) Gaussian smoothing, 2) Sobel gradient, 3) non-maximum suppression (thin edges to 1 pixel), 4) double threshold (strong/weak edges), 5) hysteresis (keep weak edges only if they touch strong ones).",
    "CV_64F / CV_32F output types are used so negative gradient values are not cut off at 0, as they would be with uint8.",
]

CODE = r'''import cv2
import numpy as np
import matplotlib.pyplot as plt

image_path = __PATH__

img = cv2.imread(image_path)
if img is None:
    raise FileNotFoundError("Could not read the image at " + image_path)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)

sobel_x = cv2.Sobel(blur, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(blur, cv2.CV_64F, 0, 1, ksize=3)
sobel = np.sqrt(sobel_x ** 2 + sobel_y ** 2)

prewitt_kx = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.float32)
prewitt_ky = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=np.float32)
prewitt_x = cv2.filter2D(blur, cv2.CV_32F, prewitt_kx)
prewitt_y = cv2.filter2D(blur, cv2.CV_32F, prewitt_ky)
prewitt = np.sqrt(prewitt_x ** 2 + prewitt_y ** 2)

roberts_kx = np.array([[1, 0], [0, -1]], dtype=np.float32)
roberts_ky = np.array([[0, 1], [-1, 0]], dtype=np.float32)
roberts_x = cv2.filter2D(blur, cv2.CV_32F, roberts_kx)
roberts_y = cv2.filter2D(blur, cv2.CV_32F, roberts_ky)
roberts = np.sqrt(roberts_x ** 2 + roberts_y ** 2)

laplacian = np.abs(cv2.Laplacian(blur, cv2.CV_64F, ksize=3))

canny = cv2.Canny(blur, 50, 150)

results = [(gray, "Original"), (blur, "Gaussian blur"), (np.abs(sobel_x), "Sobel X"),
           (np.abs(sobel_y), "Sobel Y"), (sobel, "Sobel magnitude"), (prewitt, "Prewitt"),
           (roberts, "Roberts"), (laplacian, "Laplacian"), (canny, "Canny")]
plt.figure(figsize=(15, 13))
for i, (image, name) in enumerate(results):
    plt.subplot(3, 3, i + 1)
    plt.imshow(np.clip(image, 0, 255).astype(np.uint8), cmap="gray")
    plt.title(name)
    plt.axis("off")
plt.tight_layout()
plt.show()

print("Canny edge pixels:", np.count_nonzero(canny), "out of", canny.size)
'''
