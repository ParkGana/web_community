from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.views import View
import datetime

from app_web_community.models import User

#로그인
class login(View):
    @csrf_exempt
    def get(self, request):
        # 로그인 되어있는 경우
        if request.session.get('userID'):
            return redirect('/')
        # 로그인 되어있지 않은 경우
        else:
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
    
    @csrf_exempt
    def post(self, request):
        user_id = request.POST.get('user_id')
        user_pwd = request.POST.get('user_pwd')

        try:
            user = User.objects.get(USER_ID=user_id)

            # 비밀번호 오류
            if user_pwd != user.USER_PWD:
                error_message = '비밀번호가 틀렸습니다.'
                check_user_id = user_id
            # 로그인 성공
            else:
                request.session['userID'] = user_id

                return redirect('/')
        # 아이디 오류
        except Exception:
            error_message = '존재하지 않는 아이디입니다.'
            check_user_id = ''

        context = {
            'error_message': error_message,
            'user_id': check_user_id,
        }

        return render(request, 'login.html', context=context)


# 로그아웃
@csrf_exempt
def logout(request):
    request.session['userID'] = {}
    request.session.modified = True

    return redirect('/')


# 회원가입
@csrf_exempt
def join(request):
    user_id = request.POST.get('user_id')
    user_pwd = request.POST.get('user_pwd')
    user_name = request.POST.get('user_name')
    user_gender = request.POST.get('user_gender')
    user_birth = str(request.POST.get('user_birth'))
    user_email = request.POST.get('user_email')
    user_tel = request.POST.get('user_tel')

    # 날짜 타입의 데이터로 변환
    user_birth = datetime.datetime.strptime(user_birth, '%Y%m%d')
    user_birth = datetime.date.strftime(user_birth, '%Y-%m-%d')

    try:
        User.objects.create(USER_ID=user_id, USER_PWD=user_pwd, USER_NAME=user_name, USER_GENDER=user_gender, USER_BIRTH=user_birth, USER_EMAIL=user_email, USER_TEL=user_tel)

        return HttpResponse(status=200)
    except Exception:
        return JsonResponse({"message": "DUPLICATE_DATA"}, status=409)


# 아이디 중복 체크
@csrf_exempt
def checkUserID(request):
    user_id = request.POST.get('user_id')

    try:
        User.objects.get(USER_ID=user_id)

        return HttpResponse(status=200)
    except Exception:
        return JsonResponse({"message": "DUPLICATE_DATA"}, status=409)
