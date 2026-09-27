from django.db.models import Q
from .models import Record
from .forms import AdvancedSearchForm, SimpleSearchForm

NUMERIC_RANGE_FIELDS = [
    # Musical metrics
    "q1_freq",
    "q3_freq",
    "median_freq",
    "min_freq",
    "max_freq",

    # Timing
    "cycle_dose",
    "time_dose",
    "rest_time",
    "total_time",

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

        # =====================================================
        # Numeric fields
        #
        # Simple Search has the five pitch metrics.
        # Advanced Search has those plus timing/passaggio.
        # NUMERIC_RANGE_FIELDS can therefore be used for both.
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

    # =========================================================
    # Simple Search:
    #
    # Filter first, THEN collapse the matching Bass/Treble
    # records into one result per submission.
    #
    # This means either clef can satisfy the search.
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

    if sort == "submitter":

        records = records.order_by(
            "submitted_by__first_name",
            "submitted_by__last_name",
        )

    elif sort == "-submitter":

        records = records.order_by(
            "-submitted_by__first_name",
            "-submitted_by__last_name",
        )

    elif sort in ALLOWED_SORTS:

        records = records.order_by(sort)

    return records, search_form, sort
