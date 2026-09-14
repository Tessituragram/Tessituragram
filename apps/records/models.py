from django.conf import settings
from django.db import models


class Record(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending Review"),
        ("public", "Public"),
        ("private", "Private"),
        ("rejected", "Rejected"),
    ]

    INITIAL_KEY_CHOICES = [
    ("0 flats or sharps", "0 Flats or Sharps"),
    ("1 flat", "1 Flat"),
    ("2 flats", "2 Flats"),
    ("3 flats", "3 Flats"),
    ("4 flats", "4 Flats"),
    ("5 flats", "5 Flats"),
    ("6 flats", "6 Flats"),
    ("7 flats", "7 Flats"),
    ("1 sharp", "1 Sharp"),
    ("2 sharps", "2 Sharps"),
    ("3 sharps", "3 Sharps"),
    ("4 sharps", "4 Sharps"),
    ("5 sharps", "5 Sharps"),
    ("6 sharps", "6 Sharps"),
    ("7 sharps", "7 Sharps")
]

    VOICE_PART_CHOICES = [
    ('unspecified_bass', 'Unspecified Bass'),
    ('unspecified_treble', 'Unspecified Treble'),
    ('part_1', 'Part 1'),
    ('part_2', 'Part 2'),
    ('part_3', 'Part 3'),
    ('part_4', 'Part 4'),
    ('soprano_1', 'Soprano 1'),
    ('soprano_2', 'Soprano 2'),
    ('soprano_3', 'Soprano 3'),
    ('alto_1', 'Alto 1'),
    ('alto_2', 'Alto 2'),
    ('alto_3', 'Alto 3'),
    ('tenor_1', 'Tenor 1'),
    ('tenor_2', 'Tenor 2'),
    ('tenor_3', 'Tenor 3'),
    ('bass_1', 'Bass 1'),
    ('bass_2', 'Bass 2'),
    ('bass_3', 'Bass 3'),
]

    PERFORMING_FORCES_CHOICES = [
      ('solo', 'Soloistic Piece'),
      ('ensemble', 'Ensemble Piece'),
  ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="deleted_records",
    )

    approval_at = models.DateTimeField(null=True, blank=True)
    approval_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_records",
    )

    edited_at = models.DateTimeField(null=True, blank=True)
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="edited_records",
    )

    filename = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    larger_work = models.CharField(max_length=255, blank=True)
    clef_range = models.CharField(max_length=6, null=True)
    performing_forces = models.CharField(max_length=10, choices=PERFORMING_FORCES_CHOICES)
    voice_part = models.CharField(max_length=20, choices=VOICE_PART_CHOICES)
    composer = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    initial_key = models.CharField(
        max_length=20,
        choices=INITIAL_KEY_CHOICES,
        blank=True,
        null=True,
    )
    additional_comments = models.TextField(
        blank=True,
        null=True,
        help_text="Notes provided by the user during submission.",
    )

    STYLE_CHOICES = [
        ("western_classical", "Western Classical"),
        ("musical_theatre", "Musical Theatre"),
        ("contemporary_commerical", "Contemporary Commercial"),
        ("other", "Other"),
    ]

    style = models.CharField(max_length=25, choices=STYLE_CHOICES)
    style_other = models.CharField(max_length=100, choices=STYLE_CHOICES)

    pdf_file = models.FileField(upload_to="pdfs/", null=True, blank=True)
    midi_file = models.FileField(upload_to="midi/", null=True, blank=True)

    q1_freq = models.FloatField()
    q1_pitch = models.CharField(max_length=2)
    q1_octave = models.IntegerField()
    q3_freq = models.FloatField()
    q3_pitch = models.CharField(max_length=2)
    q3_octave = models.IntegerField()

    cycle_dose = models.FloatField()
    time_dose = models.FloatField()
    rest_time = models.FloatField()
    total_time = models.FloatField()
    median_freq = models.FloatField()
    min_freq = models.FloatField()
    max_freq = models.FloatField()

    hvhp_time_dose = models.FloatField()
    hvmp_time_dose = models.FloatField()
    hvlp_time_dose = models.FloatField()
    mvhp_time_dose = models.FloatField()
    mvmp_time_dose = models.FloatField()
    mvlp_time_dose = models.FloatField()
    lvhp_time_dose = models.FloatField()
    lvmp_time_dose = models.FloatField()
    lvlp_time_dose = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def hvhp_percentage(self):
        return (self.hvhp_time_dose / self.time_dose) * 100 if self.time_dose else 0

    @property
    def hvmp_percentage(self):
        return (self.hvmp_time_dose / self.time_dose) * 100 if self.time_dose else 0

    @property
    def hvlp_percentage(self):
        return (self.hvlp_time_dose / self.time_dose) * 100 if self.time_dose else 0

    @property
    def mvhp_percentage(self):
        return (self.mvhp_time_dose / self.time_dose) * 100 if self.time_dose else 0

    @property
    def mvmp_percentage(self):
        return (self.mvmp_time_dose / self.time_dose) * 100 if self.time_dose else 0

    @property
    def mvlp_percentage(self):
        return (self.mvlp_time_dose / self.time_dose) * 100 if self.time_dose else 0

    @property
    def lvhp_percentage(self):
        return (self.lvhp_time_dose / self.time_dose) * 100 if self.time_dose else 0

    @property
    def lvmp_percentage(self):
        return (self.lvmp_time_dose / self.time_dose) * 100 if self.time_dose else 0

    @property
    def lvlp_percentage(self):
        return (self.lvlp_time_dose / self.time_dose) * 100 if self.time_dose else 0
