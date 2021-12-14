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
