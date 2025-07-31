# core/views.py
from django.shortcuts import render, redirect
from .forms import JobForm, ApplicationForm, CustomUserCreationForm
from .models import Job, Application
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Registration
def register(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    return render(request, 'register.html', {'form': form})

# Role-based dashboard
@login_required
def dashboard(request):
    if request.user.is_employer:
        jobs = Job.objects.filter(posted_by=request.user)
        return render(request, 'employer_dashboard.html', {'jobs': jobs})
    else:
        applications = Application.objects.filter(applicant=request.user)
        return render(request, 'applicant_dashboard.html', {'applications': applications})

@login_required
def post_job(request):
    if not request.user.is_employer:
        return redirect('dashboard')  # Optional: prevent access for non-employers

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            return redirect('dashboard')
    else:
        form = JobForm()

    return render(request, 'post_job.html', {'form': form})


# Job listing & search
def job_list(request):
    query = request.GET.get('q')
    jobs = Job.objects.all()
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(company_name__icontains=query) |
            Q(location__icontains=query)
        )
    return render(request, 'job_list.html', {'jobs': jobs})

# Job detail and apply
@login_required
def apply_job(request, job_id):
    job = Job.objects.get(id=job_id)
    form = ApplicationForm()
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.job = job
            app.applicant = request.user
            app.save()
            return redirect('dashboard')
    return render(request, 'apply_job.html', {'form': form, 'job': job})
