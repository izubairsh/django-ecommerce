from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Package
from django.contrib.auth.decorators import login_required
from .forms import PackageForm
from django.db.models import Q


@login_required(login_url='login')
def index(request):
    q = ''
    packages = Package.objects.all()
    if 'q' in request.GET:
        q = request.GET['q']
        packages = packages.filter(
            Q(name__icontains=q)
        ).distinct()

    paginator = Paginator(packages, 10)
    page = request.GET.get('page')
    paged_packages = paginator.get_page(page)
    context = {
        'packages': paged_packages,
        'query': q
    }
    return render(request, 'packages/index.html', context)


@login_required(login_url='login')
def package_form(request, pk=0):
    if request.method == "POST":
        if pk == 0:
            form = PackageForm(request.POST)
        else:
            package = Package.objects.get(id=pk)
            form = PackageForm(request.POST, instance=package)
        if form.is_valid():
            form.save()
            return redirect('packages')
    else:
        if pk == 0:
            form = PackageForm()
        else:
            package = Package.objects.get(id=pk)
            form = PackageForm(instance=package)
        return render(request, "packages/package_form.html", {'form': form})

    return render(request, "packages/package_form.html", {'form': form})


@login_required(login_url='login')
def delete(request, pk):
    package = Package.objects.get(id=pk)
    package.delete()
    return redirect('packages')
