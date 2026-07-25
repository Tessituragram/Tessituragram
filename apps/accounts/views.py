from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from apps.records.models import Record
from urllib.parse import urlencode
from .forms import ProfileEditForm, SignUpForm, EmailChangeForm
from .models import PendingSignup, PendingEmailChange
from apps.records.columns import AVAILABLE_COLUMNS, DEFAULT_PROFILE_COLUMNS, get_display_columns


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
            return render(request, "registration/check_email.html", {"email": pending.email})
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
            profile_form = ProfileEditForm(request.POST, instance=request.user)
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
                pending = PendingEmailChange.objects.get(user=request.user)

                verify_url = request.build_absolute_uri(
                    reverse("verify_email_change", args=[pending.token])
                )
                send_mail(
                    subject="Confirm your new email — Tessituragram",
                    message=f"Click to confirm this email change: {verify_url}",
                    from_email=None,
                    recipient_list=[new_email],
                )
                return redirect("profile")

    records = Record.objects.filter(submitted_by=request.user, is_deleted=False)

    sort = request.GET.get("sort", "-created_at")
    if sort == "submitter":
        records = records.order_by("submitted_by__first_name", "submitted_by__last_name")
    elif sort == "-submitter":
        records = records.order_by("-submitted_by__first_name", "-submitted_by__last_name")
    elif sort.lstrip("-") in {key for key, *_ in AVAILABLE_COLUMNS} | {"title", "created_at"}:
        records = records.order_by(sort)

    selected_columns, display_columns = get_display_columns(request, DEFAULT_PROFILE_COLUMNS)

    querydict = {k: v for k, values in request.GET.lists() for v in values if v}
    active_filters = [(k, v) for k, values in request.GET.lists() for v in values if v]

    pending_email = PendingEmailChange.objects.filter(user=request.user).first()

    return render(request, "accounts/profile.html", {
        "profile_form": profile_form,
        "email_form": email_form,
        "records": records,
        "pending_email": pending_email,
        "current_sort": sort,
        "active_filters": active_filters,
        "all_columns": AVAILABLE_COLUMNS,
        "selected_columns": selected_columns,
        "display_columns": display_columns,
    })


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
    user.save()
    pending.delete()

    return render(request, "accounts/verify_success.html")
