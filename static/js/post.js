$(document).ready(function() {
    getUserCategory();
    goPage(1);
    getLike();
    getComment();
});


/***********************************************************************************************
 * 게시글 페이징
 ***********************************************************************************************/
function goPage(page) {
    $.ajax({
        type: 'GET',
        url: 'paging',
        data: {
            'page': page,
        },
        success: function(response) {
            $('#wrapList').html(response);

            // 페이지 번호 선택 시, 게시물 상단 위치로 페이지 이동
            $(".pageNum").click(function() {
                var offset = $('#wrapMainBody').offset();

               $('html, body').animate({scrollTop : offset.top - 20}, 700);

               return false;
            });
        },
        error: function(err) {
            console.log(err);
        }
    });
}


/***********************************************************************************************
 * 게시글 검색
 ***********************************************************************************************/
function goSearch(page) {
    var division = $("#inputDivision").val();
    var keyword = $("#inputKeyword").val();

    var alert_btn = document.getElementById('btnSearch');

    if(division == null) {
        $("#alert_warning_msg").text("카테고리를 선택해주세요.");
        alert_btn.setAttribute('data-target', '#alertWarningModal');
        return;
    }
    else if(keyword == '') {
        $("#alert_warning_msg").text("키워드를 입력해주세요.");
        alert_btn.setAttribute('data-target', '#alertWarningModal');
        return;
    }

    alert_btn.removeAttribute('data-target');

    $.ajax({
        type: 'GET',
        url: 'search',
        data: {
            'page': page,
            'division': division,
            'keyword': keyword,
        },
        success: function(response) {
            $('#divPagination').html(response);

            // 페이지 번호 선택 시, 게시물 상단 위치로 페이지 이동
            $(".pageNum").click(function() {
                var offset = $('#wrapMainBody').offset();

               $('html, body').animate({scrollTop : offset.top - 20}, 700);

               return false;
            });
        },
        error: function(err) {
            console.log(err);
        }
    });
}


/***********************************************************************************************
 * 게시글 좋아요 정보
 ***********************************************************************************************/
function getLike() {
    var post_id = $("#post_id").val();

    $.ajax({
        type: 'POST',
        url: 'like',
        data: {
            'post_id': post_id,
        },
        success: function(response) {
            $('#wrapLike').html(response);
        },
        error: function(err) {
            console.log(err);
        }
    });
}


/***********************************************************************************************
 * 게시글 좋아요
 ***********************************************************************************************/
function likePost(state) {
    var post_id = $("#post_id").val();
    var post_user_id = $("#post_user_id").val();
    var user_id = $("#user_id").val();
    var alert_btn;

    if(state == 'Y') {
        alert_btn = document.getElementById('divThumbsUp');
    }
    else {
        alert_btn = document.getElementById('divThumbsDown');
    }

    if(post_user_id == user_id) {
        $("#alert_warning_msg").text("본인의 게시글에서는 불가능합니다.");
        alert_btn.setAttribute('data-target', '#alertWarningModal');
        return;
    }

    alert_btn.removeAttribute('data-target');

    $.ajax({
        type: 'POST',
        url: 'like/choice',
        data: {
            'post_id': post_id,
            'state': state
        },
        success: function() {
            getLike();
        },
        error: function(err) {
            console.log(err);
        }
    });
}


/***********************************************************************************************
 * 게시글 댓글 상세정보
 ***********************************************************************************************/
function getComment() {
    var post_id = $("#post_id").val();

    $.ajax({
        type: 'POST',
        url: 'comment',
        data: {
            'post_id': post_id,
        },
        success: function(response) {
            $('#wrapCommentList').html(response);
        },
        error: function(err) {
            console.log(err);
        }
    });
}


/***********************************************************************************************
 * 게시글 댓글 작성
 ***********************************************************************************************/
