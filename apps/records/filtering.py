from django.db.models import Q
from .models import Record
from .forms import AdvancedSearchForm, SimpleSearchForm
from .columns import AVAILABLE_COLUMNS

NUMERIC_RANGE_FIELDS = [
    # Musical metrics
    "q1_freq",
    "q3_freq",
    "median_freq",
    "min_freq",
    "max_freq",

    # Timing
    "cycle_dose",

    # High voice passaggio
    "hvhp_time_dose",
    "hvmp_time_dose",
    "hvlp_time_dose",

    # Medium voice passaggio
    "mvhp_time_dose",
    "mvmp_time_dose",
    "mvlp_time_dose",

    # Low voice passaggio
    "lvhp_time_dose",
    "lvmp_time_dose",
    "lvlp_time_dose",
]

# time_dose, rest_time, total_time are now built from minutes+seconds
# pairs on the Advanced Search form, so they're handled separately
# below instead of through the generic float min/max loop.
TIME_RANGE_FIELDS = [
    "time_dose",
    "rest_time",
    "total_time",
]

ALLOWED_SORTS = {
    "title",
    "-title",
    "composer",
    "-composer",
    "author",
    "-author",
    "clef_range",
    "-clef_range",
    "q1_freq",
    "-q1_freq",
    "created_at",
    "-created_at",
    "submitter",
    "-submitter",
}

NOTE_INDEX = {
    "C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5,
    "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11,
}

import math

INDEX_TO_NOTE = {v: k for k, v in NOTE_INDEX.items()}


def freq_to_note_octave(freq):
    """
    Converts a stored Hz value to the nearest (note, octave) pair,
    using the same equal-temperament tuning as _pitch_to_freq_band.
    Returns None if freq is None.
    """
    if freq is None:
        return None
    midi = round(69 + 12 * math.log2(freq / 440.0))
    return INDEX_TO_NOTE[midi % 12], midi // 12 - 1


def _midi_number(note, octave):
    return 12 * (int(octave) + 1) + NOTE_INDEX[note]


def _freq_from_midi(midi_number):
    return 440.0 * (2 ** ((midi_number - 69) / 12))


def _pitch_to_freq_band(note, octave):
    midi = _midi_number(note, octave)
    low_hz = round(_freq_from_midi(midi), 1)
    high_hz = round(_freq_from_midi(midi + 1), 1)
    return low_hz, high_hz


def _minutes_seconds_to_total(minutes, seconds):
    if minutes is None and seconds is None:
        return None
    return (minutes or 0) * 60 + (seconds or 0)


def apply_record_sort(records, sort):
    allowed_sort_fields = {
        sort_field
        for _, _, sort_field, _ in AVAILABLE_COLUMNS
        if sort_field
    }

    if sort == "submitter":

        return records.order_by(
            "submitted_by__first_name",
            "submitted_by__last_name",
        )

    elif sort == "-submitter":

        return records.order_by(
            "-submitted_by__first_name",
            "-submitted_by__last_name",
        )

    elif sort.lstrip("-") in allowed_sort_fields:

        return records.order_by(sort)

    return records


def get_filtered_records(request, mode="advanced"):
    records = (
        Record.objects
        .filter(status="public")
        .exclude(is_deleted=True)
    )

    if mode == "simple":
        search_form = SimpleSearchForm(request.GET or None)
    else:
        search_form = AdvancedSearchForm(request.GET or None)

    if search_form.is_valid():
        data = search_form.cleaned_data

        # =====================================================
        # General fields shared by both search modes
        # =====================================================

        if data.get("title"):
            records = records.filter(
                title__icontains=data["title"]
            )

        if data.get("composer"):
            records = records.filter(
                composer__icontains=data["composer"]
            )

        if data.get("author"):
            records = records.filter(
                author__icontains=data["author"]
            )

        if data.get("larger_work"):
            records = records.filter(
                larger_work__icontains=data["larger_work"]
            )

        if data.get("style"):
            records = records.filter(
                style=data["style"]
            )

        if data.get("submitter"):
            submitter_query = data["submitter"]

            records = records.filter(
                Q(
                    submitted_by__first_name__icontains=submitter_query
                )
                |
                Q(
                    submitted_by__last_name__icontains=submitter_query
                )
            )

        # =====================================================
        # Advanced-only general fields
        # =====================================================

        if mode == "advanced":

            if data.get("initial_key"):
                records = records.filter(
                    initial_key=data["initial_key"]
                )

            if data.get("style_other"):
                records = records.filter(
                    style_other__icontains=data["style_other"]
                )

            if data.get("clef_range"):
                records = records.filter(
                    clef_range=data["clef_range"]
                )

            if data.get("performing_forces"):
                records = records.filter(
                    performing_forces=data["performing_forces"]
                )

            if data.get("voice_part"):
                records = records.filter(
                    voice_part=data["voice_part"]
                )

            # =================================================
            # Tessitura pitch fields (note + octave -> Hz band)
            #
            # Each is a single pitch pick, not a min/max range,
            # so we match records whose stored frequency falls
            # within that semitone's band.
            # =================================================

            pitch_field_map = {
                "tessitura_bottom": "q1_freq",
                "median_pitch": "median_freq",
                "tessitura_top": "q3_freq",
            }

            for form_prefix, model_field in pitch_field_map.items():
                note = data.get(f"{form_prefix}_note")
                octave = data.get(f"{form_prefix}_octave")

                if note and octave:
                    low_hz, high_hz = _pitch_to_freq_band(note, octave)
                    records = records.filter(**{
                        f"{model_field}__gte": low_hz,
                        f"{model_field}__lt": high_hz,
                    })

        # =====================================================
        # Numeric fields (plain float min/max ranges)
        #
        # Simple Search has the five pitch metrics.
        # Advanced Search has those plus cycle dose/passaggio.
        # =====================================================

        for field in NUMERIC_RANGE_FIELDS:

            min_val = data.get(f"{field}_min")
            max_val = data.get(f"{field}_max")

            if min_val is not None:
                records = records.filter(
                    **{f"{field}__gte": min_val}
                )

            if max_val is not None:
                records = records.filter(
                    **{f"{field}__lte": max_val}
                )

        # =====================================================
        # Timing fields built from minutes + seconds pairs
        # (Advanced Search only)
        # =====================================================

        if mode == "advanced":

            for field in TIME_RANGE_FIELDS:

                min_val = _minutes_seconds_to_total(
                    data.get(f"{field}_min_minutes"),
                    data.get(f"{field}_min_seconds"),
                )
                max_val = _minutes_seconds_to_total(
                    data.get(f"{field}_max_minutes"),
                    data.get(f"{field}_max_seconds"),
                )

                if min_val is not None:
                    records = records.filter(
                        **{f"{field}__gte": min_val}
                    )

                if max_val is not None:
                    records = records.filter(
                        **{f"{field}__lte": max_val}
                    )

    # =========================================================
    # Simple Search: collapse Bass/Treble into one result
    # =========================================================

    if mode == "simple":

        representative_ids = list(
            records
            .order_by("submission_group", "-created_at")
            .distinct("submission_group")
            .values_list("id", flat=True)
        )

        records = (
            Record.objects
            .filter(id__in=representative_ids)
            .select_related("submitted_by")
        )

    # =========================================================
    # Sorting
    # =========================================================

    sort = request.GET.get("sort", "-created_at")

    records = apply_record_sort(records, sort)

    return records, search_form, sort