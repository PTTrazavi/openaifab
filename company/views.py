from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
import logging
logger = logging.getLogger(__name__)
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required, permission_required
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
#from django.views.generic.edit import CreateView, UpdateView
import time, datetime
from django import forms
from django.db.models import Q

from .models import company, profile, project, staff, report
#staff dict
staff_dict = {"jonhuang":1, "jeremylai":2, "test1":3, "test2":4, "test3":5, "test4":6}
# Create your views here.
@login_required
def pw_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            logging.error('%s %s changed password.', request.user.pk, request.user.username)
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'company/pw_change.html', {'form': form})

#home page
@login_required
def home(request):
    logging.error('%s %s visited homepage.', request.user.pk, request.user.username)
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

###report###
class report_list(LoginRequiredMixin, generic.ListView):
    #model = report
    #ordering='-pk'
    paginate_by = 20

    def get_queryset(self):
        return report.objects.filter(staff_id=staff_dict[self.request.user.get_username()]).order_by('-pk')

class report_add(LoginRequiredMixin, generic.edit.CreateView):
    model = report
    fields = ['staff_id', 'date_app', 'date_start', 'date_end', 'work', 'status', 'b0', 'b1', 'b2']
    success_url = reverse_lazy('report_list')

    #set the initial value for dates
    def get_initial(self):
        staff_id_now = staff_dict[self.request.user.get_username()]
        return {'date_app': datetime.date.today(),
                'status': 'a',
                'staff_id': staff_id_now,
                'b0': get_object_or_404(staff, pk=staff_id_now).boss0,
                'b1': get_object_or_404(staff, pk=staff_id_now).boss1,
                'b2': get_object_or_404(staff, pk=staff_id_now).boss2
        }
    #make date_app readonly
    def get_form(self, form_class = None):
        form = super().get_form(form_class)
        form.fields['date_app'].widget = forms.DateInput(attrs={'readonly':True})
        CHOICES = [('a', '暫存'), ('b', '申請')]
        form.fields['status'].widget = forms.RadioSelect(choices=CHOICES)
        form.fields['b0'].widget = forms.TextInput(attrs={'type':'hidden'})
        form.fields['b1'].widget = forms.TextInput(attrs={'type':'hidden'})
        form.fields['b2'].widget = forms.TextInput(attrs={'type':'hidden'})
        return form

class report_update(LoginRequiredMixin, generic.edit.UpdateView):
    model = report
    fields = ['staff_id', 'date_app', 'date_start', 'date_end', 'work', 'status']
    success_url = reverse_lazy('report_list')

    #set the initial value for dates
    def get_initial(self):
        return {'date_app': datetime.date.today(),
                'status': 'a',
        }
    #make date_app readonly
    def get_form(self, form_class = None):
        form = super().get_form(form_class)
        form.fields['date_app'].widget = forms.DateInput(attrs={'readonly':True})
        CHOICES = [('a', '暫存'), ('b', '申請')]
        form.fields['status'].widget = forms.RadioSelect(choices=CHOICES)
        return form

class report_detail(LoginRequiredMixin, generic.DetailView):
    model = report
    #replace \n etc to <br>
    def get_context_data(self, **kwargs): #**kwargs are dict parameter
        context = super().get_context_data(**kwargs)
        context['work_br'] = context['report'].work
        for i in ["\r\n", "\n\r", "\n", "\r"]:
            context['work_br'] = context['work_br'].replace(i, '<br>')
        #get boss names
        if context['report'].b0 != 0:
            context['boss0'] = get_object_or_404(staff, pk=context['report'].b0).name
        else:
            context['boss0'] = '--'
        if context['report'].b1 != 0:
            context['boss1'] = get_object_or_404(staff, pk=context['report'].b1).name
        else:
            context['boss1'] = '--'
        if context['report'].b2 != 0:
            context['boss2'] = get_object_or_404(staff, pk=context['report'].b2).name
        else:
            context['boss2'] = '--'
        return context

class report_check_list(PermissionRequiredMixin, generic.ListView):
    permission_required = 'company.can_check_others'
    template_name = 'company/report_check_list.html'
    paginate_by = 20

    def get_queryset(self):
        return report.objects.filter(Q(b0=staff_dict[self.request.user.get_username()])
                                    |Q(b1=staff_dict[self.request.user.get_username()])
                                    |Q(b2=staff_dict[self.request.user.get_username()])).order_by('-pk')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['staff_id_now'] = staff_dict[self.request.user.get_username()]
        return context

class report_check_detail(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'company.can_check_others'
    model = report
    template_name = 'company/report_check_detail.html'
    #replace \n etc to <br>
    def get_context_data(self, **kwargs): #**kwargs are dict parameter
        context = super().get_context_data(**kwargs)
        context['work_br'] = context['report'].work
        for i in ["\r\n", "\n\r", "\n", "\r"]:
            context['work_br'] = context['work_br'].replace(i, '<br>')
        #get boss names
        if context['report'].b0 != 0:
            context['boss0'] = get_object_or_404(staff, pk=context['report'].b0).name
        else:
            context['boss0'] = '--'
        if context['report'].b1 != 0:
            context['boss1'] = get_object_or_404(staff, pk=context['report'].b1).name
        else:
            context['boss1'] = '--'
        if context['report'].b2 != 0:
            context['boss2'] = get_object_or_404(staff, pk=context['report'].b2).name
        else:
            context['boss2'] = '--'
        return context

from .forms import ReportcheckForm
@login_required
@permission_required('company.can_check_others')
def report_check(request, pk):
    if request.method == 'POST':
        item = get_object_or_404(report, pk=pk)
        form = ReportcheckForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            # approved case
            if form.cleaned_data['check'] == '1':
                # process boss checked date
                if item.b0 == staff_dict[request.user.get_username()]:
                    item.date_b0 = str(datetime.date.today())
                elif item.b1 == staff_dict[request.user.get_username()]:
                    item.date_b1 = str(datetime.date.today())
                elif item.b2 == staff_dict[request.user.get_username()]:
                    item.date_b2 = str(datetime.date.today())
                # process status
                for i, j in zip([item.b0, item.b1, item.b2],[item.date_b0, item.date_b1, item.date_b2]):
                    if not j and i != 0:
                        item.status = 'b'
                        break
                    else:
                        item.status = 'c'
                logging.error('%s %s approved report ID %s.', request.user.pk, request.user.username, pk)
            # rejected case
            else:
                item.date_b0 = None
                item.date_b1 = None
                item.date_b2 = None
                item.status = 'd'
                logging.error('%s %s rejected report ID %s.', request.user.pk, request.user.username, pk)
            item.save()
            return HttpResponseRedirect(reverse('report_check_list'))

    else:
        item = get_object_or_404(report, pk=pk)
        #replace \n etc to <br>
        work_br = item.work
        for i in ["\r\n", "\n\r", "\n", "\r"]:
            work_br = work_br.replace(i, '<br>')
        #get boss names
        if item.b0 != 0:
            boss0 = get_object_or_404(staff, pk=item.b0).name
        else:
            boss0 = '--'
        if item.b1 != 0:
            boss1 = get_object_or_404(staff, pk=item.b1).name
        else:
            boss1 = '--'
        if item.b2 != 0:
            boss2 = get_object_or_404(staff, pk=item.b2).name
        else:
            boss2 = '--'

        form = ReportcheckForm()
        content = {
                'report': item,
                'work_br': work_br,
                'form': form,
                'boss0': boss0,
                'boss1': boss1,
                'boss2': boss2,
        }
        return render(request, 'company/report_check.html', content)
