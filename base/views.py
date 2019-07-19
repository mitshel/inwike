import os
import base64

from django.views.generic import TemplateView
from django.urls import reverse, reverse_lazy
from django.template.context_processors import csrf
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, Http404

from functools import wraps

from conn1c.views import conn1c

scope_names = {0:'Знания, умения, мастерство', 1:'Коммуникабельность',2:'Ответственность', 3:'Активность', 4:'Инновационность', 5:'Предприимчивость'}
scope_rat_names = {0:'knlds',1:'socs', 2:'resps', 3:'activs', 4:'innovs', 5:'ents'}
scope_icons = {0:'fa-graduation-cap', 1:'fa-users',2:'fa-flag', 3:'fa-trophy', 4:'fa-cog', 5:'fa-truck'}
scope_parts = {0: [
	                'Дипломы о среднем/высшем образовании с отличем/без',
	                'Научные звания',
	                'Обучение на курсах повышения квалификации',
	                'Сертификаты',
	                'Производственное обучение (слушатель)', ],
               1: [
                    'Наставничество (приказы о стажировке)',
                    'Производственное обучение (как преподаватель)',
                    'Участие в проектных группах',
                    'Оценка коллективом (анкетирование)',
                    'Оценка руководителя', ],
               2: [
                    'Замечания, предупреждения, дисциплинарные взыскания',
                    'Данные СКУД (время входа/выхода)',
                    'Данные СДОУ',
                    'KPI',
                    'Протоколы проверки знаний (корпоративные регламенты, охрана труда)',
                    'Стаж в комании', ],
               3: [
                    'Участие в конкурсах',
                    'Участие в общественных, спортивных мероприятиях',
                    'Значок ГТО',
                    'Награды',
                    'Участие в волентерских образованиях', ],
               4: [
                    'Рационализаторские/Кайдзен предложения',
                    'Вклад в улучшение внутренних процессов',
                    'Вклад в улучшение внешних процессов',
                    'Участие инициация прорывных проектов', ],
               5: [
                    'Оценка руководителя', ]
            }

# Create your views here.
def base_login(function=None):
    def decorator(func):
        @wraps(func)
        def _wrapped_view(request, *args, **kwargs):
            if request.session.get('emp_uid', False):
                return func(request, *args, **kwargs)
            return redirect(reverse_lazy('base:login'))
        return _wrapped_view

    if function:
        return decorator(function)
    return decorator

def is_logged_on(request):
    if request.session.get('emp_uid', False):
        return True
    return False

def base_processor(request):
    args={}
    args['logged_on'] = is_logged_on(request)
    args['emp_uid'] = request.session.get('emp_uid', 'None')
    return args

def loginView(request):
    args = {}
    args.update(csrf(request))
    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        return render(request, 'base_login.html', args)

    connection = conn1c()
    emp_uid = connection.get_uid(username, password)

    if not emp_uid:
        return render(request, 'base_login.html', args)

    request.session['emp_uid'] = emp_uid
    return redirect(reverse('base:home'))

def nofoto(request):
    if os.path.exists(settings.NOPHOTO_PATH):
        response = HttpResponse()
        response["Content-Type"] = 'image/jpeg'
        f = open(settings.NOPHOTO_PATH, "rb")
        response.write(f.read())
        f.close()
        return response
    else:
        raise Http404

def get_photo(request):
    data1с = conn1c()
    emp_uid = request.session.get('emp_uid', '')
    s = data1с.get_photo(emp_uid)

    if s:
        dstr = base64.b64decode(s)
        response = HttpResponse()
        response["Content-Type"] = 'image/jpeg'
        response.write(dstr)
        return response

    return nofoto(request)

def upload_photo(request):
    print('POST=',request.POST)
    return redirect(reverse('base:home'))

@base_login()
def logoutView(request):
    try:
        del request.session['emp_uid']
    except KeyError:
        pass
    args = {}
    return redirect(reverse('base:login'))

class HomeView(TemplateView):
    template_name = 'base_hello.html'

class ProfileView(TemplateView):
    template_name = 'base_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        data_rating = conn1c()
        # '87433449-7cc0-11e2-9368-001b11b25590'
        emp_uid = self.request.session.get('emp_uid', '')
        emp_rating = data_rating.emp_rating(emp_uid)
        emp_data =  data_rating.emp_data(emp_uid)

        context['data'] = emp_rating
        context['emp'] = emp_data
        context['fio'] = 'Малютина Ирина Иосифовна'
        context['position'] = 'Бухгалтер-экономист'
        return context

class ScopeView(TemplateView):
    template_name = 'base_scope.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scope_id = kwargs['scope_id']

        data_rating = conn1c()
        emp_uid = self.request.session.get('emp_uid', '')
        emp_rating = data_rating.emp_rating(emp_uid)
        emp_data =  data_rating.emp_data(emp_uid)
        context['data'] = emp_rating
        context['emp'] = emp_data
        context['scope_chart'] = emp_rating[scope_rat_names[scope_id]]
        context['scope_rating'] = context['scope_chart'][-1]
        context['scope_name'] = scope_names[scope_id]
        context['scope_icon'] = scope_icons[scope_id]
        context['scope_parts'] = scope_parts[scope_id]
        context['fio'] = 'Малютина Ирина Иосифовна'
        context['position'] = 'Бухгалтер-экономист'
        return context