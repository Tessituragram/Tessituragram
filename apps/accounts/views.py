from django.db.models import Case, CharField, IntegerField, Value, When
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from apps.records.filtering import apply_record_sort
from apps.records.models import Record
from urllib.parse import urlencode
from .forms import ProfileEditForm, SignUpForm, EmailChangeForm
from .models import PendingSignup, PendingEmailChange

from apps.records.columns import (
    AVAILABLE_COLUMNS,
    DEFAULT_PROFILE_COLUMNS,
    SIMPLE_SEARCH_COLUMNS,
    get_display_columns,
)

@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user

        logout(request)
        user.delete()

        return redirect("home")

    return redirect("profile")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            pending = form.save()

            verify_url = request.build_absolute_uri(
                reverse("verify_email", args=[pending.token])
            )
            send_mail(
                subject="Verify your Tessituragram account",
                message=f"Click to verify your account: {verify_url}",
                from_email=None,
                recipient_list=[pending.email],
            )
            return render(
                request, "registration/check_email.html", {"email": pending.email}
            )
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})


def verify_email(request, token):
    try:
        pending = PendingSignup.objects.get(token=token)
    except PendingSignup.DoesNotExist:
        return render(request, "registration/verify_invalid.html")

    if pending.is_expired():
        pending.delete()
        return render(request, "registration/verify_invalid.html")

    user = User(
        username=pending.username,
        first_name=pending.first_name,
        last_name=pending.last_name,
        email=pending.email,
    )
    user.password = pending.password_hash
    user.save()
    pending.delete()

    return render(request, "registration/verify_success.html")


@login_required
def profile(request):
    profile_form = ProfileEditForm(instance=request.user)
    email_form = EmailChangeForm()

    if request.method == "POST":
        if "save_profile" in request.POST:
            profile_form = ProfileEditForm(
                request.POST,
                instance=request.user,
            )

            if profile_form.is_valid():
                profile_form.save()
                return redirect("profile")

        elif "request_email_change" in request.POST:
            email_form = EmailChangeForm(request.POST)

            if email_form.is_valid():
                new_email = email_form.cleaned_data["new_email"]

                PendingEmailChange.objects.update_or_create(
                    user=request.user,
                    defaults={"new_email": new_email},
                )

                pending = PendingEmailChange.objects.get(
                    user=request.user
                )

                verify_url = request.build_absolute_uri(
                    reverse(
                        "verify_email_change",
                        args=[pending.token],
                    )
                )

                send_mail(
                    subject="Confirm your new email — Tessituragram",
                    message=f"Click to confirm this email change: {verify_url}",
                    from_email=None,
                    recipient_list=[new_email],
                )

                return redirect("profile")

    # --------------------------------------------------
    # Records submitted by this user
    # --------------------------------------------------

    records = Record.objects.filter(
        submitted_by=request.user,
        is_deleted=False,
    )

    # --------------------------------------------------
    # Consolidate Bass/Treble records into one row
    # per submission
    # --------------------------------------------------

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

    # --------------------------------------------------
    # Sorting
    # --------------------------------------------------

    sort = request.GET.get("sort", "-created_at")

    records = apply_record_sort(records, sort)

    # --------------------------------------------------
    # Display columns
    # --------------------------------------------------

    selected_columns, display_columns = get_display_columns(
        request,
        DEFAULT_PROFILE_COLUMNS,
    )

    # --------------------------------------------------
    # Query parameters
    # --------------------------------------------------

    querydict = request.GET.copy()
    querydict.pop("sort", None)

    search_querystring = urlencode(
        [
            (key, value)
            for key, values in querydict.lists()
            for value in values
            if value
        ]
    )

    active_filters = [
        (key, value)
        for key, values in request.GET.lists()
        for value in values
        if value
        and key != "sort"
        and key != "columns_submitted"
    ]

    pending_email = PendingEmailChange.objects.filter(
        user=request.user
    ).first()

    return render(
        request,
        "accounts/profile.html",
        {
            "profile_form": profile_form,
            "email_form": email_form,
            "records": records,
            "pending_email": pending_email,
            "current_sort": sort,
            "active_filters": active_filters,
            "search_querystring": search_querystring,
            "all_columns": [
                column
                for column in AVAILABLE_COLUMNS
                if column[0] in SIMPLE_SEARCH_COLUMNS
                or column[0] == "status"
            ],
            "selected_columns": selected_columns,
            "display_columns": display_columns,
        },
    )


def verify_email_change(request, token):
    try:
        pending = PendingEmailChange.objects.get(token=token)
    except PendingEmailChange.DoesNotExist:
        return render(request, "accounts/verify_invalid.html")

    if pending.is_expired():
        pending.delete()
        return render(request, "accounts/verify_invalid.html")

    user = pending.user
    user.email = pending.new_email
    user.username = pending.new_email
    user.save()
    pending.delete()

    return render(request, "accounts/verify_success.html")
