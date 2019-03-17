from django.shortcuts import render
from django.http import JsonResponse, Http404
from DevJobs.src.StackOverflowJobs import Tags, SearchJobs
from DevJobs.src.Udemy import Cursos
from accounts.models import Profile

def get_competencias_user(request):
    profile = Profile.objects.get(username=request.user.username)
    comp = [p.nome for p in profile.competencias.all()]
    print(comp)
    return comp


def jobs_list(request):
    context = {'jobs': ''}

    if not request.POST:
        if request.user.is_authenticated:
            comp = ' '.join(get_competencias_user(request))
            context['jobs'] = SearchJobs.jobs_similares(comp, 20)
            context['descricao'] = 'Vagas baseadas no seu perfil'
        else:
            context['jobs'] = SearchJobs.df_jobs.iloc[:20].to_dict(orient='records')
            context['descricao'] = 'Vagas disponíveis'
    else:
        context['jobs'] = SearchJobs.jobs_similares(request.POST['search_jobs'], 20)
        context['descricao'] = 'Vagas baseadas na sua busca'

    # Transforma as tags em lista
    for i, _ in enumerate(context['jobs']):
        context['jobs'][i]['tags'] = context['jobs'][i]['tags'].split(', ')

    return render(request, 'jobs/vagas.html', context)


def job_detail(request, codigo):
    try: SearchJobs.df_jobs.iloc[codigo]
    except IndexError: return Http404('Esta vaga não foi encontrada!')
    
    context = {'job': dict(SearchJobs.df_jobs.iloc[codigo])}
    context['job']['tags'] = context['job']['tags'].split(', ')

    # Verifica as competencias que o usuário não tem para a vaga.
    competencias = get_competencias_user(request)
    context['nao_competencias'] = []
    for t in context['job']['tags']:
        if t not in competencias:
            context['nao_competencias'].append(t)

    # Se não houver competencia compatível, obtem cursos similares para essas competencias
    competencias_curso = context['job']['tags'].copy()
    if context['nao_competencias']:
        competencias_curso += (context['nao_competencias'] * 3)
    context['cursos'] = Cursos.cursos_similares(' '.join(competencias_curso), 6)
    print('comp cursos', competencias_curso)

    # Descobri as tags de cada curso
    for c in context['cursos']:
        desc_curso = c['description'] + c['title'] + c['what_learn']
        desc_curso += Cursos._processar_texto(desc_curso)
        c['tags'] = Cursos.descobrir_tags_do_curso(desc_curso)

    return render(request, 'jobs/vaga.html', context)