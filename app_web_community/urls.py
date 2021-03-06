from django.urls import path

import app_web_community.views.indexviews as indexviews
import app_web_community.views.accountviews as accountviews
import app_web_community.views.postviews as postviews

urlpatterns = [
    path('', indexviews.index, name='index'),
    path('paging', indexviews.indexPaging, name='indexPaging'),
    path('search', indexviews.indexSearch, name='indexSearch'),

    path('login', accountviews.login.as_view(), name='login'),
    path('logout', accountviews.logout, name='logout'),
    path('join', accountviews.join, name='join'),
    path('join/checkUserID', accountviews.checkUserID, name='checkUserID'),

    path('post/list', postviews.postList, name='postList'),
    path('post/paging', postviews.postPaging, name='postPaging'),
    path('post/search', postviews.postSearch, name='postSearch'),
    path('post/detail', postviews.postDetail, name='postDetail'),
    path('post/write', postviews.postWrite.as_view(), name='postWrite'),
    path('post/update', postviews.postUpdate.as_view(), name='postUpdate'),
    path('post/delete', postviews.postDelete, name='postDelete'),
    path('post/like', postviews.postLike, name='postLike'),
    path('post/like/choice', postviews.postLikeChoice, name='postLikeChoice'),
    path('post/comment', postviews.postComment, name='postComment'),
    path('post/comment/write', postviews.postCommentWrite, name='postCommentWrite'),
    path('post/comment/delete', postviews.postCommentDelete, name='postCommentDelete'),
    path('post/category', postviews.postCategory, name='postCategory'),
    path('post/category/paging', postviews.postCategoryPaging, name='postCategoryPaging'),
    path('post/category/create', postviews.postCategoryCreate, name='postCategoryCreate'),
    path('post/category/update', postviews.postCategoryUpdate, name='postCategoryUpdate'),
    path('post/category/delete', postviews.postCategoryDelete, name='postCategoryDelete'),
]