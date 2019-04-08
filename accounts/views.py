from django.core import exceptions
from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView 
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django import forms
from django.contrib import messages
from django.http import JsonResponse
import json

from .models import Profile, Competencia
from .forms import ProfileForm
from DevJobs.settings import STACK_JOBS_DATA
from DevJobs.src.StackOverflowJobs import Tags



class UserCreate(CreateView):
    form_class = ProfileForm
    template_name='accounts/user_form.html'

    def get_context_data(self, **kwargs):
        context = super(UserCreate, self).get_context_data(**kwargs)

        with open(STACK_JOBS_DATA + 'tags_list.json') as file:
            context['tags'] = json.load(file)
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()

        for comp in form.cleaned_data['comp']:
            # Se a competência nao existir no BD, armazena.
            try:
                obj_comp = Competencia.objects.get(nome__iexact=comp)
            except:
                obj_comp = Competencia(nome=comp)
                obj_comp.save()

            user.competencias.add(obj_comp)

        user.save()

        return HttpResponseRedirect(reverse('accounts:login'))


def filter_tag(request):
    filtro = request.POST['filtro']
    response = {'tags': []}

    if not filtro:
        response['tags'] = Tags.df_tags.columns.tolist()
    else:
        response['tags'] = Tags.obter_tags_correlacionadas(filtro)

    return JsonResponse(response)
