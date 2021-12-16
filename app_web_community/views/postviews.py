from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone
from django.db.models import Q, Subquery, Count
import datetime

from app_web_community.models import ComCategory, Post, PerCategory, Like, Comment

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


# 게시글 좋아요 상세정보
@csrf_exempt
def postLike(request):
    post_id = request.POST.get('post_id')
    user_id = request.session.get('userID')

    like_cnt = Like.objects.filter(POST_ID=post_id, LIKE_STATE='Y').count()
    hate_cnt = Like.objects.filter(POST_ID=post_id, LIKE_STATE='N').count()

    like_user = Like.objects.filter(POST_ID=post_id, USER_ID=user_id).values('LIKE_STATE')

    if like_user:
        like_user = like_user[0]

    context = {
        'like_cnt':like_cnt,
        'hate_cnt': hate_cnt,
        'like_user': like_user,
    }

    return render(request, 'ajax/postLike.html', context=context)


# 게시글 좋아요
@csrf_exempt
def postLikeChoice(request):
    post_id = request.POST.get('post_id')
    state = request.POST.get('state')
    user_id = request.session.get('userID')

    like_user = Like.objects.filter(USER_ID=user_id, POST_ID=post_id).values('LIKE_ID', 'LIKE_STATE')

    # 데이터 존재하는 경우
    if like_user:
        # 이미 선택한 상태를 다시 선택할 경우, 해당 선택사항 삭제
        if state == like_user[0]['LIKE_STATE']:
            try:
                like_id = like_user[0]['LIKE_ID']

                Like.objects.get(LIKE_ID=like_id).delete()
            except Exception:
                print('like delete error')
        # 이전에 선택한 상태와 다른 상태를 선택할 경우, 해당 선택사항 수정
        else:
            try:
                like_id = like_user[0]['LIKE_ID']

                update_data = Like.objects.get(LIKE_ID=like_id)

                update_data.LIKE_STATE = state

                update_data.save()
            except Exception:
                print('like update error')
    # 데이터 존재하지 않는 경우, 해당 선택사항 생성
    else:
        try:
            last_id = Like.objects.values('LIKE_ID').order_by('-LIKE_ID')[0]
            like_id = last_id['LIKE_ID'] + 1

            Like.objects.create(LIKE_ID=like_id, USER_ID=user_id, POST_ID=post_id, LIKE_STATE=state)
        except Exception:
            print('like create error')

    return render(request, 'ajax/postLike.html')


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


# 게시글 댓글 상세정보
@csrf_exempt
def postComment(request):
    post_id = request.POST.get('post_id')

    post = Post.objects.filter(POST_ID=post_id).values('POST_ID', 'POST_TITLE', 'POST_CONTENT', 'POST_WRITE_DATE', 'POST_UPDATE_DATE', 'USER_ID', 'COM_CATEGORY_ID', 'PER_CATEGORY_ID')[0]

    comment = Comment.objects.filter(POST_ID=post_id, PARENT_COMMENT_ID__isnull=True).values('COMMENT_ID', 'USER_ID', 'COMMENT_CONTENT', 'COMMENT_WRITE_DATE').order_by('-COMMENT_WRITE_DATE')
    comment_re = Comment.objects.filter(POST_ID=post_id, PARENT_COMMENT_ID__isnull=False).values('COMMENT_ID', 'USER_ID', 'COMMENT_CONTENT', 'COMMENT_WRITE_DATE', 'PARENT_COMMENT_ID').order_by('-COMMENT_WRITE_DATE')
    comment_re_cnt = Comment.objects.filter(POST_ID=post_id, PARENT_COMMENT_ID__isnull=False).values('PARENT_COMMENT_ID').annotate(Count('PARENT_COMMENT_ID'))

    context = {
        'post': post,
        'comment': comment,
        'comment_re': comment_re,
        'comment_re_cnt': comment_re_cnt
    }

    return render(request, 'ajax/postComment.html', context=context)


