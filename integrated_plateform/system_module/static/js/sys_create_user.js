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

function getUserInfo() {
    $.ajax({
        type:'get',
        url: "/project_info",
        dataType:'json',
        success: function (data) {
            // console.log(data);
            var array0;
            for(var i=0;i<data.length;i++){
                if (data[i][0] == ide_id){
                    array0 = data[i];
                    break;
                }
            }
            // console.log(array0);
            $("#ide_update_name").val(array0[1]);
            $("#ide_update_desc").val(array0[2]);
        }
    })
}
