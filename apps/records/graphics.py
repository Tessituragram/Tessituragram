# records/graphics.py
import hashlib
import logging
from filelock import FileLock
from pathlib import Path

from django.conf import settings

from .music_graphics import (
    generate_compositional_range,
    generate_median_pitch,
    generate_tessitura,
)

logger = logging.getLogger(__name__)

GENERATORS = {
    "range": generate_compositional_range,
    "tessitura": generate_tessitura,
    "median": generate_median_pitch,
}

CACHE_DIR = Path(settings.MEDIA_ROOT) / "graphics_cache"
LOCK_PATH = CACHE_DIR / ".render.lock"


def _cache_path(record, kind):
    # Include something that changes when the record's data changes.
    # Swap in whatever field you have (updated_at, a file hash, etc.).
    stamp = str(getattr(record, "updated_at", ""))
    key = hashlib.sha1(f"{record.pk}:{kind}:{stamp}".encode()).hexdigest()[:12]
    return CACHE_DIR / f"{record.pk}_{kind}_{key}.png"


def get_graphic_path(record, kind):
    """Return the cached PNG path, rendering it if needed.
    A file lock means only one MuseScore render runs at a time
    across all Gunicorn workers."""
    path = _cache_path(record, kind)
    if path.exists():
        return path

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with FileLock(str(LOCK_PATH), timeout=120):
        if path.exists():  # another worker finished it while we waited
            return path
        png_bytes = GENERATORS[kind](record)
        tmp = path.with_suffix(".tmp")
        tmp.write_bytes(png_bytes)
        tmp.replace(path)
    return path