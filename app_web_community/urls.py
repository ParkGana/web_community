from django.urls import path

import app_web_community.views.indexviews as indexviews

urlpatterns = [
    path('', indexviews.index, name='index'),
]