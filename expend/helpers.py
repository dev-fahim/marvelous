def get_month_name(num_of_month):
    if num_of_month == 1 or num_of_month == '01':
        name = 'January'
    elif num_of_month == 2 or num_of_month == '02':
        name = 'February'
    elif num_of_month == 3 or num_of_month == '03':
        name = 'March'
    elif num_of_month == 4 or num_of_month == '04':
        name = 'April'
    elif num_of_month == 5 or num_of_month == '05':
        name = 'May'
    elif num_of_month == 6 or num_of_month == '06':
        name = 'June'
    elif num_of_month == 7 or num_of_month == '07':
        name = 'July'
    elif num_of_month == 8 or num_of_month == '08':
        name = 'August'
    elif num_of_month == 9 or num_of_month == '09':
        name = 'September'
    elif num_of_month == 10 or num_of_month == '10':
        name = 'October'
    elif num_of_month == 11 or num_of_month == '11':
        name = 'November'
    elif num_of_month == 12 or num_of_month == '12':
        name = 'December'
    else:
        name = num_of_month
    return name


def search(request):
    query = request.GET.get("search")
    if query:
        result = models.Expend.objects.filter(
            Q(source_fund__icontains=query) |
            Q(source_amount__icontains=query) |
            Q(expend_in__icontains=query) |
            Q(expend_amount__icontains=query) |
            Q(description__icontains=query) |
            Q(added_date__icontains=query)
                )
        return render(request, 'expend/search_result.html', context={'search_result_list': result})

    return HttpResponseRedirect(reverse('expenditure:expend'))
