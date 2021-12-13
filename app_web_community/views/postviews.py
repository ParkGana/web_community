from django.shortcuts import render

# 게시글 목록
def postList(request):
    return render(request, 'postList.html')

# 게시글 상세정보
def postDetail(request):
    return render(request, 'postDetail.html')

# 게시글 작성
def postWrite(request):
    return render(request, 'postWrite.html')