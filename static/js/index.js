$(document).ready(function() {
    goPage(1, '');
});


/***********************************************************************************************
 * 게시글 페이징
 ***********************************************************************************************/
 function goPage(page, com_category_id) {
    $.ajax({
        type: 'GET',
        url: 'paging',
        data: {
            'page': page,
            'com_category_id': com_category_id,
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
 * 게시글 검색
 ***********************************************************************************************/
function goSearch(page) {
    var division = $("#inputDivision").val();
    var keyword = $("#inputKeyword").val();

    var alert_btn = document.getElementById('btnSearch');

    if(division == null) {
        $("#alert_msg").text("카테고리를 선택해주세요.");
        alert_btn.setAttribute('data-target', '#alertModal');
        return;
    }
    else if(keyword == '') {
        $("#alert_msg").text("키워드를 입력해주세요.");
        alert_btn.setAttribute('data-target', '#alertModal');
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