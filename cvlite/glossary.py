GLOSSARY = {
    "cv2.imread": (
        "cv2.imread(path, flag)", "OpenCV",
        "Reads an image file from disk and returns it as a NumPy array of shape (height, width, 3) in BGR order with values 0-255 (uint8). "
        "It returns None (instead of raising an error) if the file does not exist or cannot be decoded, which is why the code checks 'if img is None'. "
        "Optional flag: cv2.IMREAD_COLOR (default, 3 channels), cv2.IMREAD_GRAYSCALE (1 channel), cv2.IMREAD_UNCHANGED (keeps alpha / 16-bit).",
    ),
    "FileNotFoundError": (
        "raise FileNotFoundError(message)", "Python built-in",
        "A built-in exception class. 'raise' stops the program with a clear message when the image or video path is wrong, instead of failing later with a confusing error.",
    ),
    "cv2.cvtColor": (
        "cv2.cvtColor(src, code)", "OpenCV",
        "Converts an image from one colour space to another. The code says which conversion to do, e.g. COLOR_BGR2RGB (for displaying with matplotlib), "
        "COLOR_BGR2GRAY (single-channel intensity), COLOR_BGR2HSV, COLOR_BGR2LAB, COLOR_BGR2YCrCb, COLOR_YCrCb2BGR and COLOR_GRAY2BGR. Returns a new image.",
    ),
    ".astype": (
        "array.astype(dtype)", "NumPy array method",
        "Returns a copy of the array converted to another data type, e.g. np.float64 / np.float32 for maths that needs decimals and negatives, "
        "np.uint8 for images (0-255), or int for printing whole numbers.",
    ),
    "np.max": (
        "np.max(array, axis)", "NumPy",
        "Returns the largest value. With axis=2 on an (H, W, 3) image it takes the maximum over the 3 colour channels for every pixel, giving an (H, W) array. Used for K = 1 - max(R, G, B) in CMYK.",
    ),
    "plt.figure": (
        "plt.figure(figsize=(width, height))", "Matplotlib",
        "Creates a new empty figure (drawing window). figsize is the size in inches. Everything drawn afterwards goes into this figure until plt.show().",
    ),
    "enumerate": (
        "enumerate(iterable)", "Python built-in",
        "Loops over a list and gives back pairs (index, item), so you get the position (0, 1, 2, ...) and the value at the same time. "
        "Used to know which subplot number or colour to use for each item.",
    ),
    "plt.subplot": (
        "plt.subplot(rows, cols, index)", "Matplotlib",
        "Splits the figure into a grid of rows x cols small plots and selects plot number 'index' (counting from 1, left to right, top to bottom). The next imshow/plot/hist draws there.",
    ),
    "plt.imshow": (
        "plt.imshow(image, cmap=None, vmin=None, vmax=None)", "Matplotlib",
        "Displays an array as an image. A 3-channel array is shown as RGB, so OpenCV BGR images must be converted with cv2.cvtColor first. "
        "A 2-D array is shown using a colour map; cmap='gray' shows it in black and white. vmin/vmax fix the display range (0-255) instead of auto-stretching.",
    ),
    "plt.title": (
        "plt.title(text)", "Matplotlib",
        "Writes a title above the current subplot. Optional fontsize changes the text size.",
    ),
    "plt.axis": (
        "plt.axis('off')", "Matplotlib",
        "Hides the x and y axes, ticks and numbers so only the image is shown.",
    ),
    "plt.tight_layout": (
        "plt.tight_layout()", "Matplotlib",
        "Automatically adjusts the spacing between subplots so titles and images do not overlap.",
    ),
    "plt.show": (
        "plt.show()", "Matplotlib",
        "Displays the current figure. In Google Colab the figure appears below the cell.",
    ),
    "cv2.split": (
        "cv2.split(image)", "OpenCV",
        "Splits a multi-channel image into separate single-channel images, e.g. an RGB image into R, G and B arrays (each H x W). The opposite of cv2.merge.",
    ),
    "cv2.applyColorMap": (
        "cv2.applyColorMap(gray, colormap)", "OpenCV",
        "Pseudo-colouring: replaces every gray level (0-255) with a colour from a lookup table, giving a BGR colour image. "
        "Examples: cv2.COLORMAP_JET (blue to red), COLORMAP_TURBO (improved JET), COLORMAP_BONE (bluish gray), COLORMAP_HOT (black-red-yellow-white). Makes small intensity differences easier to see.",
    ),
    "print": (
        "print(values...)", "Python built-in",
        "Prints values to the output, separated by spaces. Used to show measurements and results as text.",
    ),
    "np.mean": (
        "np.mean(array)", "NumPy",
        "Returns the average of all values in the array, e.g. the average intensity of a channel.",
    ),
    "cv2.equalizeHist": (
        "cv2.equalizeHist(gray)", "OpenCV",
        "Global histogram equalization of an 8-bit single-channel image. It maps every intensity through the normalised cumulative histogram (CDF), "
        "so the output histogram is spread over the whole 0-255 range and contrast increases. Input must be uint8 grayscale.",
    ),
    "cv2.createCLAHE": (
        "cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))", "OpenCV",
        "Creates a CLAHE object (Contrast Limited Adaptive Histogram Equalization). The image is divided into tileGridSize tiles, each tile is equalized separately, "
        "and the histogram is clipped at clipLimit so noise is not over-amplified. Use its .apply(image) method to process an image.",
    ),
    ".apply": (
        "clahe.apply(gray)", "OpenCV object method",
        "Runs the CLAHE algorithm created by cv2.createCLAHE on a grayscale uint8 image and returns the contrast-enhanced image.",
    ),
    "plt.hist": (
        "plt.hist(values, bins=256, range=(0, 256))", "Matplotlib",
        "Draws a histogram: counts how many values fall into each bin and draws a bar for each. With 256 bins over 0-256 there is one bar per gray level.",
    ),
    ".ravel": (
        "array.ravel()", "NumPy array method",
        "Flattens a 2-D (or 3-D) array into a 1-D list of all pixel values. plt.hist needs a 1-D array.",
    ),
    "plt.xlabel": (
        "plt.xlabel(text)", "Matplotlib",
        "Sets the label of the x-axis of the current plot.",
    ),
    "plt.ylabel": (
        "plt.ylabel(text)", "Matplotlib",
        "Sets the label of the y-axis of the current plot.",
    ),
    "cv2.calcHist": (
        "cv2.calcHist([image], [channel], mask, [histSize], [range])", "OpenCV",
        "Calculates the histogram of an image. [0] = use channel 0, None = no mask (whole image), [256] = 256 bins, [0, 256] = range of values. Returns a 256 x 1 float array of pixel counts.",
    ),
    ".cumsum": (
        "array.cumsum()", "NumPy array method",
        "Cumulative sum: element i is the sum of all elements up to i. Applied to a histogram it gives the CDF (cumulative distribution function). Dividing by the last value normalises it to 0-1.",
    ),
    "plt.plot": (
        "plt.plot(x, y) or plt.plot(y)", "Matplotlib",
        "Draws a line graph. With one argument, the x values are 0, 1, 2, ... Optional label (for the legend), color and linewidth.",
    ),
    "plt.legend": (
        "plt.legend()", "Matplotlib",
        "Shows a legend box listing every line/marker that was drawn with a label=... argument.",
    ),
    "cv2.merge": (
        "cv2.merge([ch1, ch2, ch3])", "OpenCV",
        "Combines single-channel images into one multi-channel image. The opposite of cv2.split. Used to put the equalized Y channel back with Cr and Cb.",
    ),
    "np.std": (
        "np.std(array)", "NumPy",
        "Standard deviation of all values: how spread out the intensities are. A larger standard deviation means higher global contrast.",
    ),
    "cv2.GaussianBlur": (
        "cv2.GaussianBlur(image, (5, 5), 0)", "OpenCV",
        "Smooths the image by convolving it with a Gaussian kernel. (5, 5) is the kernel size (must be odd), and 0 means sigma is calculated from the kernel size. "
        "Removes noise before edge detection or thresholding.",
    ),
    "cv2.Sobel": (
        "cv2.Sobel(image, ddepth, dx, dy, ksize=3)", "OpenCV",
        "Computes the image derivative with the Sobel operator. dx=1, dy=0 gives the horizontal gradient Gx (finds vertical edges); dx=0, dy=1 gives Gy (finds horizontal edges). "
        "ddepth=cv2.CV_64F stores the result as 64-bit float so negative gradients are kept. ksize is the kernel size.",
    ),
    "np.sqrt": (
        "np.sqrt(x)", "NumPy",
        "Element-wise square root. Used for gradient magnitude sqrt(Gx^2 + Gy^2), equivalent diameter, axis lengths from eigenvalues, and distances.",
    ),
    "np.array": (
        "np.array(list, dtype=...)", "NumPy",
        "Creates a NumPy array from a Python list. Used to build the convolution kernels (Prewitt, Roberts) as float32 matrices, and to turn the list of tracked points into an array.",
    ),
    "cv2.filter2D": (
        "cv2.filter2D(image, ddepth, kernel)", "OpenCV",
        "Convolves (strictly, correlates) the image with any custom kernel: every output pixel is the weighted sum of its neighbourhood using the kernel weights. "
        "ddepth=cv2.CV_32F gives a float result so negative values are kept. Used to apply the Prewitt and Roberts kernels.",
    ),
    "np.abs": (
        "np.abs(array)", "NumPy",
        "Element-wise absolute value. Turns negative derivatives into positive edge strengths for display.",
    ),
    "cv2.Laplacian": (
        "cv2.Laplacian(image, ddepth, ksize=3)", "OpenCV",
        "Computes the Laplacian (sum of second derivatives d2I/dx2 + d2I/dy2). Edges appear where it crosses zero. It responds to edges in all directions but is very sensitive to noise.",
    ),
    "cv2.Canny": (
        "cv2.Canny(image, threshold1, threshold2)", "OpenCV",
        "Canny edge detector. Steps: Sobel gradient, non-maximum suppression (thin edges), double threshold and hysteresis. "
        "Gradients above threshold2 (150) are strong edges, those below threshold1 (50) are discarded, and those in between are kept only if they connect to a strong edge. Returns a binary edge image (0 or 255).",
    ),
    "np.clip": (
        "np.clip(array, min, max)", "NumPy",
        "Limits all values to the range [min, max]. Values below 0 become 0 and values above 255 become 255, so the result can be safely converted to uint8.",
    ),
    "np.count_nonzero": (
        "np.count_nonzero(array)", "NumPy",
        "Counts how many elements are not zero, e.g. the number of edge pixels in the Canny output.",
    ),
    "max": (
        "max(iterable, key=...) or max(a, b)", "Python built-in",
        "Returns the largest item. With key=cv2.contourArea it returns the contour with the largest area. With key=captions.count it returns the most frequent caption. "
        "max(a, b) returns the bigger number (e.g. the longest image side).",
    ),
    "cv2.resize": (
        "cv2.resize(image, dsize, fx=None, fy=None, interpolation=...)", "OpenCV",
        "Changes the image size. Either give dsize=(width, height), or dsize=None with scale factors fx and fy. "
        "cv2.INTER_AREA is the best interpolation for shrinking. Used to make big photos smaller so the algorithms run fast.",
    ),
    "cv2.threshold": (
        "cv2.threshold(image, thresh, maxval, type)", "OpenCV",
        "Converts a grayscale (or float) image to binary: pixels above thresh become maxval (255), the rest become 0. THRESH_BINARY_INV does the opposite. "
        "Adding cv2.THRESH_OTSU makes OpenCV choose the best threshold automatically (thresh=0 is ignored). Returns (threshold_used, binary_image).",
    ),
    "np.ones": (
        "np.ones((rows, cols), dtype)", "NumPy",
        "Creates an array filled with ones. np.ones((9, 9), np.uint8) is the square structuring element (kernel) used for morphology.",
    ),
    "cv2.morphologyEx": (
        "cv2.morphologyEx(image, operation, kernel)", "OpenCV",
        "Applies a morphological operation on a binary image. cv2.MORPH_OPEN = erosion then dilation (removes small white noise). "
        "cv2.MORPH_CLOSE = dilation then erosion (fills small black holes). iterations=2 repeats the erosion and dilation steps twice. Others: MORPH_GRADIENT, MORPH_TOPHAT, MORPH_BLACKHAT.",
    ),
    "cv2.findContours": (
        "cv2.findContours(binary, mode, method)", "OpenCV",
        "Finds the boundaries (contours) of the white regions in a binary image. Returns (contours, hierarchy); each contour is an array of (x, y) boundary points. "
        "cv2.RETR_EXTERNAL keeps only the outermost contours. cv2.CHAIN_APPROX_SIMPLE compresses straight lines to their end points to save memory.",
    ),
    "sorted": (
        "sorted(iterable, key=..., reverse=True)", "Python built-in",
        "Returns a new sorted list. key=cv2.contourArea sorts the contours by area, and reverse=True puts the largest first. [:3] then keeps the top three.",
    ),
    "cv2.contourArea": (
        "cv2.contourArea(contour)", "OpenCV",
        "Returns the area (in pixels) enclosed by a contour, calculated with the shoelace (Green's) formula. Also used as the key to sort or pick the largest contour.",
    ),
    ".copy": (
        "array.copy()", "NumPy array method",
        "Makes an independent copy of an image, so drawing boxes and text on the copy does not change the original.",
    ),
    "cv2.boundingRect": (
        "cv2.boundingRect(contour)", "OpenCV",
        "Returns (x, y, w, h): the top-left corner, width and height of the smallest upright rectangle that contains the contour.",
    ),
    "cv2.rectangle": (
        "cv2.rectangle(image, (x1, y1), (x2, y2), colour, thickness)", "OpenCV",
        "Draws a rectangle on the image in place, from the top-left corner to the bottom-right corner. Colour is in BGR, e.g. (0, 255, 0) = green. thickness=-1 would fill it.",
    ),
    "cv2.putText": (
        "cv2.putText(image, text, (x, y), font, scale, colour, thickness)", "OpenCV",
        "Writes text on the image in place. (x, y) is the bottom-left corner of the text, font e.g. cv2.FONT_HERSHEY_SIMPLEX, scale is the text size.",
    ),
    "str": (
        "str(value)", "Python built-in",
        "Converts a value (e.g. a number) to text so it can be joined with other text using +.",
    ),
    ".append": (
        "list.append(item)", "Python list method",
        "Adds an item to the end of a list, e.g. each cropped ROI, each tracked centre point, each frame or each caption.",
    ),
    "len": (
        "len(object)", "Python built-in",
        "Returns the number of items in a list (or the length of an array/string), e.g. how many ROIs, points or frames there are.",
    ),
    "cv2.bitwise_and": (
        "cv2.bitwise_and(img, img, mask=mask)", "OpenCV",
        "Bitwise AND of two images. Passing the same image twice with a mask keeps the original pixels where the mask is white (255) and makes everything else black: it cuts out the segmented object.",
    ),
    ".reshape": (
        "array.reshape(new_shape)", "NumPy array method",
        "Changes the shape of an array without changing its data. img.reshape(-1, 3) turns an H x W x 3 image into a list of N pixels with 3 values each (-1 = work out this size automatically). "
        "The K-means result is reshaped back to the image shape.",
    ),
    "cv2.kmeans": (
        "cv2.kmeans(data, K, bestLabels, criteria, attempts, flags)", "OpenCV",
        "K-means clustering. data = float32 N x 3 pixel colours, K = number of clusters (3), bestLabels = None, "
        "criteria = (TERM_CRITERIA_EPS + TERM_CRITERIA_MAX_ITER, 10, 1.0): stop after 10 iterations or when the centres move less than 1.0, attempts = how many times to run with different starts (the best is kept), "
        "flags = cv2.KMEANS_PP_CENTERS (k-means++ initialisation). Returns (compactness, labels, centers).",
    ),
    ".flatten": (
        "array.flatten()", "NumPy array method",
        "Returns a 1-D copy of the array. The N x 1 labels from kmeans become a flat list used to look up each pixel's cluster centre colour.",
    ),
    "int": (
        "int(value)", "Python built-in",
        "Converts a value to a whole number (decimals are dropped). OpenCV drawing functions need integer pixel coordinates.",
    ),
    "np.zeros": (
        "np.zeros(shape, dtype)", "NumPy",
        "Creates an array filled with zeros. np.zeros((h, w), np.int32) is the empty marker image for watershed: 0 means 'unknown', and the code then writes 1 (background) and 2 (object) into it. Markers must be int32.",
    ),
    "cv2.dilate": (
        "cv2.dilate(binary, kernel, iterations=3)", "OpenCV",
        "Dilation: grows the white regions. Each pixel takes the maximum value under the kernel, repeated 'iterations' times. "
        "Dilating the cleaned mask gives the 'sure background' area: anything outside it is certainly background. It is also used to thicken the 1-pixel watershed boundary lines so they are visible.",
    ),
    "cv2.distanceTransform": (
        "cv2.distanceTransform(binary, cv2.DIST_L2, 5)", "OpenCV",
        "For every white pixel, calculates its distance to the nearest black (background) pixel. DIST_L2 = Euclidean distance, 5 = mask size. "
        "Pixels in the middle of objects get the biggest values, so thresholding the result gives the 'sure foreground' seeds. Returns a float32 image.",
    ),
    ".max": (
        "array.max()", "NumPy array method",
        "Returns the largest value in the array, e.g. the largest distance in the distance transform (to threshold at 50% of it), or the tallest histogram bar (to scale the CDF to the same height).",
    ),
    "cv2.subtract": (
        "cv2.subtract(a, b)", "OpenCV",
        "Pixel-wise a - b, clipped at 0 (saturated) so it never wraps around below 0 like plain uint8 subtraction does. "
        "sure_bg - sure_fg gives the 'unknown' band around each object where the boundary must lie.",
    ),
    "cv2.connectedComponents": (
        "cv2.connectedComponents(binary)", "OpenCV",
        "Gives every separate white blob its own label number (1, 2, 3, ...), with the background as 0. Returns (count, labels), where count includes the background. Used to give each seed its own watershed marker.",
    ),
    "cv2.watershed": (
        "cv2.watershed(image, markers)", "OpenCV",
        "Marker-controlled watershed segmentation. image must be 8-bit 3-channel, and markers is an int32 image where positive numbers are seeds and 0 means unknown. "
        "It floods outward from each seed using colour differences, so the regions meet along the strongest edges. It fills every unknown pixel with a seed's label, marks the boundaries between regions with -1 and returns the markers array. "
        "It is fully automatic (no mouse input) and always finishes, so it is the safe Colab replacement for GrabCut.",
    ),
    "np.where": (
        "np.where(condition, a, b) or np.where(condition)", "NumPy",
        "With three arguments: picks a where the condition is True and b where it is False, e.g. 255 for pixels whose watershed label is 2 (the object) and 0 for the rest. "
        "With one argument: returns the row and column indices (ys, xs) of the pixels where the condition is True.",
    ),
    "round": (
        "round(number, digits)", "Python built-in",
        "Rounds a number to the given number of decimal places for neat printing.",
    ),
    "plt.xlim": (
        "plt.xlim(left, right)", "Matplotlib",
        "Sets the range shown on the x-axis. plt.xlim(0, 256) shows all gray levels so the histograms are easy to compare.",
    ),
    "cv2.countNonZero": (
        "cv2.countNonZero(image)", "OpenCV",
        "Counts the non-zero (white) pixels in a single-channel image. Divided by h*w it gives the percentage of the image that is foreground.",
    ),
    "np.zeros_like": (
        "np.zeros_like(array)", "NumPy",
        "Creates an array of zeros with the same shape and type as another array. Used as a blank canvas to draw the filled region mask.",
    ),
    "cv2.drawContours": (
        "cv2.drawContours(image, [contour], index, colour, thickness)", "OpenCV",
        "Draws contours on an image in place. index -1 draws all contours in the list. thickness -1 fills the inside (used to make a solid mask); a positive thickness draws only the outline.",
    ),
    "cv2.arcLength": (
        "cv2.arcLength(contour, closed)", "OpenCV",
        "Returns the perimeter (length) of the contour. closed=True means the last point joins back to the first.",
    ),
    "cv2.moments": (
        "cv2.moments(contour)", "OpenCV",
        "Calculates the image moments of a shape as a dictionary. m00 = area, m10 and m01 = first-order moments. The centroid is cx = m10/m00, cy = m01/m00. Also contains central moments (mu..) and normalised moments (nu..).",
    ),
    "cv2.convexHull": (
        "cv2.convexHull(contour)", "OpenCV",
        "Returns the convex hull: the smallest convex polygon that encloses the contour (like a rubber band stretched around it). Used for solidity = area / hull area.",
    ),
    "np.column_stack": (
        "np.column_stack((xs, ys))", "NumPy",
        "Stacks 1-D arrays as columns of a 2-D array, giving an N x 2 array of (x, y) pixel coordinates for PCA.",
    ),
    "cv2.PCACompute2": (
        "cv2.PCACompute2(data, mean)", "OpenCV",
        "Principal Component Analysis. data is N x 2 (x, y) points. Passing mean=np.empty((0)) tells OpenCV to compute the mean itself. "
        "Returns (mean, eigenvectors, eigenvalues). The first eigenvector is the direction of greatest spread (the major axis), and the eigenvalues are the variances along each axis.",
    ),
    "np.empty": (
        "np.empty((0))", "NumPy",
        "Creates an array without initialising its values. An empty array of size 0 is passed as 'mean' to cv2.PCACompute2 so that it calculates the mean itself.",
    ),
    "np.degrees": (
        "np.degrees(radians)", "NumPy",
        "Converts an angle from radians to degrees.",
    ),
    "np.arctan2": (
        "np.arctan2(y, x)", "NumPy",
        "Returns the angle (in radians, -pi to pi) of the vector (x, y), taking the quadrant into account. Used to get the orientation of the major axis from the first eigenvector.",
    ),
    "cv2.mean": (
        "cv2.mean(image, mask=mask)", "OpenCV",
        "Returns the mean value of each channel, using only the pixels where the mask is non-zero. Always returns a 4-tuple (B, G, R, 0) for colour or (value, 0, 0, 0) for gray images.",
    ),
    "graycomatrix": (
        "graycomatrix(image, distances, angles, levels, symmetric, normed)", "scikit-image",
        "Computes the Gray Level Co-occurrence Matrix (GLCM): a levels x levels table counting how often a pixel with gray level i has a neighbour with gray level j. "
        "distances=[1] means neighbouring pixels, angles=[0] means horizontal neighbours, symmetric=True counts (i, j) and (j, i), normed=True turns counts into probabilities.",
    ),
    "graycoprops": (
        "graycoprops(glcm, property)", "scikit-image",
        "Calculates a texture feature from the GLCM: 'contrast' (local intensity variation), 'homogeneity' (closeness to the diagonal), 'energy' (uniformity) or 'correlation'. "
        "Returns an array indexed [distance, angle], so [0, 0] picks the single value.",
    ),
    "pd.DataFrame": (
        "pd.DataFrame(data, columns=[...])", "pandas",
        "Creates a table (DataFrame) with named columns. Here each row is one measurement name and its value.",
    ),
    "list": (
        "list(iterable)", "Python built-in",
        "Converts an iterable (such as dict.items()) into a list.",
    ),
    ".items": (
        "dict.items()", "Python dict method",
        "Returns all (key, value) pairs of a dictionary, e.g. ('Area (px)', 12345.0).",
    ),
    ".to_string": (
        "df.to_string(index=False)", "pandas DataFrame method",
        "Converts the whole table to neatly aligned text for printing. index=False hides the row numbers.",
    ),
    ".to_csv": (
        "df.to_csv(filename, index=False)", "pandas DataFrame method",
        "Saves the table as a CSV file (opens in Excel). In Colab it appears in the Files panel on the left (/content).",
    ),
    "cv2.circle": (
        "cv2.circle(image, centre, radius, colour, thickness)", "OpenCV",
        "Draws a circle on the image in place. thickness=-1 makes a filled dot, used to mark the centroid or the tracked centre point.",
    ),
    "cv2.line": (
        "cv2.line(image, point1, point2, colour, thickness)", "OpenCV",
        "Draws a straight line between two points in place. Used for the major axis and for joining consecutive tracking points into a path.",
    ),
    "cv2.VideoCapture": (
        "cv2.VideoCapture(path)", "OpenCV",
        "Opens a video file (or camera if given a number) for reading frames. Use .read() to get frames, .get()/.set() for properties and .release() to close it.",
    ),
    ".read": (
        "cap.read()", "OpenCV VideoCapture method",
        "Reads the next frame of the video. Returns (ret, frame): ret is True if a frame was read and False at the end of the video or on an error; frame is a BGR image.",
    ),
    "min": (
        "min(a, b)", "Python built-in",
        "Returns the smallest value. min(1.0, 640 / longest_side) makes sure the frames are only ever shrunk, never enlarged.",
    ),
    ".get": (
        "cap.get(property)", "OpenCV VideoCapture method",
        "Reads a video property, e.g. cv2.CAP_PROP_FPS (frames per second), cv2.CAP_PROP_FRAME_COUNT (number of frames), CAP_PROP_FRAME_WIDTH / CAP_PROP_FRAME_HEIGHT. Returns a float.",
    ),
    "hasattr": (
        "hasattr(object, name)", "Python built-in",
        "Returns True if the object has an attribute with that name. Used to check whether this OpenCV build includes the CSRT tracker before calling it, so the code never crashes.",
    ),
    "cv2.TrackerCSRT_create": (
        "cv2.TrackerCSRT_create()", "OpenCV (contrib)",
        "Creates a CSRT tracker (Channel and Spatial Reliability Tracker), a discriminative correlation filter tracker. Accurate, handles non-rectangular objects, but slower. Available when opencv-contrib-python is installed.",
    ),
    "cv2.legacy.TrackerCSRT_create": (
        "cv2.legacy.TrackerCSRT_create()", "OpenCV (contrib)",
        "The same CSRT tracker from the cv2.legacy module, where some OpenCV versions keep the older tracking API.",
    ),
    "cv2.TrackerMIL_create": (
        "cv2.TrackerMIL_create()", "OpenCV",
        "Creates a MIL (Multiple Instance Learning) tracker. It is included in every OpenCV build, so it is the fallback. It learns the object's appearance online from bags of positive and negative samples.",
    ),
    ".init": (
        "tracker.init(frame, box)", "OpenCV Tracker method",
        "Starts the tracker on the first frame with the object's bounding box (x, y, width, height).",
    ),
    "cv2.VideoWriter": (
        "cv2.VideoWriter(filename, fourcc, fps, (width, height))", "OpenCV",
        "Creates a video file writer. Every frame written with .write() must be exactly width x height and BGR. Call .release() at the end to finish the file.",
    ),
    "cv2.VideoWriter_fourcc": (
        "cv2.VideoWriter_fourcc(*'mp4v')", "OpenCV",
        "Builds the FourCC code (four-character codec ID) for the video writer. 'mp4v' = MPEG-4 for .mp4 files. The * splits the string into 4 separate characters.",
    ),
    ".write": (
        "writer.write(frame)", "OpenCV VideoWriter method",
        "Appends one frame to the output video file.",
    ),
    ".update": (
        "tracker.update(frame)", "OpenCV Tracker method",
        "Finds the object in the new frame. Returns (success, box): success is False if the object was lost; box is the new (x, y, width, height).",
    ),
    "range": (
        "range(start, stop)", "Python built-in",
        "Produces the numbers start, start+1, ..., stop-1. Used to loop over consecutive pairs of tracked points to draw the path.",
    ),
    ".release": (
        "cap.release() / writer.release()", "OpenCV method",
        "Closes the video file. For VideoCapture it frees the file or camera; for VideoWriter it finishes writing so the .mp4 file is valid.",
    ),
    "plt.scatter": (
        "plt.scatter(x, y, color, s, label)", "Matplotlib",
        "Draws marker points at (x, y). s is the marker size. Used to mark the start (green) and end (red) of the trajectory.",
    ),
    "np.diff": (
        "np.diff(array, axis=0)", "NumPy",
        "Differences between consecutive rows: point[i+1] - point[i]. Gives the (dx, dy) movement between frames.",
    ),
    "np.sum": (
        "np.sum(array, axis)", "NumPy",
        "Adds up the values (along an axis if given). Used to compute dx^2 + dy^2 for each step, then the total distance.",
    ),
    "np.hypot": (
        "np.hypot(dx, dy)", "NumPy",
        "Returns sqrt(dx^2 + dy^2), the straight-line (Euclidean) distance. Used for the displacement from start to end.",
    ),
    "type": (
        "type(object).__name__", "Python built-in",
        "type() returns the class of an object, and __name__ is the class name, e.g. 'TrackerCSRT' or 'TrackerMIL'. Shows which tracker was actually used.",
    ),
    "float": (
        "float(value)", "Python built-in",
        "Converts a value (e.g. a NumPy number) to a normal Python decimal number for clean printing.",
    ),
    ".endswith": (
        "text.endswith((suffixes))", "Python string method",
        "Returns True if the text ends with any of the given suffixes. Used to decide whether the path is an image file (.jpg, .png, ...) or a video.",
    ),
    ".lower": (
        "text.lower()", "Python string method",
        "Returns the text in lower case, so '.JPG' and '.jpg' are treated the same.",
    ),
    "np.unique": (
        "np.unique(array)", "NumPy",
        "Returns the sorted unique values. Removes duplicate frame numbers when the video is very short.",
    ),
    "np.linspace": (
        "np.linspace(start, stop, num)", "NumPy",
        "Returns num evenly spaced numbers from start to stop (inclusive). Used to pick 5 frame numbers spread over the whole video.",
    ),
    ".set": (
        "cap.set(cv2.CAP_PROP_POS_FRAMES, index)", "OpenCV VideoCapture method",
        "Sets a video property. With CAP_PROP_POS_FRAMES it jumps to the given frame number, so the next .read() returns that frame.",
    ),
    "torch.cuda.is_available": (
        "torch.cuda.is_available()", "PyTorch",
        "Returns True if a CUDA GPU can be used. In Colab this is True when the runtime type is set to GPU (Runtime > Change runtime type).",
    ),
    "BlipProcessor.from_pretrained": (
        "BlipProcessor.from_pretrained(model_name)", "Hugging Face transformers",
        "Downloads (the first time) and loads the BLIP processor, which combines the image processor (resizes to 384x384, normalises and converts the image to a tensor) and the tokenizer (converts between text and token ids).",
    ),
    ".to": (
        "model.to(device) / inputs.to(device)", "PyTorch",
        "Moves the model weights or the input tensors to the CPU or the GPU ('cuda'). The model and its inputs must be on the same device.",
    ),
    "BlipForConditionalGeneration.from_pretrained": (
        "BlipForConditionalGeneration.from_pretrained(model_name)", "Hugging Face transformers",
        "Downloads and loads the pretrained BLIP captioning model 'Salesforce/blip-image-captioning-base': a Vision Transformer image encoder plus a Transformer text decoder that generates captions.",
    ),
    ".eval": (
        "model.eval()", "PyTorch",
        "Puts the model in evaluation (inference) mode, which turns off dropout so the outputs are consistent.",
    ),
    "processor": (
        "processor(images=image, return_tensors='pt')", "Hugging Face transformers",
        "Calling the processor prepares an image for the model: resize, normalise and convert it to a PyTorch tensor (return_tensors='pt'). Returns a dictionary containing pixel_values.",
    ),
    "Image.fromarray": (
        "Image.fromarray(array)", "Pillow (PIL)",
        "Converts a NumPy RGB array into a PIL Image object, which is the format the BLIP processor expects.",
    ),
    "torch.no_grad": (
        "with torch.no_grad():", "PyTorch",
        "Turns off gradient tracking inside the block. Gradients are only needed for training, so this saves memory and makes inference faster.",
    ),
    ".generate": (
        "model.generate(**inputs, max_new_tokens=30, num_beams=3, repetition_penalty=1.5, no_repeat_ngram_size=2)", "Hugging Face transformers",
        "Generates the caption token by token. **inputs passes pixel_values. max_new_tokens limits the length, num_beams=3 uses beam search (keeps the 3 best partial sentences), "
        "repetition_penalty discourages repeated words, and no_repeat_ngram_size=2 forbids repeating any pair of words. Returns a tensor of token ids.",
    ),
    ".decode": (
        "processor.decode(token_ids, skip_special_tokens=True)", "Hugging Face transformers",
        "Converts the generated token ids back into a readable sentence. skip_special_tokens=True removes tokens such as [SEP] and [PAD].",
    ),
    "set": (
        "set(list)", "Python built-in",
        "Makes a collection of the unique items (duplicates removed). max(set(captions), key=captions.count) checks each different caption once and picks the most frequent.",
    ),
    ".count": (
        "list.count(item)", "Python list method",
        "Returns how many times an item appears in the list. Passed as key= to max() to find the most common caption (majority vote).",
    ),
    ".join": (
        "'; '.join(list_of_strings)", "Python string method",
        "Joins a list of strings into one string, putting '; ' between them.",
    ),
    "dict.fromkeys": (
        "dict.fromkeys(list)", "Python built-in",
        "Creates a dictionary using the list items as keys. Because keys are unique and keep their order, it removes duplicate captions while keeping their original order.",
    ),
    "textwrap.fill": (
        "textwrap.fill(text, width)", "Python textwrap module",
        "Wraps long text onto several lines of at most width characters, so long captions fit above each image.",
    ),
    "plt.suptitle": (
        "plt.suptitle(text, fontsize)", "Matplotlib",
        "Writes one main title above the whole figure (above all subplots).",
    ),
}
