from django.db.models import Q
from .models import Record
from .forms import AdvancedSearchForm

NUMERIC_RANGE_FIELDS = [
    "q1_freq",
    "q3_freq",
    "median_freq",
    "min_freq",
    "max_freq",
    "cycle_dose",
    "time_dose",
    "rest_time",
    "total_time",
    "hvhp_time_dose",
    "hvmp_time_dose",
    "hvlp_time_dose",
    "mvhp_time_dose",
    "mvmp_time_dose",
    "mvlp_time_dose",
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


def get_filtered_records(request):
    records = Record.objects.filter(status="public").exclude(is_deleted=True)

    search_form = AdvancedSearchForm(request.GET or None)
    if search_form.is_valid():
        data = search_form.cleaned_data

        if data.get("title"):
            records = records.filter(title__icontains=data["title"])
        if data.get("composer"):
            records = records.filter(composer__icontains=data["composer"])
        if data.get("author"):
            records = records.filter(author__icontains=data["author"])
        if data.get("style"):
            records = records.filter(style=data["style"])
        if data.get("clef_range"):
            records = records.filter(clef_range=data["clef_range"])
        if data.get("submitter"):
            submitter_query = data["submitter"]
            records = records.filter(
                Q(submitted_by__first_name__icontains=submitter_query)
                | Q(submitted_by__last_name__icontains=submitter_query)
            )

        for field in NUMERIC_RANGE_FIELDS:
            min_val = data.get(f"{field}_min")
            max_val = data.get(f"{field}_max")
            if min_val is not None:
                records = records.filter(**{f"{field}__gte": min_val})
            if max_val is not None:
                records = records.filter(**{f"{field}__lte": max_val})

    sort = request.GET.get("sort", "-created_at")
    if sort == "submitter":
        records = records.order_by(
            "submitted_by__first_name", "submitted_by__last_name"
        )
    elif sort == "-submitter":
        records = records.order_by(
            "-submitted_by__first_name", "-submitted_by__last_name"
        )
    elif sort in ALLOWED_SORTS:
        records = records.order_by(sort)

    return records, search_form, sort
