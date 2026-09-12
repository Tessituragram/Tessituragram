from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.views.generic import TemplateView
from .forms import ContactForm


def home(request):
    return render(request, "pages/home.html")


class AboutView(TemplateView):
    template_name = "pages/static_page.html"
    extra_context = {
        "page_title": "About",
        "content": ["This is the about page."],
    }


class InstructionsView(TemplateView):
    template_name = "pages/static_page.html"
    extra_context = {
        "page_title": "Instructions",
        "content": [
            "Here are instructions for creating MIDI files and using the website."
        ],
    }


class MethodologyView(TemplateView):
    template_name = "pages/static_page.html"
    extra_context = {
        "page_title": "Methodology",
        "content": ["Here is our methodology."],
    }


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]

            email_msg = EmailMessage(
                subject=f"Contact form: {subject}",
                body=f"From: {name} ({email})\n\n{message}",
                from_email="contact@tessituragram.com",
                to=["contact@tessituragram.com"],
                reply_to=[email],
            )
            email_msg.send()
            return redirect("contact_success")
    else:
        form = ContactForm()

    return render(request, "pages/contact.html", {"form": form})


def contact_success(request):
    return render(request, "pages/contact_success.html")
