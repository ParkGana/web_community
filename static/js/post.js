$(document).ready(function() {
    getUserCategory();
});


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