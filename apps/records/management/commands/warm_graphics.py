# apps/records/management/commands/warm_graphics.py
import logging
from django.core.management.base import BaseCommand
from filelock import FileLock, Timeout

from apps.records.models import Record
from apps.records.graphics import CACHE_DIR, GENERATORS, _cache_path, get_graphic_path

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Render any missing graphics for pending and public records."

    def handle(self, *args, **opts):
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        failed = set()
        try:
            with FileLock(str(CACHE_DIR / ".sweep.lock"), timeout=0):
                while True:
                    todo = [
                        (r, k)
                        for r in Record.objects.filter(status__in=["pending", "public"])
                        for k in GENERATORS
                        if (r.pk, k) not in failed and not _cache_path(r, k).exists()
                    ]
                    if not todo:
                        break
                    for r, k in todo:
                        try:
                            get_graphic_path(r, k)
                        except Exception:
                            logger.exception("Warm failed: %s %s", r.pk, k)
                            failed.add((r.pk, k))
        except Timeout:
            pass  # another sweep is running and will pick up new records