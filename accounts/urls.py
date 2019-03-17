from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [    
    path('sign-up/', views.UserCreate.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'), 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('sign-up/filter-tag/', views.filter_tag, name='filter-tag')
]

