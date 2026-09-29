import math

import openpyxl
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .filtering import get_filtered_records, freq_to_note_octave


def _pitch_label(freq):
    result = freq_to_note_octave(freq)
    if result is None:
        return ""
    note, octave = result
    return f"{note}{octave}"


COLUMN_DEFINITIONS = [
    ("title", "Title", lambda r: r.title),
    ("composer", "Composer", lambda r: r.composer),
    ("author", "Author", lambda r: r.author),
    ("larger_work", "Larger Work", lambda r: r.larger_work),
    ("style", "Style", lambda r: r.get_style_display()),
    ("clef_range", "Clef", lambda r: r.clef_range),
    ("style_other", "Performance Style - Other", lambda r: r.style_other),
    ("initial_key", "Initial Musical Key", lambda r: r.get_initial_key_display()),
    ("performing_forces", "Performing Forces", lambda r: r.get_performing_forces_display()),
    (
        "submitter",
        "Submitter",
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

    ("q0_freq", "Q0 - Range Bottom (Hz)", lambda r: r.min_freq),
    ("q0_pitch", "Q0 - Range Bottom (Pitch)", lambda r: _pitch_label(r.min_freq)),

    ("q1_freq", "Q1 - Tessitura Bottom (Hz)", lambda r: r.q1_freq),
    ("q1_pitch", "Q1 - Tessitura Bottom (Pitch)", lambda r: f"{r.q1_pitch}{r.q1_octave}"),

    ("q2_freq", "Q2 - Median (Hz)", lambda r: r.median_freq),
    ("q2_pitch", "Q2 - Median (Pitch)", lambda r: _pitch_label(r.median_freq)),

    ("q3_freq", "Q3 - Tessitura Top (Hz)", lambda r: r.q3_freq),
    ("q3_pitch", "Q3 - Tessitura Top (Pitch)", lambda r: f"{r.q3_pitch}{r.q3_octave}"),

    ("q4_freq", "Q4 - Range Top (Hz)", lambda r: r.max_freq),
    ("q4_pitch", "Q4 - Range Top (Pitch)", lambda r: _pitch_label(r.max_freq)),

    ("cycle_dose", "Fptp - Cycle Dose", lambda r: r.cycle_dose),
    ("time_dose", "tp - Time Dose", lambda r: r.time_dose),
    ("rest_time", "tp - Rest Time", lambda r: r.rest_time),
    ("total_time", "t - Total Time", lambda r: r.total_time),

    ("hvhp_time_dose", "HV Hp", lambda r: r.hvhp_time_dose),
    ("hvmp_time_dose", "HV Mp", lambda r: r.hvmp_time_dose),
    ("hvlp_time_dose", "HV Lp", lambda r: r.hvlp_time_dose),

    ("mvhp_time_dose", "MV Hp", lambda r: r.mvhp_time_dose),
    ("mvmp_time_dose", "MV Mp", lambda r: r.mvmp_time_dose),
    ("mvlp_time_dose", "MV Lp", lambda r: r.mvlp_time_dose),

    ("lvhp_time_dose", "LV Hp", lambda r: r.lvhp_time_dose),
    ("lvmp_time_dose", "LV Mp", lambda r: r.lvmp_time_dose),
    ("lvlp_time_dose", "LV Lp", lambda r: r.lvlp_time_dose),
]

DEFAULT_COLUMNS = ["title", "composer", "author", "style", "clef_range", "q1_pitch"]


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