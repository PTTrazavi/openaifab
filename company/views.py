from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
import logging
logger = logging.getLogger(__name__)
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
#from django.views.generic.edit import CreateView, UpdateView
import time, datetime

from .models import company, profile, project
# Create your views here.
@login_required
def pw_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'company/pw_change.html', {'form': form})

#home page
@login_required
def home(request):
    logging.error('%s %s, Hello world openaifab in the log...', request.user.pk, request.user.username)
    return render(request, 'company/home.html')

###company###
class company_list(LoginRequiredMixin, generic.ListView):
    model = company
    paginate_by = 20
    ordering='name'

class company_add(LoginRequiredMixin, generic.edit.CreateView):
    model = company
    fields = '__all__'
    success_url = reverse_lazy('company_list')

class company_update(LoginRequiredMixin, generic.edit.UpdateView):
    model = company
    fields = '__all__'
    success_url = reverse_lazy('company_list')

class company_detail(LoginRequiredMixin, generic.DetailView):
    model = company

###profile###
class profile_add(LoginRequiredMixin, generic.edit.CreateView):
    model = profile
    fields = '__all__'
    #set the initial value for company
    def get_initial(self):
        return {'company': self.kwargs['cpk']}
    #set the url after completion
    def get_success_url(self):
        return reverse_lazy('company_detail', kwargs={'pk':self.kwargs['cpk']})

class profile_update(LoginRequiredMixin, generic.edit.UpdateView):
    model = profile
    fields = '__all__'
    #set the url after completion
    def get_success_url(self):
        return reverse_lazy('company_detail', kwargs={'pk':self.kwargs['cpk']})

class profile_detail(LoginRequiredMixin, generic.DetailView):
    model = profile

###project###
class project_list(LoginRequiredMixin, generic.ListView):
    model = project
    paginate_by = 20
    ordering='-pk'

class project_add(LoginRequiredMixin, generic.edit.CreateView):
    model = project
    fields = '__all__'
    success_url = reverse_lazy('project_list')
    #set the initial value for dates
    def get_initial(self):
        return {'date_start': datetime.date.today(),
                'date_update': datetime.date.today()
        }

class project_update(LoginRequiredMixin, generic.edit.UpdateView):
    model = project
    fields = ['company', 'name', 'product', 'member', 'date_update', 'status', 'detail', 'technical', 'sales']
    success_url = reverse_lazy('project_list')
    initial = {'date_update': datetime.date.today()}

class project_detail(LoginRequiredMixin, generic.DetailView):
    model = project
    #replace \n etc to <br>
    def get_context_data(self, **kwargs): #**kwargs are dict parameter
        context = super().get_context_data(**kwargs)
        context['detail_br'] = context['project'].detail
        for i in ["\r\n", "\n\r", "\n", "\r"]:
            context['detail_br'] = context['detail_br'].replace(i, '<br>')
        return context
