TITLE = "Scene understanding and caption generation (BLIP)"
INPUT = "video or image"
DEFAULT_PATH = "/content/video.mp4"

AIM = "Understand the scene in a video (or a single image) and generate a natural-language caption using the pretrained BLIP image-captioning model."

STEPS = [
    "If the path is an image, read that one image. If it is a video, read 5 frames spread evenly over the video (cap.set jumps to a frame number).",
    "Convert the frames from BGR to RGB because BLIP expects RGB images.",
    "Load the BLIP processor (image preprocessing and tokenizer) and the BLIP captioning model. Use the GPU if one is available.",
    "For every frame: the processor turns the image into tensors, model.generate writes the caption with beam search, and processor.decode turns the token ids back into text.",
    "The caption that appears most often is used as the caption for the whole scene/video.",
    "Show the frames with their captions and print every caption.",
]

THEORY = [
    "Image captioning = vision (understand the scene) + language (describe it as a sentence).",
    "BLIP (Bootstrapping Language-Image Pre-training): a Vision Transformer (ViT) encodes the image, and a Transformer text decoder generates the caption one token at a time.",
    "Beam search (num_beams=3) keeps the 3 best partial sentences at every step instead of only the single best word, which gives better captions.",
    "repetition_penalty and no_repeat_ngram_size stop the model from repeating words or word pairs.",
    "Video captioning here works by captioning key frames and taking a majority vote (the mode) of the captions.",
    "The model weights are downloaded from the Hugging Face Hub the first time, so Colab needs internet access. A GPU runtime makes it faster but is not required.",
]

CODE = r'''import cv2
import numpy as np
import torch
import textwrap
import matplotlib.pyplot as plt
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

media_path = __PATH__

frames = []
if media_path.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff")):
    img = cv2.imread(media_path)
    if img is not None:
        frames.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
else:
    cap = cv2.VideoCapture(media_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    for index in np.unique(np.linspace(0, max(total_frames - 1, 0), 5).astype(int)):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(index))
        ret, frame = cap.read()
        if ret:
            frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    cap.release()
if len(frames) == 0:
    raise FileNotFoundError("Could not read any frames from " + media_path)

device = "cuda" if torch.cuda.is_available() else "cpu"
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)
model.eval()

captions = []
for frame in frames:
    inputs = processor(images=Image.fromarray(frame), return_tensors="pt").to(device)
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=30, num_beams=3, repetition_penalty=1.5, no_repeat_ngram_size=2)
    caption = processor.decode(output[0], skip_special_tokens=True)
    captions.append(caption)
    print("Frame", len(captions), "caption:", caption)

scene_caption = max(set(captions), key=captions.count)
print("\nScene caption:", scene_caption)
print("Everything described in the scene:", "; ".join(dict.fromkeys(captions)))

plt.figure(figsize=(5 * len(frames), 6))
for i, frame in enumerate(frames):
    plt.subplot(1, len(frames), i + 1)
    plt.imshow(frame)
    plt.title(textwrap.fill(captions[i], 30), fontsize=10)
    plt.axis("off")
plt.suptitle("Scene caption: " + scene_caption, fontsize=14)
plt.tight_layout()
plt.show()
'''
