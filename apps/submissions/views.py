import os
import tempfile
import shutil
import uuid

from django.core.files import File
from django.core.mail import send_mail
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from fpdf import FPDF

from src import midi_reader, tessitura, utils
from src.tessitura import TessPassContainer
from apps.records.models import Record
from apps.records.columns import (
    AVAILABLE_COLUMNS,
    DEFAULT_REVIEW_COLUMNS,
    get_display_columns,
)
from .forms import SubmissionForm, ReviewerEditForm

NOTIFICATION_EMAIL = "tessituragram@tessituragram.com"


def notify_admins_of_submission(request, record):
    review_url = request.build_absolute_uri(
        reverse("submissions:review_detail", args=[record.pk])
    )
    send_mail(
        subject=f"New submission for review: {record.filename}",
        message=(
            f'{record.submitted_by} submitted "{record.filename}" '
            f"({record.composer}) for review.\n\n"
            f"Review it here: {review_url}"
        ),
        from_email=None,
        recipient_list=[NOTIFICATION_EMAIL],
    )


@login_required
def submit_form(request):
    if request.method == "POST":
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data["title"]
            larger_work = form.cleaned_data["larger_work"]
            uploaded_file = form.cleaned_data["midi_file"]
            filename = os.path.splitext(uploaded_file.name)[0]
            composer = form.cleaned_data["composer"]
            style = form.cleaned_data["style"]
            author = form.cleaned_data.get("author", "")
            initial_key = form.cleaned_data["initial_key"]
            clef_range = form.cleaned_data.get("clef_range") or None
            performing_forces = form.cleaned_data["performing_forces"]
            voice_part= form.cleaned_data["voice_part"]

            work_dir = tempfile.mkdtemp(prefix="tessitura_")
            output_dir = os.path.join(work_dir, "results")
            os.makedirs(output_dir, exist_ok=True)

            try:
                midi_path = os.path.join(work_dir, uploaded_file.name)
                with open(midi_path, "wb") as f:
                    for chunk in uploaded_file.chunks():
                        f.write(chunk)

                with midi_reader.MidiParser(midi_path) as parser:
                    status = parser.parse_midi()
                    if status == -1:
                        error_msg = parser.error_message or "Could not parse MIDI file."
                        form.add_error(None, error_msg)
                        return render(
                            request, "submissions/submit_form.html", {"form": form}
                        )
                    notes = parser.get_notes()
                    if notes == -1:
                        error_msg = (
                            parser.error_message
                            or "Could not extract notes from MIDI file."
                        )
                        form.add_error(None, error_msg)
                        return render(
                            request, "submissions/submit_form.html", {"form": form}
                        )

                tesses, passaggios, _ = tessitura.get_tessitura_and_passaggio(
                    notes, clef_range
                )

                keep_private = form.cleaned_data.get("keep_private", False)
                initial_status = "private" if keep_private else "pending"

                for tess, passaggio in zip(tesses, passaggios):
                    record = Record.objects.create(
                        submitted_by=request.user,
                        filename=filename,
                        title=title,
                        larger_work=larger_work,
                        composer=composer,
                        author=author,
                        initial_key=initial_key,
                        style=style,
                        clef_range=tess.clef_range,
                        performing_forces=performing_forces,
                        voice_part=voice_part,
                        status=initial_status,
                        q1_freq=tess.lowFreq,
                        q1_pitch=tess.lowNote,
                        q1_octave=tess.lowOctave,
                        q3_freq=tess.highFreq,
                        q3_pitch=tess.highNote,
                        q3_octave=tess.highOctave,
                        cycle_dose=tess.cycle_dose,
                        time_dose=tess.time_dose,
                        rest_time=tess.rest_time,
                        total_time=tess.total_time,
                        median_freq=tess.median_freq,
                        min_freq=tess.min_pitch,
                        max_freq=tess.max_pitch,
                        hvhp_time_dose=passaggio.hvhp.time_dose,
                        hvmp_time_dose=passaggio.hvmp.time_dose,
                        hvlp_time_dose=passaggio.hvlp.time_dose,
                        mvhp_time_dose=passaggio.mvhp.time_dose,
                        mvmp_time_dose=passaggio.mvmp.time_dose,
                        mvlp_time_dose=passaggio.mvlp.time_dose,
                        lvhp_time_dose=passaggio.lvhp.time_dose,
                        lvmp_time_dose=passaggio.lvmp.time_dose,
                        lvlp_time_dose=passaggio.lvlp.time_dose,
                    )

                    with open(midi_path, "rb") as midi_f:
                        record.midi_file.save(
                            uploaded_file.name, File(midi_f), save=True
                        )

                    pdf = FPDF()
                    pdf.add_font(
                        "times_new",
                        "",
                        utils.resource_path(
                            os.path.join("data", "Times New Roman.ttf")
                        ),
                    )
                    pdf.add_font(
                        "times_new",
                        "B",
                        utils.resource_path(
                            os.path.join("data", "Times New Roman Bold.ttf")
                        ),
                    )
                    pdf.add_font(
                        "times_new",
                        "I",
                        utils.resource_path(
                            os.path.join("data", "Times New Roman Italic.ttf")
                        ),
                    )
                    pdf.add_font(
                        "times_new",
                        "BI",
                        utils.resource_path(
                            os.path.join("data", "Times New Roman Bold Italic.ttf")
                        ),
                    )
                    pdf.add_page()

                    container = TessPassContainer(
                        tess,
                        passaggio,
                        title,
                        pdf,
                        output_dir=output_dir,
                        submitted_by=f"{request.user.first_name} {request.user.last_name}",
                    )
                    container.ensure_musescore_configured()
                    container.write_to_pdf()

                    pdf_filename = (
                        f"{record.pk}-{tess.clef_range}-{uuid.uuid4().hex[:8]}.pdf"
                    )
                    pdf_path = os.path.join(work_dir, pdf_filename)
                    pdf.output(pdf_path)

                    with open(pdf_path, "rb") as pdf_f:
                        record.pdf_file.save(pdf_filename, File(pdf_f), save=True)

                    if not keep_private:
                        notify_admins_of_submission(request, record)

                return redirect("submissions:submission_success")

            finally:
                shutil.rmtree(work_dir, ignore_errors=True)
    else:
        form = SubmissionForm()

    return render(request, "submissions/submit_form.html", {"form": form})