function writeComment(state, comment_id) {
    var post_id = $("#post_id").val();

    if (state == 'C') {
        var comment_content = $("#inputComment").val();

        if(comment_content == '') {
            $("#alert_warning_msg").text("댓글을 입력해주세요.");
            document.getElementById('btnCommentWrite').setAttribute('data-target', '#alertWarningModal');
            return;
        }

        $.ajax({
            type: 'POST',
            url: 'comment/write',
            data: {
                'post_id': post_id,
                'comment_content': comment_content,
                'state': state
            },
            success: function() {
                getComment();
            },
            error: function(err) {
                console.log(err);
            }
        });
    }
    else if (state == 'R') {
        var comment_content = $("#inputCommentRe" + comment_id).val();

        if(comment_content == '') {
            $("#alert_warning_msg").text("답글을 입력해주세요.");
            document.getElementById('btnCommentReWrite' + parent).setAttribute('data-target', '#alertWarningModal');
            return;
        }

        $.ajax({
            type: 'POST',
            url: 'comment/write',
            data: {
                'post_id': post_id,
                'comment_content': comment_content,
                'state': state,
                'parent_comment_id': comment_id
            },
            success: function() {
                getComment();
            },
            error: function(err) {
                console.log(err);
            }
        });
    }
}


/***********************************************************************************************
 * 게시글 댓글에 달린 답글 영역 접고 펼치기
 ***********************************************************************************************/
function toggleCommentRe(comment_id) {
    var div_comment_re = $("#wrapCommentRe" + comment_id);
    var i_comment_re = $("#i" + comment_id);

    if (div_comment_re.css('display') == 'none') {
        i_comment_re.attr('class', "fas fa-angle-up");
    }
    else {
        i_comment_re.attr('class', "fas fa-angle-down");
    }

    div_comment_re.toggle();
}


/***********************************************************************************************
 * 게시글 댓글에 답글 작성하는 영역 접고 펼치기
 ***********************************************************************************************/
function toggleCommentReWrite(comment_id) {
    var div_input_comment_re = $("#divInputCommentRe" + comment_id);

    div_input_comment_re.toggle();

    if (div_input_comment_re.css('display') == 'block') {
        div_input_comment_re.css('display', 'inline-block');
    }
}


/***********************************************************************************************
 * 게시글 댓글 삭제
 ***********************************************************************************************/
function deleteComment(state, comment_id, parent_comment_id) {
    $.ajax({
        type: 'POST',
        url: 'comment/delete',
        data: {
            'comment_id': comment_id,
            'parent_comment_id': parent_comment_id,
            'state': state
        },
        success: function() {
            getComment();
        },
        error: function(err) {
            console.log(err);
        }
    });
}


/***********************************************************************************************
 * 게시글 입력 내용 크기에 맞게 textarea 크기 자동 조절
 ***********************************************************************************************/
 function postContentResize(e) {
    var xe = document.getElementById('hiddenInputContent');

    xe.value = e.value;
    e.style.height = (xe.scrollHeight + 100) + 'px';

    if (xe.scrollHeight < 500) {
        e.style.height = 500 + 'px';
    }
}


/***********************************************************************************************
 * 게시글 작성
 ***********************************************************************************************/
 function writePost() {
    var btn_write_post = document.getElementById('btnPostWrite');
    var com_category = $("#selectCommonCategory").val();
    var per_category = $("#selectPersonalCategory").val();

    if(com_category == null) {
        $("#alert_warning_msg").html("공통 카테고리를 선택해 주세요.");
        btn_write_post.setAttribute('data-target', '#alertWarningModal');
        return;
    }
    if(per_category == null) {
        $("#alert_warning_msg").html("사용자 카테고리를 선택해 주세요.");
        btn_write_post.setAttribute('data-target', '#alertWarningModal');
        return;
    }

    btn_write_post.removeAttribute('data-target');
    btn_write_post.setAttribute('onclick','document.getElementById("formPostWrite").submit()');
    btn_write_post.onclick();
}


/***********************************************************************************************
 * 게시글 작성 취소
 ***********************************************************************************************/
 function cancelWritePost() {
    var btn_cancel_write_post = document.getElementById('btnModalYes');

    $("#alert_check_msg").html("작성한 데이터가 모두 지워집니다.<br>정말로 나가겠습니까?");
    document.getElementById('btnPostWriteExit').setAttribute('data-target', '#alertCheckModal');
    btn_cancel_write_post.setAttribute('onclick','document.getElementById("formPostBack").submit()');
    
    return;
}


