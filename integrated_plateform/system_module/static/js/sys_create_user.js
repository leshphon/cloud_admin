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



<!-- update user -->
var update_user_id;
function getUserInfo(id,name,email) {
    update_user_id = id;
    $("#update_name").val(name);
    $("#update_email").val(email);

}
function updateUserJsonGet(){
    let update_name = $("#update_name").val();
    let update_email = $("#update_email").val();
    let json_param = {
        "name":update_name,
        "email":update_email,
        "user_id":update_user_id,
    };
    console.log(json_param);
    return json_param;
}
$(document).on('click','#updateUser_btn',function () {
    $.ajax({
        type:"GET",
        url:"/sys_update_user",
        data:{"data":JSON.stringify(updateUserJsonGet())},
        success:function (data) {
            console.log("success",data)
            window.location.reload();
        },
        error:function () {
            alert("update error");
            // console.log(data["data"]);
        }
    });
});
<!-- update user -->