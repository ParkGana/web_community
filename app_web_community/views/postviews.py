from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.db import connection

from app_web_community.models import Post, PerCategory

# 게시글 목록
@csrf_exempt
def postList(request):
    user_id = request.POST.get('userID')

    request.session['post_userID'] = user_id

    return render(request, 'postList.html')


# 게시글 상세정보
def postDetail(request):
    return render(request, 'postDetail.html')


# 게시글 작성
def postWrite(request):
    return render(request, 'postWrite.html')


# 사용자 카테고리
@csrf_exempt
def postCategory(request):
    user_id = request.POST.get('user_id')

    per_category = PerCategory.objects.filter(USER_ID=user_id, PARENT_PER_CATEGORY_ID__isnull=True).all().order_by('PER_CATEGORY_NAME')
    per_category_re = PerCategory.objects.filter(USER_ID=user_id, PARENT_PER_CATEGORY_ID__isnull=False).all().order_by('PER_CATEGORY_NAME')

    context = {
        'per_category': per_category,
        'per_category_re': per_category_re
    }

    return render(request, 'ajax/postCategory.html', context=context)


# 사용자 카테고리 생성
@csrf_exempt
def postCategoryCreate(request):
    state = request.POST.get('state')
    user_id = request.session.get('userID')

    if state == 'C':
        try:
            per_category_name = request.POST.get('per_category_name')

            last_id = PerCategory.objects.values('PER_CATEGORY_ID').order_by('-PER_CATEGORY_ID')[0]
            category_id = last_id['PER_CATEGORY_ID'] + 1

            PerCategory.objects.create(PER_CATEGORY_ID=category_id, PER_CATEGORY_NAME=per_category_name, USER_ID=user_id)
        except Exception:
            print('category create error')
    elif state == 'R':
        try:
            per_category_name = request.POST.get('per_category_name')
            parent_category_id = request.POST.get('parent_category_id')

            last_id = PerCategory.objects.values('PER_CATEGORY_ID').order_by('-PER_CATEGORY_ID')[0]
            category_id = last_id['PER_CATEGORY_ID'] + 1

            PerCategory.objects.create(PER_CATEGORY_ID=category_id, PER_CATEGORY_NAME=per_category_name, PARENT_PER_CATEGORY_ID=parent_category_id, USER_ID=user_id)
        except Exception:
            print('category create error')

    return render(request, 'ajax/postCategory.html')


# 사용자 카테고리 수정
@csrf_exempt
def postCategoryUpdate(request):
    try:
        per_category_id = request.POST.get('per_category_id')
        per_category_name = request.POST.get('per_category_name')

        update_data = PerCategory.objects.get(PER_CATEGORY_ID=per_category_id)

        update_data.PER_CATEGORY_NAME = per_category_name

        update_data.save()
    except Exception:
        print('category update error')
    
    return render(request, 'ajax/postCategory.html')


# 사용자 카테고리 삭제
@csrf_exempt
def postCategoryDelete(request):
    state = request.POST.get('state')

    if state == 'C':
        try:
            per_category_id = request.POST.get('per_category_id')

            PerCategory.objects.get(PER_CATEGORY_ID=per_category_id).delete()
            PerCategory.objects.get(PARENT_PER_CATEGORY_ID=per_category_id).delete()
        except Exception:
            print('category delete error')
    elif state == 'R':
        try:
            per_category_id = request.POST.get('per_category_id')

            PerCategory.objects.get(PER_CATEGORY_ID=per_category_id).delete()
        except Exception:
            print('category delete error')
    
    return render(request, 'ajax/postCategory.html')