from django.db import models
from django.urls import reverse

# Create your models here.


class Expend(models.Model):
    select = (
        ('yes', 'yes'),
        ('no', 'no')
    )
    by_user = models.CharField(max_length=255, blank=False, unique=False, null=True)
    added_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    source_fund = models.CharField(max_length=255)
    source_amount = models.PositiveIntegerField()
    expend_in = models.CharField(max_length=255)
    expend_amount = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    verified = models.CharField(choices=select, max_length=255, default='no')

    def get_absolute_url(self):
        return reverse('expenditure:expend_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.expend_in
