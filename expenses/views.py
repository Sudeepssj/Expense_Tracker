from datetime import datetime
from decimal import Decimal
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from expenses.models import Category, Expense
from django.db.models import Sum
from django.http import JsonResponse
from django.db.models import Q





@login_required
def dashboard(request):
    return render(request, 'expenses/dashboard.html')


@login_required
def add_expense_get(request):
    categories = Category.objects.all()
    return render(request, 'expenses/add_expense.html', {'categories': categories})


@login_required
def add_expense_post(request):
    category_id = request.POST.get('category', '').strip()
    new_category = request.POST.get('new_category', '').strip()
    amount_raw = request.POST.get('amount', '').strip()
    date = request.POST.get('date')
    description = request.POST.get('description', '')

    # validate required fields
    if not amount_raw or not date:
        return redirect('expenses/add_expense_get')

    try:
        amount = Decimal(amount_raw)
    except:
        return redirect('expenses/add_expense_get')

    # determine category
    if new_category:
        category, created = Category.objects.get_or_create(
            name=new_category.strip()
        )
    elif category_id:
        category = Category.objects.get(id=category_id)
    else:
        return redirect('expenses/add_expense_get')

    # ✅ ALWAYS create expense
    Expense.objects.create(
        user=request.user,
        category=category,
        amount=amount,
        date=date,
        description=description
    )

    return redirect('expense_list')


# @login_required
# def expense_list_get(request):
#     expenses = Expense.objects.filter(user=request.user).order_by('-date')
#     return render(request, 'expenses/expense_list.html', {'expenses': expenses})


# @login_required
# def expense_delete_post(request):
#     if request.method == 'POST':
#         expense_id = request.POST.get('expense_id')
#         Expense.objects.filter(id=expense_id, user=request.user).delete()
#     return redirect('expense_list')
@login_required
def edit_expense_post(request):
    if request.method == "POST":
        expense_id = request.POST.get("expense_id")

        try:
            expense = Expense.objects.get(
                id=expense_id,
                user=request.user   # 🔐 security: only own expense
            )
        except Expense.DoesNotExist:
            return redirect("expense_list")

        category_id = request.POST.get("category")
        amount = request.POST.get("amount")
        date = request.POST.get("date")
        description = request.POST.get("description")

        if category_id:
            expense.category = Category.objects.get(id=category_id)

        if amount:
            expense.amount = amount

        if date:
            expense.date = date

        expense.description = description
        expense.save()

    return redirect("expense_list")



@login_required
def monthly_summary_get(request):
    year = request.GET.get('year')
    month = request.GET.get('month')

    expenses = Expense.objects.filter(user=request.user)

    if year and month:
        try:
            year = int(year)
            month = int(month)
            expenses = expenses.filter(
                date__year=year,
                date__month=month
            )
        except ValueError:
            year = None
            month = None

    total_amount = expenses.aggregate(
        total=Sum('amount')
    )['total'] or 0

    category_summary = expenses.values(
        'category__name'
    ).annotate(
        total=Sum('amount')
    ).order_by('-total')

    # prepare data for chart
    labels = [item['category__name'] for item in category_summary]
    data = [float(item['total']) for item in category_summary]

    context = {
        'total_amount': total_amount,
        'category_summary': category_summary,
        'labels': labels,
        'data': data,
        'year': year,
        'month': month,
        'months': range(1, 13),
    }

    return render(request, 'expenses/monthly_summary.html', context)




@login_required
def expense_list_get(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    categories = Category.objects.all()

    return render(
        request,
        'expenses/expense_list.html',
        {
            'expenses': expenses,
            'categories': categories
        }
    )


@login_required
def expense_filter_ajax(request):
    expenses = Expense.objects.filter(user=request.user)

    search = request.GET.get('search', '')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if search:
        expenses = expenses.filter(
            Q(category__name__icontains=search) |
            Q(description__icontains=search)
        )

    if start_date:
        expenses = expenses.filter(date__gte=start_date)

    if end_date:
        expenses = expenses.filter(date__lte=end_date)

    data = []
    for exp in expenses.order_by('-date'):
        data.append({
            'id': exp.id,
            'date': exp.date.strftime('%b %d, %Y'),
            'raw_date': exp.date.strftime('%Y-%m-%d'),  # ✅ ADD THIS
            'category': exp.category.name,
            'category_id': exp.category.id,
            'amount': str(exp.amount),
            'description': exp.description
        })


    return JsonResponse({'expenses': data})


from datetime import datetime
from decimal import Decimal
from django.http import JsonResponse

@login_required
def expense_edit_ajax(request):
    if request.method == "POST":
        expense = Expense.objects.get(
            id=request.POST.get("expense_id"),
            user=request.user
        )

        expense.category_id = request.POST.get("category")
        expense.amount = Decimal(request.POST.get("amount"))

        # ✅ convert string → date object
        expense.date = datetime.strptime(
            request.POST.get("date"),
            "%Y-%m-%d"
        ).date()

        expense.description = request.POST.get("description")
        expense.save()

        return JsonResponse({
            "success": True,
            "id": expense.id,
            "date": expense.date.strftime('%b %d, %Y'),
            "category": expense.category.name,
            "amount": str(expense.amount),
            "description": expense.description
        })



@login_required
def expense_delete_ajax(request):
    if request.method == "POST":
        Expense.objects.filter(
            id=request.POST.get("expense_id"),
            user=request.user
        ).delete()

        return JsonResponse({"success": True})



@login_required
def monthly_summary_ajax(request):
    year = request.GET.get("year")
    month = request.GET.get("month")

    expenses = Expense.objects.filter(user=request.user)

    if year:
        expenses = expenses.filter(date__year=year)

    if month:
        expenses = expenses.filter(date__month=month)

    total_amount = expenses.aggregate(total=Sum("amount"))["total"] or 0

    category_summary = expenses.values(
        "category__name"
    ).annotate(
        total=Sum("amount")
    ).order_by("-total")

    labels = []
    values = []

    for item in category_summary:
        labels.append(item["category__name"])
        values.append(float(item["total"]))

    return JsonResponse({
        "total": float(total_amount),
        "labels": labels,
        "values": values
    })
