from django import forms
from . import models


class ExpendCreateForm(forms.ModelForm):

    class Meta:
        model = models.Expend
        fields = ('source_fund', 'source_amount', 'expend_in', 'expend_amount', 'description')


class ExpendFilterDateForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'Input Date Format : Y-m-d',
                                                         'class': 'form-control'}), required=True)


class ExpendFilterYearForm(forms.Form):
    YEAR_CHOICES = (
        (2018, 2018),
        (2019, 2019),
        (2020, 2020),
        (2021, 2021),
        (2022, 2022),
    )
    year = forms.IntegerField(required=True, widget=forms.Select(choices=YEAR_CHOICES))


class ExpendFilterMonthForm(forms.Form):
    MONTH_CHOICES = (
        (1, 'January'),
        (2, 'February'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December'),
    )
    YEAR_CHOICES = (
        (2018, 2018),
        (2019, 2019),
        (2020, 2020),
        (2021, 2021),
        (2022, 2022),
    )
    year = forms.IntegerField(required=True, widget=forms.Select(choices=YEAR_CHOICES))
    month = forms.IntegerField(required=True, widget=forms.Select(choices=MONTH_CHOICES))


class ExpendFilterRangeForm(forms.Form):
    date_1 = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'Input Date1 Format : Y-m-d',
                                                         'class': 'form-control'}), required=True)
    date_2 = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'Input Date2 Format : Y-m-d',
                                                         'class': 'form-control'}), required=True)
