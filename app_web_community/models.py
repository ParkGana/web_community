from django.db import models


# 사용자 테이블
class User(models.Model):
    USER_ID = models.CharField(max_length=20,primary_key=True,null=False)
    USER_PWD = models.CharField(max_length=20,null=False)
    USER_NAME = models.CharField(max_length=30,null=False)
    USER_GENDER = models.CharField(max_length=1,null=False)
    USER_BIRTH = models.DateField(null=False)
    USER_EMAIL = models.CharField(max_length=50,null=True)
    USER_TEL = models.CharField(max_length=11,null=True)

    class Meta:
        managed = True
        db_table = 'TBL_USER'


# 공통 카테고리 테이블
class ComCategory(models.Model):
    COM_CATEGORY_ID = models.CharField(max_length=10,primary_key=True,null=False)
    COM_CATEGORY_NAME = models.CharField(max_length=30,null=False)

    class Meta:
        managed = True
        db_table = 'TBL_COM_CATEGORY'


# 사용자 카테고리 테이블
class PerCategory(models.Model):
    PER_CATEGORY_ID = models.IntegerField(primary_key=True,null=False)
    PER_CATEGORY_NAME = models.CharField(max_length=30,null=False)
    PARENT_PER_CATEGORY_ID = models.IntegerField(null=True)
    USER_ID = models.CharField(max_length=20, null=False)

    class Meta:
        managed = True
        db_table = 'TBL_PER_CATEGORY'


# 게시물 테이블
class Post(models.Model):
    POST_ID = models.IntegerField(primary_key=True,null=False)
    POST_TITLE = models.CharField(max_length=100,null=False)
    POST_CONTENT = models.TextField(null=False)
    POST_WRITE_DATE = models.DateTimeField(null=False)
    POST_UPDATE_DATE = models.DateTimeField(null=False)
    USER_ID = models.CharField(max_length=20, null=False)
    COM_CATEGORY_ID = models.CharField(max_length=10,null=False)
    PER_CATEGORY_ID = models.IntegerField(null=True)

    class Meta:
        managed = True
        db_table = 'TBL_POST'


# 댓글 테이블
class Comment(models.Model):
    COMMENT_ID = models.IntegerField(primary_key=True,null=False)
    COMMENT_CONTENT = models.TextField(null=False)
    COMMENT_WRITE_DATE = models.DateTimeField(null=False)
    COMMENT_UPDATE_DATE = models.DateTimeField(null=False)
    PARENT_COMMENT_ID = models.IntegerField(null=True)
    USER_ID = models.CharField(max_length=20,null=False)
    POST_ID = models.IntegerField(null=False)

    class Meta:
        managed = True
        db_table = 'TBL_COMMENT'


# 좋아요 테이블
class Like(models.Model):
    LIKE_ID = models.IntegerField(primary_key=True,null=False)
    LIKE_STATE = models.CharField(max_length=1,null=False)
    USER_ID = models.CharField(max_length=20, null=False)
    POST_ID = models.IntegerField(null=False)
    
    class Meta:
        managed = True
        db_table = 'TBL_LIKE'
