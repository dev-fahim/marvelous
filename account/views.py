from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from . import forms
from . import models
from expend.models import Expend
import datetime
from django.db.models import Sum

# Create your views here.


class Login(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = AuthenticationForm


class Logout(LogoutView):
    next_page = reverse_lazy('account:login')


class HomeView(TemplateView, LoginRequiredMixin):
    login_url = 'login'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):
        now = datetime.datetime.now()
        if now.month == 1 or now.month == 3 or now.month == 5 or now.month == 7 or now.month == 8:
            total = [Expend.objects.filter(added_date__year=now.year, added_date__month=3, added_date__day=i + 1).aggregate(Sum('expend_amount')).get('expend_amount__sum', 0.00) for i in range(31)]
            dates = [i + 1 for i in range(31)]
            total_s = [
                Expend.objects.filter(added_date__year=now.year, added_date__month=3, added_date__day=i + 1).aggregate(
                    Sum('source_amount')).get('source_amount__sum', 0.00) for i in range(31)]
        else:
            total = [
                Expend.objects.filter(added_date__year=now.year, added_date__month=3, added_date__day=i + 1).aggregate(
                    Sum('expend_amount')).get('expend_amount__sum', 0.00) for i in range(30)]
            total_s = [
                Expend.objects.filter(added_date__year=now.year, added_date__month=3, added_date__day=i + 1).aggregate(
                    Sum('source_amount')).get('source_amount__sum', 0.00) for i in range(30)]
            dates = [i + 1 for i in range(30)]
        total_all_expend_amount = Expend.objects.filter(added_date__year=now.year, added_date__month=3).aggregate(Sum('expend_amount')).get('expend_amount__sum', 0.00)
        total_all_source_amount = Expend.objects.filter(added_date__year=now.year, added_date__month=3).aggregate(Sum('source_amount')).get('source_amount__sum', 0.00)

        utilized = total_all_expend_amount / total_all_source_amount * 100
        non_utilized = 100 - utilized
        context = {
            'total': total,
            'dates': dates,
            'total_s': total_s,
            'utilized': utilized,
            'non_utilized': non_utilized
        }
        return render(request, 'accounts/account_home.html', context)


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

    return render(request, 'accounts/signup.html', {'form': user_form})


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
