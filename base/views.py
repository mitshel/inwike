from django.shortcuts import render
from django.views.generic import TemplateView

scope_names = {0:'Знания, умения, мастерство', 1:'Коммуникабельность',2:'Ответственность', 3:'Активность', 4:'Инновационность', 5:'Предприимчивость'}
scope_icons = {0:'fa-graduation-cap', 1:'fa-users',2:'fa-flag', 3:'fa-trophy', 4:'fa-cog', 5:'fa-truck'}

# Create your views here.
class HomeView(TemplateView):
    template_name = 'base_hello.html'

class ProfileView(TemplateView):
    template_name = 'base_profile.html'

class ScopeView(TemplateView):
    template_name = 'base_scope.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        scope_id = kwargs['scope_id']
        context['scope_name'] = scope_names[scope_id]
        context['scope_icon'] = scope_icons[scope_id]
        context['fio'] = 'Малютина Ирина Иосифовна'
        return context