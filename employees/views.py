from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Employee
from jobs.models import Job
from django.contrib.auth.decorators import login_required
from .forms import EmployeeForm
from django.db.models import Q


@login_required(login_url='login')
def index(request):
    q = ''
    employees = Employee.objects.order_by(
        '-date_created').filter(deleted=False)
    if 'q' in request.GET:
        q = request.GET['q']
        employees = employees.filter(
            Q(name__icontains=q) |
            Q(phone__icontains=q) |
            Q(cnic__icontains=q)
        ).distinct()

    paginator = Paginator(employees, 10)
    page = request.GET.get('page')
    paged_employees = paginator.get_page(page)
    context = {
        'employees': paged_employees,
        'query': q
    }
    return render(request, 'employees/index.html', context)


@login_required(login_url='login')
def employee(request, pk):
    q = ''
    employee = Employee.objects.get(id=pk)
    jobs = employee.job_set.all().order_by('-date_created')
    total_jobs = jobs.count()
    if 'q' in request.GET:
        q = request.GET['q']
        jobs = jobs.filter(
            Q(date_created__icontains=q) |
            Q(id__icontains=q)
        ).distinct()
    paginator = Paginator(jobs, 10)
    page = request.GET.get('page')
    paged_jobs = paginator.get_page(page)

    context = {
        'employee': employee,
        'jobs': paged_jobs,
        'total_jobs': total_jobs,
        'query': q
    }
    return render(request, 'employees/employee.html', context)


@login_required(login_url='login')
def employee_form(request, pk=0):
    if request.method == "POST":
        if pk == 0:
            phone = request.POST['phone']
            try:
                e = Employee.objects.get(phone=phone)
                e.deleted = False
                e.save()
            except Employee.DoesNotExist:
                e = None
            if e:
                form = EmployeeForm(request.POST, instance=e)
            else:
                form = EmployeeForm(request.POST)

        else:
            employee = Employee.objects.get(id=pk)
            form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employees')
    else:
        if pk == 0:
            form = EmployeeForm()
        else:
            employee = Employee.objects.get(id=pk)
            form = EmployeeForm(instance=employee)
        return render(request, "employees/employee_form.html", {'form': form})

    return render(request, "employees/employee_form.html", {'form': form})


@login_required(login_url='login')
def delete(request, pk):
    employee = Employee.objects.get(id=pk)
    employee.deleted = True
    employee.save()
    return redirect('employees')
