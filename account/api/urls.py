from django.urls import path
from . import views

app_name = 'api'


urlpatterns = [
    path('expends/', views.ExpendSearchApiView.as_view(), name='expend-search'),
    path('expends/create/', views.ExpendApiView.as_view(), name='expend-create'),
    path('expends/update/<int:pk>/', views.ExpendUpdateApiView.as_view(), name='expend-update'),
    path('expends/all/', views.ExpendRudView.as_view(), name='expend-rud'),
]