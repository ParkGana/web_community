from django.shortcuts import render
import datetime

#로그인
def login(request):
    select_year_date = []
    select_month_date = []
    select_day_date = []

    for year in range(0, 100):
        select_year_date.append(datetime.date.strftime(datetime.datetime.now() - datetime.timedelta(year * 365), '%Y'))

    for month in range(1, 13):
        select_month_dt = datetime.datetime.strptime(str(month), '%m')
        select_month_date.append(datetime.date.strftime(select_month_dt, '%#m'))

    for day in range(1, 32):
        select_day_dt = datetime.datetime.strptime(str(day), '%d')
        select_day_date.append(datetime.date.strftime(select_day_dt, '%#d'))

    context = {
        'select_year_date': select_year_date,
        'select_month_date': select_month_date,
        'select_day_date': select_day_date,
    }

    return render(request, 'login.html', context=context)