from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, FormView, CreateView, DeleteView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from . import forms
from . import models
from django.db.models import Sum
from django.utils import timezone

# Create your views here.
today = timezone.localdate()


class Login(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = AuthenticationForm


class Logout(LogoutView):
    next_page = reverse_lazy('account:login')


class HomeView(TemplateView, LoginRequiredMixin):
    login_url = 'login'
    redirect_field_name = '/login/'
    template_name = 'accounts/account_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account_header'] = 'Dashboard'
        return context


def signup(request):

    if request.method == 'POST':
        user_form = forms.SignUpForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            return HttpResponseRedirect(reverse('account:profile'))
    else:
        user_form = forms.SignUpForm()

    return render(request, 'accounts/signup.html', {'user_form': user_form})


def update(request):

    if request.method == 'POST':
        user_form = forms.UpdateUserForm(request.POST, instance=models.UserProfile.objects.get(user__exact=request.user))
        user_base_form = forms.UpdateUserBaseForm(data=request.POST, instance=request.user)
        if user_form.is_valid():
            base_user = user_base_form.save()
            base_user.save()

            user = user_form.save()
            if 'profile_pic' in request.FILES:
                user.profile_pic = request.FILES['profile_pic']
            user.save()
            return HttpResponseRedirect(reverse('account:profile'))
    else:
        user_form = forms.UpdateUserForm(instance=models.UserProfile.objects.get(user__exact=request.user))
        user_base_form = forms.UpdateUserBaseForm(instance=request.user)

    return render(request, 'accounts/personalInfo.html', {'user_form': user_form, 'user_base_form': user_base_form})


# Now For Utilities


class ExpendListView(ListView):
    model = models.Expend
    template_name = 'expend/expend_list.html'
    ordering = ['-added_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expend_list_user'] = models.Expend.objects.filter(
            by_user__exact=self.request.user.username).order_by('added_date')
        context['sum_user_expend_amount'] = models.Expend.objects.filter(
            by_user__exact=self.request.user.username).aggregate(
            Sum('expend_amount')).get('expend_amount__sum', 0.00)
        context['sum_user_expend_amount_verified'] = models.Expend.objects.filter(
            by_user__exact=self.request.user.username,
            verified__exact='yes').aggregate(Sum('expend_amount')).get('expend_amount__sum', 0.00)
        context['sum_user_expend_amount_unverified'] = models.Expend.objects.filter(
            by_user__exact=self.request.user.username,
            verified__exact='no').aggregate(
            Sum('expend_amount')).get('expend_amount__sum', 0.00)
        context['sum_expend_amount'] = models.Expend.objects.aggregate(Sum('expend_amount')).get('expend_amount__sum', 0.00)
        context['sum_expend_amount_verified'] = models.Expend.objects.filter(verified__exact='yes').aggregate(
            Sum('expend_amount')).get('expend_amount__sum', 0.00)
        context['sum_expend_amount_unverified'] = models.Expend.objects.filter(verified__exact='no').aggregate(
            Sum('expend_amount')).get('expend_amount__sum', 0.00)
        return context


class ExpendListViewByDate(ListView):

    def get(self, request, *args, **kwargs):
        date = kwargs['date']
        context = {
            'filter_by_time': True,
            'filter_date_user': models.Expend.objects.filter(by_user__exact=request.user.username,
                                                             added_date__date=date),
            'sum_user_expend_amount': models.Expend.objects.filter(by_user__exact=self.request.user.username
                                                                   , added_date__date=date).aggregate(
                Sum('expend_amount')).get('expend_amount__sum', 0.00),
            'sum_user_expend_amount_verified': models.Expend.objects.filter(by_user__exact=self.request.user.username,
                                                                            added_date__date=date,
                                                                            verified__exact='yes').aggregate(
                Sum('expend_amount')).get('expend_amount__sum', 0.00),
            'sum_user_expend_amount_unverified': models.Expend.objects.filter(by_user__exact=self.request.user.username,
                                                                              added_date__date=date,
                                                                              verified__exact='no').aggregate(
                Sum('expend_amount')).get('expend_amount__sum', 0.00),
            'sum_expend_amount': models.Expend.objects.filter(verified__exact='yes', added_date__date=date).aggregate(
                Sum('expend_amount')).get('expend_amount__sum', 0.00),
            'sum_expend_amount_verified': models.Expend.objects.filter(verified__exact='yes',
                                                                       added_date__date=date).aggregate(
                Sum('expend_amount')).get('expend_amount__sum', 0.00),
            'sum_expend_amount_unverified': models.Expend.objects.filter(verified__exact='no', added_date__date=date
                                                                         ).aggregate(
                Sum('expend_amount')).get('expend_amount__sum', 0.00),

        }
        return render(request, 'expend/expend_list.html', context=context)


