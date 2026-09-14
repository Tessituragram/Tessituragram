TITLE_SORT = "title"

AVAILABLE_COLUMNS = [
    ("larger_work", "Larger Work", "larger_work", lambda r: r.larger_work),
    ("composer", "Musical Composer", "composer", lambda r: r.composer),
    ("author", "Text Author", "author", lambda r: r.author),
    ("initial_key", "Initial Musical Key", "initial_key", lambda r: r.initial_key),
    ("style", "Performance Style", "style", lambda r: r.get_style_display()),
    ("clef_range", "Clef Range", "clef_range", lambda r: r.clef_range),
    (
        "submitter",
        "Submitted By",
        "submitter",
        lambda r: (
            f"{r.submitted_by.first_name} {r.submitted_by.last_name}"
            if r.submitted_by
            else ""
        ),
    ),
    (
        "created_at",
        "Submitted On",
        "created_at",
        lambda r: r.created_at.strftime("%b %-d, %Y") if r.created_at else "",
    ),
    (
        "tessitura_range",
        "Tessitura Range",
        "q1_freq",
        lambda r: f"{r.q1_pitch}{r.q1_octave}–{r.q3_pitch}{r.q3_octave}",
    ),
    (
        "full_range",
        "Full Range (Hz)",
        "min_freq",
        lambda r: f"{r.min_freq}–{r.max_freq}",
    ),
    ("q1_freq", "Q1 (Hz)", "q1_freq", lambda r: r.q1_freq),
    ("q3_freq", "Q3 (Hz)", "q3_freq", lambda r: r.q3_freq),
    ("median_freq", "Median (Hz)", "median_freq", lambda r: r.median_freq),
    ("cycle_dose", "Cycle Dose", "cycle_dose", lambda r: r.cycle_dose),
    ("time_dose", "Time Dose", "time_dose", lambda r: r.time_dose),
    ("rest_time", "Rest Time", "rest_time", lambda r: r.rest_time),
    ("total_time", "Total Time", "total_time", lambda r: r.total_time),
    (
        "hvhp_time_dose",
        "HV High Passaggio",
        "hvhp_time_dose",
        lambda r: r.hvhp_time_dose,
    ),
    (
        "hvmp_time_dose",
        "HV Middle Passaggio",
        "hvmp_time_dose",
        lambda r: r.hvmp_time_dose,
    ),
    (
        "hvlp_time_dose",
        "HV Low Passaggio",
        "hvlp_time_dose",
        lambda r: r.hvlp_time_dose,
    ),
    (
        "mvhp_time_dose",
        "MV High Passaggio",
        "mvhp_time_dose",
        lambda r: r.mvhp_time_dose,
    ),
    (
        "mvmp_time_dose",
        "MV Middle Passaggio",
        "mvmp_time_dose",
        lambda r: r.mvmp_time_dose,
    ),
    (
        "mvlp_time_dose",
        "MV Low Passaggio",
        "mvlp_time_dose",
        lambda r: r.mvlp_time_dose,
    ),
    (
        "lvhp_time_dose",
        "LV High Passaggio",
        "lvhp_time_dose",
        lambda r: r.lvhp_time_dose,
    ),
    (
        "lvmp_time_dose",
        "LV Middle Passaggio",
        "lvmp_time_dose",
        lambda r: r.lvmp_time_dose,
    ),
    (
        "lvlp_time_dose",
        "LV Low Passaggio",
        "lvlp_time_dose",
        lambda r: r.lvlp_time_dose,
    ),
    ("status", "Status", "status", lambda r: r.get_status_display()),
]

DEFAULT_TABLE_COLUMNS = [
    "composer",
    "larger_work",
    "author",
    "style",
    "clef_range",
    "tessitura_range",
]
DEFAULT_PROFILE_COLUMNS = [
    "composer",
    "larger_work",
    "author",
    "style",
    "clef_range",
    "tessitura_range",
    "status",
]
DEFAULT_REVIEW_COLUMNS = [
    "composer",
    "larger_work",
    "author",
    "style",
    "clef_range",
    "submitter",
    "created_at",
]

COLUMN_MAP = {
    key: (label, sort_field, accessor)
    for key, label, sort_field, accessor in AVAILABLE_COLUMNS
}


def get_display_columns(request, default_columns):
    from .columns import AVAILABLE_COLUMNS

    selected_columns = request.GET.getlist("cols") or default_columns
    display_columns = [
        (key, label, sort_field)
        for key, label, sort_field, _ in AVAILABLE_COLUMNS
        if key in selected_columns
    ]
    return selected_columns, display_columns
