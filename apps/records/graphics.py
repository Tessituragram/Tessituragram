# records/graphics.py
import hashlib
import logging
from filelock import FileLock
from pathlib import Path
import subprocess
import sys
from django.conf import settings

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
    stamp = "|".join(str(getattr(record, f, "")) for f in (
        "clef_range", "min_freq_note", "min_freq_octave",
        "max_freq_note", "max_freq_octave",
        "q1_pitch", "q1_octave", "q3_pitch", "q3_octave",
        "median_pitch", "median_octave",
    ))
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

def queue_graphics():
    subprocess.Popen(
        [sys.executable, str(settings.BASE_DIR / "manage.py"), "warm_graphics"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
        close_fds=True,
    )