@login_required
def submission_success(request):
    return render(request, "submissions/submission_success.html")


@staff_member_required
def review_list(request):
    records = Record.objects.filter(status="pending", is_deleted=False)

    sort = request.GET.get("sort", "created_at")
    if sort == "submitter":
        records = records.order_by(
            "submitted_by__first_name", "submitted_by__last_name"
        )
    elif sort == "-submitter":
        records = records.order_by(
            "-submitted_by__first_name", "-submitted_by__last_name"
        )
    elif sort.lstrip("-") in {key for key, *_ in AVAILABLE_COLUMNS} | {
        "title",
        "created_at",
    }:
        records = records.order_by(sort)

    selected_columns, display_columns = get_display_columns(
        request, DEFAULT_REVIEW_COLUMNS
    )

    active_filters = [(k, v) for k, values in request.GET.lists() for v in values if v]

    return render(
        request,
        "submissions/review_list.html",
        {
            "records": records,
            "current_sort": sort,
            "active_filters": active_filters,
            "all_columns": AVAILABLE_COLUMNS,
            "selected_columns": selected_columns,
            "display_columns": display_columns,
        },
    )


@staff_member_required
def review_detail(request, pk):
    record = get_object_or_404(Record, pk=pk, status="pending")

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "approve":
            record.status = "public"
            record.approval_at = timezone.now()
            record.approval_by = request.user
            record.save()
            return redirect("submissions:review_list")
        elif action == "reject":
            record.status = "rejected"
            record.save()
            return redirect("submissions:review_list")

    return render(request, "submissions/review_detail.html", {"record": record})


