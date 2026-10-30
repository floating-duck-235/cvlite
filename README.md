# cvlite

Ready-to-run Google Colab code for 8 computer vision topics, with an explanation of every function each one uses.

## Install in Google Colab

1. Upload `cvlite-1.0.0-py3-none-any.whl` (from the `dist` folder) using the Files panel on the left.
2. Run:

```python
!pip install -q /content/cvlite-1.0.0-py3-none-any.whl
import cvlite
```

No other installs are needed. OpenCV, NumPy, Matplotlib, scikit-image, pandas, PyTorch and transformers are already in Colab.

## Use

```python
cvlite.labs()                          # list the 8 labs
cvlite.code(3, "/content/photo.jpg")   # print ready-to-run code for lab 3 using your image
cvlite.explain(3)                      # aim, steps, theory and every function used, explained
cvlite.run(3, "/content/photo.jpg")    # run lab 3 straight away
cvlite.get_code(3, "/content/photo.jpg")  # the code as a string
cvlite.usage()                         # this help
```

Copy the printed code into a new Colab cell and run it.

| Lab | Input | Topic |
|-----|-------|-------|
| 1 | image | Colour models (RGB, Gray, HSV, LAB, YCrCb, CMY, CMYK) and colour maps |
| 2 | image | Histogram equalization, CLAHE, CDF, colour equalization |
| 3 | image | Edge detection: Sobel, Prewitt, Roberts, Laplacian, Canny |
| 4 | image | ROI identification (Otsu, morphology, contours) |
| 5 | image | Segmentation: Otsu, K-means, Watershed |
| 6 | image | Region analysis (watershed segmentation): shape, PCA orientation, GLCM texture, description, CSV |
| 7 | video | Object tracking (CSRT, or MIL if CSRT is missing) with trajectory |
| 8 | video or image | Scene caption with BLIP (needs internet; a GPU is optional) |

Lab 6 writes `region_measurements.csv` and lab 7 writes `tracking_output.mp4` into the current folder (`/content` in Colab).