/***********************************************************************************************
 * 게시글 수정 취소
 ***********************************************************************************************/
 function cancelUpdatePost() {
    var btn_cancel_update_post = document.getElementById('btnModalYes');

    $("#alert_check_msg").html("수정한 데이터가 모두 지워집니다.<br>정말로 나가겠습니까?");
    document.getElementById('btnPostWriteExit').setAttribute('data-target', '#alertCheckModal');
    btn_cancel_update_post.setAttribute('onclick','document.getElementById("formPostBack").submit()');
    
    return;
}


/***********************************************************************************************
 * 게시글 삭제
 ***********************************************************************************************/
function deletePost() {
    var btn_delete_post = document.getElementById('btnModalYes');

    $("#alert_check_msg").html("삭제된 데이터는 복구할 수 없습니다.<br>정말로 삭제하시겠습니까?");
    document.getElementById('btnPostDelete').setAttribute('data-target', '#alertCheckModal');
    btn_delete_post.setAttribute('onclick','document.getElementById("formPostDelete").submit()');
    
    return;
}


/***********************************************************************************************
 * 사용자 카테고리 영역 접고 펼치기
 ***********************************************************************************************/
function toggleUserCategory() {
    $('#wrapUserCategory').toggle();
}


/***********************************************************************************************
 * 사용자 카테고리 설정 영역 접고 펼치기
 ***********************************************************************************************/
function toggleUserCategorySetting(state) {
    if(state == 'open') {
        $('#userCategorySetting').hide();
        $('#userCategorySettingClose').show();
        $('#divCreateUserCategoryNew').show();
        $('.iUserCategory').show();
    }
    else if(state == 'close') {
        $('#userCategorySetting').show();
        $('#userCategorySettingClose').hide();
        $('#divCreateUserCategoryNew').hide();
        $('.iUserCategory').hide();
    }
}


/***********************************************************************************************
 * 사용자 카테고리 가져오기
 ***********************************************************************************************/
function getUserCategory() {
    var user_id = $("#userID").val();

    $.ajax({
        type: 'POST',
        url: 'category',
        data: {
            'user_id': user_id,
        },
        success: function(response) {
            $('#wrapUserCategory').html(response);
        },
        error: function(err) {
            console.log(err);
        }
    });
}


/***********************************************************************************************
 * 사용자 카테고리 생성 영역 접고 펼치기
 ***********************************************************************************************/
function toggleCreateUserCategory(state, category_id) {
    if (state == 'C') {
        var div_create_user_category = $("#divCreateUserCategory0");

        div_create_user_category.toggle();

        if (div_create_user_category.css('display') == 'block') {
            div_create_user_category.css('display', 'inline-block');
        }
    }
    else if (state == 'R') {
        var div_create_user_category = $("#divCreateUserCategoryRe" +category_id);

        div_create_user_category.toggle();

        if (div_create_user_category.css('display') == 'block') {
            div_create_user_category.css('display', 'inline-block');
        }
    }
}


/***********************************************************************************************
 * 사용자 카테고리 게시글 페이징
 ***********************************************************************************************/
function goCategoryPage(page, state, per_category_id) {
    $.ajax({
        type: 'POST',
        url: 'category/paging',
        data: {
            'page': page,
            'state': state,
            'per_category_id': per_category_id,
        },
        success: function(response) {
            $('#wrapList').html(response);

            // 페이지 번호 선택 시, 게시물 상단 위치로 페이지 이동
            $(".pageNum").click(function() {
                var offset = $('#wrapMainBody').offset();

               $('html, body').animate({scrollTop : offset.top - 20}, 700);

               return false;
            });
        },
        error: function(err) {
            console.log(err);
        }
    });
}


/***********************************************************************************************
 * 사용자 카테고리 생성
 ***********************************************************************************************/
