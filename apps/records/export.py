import openpyxl
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .filtering import get_filtered_records

COLUMN_DEFINITIONS = [
    ("title", "Title", lambda r: r.title),
    ("larger_work", "Larger Work", "larger_work", lambda r: r.larger_work),
    ("composer", "Composer", lambda r: r.composer),
    ("author", "Author", lambda r: r.author),
    ("initial_key", "Initial Musical Key", "initial_key", lambda r: r.get_initial_key_display()),
    ("style", "Style", lambda r: r.get_style_display()),
    ("clef_range", "Clef", lambda r: r.clef_range),
    ("performing_forces", "Performing Forces", "performing_forces", lambda r: r.get_performing_forces_display()),
    ("voice_part", "Voice Part", "voice_part", lambda r: r.voice_part),
    (
        "submitter",
        "Submitted By",
        lambda r: (
            f"{r.submitted_by.first_name} {r.submitted_by.last_name}"
            if r.submitted_by
            else ""
        ),
    ),
    (
        "created_at",
        "Submitted On",
        lambda r: r.created_at.strftime("%Y-%m-%d") if r.created_at else "",
    ),
    (
        "q1_range",
        "Tessitura Range",
        lambda r: f"{r.q1_pitch}{r.q1_octave}–{r.q3_pitch}{r.q3_octave}",
    ),
    ("q1_freq", "Q1 (Hz)", lambda r: r.q1_freq),
    ("q3_freq", "Q3 (Hz)", lambda r: r.q3_freq),
    ("median_freq", "Median (Hz)", lambda r: r.median_freq),
    ("full_range", "Full Range (Hz)", lambda r: f"{r.min_freq}–{r.max_freq}"),
    ("cycle_dose", "Cycle Dose", lambda r: r.cycle_dose),
    ("time_dose", "Time Dose", lambda r: r.time_dose),
    ("rest_time", "Rest Time", lambda r: r.rest_time),
    ("total_time", "Total Time", lambda r: r.total_time),
    ("hvhp_time_dose", "HV High Passaggio", lambda r: r.hvhp_time_dose),
    ("hvmp_time_dose", "HV Middle Passaggio", lambda r: r.hvmp_time_dose),
    ("hvlp_time_dose", "HV Low Passaggio", lambda r: r.hvlp_time_dose),
    ("mvhp_time_dose", "MV High Passaggio", lambda r: r.mvhp_time_dose),
    ("mvmp_time_dose", "MV Middle Passaggio", lambda r: r.mvmp_time_dose),
    ("mvlp_time_dose", "MV Low Passaggio", lambda r: r.mvlp_time_dose),
    ("lvhp_time_dose", "LV High Passaggio", lambda r: r.lvhp_time_dose),
    ("lvmp_time_dose", "LV Middle Passaggio", lambda r: r.lvmp_time_dose),
    ("lvlp_time_dose", "LV Low Passaggio", lambda r: r.lvlp_time_dose),
]

DEFAULT_COLUMNS = ["title", "composer", "author", "style", "clef_range", "q1_range"]


@login_required
def export_database(request):
    records, _, _ = get_filtered_records(request)

    selected_keys = request.GET.getlist("columns") or DEFAULT_COLUMNS
    columns = [
        (key, label, accessor)
        for key, label, accessor in COLUMN_DEFINITIONS
        if key in selected_keys
    ]

    if not columns:
        columns = [
            (key, label, accessor)
            for key, label, accessor in COLUMN_DEFINITIONS
            if key in DEFAULT_COLUMNS
        ]

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Tessituragram Export"

    ws.append([label for _, label, _ in columns])

    for record in records:
        row = []
        for _, _, accessor in columns:
            try:
                row.append(accessor(record))
            except Exception:
                row.append("")
        ws.append(row)

    for i, (_, label, _) in enumerate(columns, start=1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = max(
            len(label) + 2, 12
        )

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="tessituragram_export.xlsx"'
    wb.save(response)
    return response
