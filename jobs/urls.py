from django.urls import path
from . import views
from django.views.generic.base import TemplateView


app_name = 'jobs'

urlpatterns = [    
    #path('', TemplateView.as_view(template_name='jobs/vagas.html'), name='vagas'),
    path('', views.jobs_list, name='vagas'),
    path('<int:codigo>', views.job_detail , name='detail'),
]

