# records/graphics.py
import base64
import logging
from concurrent.futures import ThreadPoolExecutor

from .music_graphics import (  # adjust to wherever your module lives
    generate_compositional_range,
    generate_median_pitch,
    generate_tessitura,
)

logger = logging.getLogger(__name__)

# Each task spends its time waiting on a MuseScore subprocess, so threads are fine.
# Keep this near your CPU count, since each MuseScore process is heavy.
_executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="musescore")

_GENERATORS = {
    "range_img": generate_compositional_range,
    "tessitura_img": generate_tessitura,
    "median_img": generate_median_pitch,
}


def _to_data_uri(png_bytes):
    return "data:image/png;base64," + base64.b64encode(png_bytes).decode("ascii")


def attach_graphics(records, timeout=60):
    """Render all graphics for the given records concurrently and set them
    as attributes (range_img, tessitura_img, median_img) on each record."""
    futures = [
        (record, attr, _executor.submit(fn, record))
        for record in records
        for attr, fn in _GENERATORS.items()
    ]

    for record, attr, future in futures:
        try:
            setattr(record, attr, _to_data_uri(future.result(timeout=timeout)))
        except Exception:
            logger.exception("Graphic %s failed for record %s", attr, record.pk)
            setattr(record, attr, None)