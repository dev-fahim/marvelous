from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'expend'

urlpatterns = [
    # this are for UTILITIES (Expenditure)

    path('', login_required(views.ExpendListView.as_view()),
         name="expend"),
    path('filter/date/', login_required(views.expenditure_filter_list_by_date_view),
         name="expend_filter_date"),
    path('filter/month/', login_required(views.expenditure_filter_list_by_month_view),
         name="expend_filter_month"),
    path('filter/year/', login_required(views.expenditure_filter_list_by_year_view),
         name="expend_filter_year"),
    path('filter/range/', login_required(views.expenditure_filter_list_by_range_view),
         name="expend_filter_range"),
    path('today/', login_required(views.ExpendListViewByToday.as_view()),
         name="expend_by_today"),
    path('date/<slug:date>/', login_required(views.ExpendListViewByDate.as_view()),
         name="expend_by_date"),
    path('year/<slug:year>/', login_required(views.ExpendListViewByYear.as_view()),
         name="expend_by_year"),
    path('month/<slug:year>/<slug:month>/', login_required(views.ExpendListViewByMonth.as_view()),
         name="expend_by_month"),
    path('update/', login_required(views.ExpendListView.as_view()),
         name="expend_list"),
    path('create/', login_required(views.create_expend),
         name="expend_create"),
    path('detail/<int:pk>/', login_required(views.ExpendDetailView.as_view()),
         name="expend_detail"),
    path('update/<int:pk>/', login_required(views.ExpendUpdateView.as_view()),
         name="expend_update"),
    path('delete/<int:pk>/', login_required(views.ExpendDeleteView.as_view()),
         name="expend_delete"),
    path('graph/<slug:year>', login_required(views.ExpendGraph.as_view()),
         name="expend_graph"
         ),
    path('/', login_required(views.search), name="search")
]
