from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.shortcuts import render
from . import forms
from . import models
from django.db.models import Sum
from django.utils import timezone
import time
from .helpers import get_month_name
from django.db.models import Q
import re
today = timezone.localdate()
# Create your views here.


class ExpendListView(ListView):
    model = models.Expend
    template_name = 'expend/expend_list.html'
    ordering = ['-added_date']
    context_object_name = 'filter_date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_date_user'] = models.Expend.objects.filter(
            by_user__exact=self.request.user.username).order_by('-added_date')
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
            'filter_by_time': date,
            'filter_date': models.Expend.objects.filter(added_date__date=date).order_by('-added_date'),
            'filter_date_user': models.Expend.objects.filter(by_user__exact=request.user.username,
                                                             added_date__date=date).order_by('-added_date'),
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
            'filter_by_time': timezone.localdate(),
            'filter_date': models.Expend.objects.filter(added_date__date=today).order_by('-added_date'),
            'filter_date_user': models.Expend.objects.filter(by_user__exact=request.user.username,
                                                             added_date__date=today).order_by('-added_date'),
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
            'filter_by_time': year,
            'filter_date': models.Expend.objects.filter(added_date__year=year).order_by('-added_date'),
            'filter_date_user': models.Expend.objects.filter(by_user__exact=request.user.username,
                                                             added_date__year=year).order_by('-added_date'),
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
            'sum_expend_amount': models.Expend.objects.filter(verified__exact='yes', added_date__year=year).aggregate(
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
            'filter_by_time': '{}, {}'.format(get_month_name(num_of_month=month), year),
            'filter_date': models.Expend.objects.filter(added_date__year=year,
                                                        added_date__month=month).order_by('-added_date'),
            'filter_date_user': models.Expend.objects.filter(by_user__exact=request.user.username,
                                                             added_date__year=year,
                                                             added_date__month=month).order_by('-added_date'),
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
    success_url = reverse_lazy('expenditure:expend')
    template_name = 'expend/expend_confirm_delete.html'
    context_object_name = 'expend'


def create_expend(request):
    if request.method == 'POST':
        expend_form = forms.ExpendCreateForm(data=request.POST)
        if expend_form.is_valid():
            add = expend_form.save(commit=False)
            add.by_user = request.user.username
            add.save()
            return HttpResponseRedirect(reverse('expenditure:expend'))
    else:
        expend_form = forms.ExpendCreateForm
    return render(request, 'expend/expend_form.html', {'form': expend_form})


def expenditure_filter_list_by_year_view(request):
    if request.method == 'POST':
        filter_form = forms.ExpendFilterYearForm(data=request.POST)
        if filter_form.is_valid():
            year = filter_form.cleaned_data['year']
            if year == '':
                year = None
            context = {
                        'form': filter_form,
                        'filter_by_time': year,
                        'filter_date_user': models.Expend.objects.filter(by_user__exact=request.user.username, added_date__year=year).order_by('-added_date'),
                        'sum_user_expend_amount': models.Expend.objects.filter(by_user__exact=request.user.username, added_date__year=year).order_by('-added_date').aggregate(Sum('expend_amount')).get('expend_amount__sum', 0.00),
                        'sum_user_expend_amount_verified': models.Expend.objects.filter(by_user__exact=request.user.username, added_date__year=year, verified__exact='yes').order_by('-added_date').aggregate(Sum('expend_amount')).get('expend_amount__sum', 0.00),
                        'sum_user_expend_amount_unverified': models.Expend.objects.filter(by_user__exact=request.user.username, added_date__year=year, verified__exact='no').order_by('-added_date').aggregate(Sum('expend_amount')).get('expend_amount__sum', 0.00),
                        'filter_date': models.Expend.objects.filter(added_date__year=year).order_by('-added_date'),
                        'sum_expend_amount': models.Expend.objects.filter(added_date__year=year).order_by('-added_date').aggregate(Sum('expend_amount')).get('expend_amount__sum', 0.00),
                        'sum_expend_amount_verified': models.Expend.objects.filter(added_date__year=year, verified__exact='yes').order_by('-added_date').aggregate(Sum('expend_amount')).get('expend_amount__sum', 0.00),
                        'sum_expend_amount_unverified': models.Expend.objects.filter(added_date__year=year, verified__exact='no').order_by('-added_date').aggregate(Sum('expend_amount')).get('expend_amount__sum', 0.00),
                      }
            return render(request, 'expend/expend_list.html', context=context)
    else:
        filter_form = forms.ExpendFilterYearForm
    return render(request, 'expend/expend_list.html', context={'form': filter_form})


def expenditure_filter_list_by_month_view(request):
    if request.method == 'POST':
        filter_form = forms.ExpendFilterMonthForm(data=request.POST)
        if filter_form.is_valid():
            year = filter_form.cleaned_data['year']
            month = filter_form.cleaned_data['month']
            if year == '':
                year = None
            if month == '':
                month = None
            context = {
                        'form': filter_form,
                        'filter_by_time': '{}, {}'.format(get_month_name(num_of_month=month), year),
                        'filter_date_user': models.Expend.objects.filter(by_user__exact=request.user.username, added_date__month=month, added_date__year=year).order_by('-added_date'),
                        'sum_user_expend_amount': models.Expend.objects.filter(by_user__exact=request.user.username, added_date__month=month, added_date__year=year).order_by('-added_date').aggregate(Sum('expend_amount')).get('expend_amount__sum', 0.00),
                        'sum_user_expend_amount_verified': models.Expend.objects.filter(by_user__exact=request.user.username, added_date__month=month, added_date__year=year, verified__exact='yes').order_by('-added_date').aggregate(Sum('expend_amount')).get('expend_amount__sum', 0.00),
                        'sum_user_expend_amount_unverified': models.Expend.objects.filter(by_user__exact=request.user.username, added_date__month=month, added_date__year=year, verified__exact='no').order_by('-added_date').aggregate(Sum('expend_amount')).get('expend_amount__sum', 0.00),
                        'filter_date': models.Expend.objects.filter(added_date__month=month, added_date__year=year).order_by('-added_date'),
                        'sum_expend_amount': models.Expend.objects.filter(added_date__month=month, added_date__year=year).order_by('-added_date').aggregate(Sum('expend_amount')).get('expend_amount__sum', 0.00),
                        'sum_expend_amount_verified': models.Expend.objects.filter(added_date__month=month, added_date__year=year, verified__exact='yes').order_by('-added_date').aggregate(Sum('expend_amount')).get('expend_amount__sum', 0.00),
                        'sum_expend_amount_unverified': models.Expend.objects.filter(added_date__month=month, added_date__year=year, verified__exact='no').order_by('-added_date').aggregate(Sum('expend_amount')).get('expend_amount__sum', 0.00),
                      }
            return render(request, 'expend/expend_list.html', context=context)
    else:
        filter_form = forms.ExpendFilterMonthForm
    return render(request, 'expend/expend_list.html', context={'form': filter_form})


def expenditure_filter_list_by_date_view(request):
    if request.method == 'POST':
        filter_form = forms.ExpendFilterDateForm(data=request.POST)
        if filter_form.is_valid():
            date = filter_form.cleaned_data['date']
            if date == '':
                date = None
            context = {
                        'form': filter_form,
                        'filter_by_time': date,
                        'filter_date_user': models.Expend.objects.filter(by_user__exact=request.user.username, added_date__date=date).order_by('-added_date'),
                        'sum_user_expend_amount': models.Expend.objects.filter(by_user__exact=request.user.username, added_date__date=date).order_by('-added_date').aggregate(Sum('expend_amount')).get('expend_amount__sum', 0.00),
                        'sum_user_expend_amount_verified': models.Expend.objects.filter(by_user__exact=request.user.username, added_date__date=date, verified__exact='yes').order_by('-added_date').aggregate(Sum('expend_amount')).get('expend_amount__sum', 0.00),
                        'sum_user_expend_amount_unverified': models.Expend.objects.filter(by_user__exact=request.user.username, added_date__date=date, verified__exact='no').order_by('-added_date').aggregate(Sum('expend_amount')).get('expend_amount__sum', 0.00),
                        'filter_date': models.Expend.objects.filter(added_date__date=date).order_by('-added_date'),
                        'sum_expend_amount': models.Expend.objects.filter(added_date__date=date).order_by('-added_date').aggregate(Sum('expend_amount')).get('expend_amount__sum', 0.00),
                        'sum_expend_amount_verified': models.Expend.objects.filter(added_date__date=date, verified__exact='yes').order_by('-added_date').aggregate(Sum('expend_amount')).get('expend_amount__sum', 0.00),
                        'sum_expend_amount_unverified': models.Expend.objects.filter(added_date__date=date, verified__exact='no').order_by('-added_date').aggregate(Sum('expend_amount')).get('expend_amount__sum', 0.00),
                      }
            return render(request, 'expend/expend_list.html', context=context)
    else:
        filter_form = forms.ExpendFilterDateForm
    return render(request, 'expend/expend_list.html', context={'form': filter_form})


def expenditure_filter_list_by_range_view(request):
    if request.method == 'POST':
        filter_form = forms.ExpendFilterRangeForm(data=request.POST)
        if filter_form.is_valid():
            date1 = filter_form.cleaned_data['date_1']
            date2 = filter_form.cleaned_data['date_2']
            if date1 == '':
                date1 = None
            if date2 == '':
                date2 = None

            context = {
                        'form': filter_form,
                        'filter_by_time': 'from {} to {}'.format(date1, date2),
                        'filter_date_user': models.Expend.objects.filter(by_user__exact=request.user.username, added_date__range=[date1, date2]).order_by('-added_date'),
                        'sum_user_expend_amount': models.Expend.objects.filter(by_user__exact=request.user.username, added_date__range=[date1, date2]).order_by('-added_date').aggregate(Sum('expend_amount')).get('expend_amount__sum', 0.00),
                        'sum_user_expend_amount_verified': models.Expend.objects.filter(by_user__exact=request.user.username, added_date__range=[date1, date2], verified__exact='yes').order_by('-added_date').aggregate(Sum('expend_amount')).get('expend_amount__sum', 0.00),
                        'sum_user_expend_amount_unverified': models.Expend.objects.filter(by_user__exact=request.user.username, added_date__range=[date1, date2], verified__exact='no').order_by('-added_date').aggregate(Sum('expend_amount')).get('expend_amount__sum', 0.00),
                        'filter_date': models.Expend.objects.filter(added_date__range=[date1, date2]).order_by('-added_date'),
                        'sum_expend_amount': models.Expend.objects.filter(added_date__range=[date1, date2]).order_by('-added_date').aggregate(Sum('expend_amount')).get('expend_amount__sum', 0.00),
                        'sum_expend_amount_verified': models.Expend.objects.filter(added_date__range=[date1, date2], verified__exact='no').order_by('-added_date').aggregate(Sum('expend_amount')).get('expend_amount__sum', 0.00),
                        'sum_expend_amount_unverified': models.Expend.objects.filter(added_date__range=[date1, date2], verified__exact='no').order_by('-added_date').aggregate(Sum('expend_amount')).get('expend_amount__sum', 0.00),
                      }
            return render(request, 'expend/expend_list.html', context=context)
    else:
        filter_form = forms.ExpendFilterRangeForm
    return render(request, 'expend/expend_list.html', context={'form': filter_form})


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    print([normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)])

    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):
    query = None
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query or or_query
    return query


def search(request):
    start = time.time()
    if ('search' in request.GET) and request.GET['search'].strip():
        query_string = request.GET.get('search')

        entry_query = get_query(query_string, ['source_fund', 'source_amount', 'expend_in', 'expend_amount', 'description', 'added_date'])
        if request.user.is_superuser:
            found_entries = models.Expend.objects.filter(entry_query).order_by('-added_date')
        else:
            found_entries = models.Expend.objects.filter(entry_query, by_user__exact=request.user.username).order_by('-added_date')
        end = time.time()
        spent = end - start
        spent_time = format(spent, '.6f')
        return render(request, 'expend/search_result.html', {'query_string': query_string, 'search_result_list': found_entries, 'time': spent_time})
    return HttpResponseRedirect(reverse('expenditure:expend'))
