# Adapting a Google Colab Model to `model.py`

This guide explains how to move a working Google Colab banknote detector into the Dongle app.

The app does not need the whole notebook. It only needs one function in `model.py`:

```python
def predict_banknotes(image_file) -> dict[int, int]:
    return {500000: 1, 200000: 0, 100000: 2}
```

The keys are Vietnamese dong denominations. The values are how many notes of each denomination were found in the uploaded image.

## 1. Find the Important Parts of the Colab Notebook

In your Colab file, identify these pieces:

- The model loading code.
- The image preprocessing code.
- The prediction/inference code.
- The code that turns model output into a class label.
- The list of class names or labels.

You usually do not need:

- Training loops.
- Dataset download code.
- Plotting cells.
- Evaluation charts.
- Notebook-only display code like `cv2_imshow`, `plt.imshow`, or `files.upload()`.

## 2. Export the Trained Model

Save the trained model from Colab into a file that can be loaded locally.

For TensorFlow/Keras:

```python
model.save("banknote_model.keras")
```

or:

```python
model.save("banknote_model.h5")
```

For PyTorch:

```python
torch.save(model.state_dict(), "banknote_model.pt")
```

For YOLO/Ultralytics:

```python
model.export()
```

or use the generated `best.pt` file.

Then download the model file from Colab and put it somewhere in this project, for example:

```text
models/banknote_model.keras
```

If the `models/` folder does not exist yet, create it.

## 3. Add Required Libraries to `requirements.txt`

Check which libraries your Colab model uses.

Common examples:

```text
tensorflow
torch
torchvision
ultralytics
opencv-python
numpy
```

Only add the libraries your model actually needs. The app already includes:

```text
streamlit
pillow
streamlit-option-menu
```

After editing `requirements.txt`, install the dependencies locally:

```bash
pip install -r requirements.txt
```

## 4. Keep the App Function Signature

Do not change the function name or input in `model.py`.

Keep this shape:

```python
def predict_banknotes(image_file) -> Dict[int, int]:
    ...
```

`image_file` comes from Streamlit. It is the uploaded/camera image from `st.file_uploader()` or `st.camera_input()`.

You can open it with Pillow:

```python
from PIL import Image

image = Image.open(image_file).convert("RGB")
```

Or read the raw bytes:

```python
image_bytes = image_file.getvalue()
```

## 5. Move Model Loading Outside the Function

Load the model once at the top of `model.py`, not every time the user clicks the button.

Good:

```python
MODEL = load_model("models/banknote_model.keras")


def predict_banknotes(image_file):
    ...
```

Avoid:

```python
def predict_banknotes(image_file):
    model = load_model("models/banknote_model.keras")
    ...
```

Loading inside the function makes every prediction slow.

## 6. Convert Notebook Image Preprocessing

Copy the preprocessing steps from Colab, but replace notebook upload code with `Image.open(image_file)`.

Example:

```python
from PIL import Image
import numpy as np


def preprocess_image(image_file):
    image = Image.open(image_file).convert("RGB")
    image = image.resize((224, 224))
    array = np.array(image) / 255.0
    array = np.expand_dims(array, axis=0)
    return array
```

Make sure these details match your Colab notebook:

- Image size.
- Color mode, usually RGB.
- Normalization, such as `/ 255.0`.
- Batch dimension, often `np.expand_dims(..., axis=0)`.

## 7. Map Model Classes to Denominations

The app needs integer denominations, not text labels.

Create a mapping in `model.py`:

```python
CLASS_TO_DENOMINATION = {
    "1000": 1000,
    "2000": 2000,
    "5000": 5000,
    "10000": 10000,
    "20000": 20000,
    "50000": 50000,
    "100000": 100000,
    "200000": 200000,
    "500000": 500000,
}
```

If your Colab labels look different, adapt the keys:

```python
CLASS_TO_DENOMINATION = {
    "note_1000": 1000,
    "note_2000": 2000,
    "note_5000": 5000,
}
```

## 8. Return Counts, Not Raw Predictions

The app expects a dictionary like this:

```python
{
    500000: 1,
    200000: 0,
    100000: 2,
    50000: 0,
}
```

For a single-label classifier, return one detected note:

```python
return {denomination: 1}
```

For an object detector, count every detected note:

```python
counts = {}

for detection in detections:
    label = detection["label"]
    denomination = CLASS_TO_DENOMINATION[label]
    counts[denomination] = counts.get(denomination, 0) + 1

return counts
```

