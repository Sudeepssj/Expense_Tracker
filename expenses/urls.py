from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),

    path('expense/add/', views.add_expense_get, name='add_expense_get'),
    path('expense/add/post/', views.add_expense_post, name='add_expense_post'),

    path('expenses/', views.expense_list_get, name='expense_list'),
    
    path("expense/edit/", views.edit_expense_post, name="expense_edit"),

    # path('expense/delete/', views.expense_delete_post, name='expense_delete'),
    path('summary/', views.monthly_summary_get, name='monthly_summary'),
    # ✅ AJAX
    path('ajax/filter/', views.expense_filter_ajax, name='expense_filter_ajax'),
    
]
