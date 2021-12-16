from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from app_web_community.models import Post, ComCategory, Like, Comment

# 메인 페이지
@csrf_exempt
def index(request):
    com_category = ComCategory.objects.values('COM_CATEGORY_ID', 'COM_CATEGORY_NAME')

    # 로그인 되어있는 경우 사용자 정보 세팅
    if request.session.get('userID'):
        user_id = request.session.get('userID')

        post_cnt = Post.objects.filter(USER_ID=user_id).count()
        like_cnt = Like.objects.filter(USER_ID=user_id, LIKE_STATE='Y').count()
        hate_cnt = Like.objects.filter(USER_ID=user_id, LIKE_STATE='N').count()
        comment_cnt = Comment.objects.filter(USER_ID=user_id).count()

        context = {
            'com_category': com_category,
            'post_cnt': post_cnt,
            'like_cnt': like_cnt,
            'hate_cnt': hate_cnt,
            'comment_cnt': comment_cnt,
        }
    else:
        context = {
            'com_category': com_category,
        }

    return render(request, 'index.html', context=context)


# 게시글 페이징
@csrf_exempt
def indexPaging(request):
    page = int(request.GET.get('page'))
    com_category_id = request.GET.get('com_category_id')

    if com_category_id is None:
        com_category_id = ''

    post = Post.objects.filter(COM_CATEGORY_ID__icontains=com_category_id).values('POST_ID', 'USER_ID', 'POST_TITLE', 'POST_CONTENT').order_by('-POST_WRITE_DATE')

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
        'com_category_id': com_category_id,
        'num_block': num_block,
        'now_block': now_block,
        'prev_block': prev_block,
        'next_block': next_block,
    }

    return render(request, 'ajax/indexPagination.html', context=context)


# 게시글 검색
@csrf_exempt
def indexSearch(request):
    page = int(request.GET.get('page'))
    division = request.GET.get('division')
    keyword = request.GET.get('keyword')

    if division == 'title':
        post = Post.objects.filter(POST_TITLE__icontains=keyword).values('POST_ID', 'USER_ID', 'POST_TITLE', 'POST_CONTENT').order_by('-POST_WRITE_DATE')
    else:
        post = Post.objects.filter(POST_CONTENT__icontains=keyword).values('POST_ID', 'USER_ID', 'POST_TITLE', 'POST_CONTENT').order_by('-POST_WRITE_DATE')

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

    return render(request, 'ajax/indexSearch.html', context=context)
