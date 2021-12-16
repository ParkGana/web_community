from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone
import datetime

from app_web_community.models import ComCategory, Post, PerCategory

# 게시글 목록 
@csrf_exempt
def postList(request):
    if(request.POST.get('userID')):
         request.session['post_userID'] = request.POST.get('userID')
    else:
        request.session['post_userID'] = request.session.get('userID')

    return render(request, 'postList.html')


# 게시글 페이징
@csrf_exempt
def postPaging(request):
    page = int(request.GET.get('page'))
    user_id = request.session.get('post_userID')

    post = Post.objects.filter(USER_ID=user_id).values('POST_ID', 'USER_ID', 'POST_TITLE', 'POST_CONTENT').order_by('-POST_WRITE_DATE')

    post_cnt = Post.objects.filter(USER_ID=user_id).count()

    paginator = Paginator(post, 5)

    try:
        pagination_data = paginator.page(page)
    except PageNotAnInteger:
        pagination_data = paginator.page(1)
    except EmptyPage:
        pagination_data = paginator.page(paginator.num_pages)

    page_numbers_range = 5
    max_index = len(paginator.page_range)
    start_index = int((page - 1) / page_numbers_range) * page_numbers_range
    end_index = start_index + page_numbers_range

    if end_index >= max_index:
        end_index = max_index

    page_range = paginator.page_range[start_index:end_index]

    if (pagination_data.paginator.num_pages / page_numbers_range) == (pagination_data.paginator.num_pages // page_numbers_range):
        num_block = pagination_data.paginator.num_pages // page_numbers_range
    else:
        num_block = pagination_data.paginator.num_pages // page_numbers_range + 1

    if (page / page_numbers_range) == (page // page_numbers_range):
        prev_block = (page // page_numbers_range - 1) * page_numbers_range
        next_block = (page // page_numbers_range) * page_numbers_range + 1
        now_block = page // page_numbers_range
    else:
        prev_block = (page // page_numbers_range) * page_numbers_range
        next_block = (page // page_numbers_range + 1) * page_numbers_range + 1
        now_block = page // page_numbers_range + 1

    context = {
        'now_page': page,
        'pagination_data': pagination_data,
        'page_range': page_range,
        'num_block': num_block,
        'now_block': now_block,
        'prev_block': prev_block,
        'next_block': next_block,
        'post_cnt': post_cnt
    }

    return render(request, 'ajax/postPagination.html', context=context)


# 게시글 검색
@csrf_exempt
def postSearch(request):
    page = int(request.GET.get('page'))
    division = request.GET.get('division')
    keyword = request.GET.get('keyword')
    user_id = request.session.get('post_userID')

    if division == 'title':
        post = Post.objects.filter(USER_ID=user_id, POST_TITLE__icontains=keyword).values('POST_ID', 'USER_ID', 'POST_TITLE', 'POST_CONTENT').order_by('-POST_WRITE_DATE')
    else:
        post = Post.objects.filter(USER_ID=user_id, POST_CONTENT__icontains=keyword).values('POST_ID', 'USER_ID', 'POST_TITLE', 'POST_CONTENT').order_by('-POST_WRITE_DATE')

    paginator = Paginator(post, 5)

    try:
        pagination_data = paginator.page(page)
    except PageNotAnInteger:
        pagination_data = paginator.page(1)
    except EmptyPage:
        pagination_data = paginator.page(paginator.num_pages)

    page_numbers_range = 5
    max_index = len(paginator.page_range)
    start_index = int((page - 1) / page_numbers_range) * page_numbers_range
    end_index = start_index + page_numbers_range

    if end_index >= max_index:
        end_index = max_index

    page_range = paginator.page_range[start_index:end_index]

    if (pagination_data.paginator.num_pages / page_numbers_range) == (pagination_data.paginator.num_pages // page_numbers_range):
        num_block = pagination_data.paginator.num_pages // page_numbers_range
    else:
        num_block = pagination_data.paginator.num_pages // page_numbers_range + 1

    if (page / page_numbers_range) == (page // page_numbers_range):
        prev_block = (page // page_numbers_range - 1) * page_numbers_range
        next_block = (page // page_numbers_range) * page_numbers_range + 1
        now_block = page // page_numbers_range
    else:
        prev_block = (page // page_numbers_range) * page_numbers_range
        next_block = (page // page_numbers_range + 1) * page_numbers_range + 1
        now_block = page // page_numbers_range + 1

    context = {
        'now_page': page,
        'pagination_data': pagination_data,
        'page_range': page_range,
        'num_block': num_block,
        'now_block': now_block,
        'prev_block': prev_block,
        'next_block': next_block,
    }

    return render(request, 'ajax/postSearch.html', context=context)


# 게시글 상세정보
@csrf_exempt
def postDetail(request):
    post_id = request.POST.get('postID')
    user_id = request.POST.get('userID')

    request.session['post_userID'] = user_id

    post = Post.objects.filter(POST_ID=post_id).values('POST_ID', 'POST_TITLE', 'POST_CONTENT', 'POST_WRITE_DATE', 'POST_UPDATE_DATE', 'USER_ID', 'COM_CATEGORY_ID', 'PER_CATEGORY_ID')[0]
    com_category = ComCategory.objects.values('COM_CATEGORY_ID', 'COM_CATEGORY_NAME')
    per_category = PerCategory.objects.filter(USER_ID=user_id, PARENT_PER_CATEGORY_ID__isnull=True).values('PER_CATEGORY_ID', 'PER_CATEGORY_NAME')
    per_category_re = PerCategory.objects.filter(USER_ID=user_id).values('PER_CATEGORY_ID', 'PER_CATEGORY_NAME', 'PARENT_PER_CATEGORY_ID')

    context = {
        'post': post,
        'com_category': com_category,
        'per_category': per_category,
        'per_category_re': per_category_re,
    }

    return render(request, 'postDetail.html', context=context)


# 게시글 작성
class postWrite(View):
    @csrf_exempt
    def get(self, request):
        user_id = request.session.get('userID')

        request.session['post_userID'] = user_id

        com_category = ComCategory.objects.values('COM_CATEGORY_ID', 'COM_CATEGORY_NAME')
        per_category = PerCategory.objects.filter(USER_ID=user_id, PARENT_PER_CATEGORY_ID__isnull=True).values('PER_CATEGORY_ID', 'PER_CATEGORY_NAME')
        per_category_re = PerCategory.objects.filter(USER_ID=user_id, PARENT_PER_CATEGORY_ID__isnull=False).values('PER_CATEGORY_ID', 'PER_CATEGORY_NAME', 'PARENT_PER_CATEGORY_ID')

        context = {
            'com_category': com_category,
            'per_category': per_category,
            'per_category_re': per_category_re
        }

        return render(request, 'postWrite.html', context=context)
    
    @csrf_exempt
    def post(self, request):
        try:
            com_category = request.POST.get('selectCommonCategory')
            per_category = request.POST.get('selectPersonalCategory')
            post_title = request.POST.get('inputTitle')
            post_content = request.POST.get('inputContent')
            user_id = request.session.get('userID')

            request.session['post_userID'] = user_id

            last_id = Post.objects.values('POST_ID').order_by('-POST_ID')[0]
            post_id = last_id['POST_ID'] + 1
            post_date = datetime.datetime.strftime(timezone.localtime(), '%Y-%m-%d %H:%M:%S')

            Post.objects.create(POST_ID=post_id, POST_TITLE=post_title, POST_CONTENT=post_content, POST_WRITE_DATE=post_date, POST_UPDATE_DATE=post_date, USER_ID=user_id, COM_CATEGORY_ID=com_category, PER_CATEGORY_ID=per_category)
        except Exception:
            print('post create error')
        
        return redirect('/post/list')


# 게시글 수정
class postUpdate(View):
    @csrf_exempt
    def get(self, request):
        post_id = request.GET.get('postID')
        user_id = request.session.get('userID')

        request.session['post_userID'] = user_id

        post = Post.objects.filter(POST_ID=post_id).values('POST_ID', 'POST_TITLE', 'POST_CONTENT', 'POST_WRITE_DATE', 'POST_UPDATE_DATE', 'USER_ID', 'COM_CATEGORY_ID', 'PER_CATEGORY_ID')[0]

        com_category = ComCategory.objects.values('COM_CATEGORY_ID', 'COM_CATEGORY_NAME')
        per_category = PerCategory.objects.filter(USER_ID=user_id, PARENT_PER_CATEGORY_ID__isnull=True).values('PER_CATEGORY_ID', 'PER_CATEGORY_NAME')
        per_category_re = PerCategory.objects.filter(USER_ID=user_id, PARENT_PER_CATEGORY_ID__isnull=False).values('PER_CATEGORY_ID', 'PER_CATEGORY_NAME', 'PARENT_PER_CATEGORY_ID')

        context = {
            'post': post,
            'com_category': com_category,
            'per_category': per_category,
            'per_category_re': per_category_re,
        }

        return render(request, 'postupdate.html', context=context)
        
    @csrf_exempt
    def post(self, request):
        try:
            com_category = request.POST.get('selectCommonCategory')
            per_category = request.POST.get('selectPersonalCategory')
            post_title = request.POST.get('inputTitle')
            post_content = request.POST.get('inputContent')
            post_id = request.POST.get('postID')
            user_id = request.session.get('user_id')

            request.session['post_userID'] = user_id

            post_date = datetime.datetime.strftime(timezone.localtime(), '%Y-%m-%d %H:%M:%S')

            update_data = Post.objects.get(POST_ID=post_id)

            update_data.COM_CATEGORY_ID = com_category
            update_data.PER_CATEGORY_ID = per_category
            update_data.POST_TITLE = post_title
            update_data.POST_CONTENT = post_content
            update_data.POST_UPDATE_DATE = post_date

            update_data.save()
        except Exception:
            print('post update error')
        
        return redirect('/post/list')


# 게시글 삭제
@csrf_exempt
def postDelete(request):
    try:
        post_id = request.POST.get('postID')
        user_id = request.session.get('userID')

        request.session['post_userID'] = user_id

        Post.objects.get(POST_ID=post_id).delete()
    except Exception:
        print('post delete error')

    return redirect('/post/list')


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
    