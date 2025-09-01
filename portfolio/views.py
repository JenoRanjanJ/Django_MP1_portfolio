from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Project, Skill, ContactMessage
from .forms import ProjectForm

# Helpers
class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

# CBVs: Gallery and Detail
class ProjectListView(ListView):
    model = Project
    template_name = "portfolio/project_list.html"
    context_object_name = "projects"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["skills"] = Skill.objects.all()
        return ctx

class ProjectDetailView(DetailView):
    model = Project
    template_name = "portfolio/project_detail.html"
    context_object_name = "project"

# CRUD for admin/staff only
class ProjectCreateView(StaffRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "portfolio/project_form.html"
    success_url = reverse_lazy("project_list")

class ProjectUpdateView(StaffRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "portfolio/project_form.html"
    success_url = reverse_lazy("project_list")

class ProjectDeleteView(StaffRequiredMixin, DeleteView):
    model = Project
    template_name = "portfolio/project_confirm_delete.html"
    success_url = reverse_lazy("project_list")

# Manual contact form (HTML form + email validation in view)
def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()

        # Validate simple required fields
        if not name or not email or not message:
            messages.error(request, "All fields are required.")
            return render(request, "portfolio/contact.html", {"name": name, "email": email, "message": message})

        # Email validation
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Please enter a valid email address.")
            return render(request, "portfolio/contact.html", {"name": name, "email": email, "message": message})

        # Save message
        ContactMessage.objects.create(name=name, email=email, message=message)
        messages.success(request, "Thanks! Your message has been sent.")
        return redirect("contact")

    return render(request, "portfolio/contact.html")
