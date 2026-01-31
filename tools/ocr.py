"""Lightweight OCR helper (best-effort).

This module tries to use pytesseract if available; otherwise it returns an empty
string and logs a warning. For production, ensure tesseract is installed or use
an OCR cloud provider.
"""
import logging

logger = logging.getLogger(__name__)

try:
    import pytesseract
    from PIL import Image

    def ocr_image(path: str) -> str:
        img = Image.open(path)
        return pytesseract.image_to_string(img)

except Exception:  # pragma: no cover - optional runtime dependency

    def ocr_image(path: str) -> str:
        logger.warning("pytesseract not available; returning empty OCR output for %s", path)
        return ""