function createUserCategory(state, category_id) {
    if (state == 'C') {
        var per_category_name = $("#createUserCategory0").val();

        if (per_category_name == '') {
            $("#alert_warning_msg").text("카테고리명을 입력해주세요.");
            document.getElementById('btnUserCategoryCreate0').setAttribute('data-target', '#alertWarningModal');
            return;
        }

        $.ajax({
            type: 'POST',
            url: 'category/create',
            data: {
                'per_category_name': per_category_name,
                'state': state
            },
            success: function () {
                getUserCategory();
            },
            error: function (err) {
                console.log(err);
            }
        });
    }
    else if (state == 'R') {
        var per_category_name = $("#createUserCategoryRe" + category_id).val();

        if (per_category_name == '') {
            $("#alert_warning_msg").text("카테고리명을 입력해주세요.");
            document.getElementById('btnUserCategoryReCreate' + category_id).setAttribute('data-target', '#alertWarningModal');
            return;
        }

        $.ajax({
            type: 'POST',
            url: 'category/create',
            data: {
                'per_category_name': per_category_name,
                'state': state,
                'parent_category_id': category_id
            },
            success: function () {
                getUserCategory();
            },
            error: function (err) {
                console.log(err);
            }
        });
    }
}


/***********************************************************************************************
 * 사용자 카테고리 수정 영역 접고 펼치기
 ***********************************************************************************************/
function toggleUpdateUserCategory(state, category_id) {
    if (state == 'C') {
        var div_user_category = $("#divUserCategory" +category_id);
        var div_update_user_category = $("#divUpdateUserCategory" +category_id);

        div_user_category.toggle();
        div_update_user_category.toggle();

        if (div_update_user_category.css('display') == 'block') {
            div_update_user_category.css('display', 'inline-block');
        }
    }
    else if (state == 'R') {
        var div_user_category = $("#divUserCategoryRe" +category_id);
        var div_update_user_category = $("#divUpdateUserCategoryRe" +category_id);

        div_user_category.toggle();
        div_update_user_category.toggle();

        if (div_update_user_category.css('display') == 'block') {
            div_update_user_category.css('display', 'inline-block');
        }
    }
}


/***********************************************************************************************
 * 사용자 카테고리 수정
 ***********************************************************************************************/
 function updateUserCategory(state, category_id) {
    if (state == 'C') {
        var per_category_name = $("#updateUserCategory" + category_id).val();
    }
    else if (state == 'R') {
        var per_category_name = $("#updateUserCategoryRe" + category_id).val();
    }

    $.ajax({
        type: 'POST',
        url: 'category/update',
        data: {
            'per_category_id': category_id,
            'per_category_name': per_category_name        },
        success: function () {
            getUserCategory();
        },
        error: function (err) {
            console.log(err);
        }
    });
}


/***********************************************************************************************
 * 사용자 카테고리 삭제 의사 확인하기
 ***********************************************************************************************/
function openDeleteUserCategory(state, category_id) {
    var btn_delete_user_category = document.getElementById('btnModalYes');

    $("#alert_check_msg").html("카테고리에 속한 하위 카테고리 및 게시글이 모두 삭제됩니다.<br>정말로 삭제하시겠습니까?");

    if (state == 'C') {
        document.getElementById('iUserCategoryDelete' + category_id).setAttribute('data-target', '#alertCheckModal');
    }
    else if (state == 'R') {
        document.getElementById('iUserCategoryReDelete' + category_id).setAttribute('data-target', '#alertCheckModal');
    }

    btn_delete_user_category.setAttribute('onclick','deleteUserCategory("' +state+ '", "' +category_id+ '")');
    btn_delete_user_category.setAttribute('data-dismiss','modal');
    
    return;
}


/***********************************************************************************************
 * 사용자 카테고리 삭제
 ***********************************************************************************************/
 function deleteUserCategory(state, category_id) {
    $.ajax({
        type: 'POST',
        url: 'category/delete',
        data: {
            'per_category_id': category_id,
            'state': state
        },
        success: function () {
            getUserCategory();
        },
        error: function (err) {
            console.log(err);
        }
    });
}