# 게시글 댓글 작성
@csrf_exempt
def postCommentWrite(request):
    post_id = request.POST.get('post_id')
    state = request.POST.get('state')
    user_id = request.session.get('userID')

     # 게시글에 대한 댓글
    if state == 'C':
        try:
            comment_content = request.POST.get('comment_content')

            last_id = Comment.objects.values('COMMENT_ID').order_by('-COMMENT_ID')[0]
            comment_id = last_id['COMMENT_ID'] + 1
            comment_date = datetime.datetime.strftime(timezone.localtime(), '%Y-%m-%d %H:%M:%S')

            Comment.objects.create(COMMENT_ID=comment_id, COMMENT_CONTENT=comment_content, COMMENT_WRITE_DATE=comment_date, COMMENT_UPDATE_DATE=comment_date, USER_ID=user_id, POST_ID=post_id)
        except Exception:
            print('comment create error')
    # 댓글에 대한 답글
    elif state == 'R':
        try:
            comment_content = request.POST.get('comment_content')
            parent_comment_id = request.POST.get('parent_comment_id')

            last_id = Comment.objects.values('COMMENT_ID').order_by('-COMMENT_ID')[0]
            comment_id = last_id['COMMENT_ID'] + 1
            comment_date = datetime.datetime.strftime(timezone.localtime(), '%Y-%m-%d %H:%M:%S')

            Comment.objects.create(COMMENT_ID=comment_id, COMMENT_CONTENT=comment_content, COMMENT_WRITE_DATE=comment_date, COMMENT_UPDATE_DATE=comment_date, PARENT_COMMENT_ID=parent_comment_id, USER_ID=user_id, POST_ID=post_id)
        except Exception:
            print('recomment create error')

    return render(request, 'ajax/postComment.html')


# 게시글 댓글 삭제
@csrf_exempt
def postCommentDelete(request):
    comment_id = request.POST.get('comment_id')
    parent_comment_id = request.POST.get('parent_comment_id')
    state = request.POST.get('state')

    if state == 'C':
        comment_re = Comment.objects.filter(COMMENT_ID__in=Subquery(Comment.objects.filter(PARENT_COMMENT_ID=comment_id).values('COMMENT_ID'))).values('COMMENT_ID')

        if comment_re :
            update_data = Comment.objects.get(COMMENT_ID=comment_id)

            update_data.COMMENT_CONTENT = '(삭제된 댓글입니다.)'

            update_data.save()
        else:
            Comment.objects.get(COMMENT_ID=comment_id).delete()
    elif state == 'R':
        parent_comment = Comment.objects.filter(COMMENT_ID=Subquery(Comment.objects.filter(COMMENT_ID=parent_comment_id).values('COMMENT_ID')), COMMENT_CONTENT='(삭제된 댓글입니다.)')

        Comment.objects.get(COMMENT_ID=comment_id).delete()

        if parent_comment:
            Comment.objects.filter(COMMENT_ID=parent_comment_id).delete()

    return render(request, 'ajax/postComment.html')


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


# 사용자 카테고리 게시글 페이징
@csrf_exempt
def postCategoryPaging(request):
    page = int(request.POST.get('page'))
    state = request.POST.get('state')
    per_category_id = request.POST.get('per_category_id')
    user_id = request.session.get('post_userID')

    if state == 'C':
        search_condition = Q()

        search_condition.add(Q(PER_CATEGORY_ID=per_category_id), search_condition.OR)
        search_condition.add(Q(PARENT_PER_CATEGORY_ID=per_category_id), search_condition.OR)

        post = Post.objects.filter(USER_ID=user_id, PER_CATEGORY_ID__in=Subquery(PerCategory.objects.filter(search_condition).values('PER_CATEGORY_ID'))).values('POST_ID', 'USER_ID', 'POST_TITLE', 'POST_CONTENT').order_by('-POST_WRITE_DATE')

        post_cnt = post.count()

        per_category = PerCategory.objects.filter(PER_CATEGORY_ID=per_category_id).values('PER_CATEGORY_ID', 'PER_CATEGORY_NAME')[0]

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

        if (pagination_data.paginator.num_pages / page_numbers_range) == (
            pagination_data.paginator.num_pages // page_numbers_range):
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
            'post_cnt': post_cnt,
            'per_category': per_category
        }

        return render(request, 'ajax/postCategoryPagination.html', context=context)
    elif state == 'R':
        post = Post.objects.filter(USER_ID=user_id, PER_CATEGORY_ID=per_category_id).values('POST_ID', 'USER_ID', 'POST_TITLE', 'POST_CONTENT').order_by('-POST_WRITE_DATE')

        post_cnt = post.count()

        per_category = PerCategory.objects.filter(PER_CATEGORY_ID=Subquery(PerCategory.objects.filter(PER_CATEGORY_ID=per_category_id).values('PARENT_PER_CATEGORY_ID'))).values('PER_CATEGORY_ID', 'PER_CATEGORY_NAME')[0]
        per_category_re = PerCategory.objects.filter(PER_CATEGORY_ID=per_category_id).values('PER_CATEGORY_ID', 'PER_CATEGORY_NAME')[0]

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

        if (pagination_data.paginator.num_pages / page_numbers_range) == (
            pagination_data.paginator.num_pages // page_numbers_range):
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
            'post_cnt': post_cnt,
            'per_category': per_category,
            'per_category_re': per_category_re
        }

        return render(request, 'ajax/postCategoryRePagination.html', context=context)


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
    