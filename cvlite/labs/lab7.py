TITLE = "Object tracking in a video"
INPUT = "video"
DEFAULT_PATH = "/content/video.mp4"

AIM = "Track an object through a video with an OpenCV tracker (CSRT, or MIL if CSRT is not installed), draw its bounding box and path on every frame, save the result as a video and plot the trajectory."

STEPS = [
    "Open the video with cv2.VideoCapture and read the first frame.",
    "Shrink the frames so the longest side is at most 640 px (faster tracking), and read the FPS.",
    "Choose the object to track: a box in the centre of the first frame (x, y, width, height).",
    "Create the tracker: CSRT if available (it needs opencv-contrib), otherwise MIL, which ships with every OpenCV.",
    "Initialise the tracker with the first frame and the box. Open a cv2.VideoWriter for the output video.",
    "Loop over the frames: tracker.update gives the new box, the centre point is stored, and the box, centre and path are drawn. Write each frame to the output video.",
    "Release the video reader and writer, then show the first frame, the last frame and the full trajectory.",
    "Print the number of frames, lost frames, start/end points and the distance travelled.",
]

THEORY = [
    "Object tracking = finding the same object in consecutive frames. It is faster than running detection on every frame.",
    "CSRT (Discriminative Correlation Filter with Channel and Spatial Reliability): accurate and handles scale change and rotation, but slower.",
    "MIL (Multiple Instance Learning): trains a classifier online using 'bags' of positive samples near the object; robust to partial occlusion.",
    "KCF is a faster correlation-filter tracker. GOTURN, DaSiamRPN, Nano and ViT are deep-learning trackers.",
    "The trajectory is the list of centre points over time. Total distance = sum of the distances between consecutive centres. Displacement = straight-line distance from start to end.",
    "FourCC 'mp4v' is the four-character code for the MPEG-4 codec used to write the .mp4 file.",
]

CODE = r'''import cv2
import numpy as np
import matplotlib.pyplot as plt

video_path = __PATH__

cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()
if not ret:
    raise FileNotFoundError("Could not read the video at " + video_path)

scale = min(1.0, 640 / max(frame.shape[:2]))
width = int(frame.shape[1] * scale)
height = int(frame.shape[0] * scale)
frame = cv2.resize(frame, (width, height))
fps = cap.get(cv2.CAP_PROP_FPS)
if not fps > 0:
    fps = 25

box = (width // 3, height // 3, width // 3, height // 3)
x, y, bw, bh = box
first_frame = frame.copy()
cv2.rectangle(first_frame, (x, y), (x + bw, y + bh), (0, 255, 0), 3)

if hasattr(cv2, "TrackerCSRT_create"):
    tracker = cv2.TrackerCSRT_create()
elif hasattr(cv2, "legacy") and hasattr(cv2.legacy, "TrackerCSRT_create"):
    tracker = cv2.legacy.TrackerCSRT_create()
else:
    tracker = cv2.TrackerMIL_create()
tracker.init(frame, box)

writer = cv2.VideoWriter("tracking_output.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))
writer.write(first_frame)

points = [(x + bw // 2, y + bh // 2)]
frame_count = 1
lost_count = 0
last_frame = first_frame

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (width, height))
    frame_count += 1
    success, box = tracker.update(frame)
    if success:
        x, y, bw, bh = [int(v) for v in box]
        centre = (x + bw // 2, y + bh // 2)
        points.append(centre)
        cv2.rectangle(frame, (x, y), (x + bw, y + bh), (0, 255, 0), 2)
        cv2.circle(frame, centre, 4, (0, 0, 255), -1)
    else:
        lost_count += 1
        cv2.putText(frame, "Tracking lost", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    for i in range(1, len(points)):
        cv2.line(frame, points[i - 1], points[i], (0, 255, 255), 2)
    writer.write(frame)
    last_frame = frame

cap.release()
writer.release()

xs = [p[0] for p in points]
ys = [p[1] for p in points]

plt.figure(figsize=(18, 6))
plt.subplot(1, 3, 1)
plt.imshow(cv2.cvtColor(first_frame, cv2.COLOR_BGR2RGB))
plt.title("First frame (object to track)")
plt.axis("off")
plt.subplot(1, 3, 2)
plt.imshow(cv2.cvtColor(last_frame, cv2.COLOR_BGR2RGB))
plt.title("Last frame with tracking path")
plt.axis("off")
plt.subplot(1, 3, 3)
plt.imshow(cv2.cvtColor(first_frame, cv2.COLOR_BGR2RGB))
plt.plot(xs, ys, color="cyan", linewidth=2)
plt.scatter(xs[0], ys[0], color="green", s=80, label="Start")
plt.scatter(xs[-1], ys[-1], color="red", s=80, label="End")
plt.legend()
plt.title("Trajectory")
plt.axis("off")
plt.tight_layout()
plt.show()

steps = np.diff(np.array(points), axis=0)
distance = np.sum(np.sqrt(np.sum(steps ** 2, axis=1)))
displacement = np.hypot(xs[-1] - xs[0], ys[-1] - ys[0])

print("Tracker used:", type(tracker).__name__)
print("Frames processed:", frame_count)
print("Frames tracked:", len(points))
print("Frames lost:", lost_count)
print("Start point:", points[0])
print("End point:", points[-1])
print("Total distance travelled (px):", round(float(distance), 2))
print("Displacement start to end (px):", round(float(displacement), 2))
print("Output video saved as tracking_output.mp4")
'''
