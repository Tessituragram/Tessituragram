from django.conf import settings
from django.db import models

class Record(models.Model):
    STATUS_CHOICES = [
    ("pending", "Pending Review"),
    ("public", "Public"),
    ("private", "Private"),
    ("rejected", "Rejected"),
]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

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
    clef_range = models.CharField(max_length=6, null=True)
    composer = models.CharField(max_length=200)
    author = models.CharField(max_length=200, blank=True)

    STYLE_CHOICES = [
    ("western_classical", "Western Classical"),
    ("musical_theatre", "Musical Theatre"),
    ("commercial_music", "Commercial Music"),
    ("choral", "Choral"),
    ("other", "Other"),
    ]

    style = models.CharField(max_length=20, choices=STYLE_CHOICES)

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
