from django.shortcuts import render
from django.http import JsonResponse, Http404
from DevJobs.src.StackOverflowJobs import Tags, SearchJobs
from DevJobs.src.Udemy import Cursos
from accounts.models import Profile

def get_competencias_user(request):
    profile = Profile.objects.get(username=request.user.username)
    comp = [p.nome for p in profile.competencias.all()]
    return comp


def jobs_list(request, page_num=None):
    page_num = 1 if not page_num or page_num < 0 else page_num
    context = {'jobs': ''}

    if not request.POST:
        if request.user.is_authenticated:
            comp = ' '.join(get_competencias_user(request))
            context['jobs'] = SearchJobs.jobs_similares(comp, -2)
            context['descricao'] = 'Vagas baseadas no seu perfil'
        else:
            context['jobs'] = SearchJobs.df_jobs.to_dict(orient='records')
            context['descricao'] = 'Vagas disponíveis'
    else:
        context['jobs'] = SearchJobs.jobs_similares(request.POST['search_jobs'], -2)
        context['descricao'] = 'Vagas baseadas na sua busca'

    context['page_num'] = page_num
    page_num = page_num - 1 if page_num > 1 else page_num
    context['n_pages'] = [x for x in range(page_num, page_num+7)]
    context['n_pages'] = ['-'] + context['n_pages'] if page_num == 1 else context['n_pages']

    min = (page_num-1) * 20
    max = min + 20
    context['jobs'] = context['jobs'][min:max]

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
    context['nao_competencias'] = []

    if request.user.is_authenticated:
        competencias = get_competencias_user(request)
        for t in context['job']['tags']:
            if t not in competencias:
                context['nao_competencias'].append(t)

    # Se não houver competencia compatível, obtem cursos similares para essas competencias
    competencias_curso = context['job']['tags'].copy()
    if context['nao_competencias']:
        competencias_curso += (context['nao_competencias'] * 3)
    context['cursos'] = Cursos.cursos_similares(' '.join(competencias_curso), 6)

    # Descobri as tags de cada curso
    for c in context['cursos']:
        desc_curso = c['description'] + c['title'] + c['what_learn']
        desc_curso += Cursos._processar_texto(desc_curso)
        c['tags'] = Cursos.descobrir_tags_do_curso(desc_curso)

    return render(request, 'jobs/vaga.html', context)