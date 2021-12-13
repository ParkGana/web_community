$(document).ready(function() {
    // 회원가입 시, ID에 영문자와 숫자만 입력 가능
    $("input[name=inputID]").keyup(function() {
        $(this).val($(this).val().replace(/[^0-9a-zA-Z]/gi, ''));
    });

    // 회원가입 시, 이름에 영문자와 한글만 입력 가능
    $("input[name=inputName]").keyup(function() {
        $(this).val($(this).val().replace(/[^a-zA-Zㄱ-ㅎ가-힣]/gi, ''));
    });

    // 회원가입 시, 전화번호에 숫자만 입력 가능
    $("input[name=inputTel]").keyup(function() {
        $(this).val($(this).val().replace(/[^0-9]/gi, ''));
    });

    $(".inputLogin").focus(function() {
       $("#divError").html('');
    });

    // 아이디 값 변경 시, 아이디 중복확인 필요
    $("#inputID").change(function() {
        $("#checkUserID").val("unchecked");
    });
});


/***********************************************************************************************
 * 회원가입
 ***********************************************************************************************/
function validation() {
    var user_id = $("#inputID").val();
    var user_pwd = $("#inputPassword").val();
    var user_pwd_check = $("#inputPasswordCheck").val();
    var user_name = $("#inputName").val();
    var user_gender = $("input[name='gender']:checked").val();
    var user_birth_year = $("#inputYear").val();
    var user_birth_month = $("#inputMonth").val();
    var user_birth_day = $("#inputDay").val();
    var user_email = $("#inputEmail").val();
    var user_tel = $("#inputTel").val();
    var check_user_id = $("#checkUserID").val();

    var alert_btn = document.getElementById('btnJoin');

    if(user_id =='') {
        $("#alert_msg").text("아이디를 입력해주세요.");
        alert_btn.setAttribute('data-target', '#alertModal');
        return;
    }
    else if(check_user_id == 'unchecked') {
        $("#alert_msg").text("아이디 중복체크를 해주세요.");
        alert_btn.setAttribute('data-target', '#alertModal');
        return;
    }
    if(user_pwd == '') {
        $("#alert_msg").text("비밀번호를 입력해주세요.");
        alert_btn.setAttribute('data-target', '#alertModal');
        return;
    }
    else if(user_pwd_check == '') {
        $("#alert_msg").text("비밀번호를 다시 한번 입력해주세요.");
        alert_btn.setAttribute('data-target', '#alertModal');
        return;
    }
    else if(user_pwd != user_pwd_check) {
        $("#alert_msg").text("입력하신 비밀번호가 서로 일치하지 않습니다.");
        alert_btn.setAttribute('data-target', '#alertModal');
        return;
    }
    if(user_name == '') {
        $("#alert_msg").text("이름을 입력해주세요.");
        alert_btn.setAttribute('data-target', '#alertModal');
        return;
    }
    if(user_gender == undefined) {
        $("#alert_msg").text("성별을 선택해주세요.");
        alert_btn.setAttribute('data-target', '#alertModal');
        return;
    }
    if(user_birth_year == null || user_birth_month == null || user_birth_day == null) {
        $("#alert_msg").text("생년월일을 선택해주세요.");
        alert_btn.setAttribute('data-target', '#alertModal');
        return;
    }
    if(user_email != '') {
        if(!(/^[_a-zA-Z0-9]+([-+.][_a-zA-Z0-9]+)*@([0-9a-zA-Z_-]+)(\.[0-9a-zA-Z_-]+){1,2}$/i.test(user_email))) {
            $("#alert_msg").text("올바른 이메일 형식으로 입력해주세요.");
            alert_btn.setAttribute('data-target', '#alertModal');
            return;
        }
    }

    // 월, 일 데이터가 한자리일 경우 앞에 0 붙이기
    if(user_birth_month.length == 1) {
        user_birth_month = '0' + user_birth_month;
    }
    if(user_birth_day.length == 1) {
        user_birth_day = '0' + user_birth_day;
    }

    $.ajax({
        type: 'POST',
        url: 'join',
        data: {
            'user_id': user_id,
            'user_pwd': user_pwd,
            'user_name': user_name,
            'user_gender': user_gender,
            'user_birth': user_birth_year + user_birth_month + user_birth_day,
            'user_email': user_email,
            'user_tel': user_tel,
        },
        success: function() {
            $("#alert_msg").text("회원가입이 성공적으로 완료되었습니다.");
            alert_btn.setAttribute('data-target', '#alertModal');

            $("#joinModal").modal('hide');
            setJoin();
        },
        error: function() {
            $("#alert_msg").text("회원가입 도중 에러가 발생하였습니다.");
            alert_btn.setAttribute('data-target', '#alertModal');
        }
    });
}


/***********************************************************************************************
 * 회원가입 유효성 검사 - 아이디 중복 확인
 ***********************************************************************************************/
function checkUserID() {
    var user_id = $("#inputID").val();

    var alert_btn = document.getElementById('btnCheckUserID');

    if(user_id =='') {
        $("#alert_msg").text("아이디를 입력해주세요.");
        alert_btn.setAttribute('data-target', '#alertModal');
        return;
    }

    $.ajax({
        type: 'POST',
        url: 'join/checkUserID',
        data: {
            'user_id': user_id,
        },
        success: function() {
            $("#alert_msg").text("사용할 수 없는 아이디입니다.");
            alert_btn.setAttribute('data-target', '#alertModal');

            $("#checkUserID").val("unchecked");
        },
        error: function() {
            $("#alert_msg").text("사용 가능한 아이디입니다.");
            alert_btn.setAttribute('data-target', '#alertModal');

            $("#checkUserID").val("checked");
        }
    });
}


/***********************************************************************************************
 * 회원가입 양식 초기화
 ***********************************************************************************************/
function setJoin() {
    $("#inputID").val('');
    $("#inputPassword").val('');
    $("#inputPasswordCheck").val('');
    $("#inputName").val('');
    $("input[name='gender']").prop('checked', false);
    $("#inputYear").val('');
    $("#inputMonth").val('');
    $("#inputDay").val('');
    $("#inputEmail").val('');
    $("#inputTel").val('');
    $("#checkUserID").val('unchecked');
}
