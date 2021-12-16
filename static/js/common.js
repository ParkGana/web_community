/***********************************************************************************************
 * TOP 버튼
 ***********************************************************************************************/
$(function() {
    $(window).scroll(function() {
        if ($(this).scrollTop() > 100) {
            $('#btnMoveTop').fadeIn();
        }
        else {
            $('#btnMoveTop').fadeOut();
        }
    });

    $("#btnMoveTop").click(function() {
        $('html, body').animate({scrollTop : 0}, 700);

        return false;
    });
});
