# core/views.py
from django.shortcuts import render, redirect
from .forms import JobForm, ApplicationForm, CustomUserCreationForm
from .models import Job, Application
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden

@login_required
def manage_applications(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if job.posted_by != request.user:
        return HttpResponseForbidden("You are not allowed to view this.")

    if request.method == 'POST':
        app_id = request.POST.get('app_id')
        action = request.POST.get('action')

        application = get_object_or_404(Application, id=app_id, job=job)
        if action == 'approve':
            application.status = 'approved'
        elif action == 'reject':
            application.status = 'rejected'
        application.save()

    applications = Application.objects.filter(job=job)
    return render(request, 'manage_applications.html', {
        'job': job,
        'applications': applications,
    })


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
        status_filter = request.GET.get('status')
        applications = Application.objects.filter(applicant=request.user)
        if status_filter in ['pending', 'approved', 'rejected']:
            applications = applications.filter(status=status_filter)
        return render(request, 'applicant_dashboard.html', {
            'applications': applications,
            'selected_status': status_filter
        })


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