class ExpendListViewByToday(ListView):

    def get(self, request, *args, **kwargs):
        context = {
            'filter_by_time': True,
            'filter_date_user': models.Expend.objects.filter(by_user__exact=request.user.username,
                                                             added_date__date=today),
            'sum_user_expend_amount': models.Expend.objects.filter(by_user__exact=self.request.user.username
                                                                   , added_date__date=today).aggregate(
                Sum('expend_amount')).get('expend_amount__sum', 0.00),
            'sum_user_expend_amount_verified': models.Expend.objects.filter(by_user__exact=self.request.user.username,
                                                                            added_date__date=today,
                                                                            verified__exact='yes').aggregate(
                Sum('expend_amount')).get('expend_amount__sum', 0.00),
            'sum_user_expend_amount_unverified': models.Expend.objects.filter(by_user__exact=self.request.user.username,
                                                                              added_date__date=today,
                                                                              verified__exact='no').aggregate(
                Sum('expend_amount')).get('expend_amount__sum', 0.00),
            'sum_expend_amount': models.Expend.objects.filter(verified__exact='yes', added_date__date=today).aggregate(
                Sum('expend_amount')).get('expend_amount__sum', 0.00),
            'sum_expend_amount_verified': models.Expend.objects.filter(verified__exact='yes',
                                                                       added_date__date=today).aggregate(
                Sum('expend_amount')).get('expend_amount__sum', 0.00),
            'sum_expend_amount_unverified': models.Expend.objects.filter(verified__exact='no', added_date__date=today
                                                                         ).aggregate(
                Sum('expend_amount')).get('expend_amount__sum', 0.00),

        }
        return render(request, 'expend/expend_list.html', context=context)


class ExpendListViewByYear(ListView):

    def get(self, request, *args, **kwargs):
        year = kwargs['year']
        context = {
            'filter_by_time': True,
            'filter_date_user': models.Expend.objects.filter(by_user__exact=request.user.username,
                                                             added_date__year=year),
            'sum_user_expend_amount': models.Expend.objects.filter(by_user__exact=self.request.user.username
                                                                   , added_date__year=year).aggregate(
                Sum('expend_amount')).get('expend_amount__sum', 0.00),
            'sum_user_expend_amount_verified': models.Expend.objects.filter(by_user__exact=self.request.user.username,
                                                                            added_date__year=year,
                                                                            verified__exact='yes').aggregate(
                Sum('expend_amount')).get('expend_amount__sum', 0.00),
            'sum_user_expend_amount_unverified': models.Expend.objects.filter(by_user__exact=self.request.user.username,
                                                                              added_date__year=year,
                                                                              verified__exact='no').aggregate(
                Sum('expend_amount')).get('expend_amount__sum', 0.00),
            'sum_expend_amount': models.Expend.objects.filter(verified__exact='yes', added_date__date=year).aggregate(
                Sum('expend_amount')).get('expend_amount__sum', 0.00),
            'sum_expend_amount_verified': models.Expend.objects.filter(verified__exact='yes',
                                                                       added_date__year=year).aggregate(
                Sum('expend_amount')).get('expend_amount__sum', 0.00),
            'sum_expend_amount_unverified': models.Expend.objects.filter(verified__exact='no', added_date__year=year
                                                                         ).aggregate(
                Sum('expend_amount')).get('expend_amount__sum', 0.00),

        }
        return render(request, 'expend/expend_list.html', context=context)


class ExpendListViewByMonth(ListView):

    def get(self, request, *args, **kwargs):
        year = kwargs['year']
        month = kwargs['month']
        context = {
            'filter_by_time': True,
            'filter_date_user': models.Expend.objects.filter(by_user__exact=request.user.username,
                                                             added_date__year=year, added_date__month=month),
            'sum_user_expend_amount': models.Expend.objects.filter(by_user__exact=self.request.user.username
                                                                   , added_date__year=year,
                                                                   added_date__month=month).aggregate(
                Sum('expend_amount')).get('expend_amount__sum', 0.00),
            'sum_user_expend_amount_verified': models.Expend.objects.filter(by_user__exact=self.request.user.username,
                                                                            added_date__year=year,
                                                                            added_date__month=month,
                                                                            verified__exact='yes').aggregate(
                Sum('expend_amount')).get('expend_amount__sum', 0.00),
            'sum_user_expend_amount_unverified': models.Expend.objects.filter(by_user__exact=self.request.user.username,
                                                                              added_date__year=year,
                                                                              added_date__month=month,
                                                                              verified__exact='no').aggregate(
                Sum('expend_amount')).get('expend_amount__sum', 0.00),
            'sum_expend_amount': models.Expend.objects.filter(verified__exact='yes', added_date__year=year,
                                                              added_date__month=month).aggregate(
                Sum('expend_amount')).get('expend_amount__sum', 0.00),
            'sum_expend_amount_verified': models.Expend.objects.filter(verified__exact='yes',
                                                                       added_date__year=year,
                                                                       added_date__month=month).aggregate(
                Sum('expend_amount')).get('expend_amount__sum', 0.00),
            'sum_expend_amount_unverified': models.Expend.objects.filter(verified__exact='no', added_date__year=year,
                                                                         added_date__month=month).aggregate(
                Sum('expend_amount')).get('expend_amount__sum', 0.00),
        }
        return render(request, 'expend/expend_list.html', context=context)


class ExpendDetailView(DetailView):
    model = models.Expend
    template_name = 'expend/expend_detail.html'
    context_object_name = 'expend'


class ExpendUpdateView(UpdateView):
    model = models.Expend
    template_name = 'expend/expend_form.html'
    success_url = ''
    context_object_name = 'form'
    fields = ('source_fund', 'source_amount', 'expend_in', 'expend_amount', 'description', 'verified')


class ExpendDeleteView(DeleteView):
    model = models.Expend
    success_url = reverse_lazy('account:expend')
    template_name = 'expend/expend_confirm_delete.html'
    context_object_name = 'expend'


def create_expend(request):
    if request.method == 'POST':
        expend_form = forms.ExpendCreateForm(data=request.POST)
        if expend_form.is_valid():
            add = expend_form.save(commit=False)
            add.by_user = request.user.username
            add.save()
            return HttpResponseRedirect(reverse('account:expend'))
    else:
        expend_form = forms.ExpendCreateForm
    return render(request, 'expend/expend_form.html', {'form': expend_form})