## 9. Example `model.py` for a Keras Classifier

```python
from __future__ import annotations

from pathlib import Path
from typing import Dict, BinaryIO

import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model


BASE = Path(__file__).parent
MODEL_PATH = BASE / "models" / "banknote_model.keras"

MODEL = load_model(MODEL_PATH)

CLASS_NAMES = [
    "1000",
    "2000",
    "5000",
    "10000",
    "20000",
    "50000",
    "100000",
    "200000",
    "500000",
]

CLASS_TO_DENOMINATION = {
    "1000": 1000,
    "2000": 2000,
    "5000": 5000,
    "10000": 10000,
    "20000": 20000,
    "50000": 50000,
    "100000": 100000,
    "200000": 200000,
    "500000": 500000,
}


def preprocess_image(image_file: BinaryIO) -> np.ndarray:
    image = Image.open(image_file).convert("RGB")
    image = image.resize((224, 224))
    array = np.array(image) / 255.0
    return np.expand_dims(array, axis=0)


def predict_banknotes(image_file: BinaryIO) -> Dict[int, int]:
    image = preprocess_image(image_file)
    predictions = MODEL.predict(image)
    class_index = int(np.argmax(predictions[0]))
    class_name = CLASS_NAMES[class_index]
    denomination = CLASS_TO_DENOMINATION[class_name]
    return {denomination: 1}
```

## 10. Example `model.py` for an Object Detector

Object detectors are better if one photo can contain multiple banknotes.

The exact code depends on your model library, but the final part should always build counts:

```python
from __future__ import annotations

from pathlib import Path
from typing import Dict, BinaryIO

from PIL import Image
from ultralytics import YOLO


BASE = Path(__file__).parent
MODEL_PATH = BASE / "models" / "best.pt"

MODEL = YOLO(MODEL_PATH)

CLASS_TO_DENOMINATION = {
    "1000": 1000,
    "2000": 2000,
    "5000": 5000,
    "10000": 10000,
    "20000": 20000,
    "50000": 50000,
    "100000": 100000,
    "200000": 200000,
    "500000": 500000,
}


def predict_banknotes(image_file: BinaryIO) -> Dict[int, int]:
    image = Image.open(image_file).convert("RGB")
    results = MODEL(image)

    counts: Dict[int, int] = {}
    result = results[0]

    for box in result.boxes:
        class_index = int(box.cls[0])
        confidence = float(box.conf[0])

        if confidence < 0.5:
            continue

        label = result.names[class_index]
        denomination = CLASS_TO_DENOMINATION[label]
        counts[denomination] = counts.get(denomination, 0) + 1

    return counts
```

## 11. Test the Function Without Streamlit

Before using the Scan tab, test `model.py` directly.

Create a small temporary test file or run this in Python:

```python
from pathlib import Path

from model import predict_banknotes


with Path("test-banknote.jpg").open("rb") as image_file:
    print(predict_banknotes(image_file))
```

Expected output:

```python
{50000: 1}
```

or:

```python
{50000: 2, 20000: 1}
```

## 12. Test Inside the App

Run the app:

```bash
streamlit run app.py
```

Then:

1. Open the Scan tab.
2. Upload or take a banknote photo.
3. Click Run AI detection.
4. Confirm that the detected notes appear.
5. Click Add to wallet.
6. Check that the Wallet total updates.

## 13. Common Problems

### The app says no module named something

Add that library to `requirements.txt`, then run:

```bash
pip install -r requirements.txt
```

### The prediction is always wrong

Check that your local preprocessing matches Colab exactly:

- Same image size.
- Same RGB/BGR color order.
- Same normalization.
- Same class order.

### The app crashes when reading the image

Use Pillow:

```python
image = Image.open(image_file).convert("RGB")
```

If you previously read from `image_file`, reset it before reading again:

```python
image_file.seek(0)
```

### The app shows the wrong denomination

The class order is probably different from Colab. Print the predicted class index and compare it with your original `CLASS_NAMES` list.

### Multiple notes are counted as one

That usually means the Colab model is a classifier, not an object detector. A classifier normally predicts one label for the whole image. To detect multiple banknotes in one image, use an object detection model.

## Final Checklist

- The trained model file is inside the project.
- `requirements.txt` includes the model library.
- `model.py` loads the model once.
- `predict_banknotes(image_file)` still exists.
- The function returns `Dict[int, int]`.
- Class labels are mapped to VND denominations.
- A local image test works before testing in Streamlit.
