from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .columns import AVAILABLE_COLUMNS, DEFAULT_TABLE_COLUMNS
from .models import Record
from .forms import AdvancedSearchForm
from .filtering import get_filtered_records
from urllib.parse import urlencode


NUMERIC_RANGE_FIELDS = [
    "q1_freq", "q3_freq", "median_freq", "min_freq", "max_freq",
    "cycle_dose", "time_dose", "rest_time", "total_time",
    "hvhp_time_dose", "hvmp_time_dose", "hvlp_time_dose",
    "mvhp_time_dose", "mvmp_time_dose", "mvlp_time_dose",
    "lvhp_time_dose", "lvmp_time_dose", "lvlp_time_dose",
]

@login_required
def delete_record(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied

    record = get_object_or_404(Record, pk=pk, is_deleted=False)

    if request.method == "POST":
        record.is_deleted = True
        record.deleted_at = timezone.now()
        record.deleted_by = request.user
        record.save()
        return redirect("records:database")

    return render(request, "records/delete_confirm.html", {"record": record})

@login_required
def database(request):
    records, search_form, sort = get_filtered_records(request)

    total_count = records.count()

    paginator = Paginator(records, 25)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    querydict = request.GET.copy()
    querydict.pop("page", None)

    active_filters = [(k, v) for k, values in querydict.lists() for v in values if v]

    querystring = urlencode(active_filters)
    search_querystring = urlencode([(k, v) for k, v in active_filters if k != "sort"])

    selected_columns = request.GET.getlist("cols") or DEFAULT_TABLE_COLUMNS
    display_columns = [
        (key, label, sort_field)
        for key, label, sort_field, _ in AVAILABLE_COLUMNS
        if key in selected_columns
    ]

    return render(request, "records/database.html", {
        "page_obj": page_obj,
        "total_count": total_count,
        "current_sort": sort,
        "search_form": search_form,
        "querystring": querystring,
        "search_querystring": search_querystring,
        "active_filters": active_filters,
        "all_columns": AVAILABLE_COLUMNS,
        "selected_columns": selected_columns,
        "display_columns": display_columns,
    })

@login_required
def record_detail(request, pk):
    record = get_object_or_404(Record, pk=pk)

    if record.is_deleted and not request.user.is_staff:
        raise PermissionDenied

    is_visible = record.status == "public" or record.submitted_by == request.user
    if not is_visible and not request.user.is_staff:
        raise PermissionDenied

    if request.method == "POST" and request.user.is_staff:
        new_status = request.POST.get("status")
        if new_status in dict(Record.STATUS_CHOICES):
            record.status = new_status
            if new_status == "public":
                record.approval_at = timezone.now()
                record.approval_by = request.user
            record.save()
            return redirect("records:record_detail", pk=record.pk)

    return render(request, "records/record_detail.html", {"record": record})

@staff_member_required
def midi_download(request, pk):
    record = get_object_or_404(Record, pk=pk)
    if not record.midi_file:
        raise Http404
    return FileResponse(record.midi_file.open("rb"), as_attachment=True, filename=record.midi_file.name.split("/")[-1])

@login_required
def deleted_list(request):
    if not request.user.is_staff:
        raise PermissionDenied

    records = Record.objects.filter(is_deleted=True).order_by("-deleted_at")
    return render(request, "records/deleted_list.html", {"records": records})


@login_required
def reinstate_record(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied

    record = get_object_or_404(Record, pk=pk, is_deleted=True)

    if request.method == "POST":
        record.is_deleted = False
        record.deleted_at = None
        record.deleted_by = None
        record.save()
        return redirect("records:deleted_list")

    return render(request, "records/reinstate_confirm.html", {"record": record})
