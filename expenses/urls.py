from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),

    path('expense/add/', views.add_expense_get, name='add_expense_get'),
    path('expense/add/post/', views.add_expense_post, name='add_expense_post'),

   
    
    path("expense/edit/", views.edit_expense_post, name="expense_edit"),

   
    path('summary/', views.monthly_summary_get, name='monthly_summary'),
    # ✅ AJAX
    

    path('expenses/', views.expense_list_get, name='expense_list'),
    path('expenses/filter/', views.expense_filter_ajax, name='expense_filter_ajax'),
    path('expenses/edit/', views.expense_edit_ajax, name='expense_edit_ajax'),
    path('expenses/delete/', views.expense_delete_ajax, name='expense_delete_ajax'),

    path("summary/ajax/", views.monthly_summary_ajax, name="monthly_summary_ajax"),


]
    