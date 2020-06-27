from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from .models import Expense
from django.contrib.auth.decorators import login_required
from expenses.forms import ExpenseForm
from django.db.models import Q


@login_required(login_url='login')
def expense_form(request, pk=0):
    if request.method == "POST":
        if pk == 0:
            form = ExpenseForm(request.POST, request.FILES)
        else:
            expense = Expense.objects.get(id=pk)
            form = ExpenseForm(request.POST, request.FILES, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        if pk == 0:
            form = ExpenseForm()
        else:
            expense = Expense.objects.get(id=pk)
            form = ExpenseForm(instance=expense)
        return render(request, "expenses/expense_form.html", {'form': form})

    return render(request, "expenses/expense_form.html", {'form': form})


@login_required(login_url='login')
def delete(request, pk):
    expense = Expense.objects.get(id=pk)
    expense.delete()
    return redirect('dashboard')
