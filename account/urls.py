from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'account'

urlpatterns = [
    # API VIEWS
    path('api/', include('account.api.urls', namespace='api')),
    # this are for USER ACCOUNTS
    path('', login_required(views.HomeView.as_view()), name='home'),
    path('login/', views.Login.as_view(), name="login"),
    path('logout/', login_required(views.Logout.as_view()), name="logout"),
    path('profile/', login_required(views.TemplateView.as_view(template_name='accounts/profile.html')), name="profile"),
    path('profile/update/', login_required(views.update), name="update_profile"),
    path('signup/', login_required(views.signup), name='signup'),

    # this are for UTILITIES

    path('expenditure/', login_required(views.ExpendListView.as_view()),
         name="expend"),
    path('expenditure/filter/date/', login_required(views.expenditure_filter_list_by_date_view),
         name="expend_filter_date"),
    path('expenditure/filter/month/', login_required(views.expenditure_filter_list_by_month_view),
         name="expend_filter_month"),
    path('expenditure/filter/year/', login_required(views.expenditure_filter_list_by_year_view),
         name="expend_filter_year"),
    path('expenditure/filter/range/', login_required(views.expenditure_filter_list_by_range_view),
         name="expend_filter_range"),
    path('expenditure/today/', login_required(views.ExpendListViewByToday.as_view()),
         name="expend_by_today"),
    path('expenditure/date/<slug:date>/', login_required(views.ExpendListViewByDate.as_view()),
         name="expend_by_date"),
    path('expenditure/year/<slug:year>/', login_required(views.ExpendListViewByYear.as_view()),
         name="expend_by_year"),
    path('expenditure/month/<slug:year>/<slug:month>/', login_required(views.ExpendListViewByMonth.as_view()),
         name="expend_by_month"),
    path('expenditure/update/', login_required(views.ExpendListView.as_view()),
         name="expend_list"),
    path('expenditure/create', login_required(views.create_expend),
         name="expend_create"),
    path('expenditure/detail/<int:pk>', login_required(views.ExpendDetailView.as_view()),
         name="expend_detail"),
    path('expenditure/update/<int:pk>', login_required(views.ExpendUpdateView.as_view()),
         name="expend_update"),
    path('expenditure/delete/<int:pk>', login_required(views.ExpendDeleteView.as_view()),
         name="expend_delete")
]
