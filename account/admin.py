from django.contrib import admin
from . import models
# Register your models here.


class ExpendAdmin(admin.ModelAdmin):
    list_display = ('expend_in', 'by_user', 'source_fund', 'added_date', 'updated_date', 'verified')


admin.site.register(models.UserProfile)
admin.site.register(models.Expend, ExpendAdmin)
