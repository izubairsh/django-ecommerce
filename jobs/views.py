from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Job
from employees.models import Employee
from django.contrib.auth.decorators import login_required
from .forms import JobForm
from django.db.models import Q


@login_required(login_url='login')
def job_form(request, pk):
    if request.method == "POST":
        print(request)
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employees')
    else:
        employee = Employee.objects.get(id=pk)

        form = JobForm(initial={"employee": employee})
        return render(request, "jobs/job_form.html", {'form': form})

    return render(request, "jobs/job_form.html", {'form': form})


@login_required(login_url='login')
def job1_form(request, pk):
    if request.method == "POST":
        job = Job.objects.get(id=pk)
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('employees')
    else:
        job = Job.objects.get(id=pk)
        form = JobForm(instance=job)
        return render(request, "jobs/job_form.html", {'form': form})

    return render(request, "jobs/job_form.html", {'form': form})


@login_required(login_url='login')
def delete(request, pk):
    job = Job.objects.get(id=pk)
    job.delete()
    return redirect('employees')
