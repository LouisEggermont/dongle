from __future__ import annotations
from typing import Dict, BinaryIO

# Replace this file with your Colab model wrapper.
# Expected output format: {500000: 1, 200000: 2, ...}


def predict_banknotes(image_file: BinaryIO) -> Dict[int, int]:
    """Temporary demo predictor.

    Hook your working Colab AI here. Keep the function signature stable so app.py
    does not need to change. For the sprint demo, this returns a plausible result
    after an image is captured/uploaded.
    """
    _ = image_file.getvalue() if hasattr(image_file, "getvalue") else image_file.read()
    return {500000: 1, 200000: 1, 50000: 2}
