# Dongle Streamlit MVP

Quick one-day sprint prototype for a smart Vietnamese cash wallet.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## What is included

- Bottom-style tab navigation using Streamlit radio + CSS
- Local wallet storage in `storage/wallet.json`
- Camera/upload scan screen
- Replaceable AI wrapper in `model.py`
- Manual wallet editing
- Payment assistant
- Currency explorer and learn content
- Placeholder SVG banknote illustrations in `assets/`

## Integrating the Colab AI

Edit `model.py` and replace:

```python
def predict_banknotes(image_file):
    return {500000: 1, 200000: 1, 50000: 2}
```

with your inference code. Keep the return format:

```python
{500000: 1, 200000: 2, 100000: 0, ...}
```

`image_file` is a Streamlit UploadedFile from either `st.camera_input` or `st.file_uploader`. You can read it as bytes with:

```python
image_bytes = image_file.getvalue()
```

or open it with Pillow:

```python
from PIL import Image
img = Image.open(image_file)
```

## Replacing note illustrations

Replace the SVGs in `assets/` with your team's simplified banknote illustrations. Keep the filenames like:

- `note_500000.svg`
- `note_200000.svg`
- `note_100000.svg`
- etc.

PNG/JPG also works, but update `note_asset()` in `app.py` if you change extensions.
