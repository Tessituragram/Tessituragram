from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, Http404, FileResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import get_list_or_404

from .columns import AVAILABLE_COLUMNS, DEFAULT_TABLE_COLUMNS, SIMPLE_SEARCH_COLUMNS
from .models import Record
from .forms import AdvancedSearchForm, SimpleSearchForm
from .filtering import get_filtered_records
from urllib.parse import urlencode
from .music_graphics import (
    generate_compositional_range,
    generate_tessitura,
    generate_median_pitch,
)

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


@staff_member_required
def delete_record(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied

    record = get_object_or_404(Record, pk=pk, is_deleted=False)

    if request.method == "POST":
        records = Record.objects.filter(
            submission_group=record.submission_group,
            is_deleted=False
        )

        for item in records:
            item.is_deleted = True
            item.deleted_at = timezone.now()
            item.deleted_by = request.user
            item.save()

        return redirect("records:soloistic_search")

    return render(request, "records/delete_confirm.html", {"record": record})


@login_required
def soloistic_search(request):
    mode = request.GET.get("mode", "simple")

    if mode not in {"simple", "advanced"}:
        mode = "simple"

    records, search_form, sort = get_filtered_records(
        request,
        mode=mode,
    )

    # =========================================================
    # Pagination
    # =========================================================

    total_count = records.count()

    paginator = Paginator(records, 25)

    page_number = request.GET.get("page", 1)

    page_obj = paginator.get_page(page_number)

    # =========================================================
    # Query strings
    # =========================================================

    querydict = request.GET.copy()

    querydict.pop("page", None)

    active_filters = [
        (key, value)
        for key, values in querydict.lists()
        for value in values
        if value
    ]

    querystring = urlencode(active_filters)

    search_querystring = urlencode(
        [
            (key, value)
            for key, value in active_filters
            if key != "sort"
        ]
    )

    # =========================================================
    # Columns
    # =========================================================

    if mode == "simple":

        selected_columns = (
            request.GET.getlist("cols")
            or SIMPLE_SEARCH_COLUMNS
        )

        all_columns = [
            column
            for column in AVAILABLE_COLUMNS
            if column[0] in SIMPLE_SEARCH_COLUMNS
        ]

    else:

        selected_columns = (
            request.GET.getlist("cols")
            or DEFAULT_TABLE_COLUMNS
        )

        all_columns = AVAILABLE_COLUMNS

    display_columns = [
        (key, label, sort_field)
        for key, label, sort_field, _ in all_columns
        if key in selected_columns
    ]

    return render(
        request,
        "records/soloistic_search.html",
        {
            "mode": mode,
            "page_obj": page_obj,
            "total_count": total_count,
            "current_sort": sort,
            "search_form": search_form,
            "querystring": querystring,
            "search_querystring": search_querystring,
            "active_filters": active_filters,
            "all_columns": all_columns,
            "selected_columns": selected_columns,
            "display_columns": display_columns,
        },
    )


@login_required
def record_detail(request, group_id):
    group_records = list(Record.objects.filter(submission_group=group_id))
    if not group_records:
        raise Http404

    primary = group_records[0]
    is_visible = primary.status == "public" or primary.submitted_by == request.user
    if primary.is_deleted and not request.user.is_staff:
        raise PermissionDenied
    if not is_visible and not request.user.is_staff:
        raise PermissionDenied

    clef_panels = {r.clef_range: r for r in group_records}

    if request.method == "POST" and request.user.is_staff:
        new_status = request.POST.get("status")
        if new_status in dict(Record.STATUS_CHOICES):
            for r in group_records:
                r.status = new_status
                if new_status == "public":
                    r.approval_at = timezone.now()
                    r.approval_by = request.user
                r.save()
            return redirect("records:record_detail", group_id=group_id)

    return render(request, "records/record_detail.html", {
        "record": primary,
        "clef_panels": clef_panels,
        "bass_record": clef_panels.get("Bass"),
        "treble_record": clef_panels.get("Treble"),
    })


@staff_member_required
def midi_download(request, pk):
    record = get_object_or_404(Record, pk=pk)
    if not record.midi_file:
        raise Http404
    return FileResponse(
        record.midi_file.open("rb"),
        as_attachment=True,
        filename=record.midi_file.name.split("/")[-1],
    )


@login_required
def deleted_list(request):
    if not request.user.is_staff:
        raise PermissionDenied

    records = Record.objects.filter(is_deleted=True).order_by("-deleted_at")
    return render(request, "records/deleted_list.html", {"records": records})

@login_required
def reinstate_record(request, submission_group):
    if not request.user.is_staff:
        raise PermissionDenied

    records = get_list_or_404(Record, submission_group=submission_group, is_deleted=True)
    record = records[0]

    if request.method == "POST":
        for item in records:
            item.is_deleted = False
            item.deleted_at = None
            item.deleted_by = None
            item.save()

        return redirect("records:deleted_list")

    return render(request, "records/reinstate_confirm.html", {"record": record})

GRAPHIC_GENERATORS = {
    "range": generate_compositional_range,
    "tessitura": generate_tessitura,
    "median": generate_median_pitch,
}


@login_required
def record_graphic(request, submission_group, clef, graphic_type):
    generator = GRAPHIC_GENERATORS.get(graphic_type)

    if generator is None:
        raise Http404

    record = get_object_or_404(
        Record,
        submission_group=submission_group,
        clef_range=clef,
    )

    is_visible = (
        (record.status == "public" and not record.is_deleted)
        or record.submitted_by == request.user
        or request.user.is_staff
    )

    if not is_visible:
        raise PermissionDenied

    image_data = generator(record)

    return HttpResponse(
        image_data,
        content_type="image/png",
    )