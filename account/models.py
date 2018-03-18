from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.urls import reverse


def user(request):
    return User.objects.get(username__exact=request.user.username)


class UserProfile(models.Model):
    select = (
        ('male', 'Male'),
        ('female', 'Female')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    created_date = models.DateTimeField(auto_now=True)
    address = models.TextField(blank=True, default='')
    birth_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, default='')
    slug = models.SlugField(max_length=50, blank=True, default='')
    gender = models.CharField(max_length=50, blank=True, choices=select, default='Not Selected')
    contact_number = models.CharField(max_length=255, blank=True, default='')

    def get_absolute_url(self):
        return reverse('account:profile')

    def __str__(self):
        return self.user.username

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance, slug=instance)

    post_save.connect(create_user_profile, sender=User)


# Now for Utilities

class Expend(models.Model):
    select = (
        ('yes', 'yes'),
        ('no', 'no')
    )
    by_user = models.CharField(max_length=255, blank=False, unique=False, null=True)
    added_date = models.DateTimeField(auto_now=True)
    source_fund = models.CharField(max_length=255)
    source_amount = models.PositiveIntegerField()
    expend_in = models.CharField(max_length=255)
    expend_amount = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    verified = models.CharField(choices=select, max_length=255, default='no')

    def get_absolute_url(self):
        return reverse('account:expend_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.expend_in


