from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'account'

urlpatterns = [
    # this are for USER ACCOUNTS
    path('', login_required(views.HomeView.as_view()), name='home'),
    path('login/', views.Login.as_view(), name="login"),
    path('logout/', login_required(views.Logout.as_view()), name="logout"),
    path('profile/', login_required(views.TemplateView.as_view(template_name='accounts/profile.html')), name="profile"),
    path('profile/update/', login_required(views.update), name="update_profile"),
    path('signup/', views.signup, name='signup'),

    # this are for UTILITIES

    path('expenditure/', views.ExpendListView.as_view(), name="expend"),
    path('expenditure/update/', views.ExpendListView.as_view(), name="expend_list"),
    path('expenditure/create', views.create_expend, name="expend_create"),
    path('expenditure/<int:pk>', views.ExpendDetailView.as_view(), name="expend_detail"),
    path('expenditure/update/<int:pk>', views.ExpendUpdateView.as_view(), name="expend_update"),
    path('expenditure/delete/<int:pk>', views.ExpendDeleteView.as_view(), name="expend_delete"),
]
