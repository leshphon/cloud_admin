$(document).on('click', '#sys_create_user_sub', function () {
    if ($('#password_1').val() === $('#password_2').val()){
        document.getElementById('sys_create_user_form').submit();
    }
    else {
        alert('两次输入的密码不一致');
    }
});

$(document).on('click', '#del_user', function () {
    let user_id = $(this).parent().parent().parent().parent().parent().find('td').eq(0).text();
    $.ajax({
        type: 'POST',
        data: {'user_id': user_id},
        url: '/sys_del_user',
        // dataType: 'json',
        success: function (data) {
            window.location.reload();
        },
        error: function () {
            alert('user delete fail');
        }
    })
});