@staff_member_required
def edit_resubmit(request, pk):
    record = get_object_or_404(Record, pk=pk, is_deleted=False)

    if request.method == "POST":
        form = ReviewerEditForm(request.POST, request.FILES, instance=record)
        
        if form.is_valid():
            uploaded_file = form.cleaned_data.get("midi_file")

            if not uploaded_file and not record.midi_file:
                form.add_error(
                    None,
                    "No MIDI file is on record. Please upload one to reprocess this submission.",
                )
                return render(
                    request,
                    "submissions/edit_resubmit.html",
                    {"form": form, "record": record},
                )

            work_dir = tempfile.mkdtemp(prefix="tessitura_edit_")
            output_dir = os.path.join(work_dir, "results")
            os.makedirs(output_dir, exist_ok=True)

            try:
                if uploaded_file:
                    record.filename = os.path.splitext(uploaded_file.name)[0]
                    midi_path = os.path.join(work_dir, uploaded_file.name)
                    with open(midi_path, "wb") as f:
                        for chunk in uploaded_file.chunks():
                            f.write(chunk)
                else:
                    midi_path = os.path.join(
                        work_dir, os.path.basename(record.midi_file.name)
                    )
                    with record.midi_file.open("rb") as source, open(
                        midi_path, "wb"
                    ) as dest:
                        shutil.copyfileobj(source, dest)

                with midi_reader.MidiParser(midi_path) as parser:
                    status = parser.parse_midi()
                    if status == -1:
                        form.add_error(None, "Could not parse MIDI file.")
                        return render(
                            request,
                            "submissions/edit_resubmit.html",
                            {"form": form, "record": record},
                        )
                    
                    notes = parser.get_notes()
                    if notes == -1:
                        form.add_error(None, "Could not extract notes from MIDI file.")
                        return render(
                            request,
                            "submissions/edit_resubmit.html",
                            {"form": form, "record": record},
                        )
                    
                    notes = parser.post_process(notes)
                    if notes == -1:
                        form.add_error(None, "File does not end with C1 note.")
                        return render(
                            request, 
                            "submissions/edit_resubmit.html", 
                            {"form": form, "record": record}
                        )

                selected_clef_range = form.cleaned_data.get("clef_range", "")
                clef_range_param = (
                    None
                    if selected_clef_range.lower() in ["none", ""]
                    else selected_clef_range.lower()
                )

                tesses, passaggios, _ = tessitura.get_tessitura_and_passaggio(
                    notes, clef_range_param
                )

                # Select the matching tessitura calculation
                match = None

                if clef_range_param is None:
                    # If no clef range was specified, pick the default (first) result
                    if tesses and passaggios:
                        match = (tesses[0], passaggios[0])
                else:
                    # Otherwise, match on the explicitly requested clef_range
                    for tess, passaggio in zip(tesses, passaggios):
                        if str(tess.clef_range or "").lower() == selected_clef_range.lower():
                            match = (tess, passaggio)
                            break

                if match is None:
                    form.add_error(
                        None, "Could not compute results for the selected clef_range."
                    )
                    return render(
                        request,
                        "submissions/edit_resubmit.html",
                        {"form": form, "record": record},
                    )

                tess, passaggio = match

                # Save updated fields to model
                record.title = form.cleaned_data["title"]
                record.larger_work = form.cleaned_data.get("larger_work", "")
                record.composer = form.cleaned_data["composer"]
                record.author = form.cleaned_data.get("author", "")
                record.initial_key = form.cleaned_data["initial_key"]
                record.style = form.cleaned_data["style"]
                record.clef_range = tess.clef_range
                record.performing_forces = form.cleaned_data["performing_forces"]
                record.voice_part = form.cleaned_data["voice_part"]
                record.status = "pending"
                record.approval_at = None
                record.approval_by = None
                record.edited_at = timezone.now()
                record.edited_by = request.user

                # Tessitura metrics updates...
                record.q1_freq = tess.lowFreq
                record.q1_pitch = tess.lowNote
                record.q1_octave = tess.lowOctave
                record.q3_freq = tess.highFreq
                record.q3_pitch = tess.highNote
                record.q3_octave = tess.highOctave
                record.median_freq = tess.median_freq
                record.cycle_dose = tess.cycle_dose
                record.time_dose = tess.time_dose
                record.rest_time = tess.rest_time
                record.total_time = tess.total_time
                record.min_freq = tess.min_pitch
                record.max_freq = tess.max_pitch
                record.hvhp_time_dose = passaggio.hvhp.time_dose
                record.hvmp_time_dose = passaggio.hvmp.time_dose
                record.hvlp_time_dose = passaggio.hvlp.time_dose
                record.mvhp_time_dose = passaggio.mvhp.time_dose
                record.mvmp_time_dose = passaggio.mvmp.time_dose
                record.mvlp_time_dose = passaggio.mvlp.time_dose
                record.lvhp_time_dose = passaggio.lvhp.time_dose
                record.lvmp_time_dose = passaggio.lvmp.time_dose
                record.lvlp_time_dose = passaggio.lvlp.time_dose

                # Generate PDF
                pdf = FPDF()
                pdf.add_font("times_new", "", utils.resource_path(os.path.join("data", "Times New Roman.ttf")))
                pdf.add_font("times_new", "B", utils.resource_path(os.path.join("data", "Times New Roman Bold.ttf")))
                pdf.add_font("times_new", "I", utils.resource_path(os.path.join("data", "Times New Roman Italic.ttf")))
                pdf.add_font("times_new", "BI", utils.resource_path(os.path.join("data", "Times New Roman Bold Italic.ttf")))
                pdf.add_page()

                container = TessPassContainer(
                    tess,
                    passaggio,
                    record.title,
                    pdf,
                    output_dir=output_dir,
                    submitted_by=(
                        f"{record.submitted_by.first_name} {record.submitted_by.last_name}"
                        if record.submitted_by
                        else None
                    ),
                )
                container.ensure_musescore_configured()
                container.write_to_pdf()

                pdf_filename = f"{record.pk}-{tess.clef_range}-{uuid.uuid4().hex[:8]}.pdf"
                pdf_path = os.path.join(work_dir, pdf_filename)
                pdf.output(pdf_path)

                if record.pdf_file:
                    record.pdf_file.delete(save=False)
                with open(pdf_path, "rb") as pdf_f:
                    record.pdf_file.save(pdf_filename, File(pdf_f), save=False)

                if uploaded_file:
                    if record.midi_file:
                        record.midi_file.delete(save=False)
                    with open(midi_path, "rb") as midi_f:
                        record.midi_file.save(
                            uploaded_file.name, File(midi_f), save=False
                        )

                record.save()

                return redirect("records:record_detail", pk=record.pk)

            finally:
                shutil.rmtree(work_dir, ignore_errors=True)
    else:
        initial_clef = (record.clef_range or "none").lower()
        form = ReviewerEditForm(instance=record, initial={"clef_range": initial_clef})

    return render(
        request, "submissions/edit_resubmit.html", {"form": form, "record": record}
    )