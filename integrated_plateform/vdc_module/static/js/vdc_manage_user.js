$(document).on('click', '#vdc_create_user_sub', function () {
    if ($('#password_1').val() === $('#password_2').val()){
        document.getElementById('vdc_create_user_form').submit();
    }
    else {
        alert('两次输入的密码不一致');
    }
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
        url:"/vdc_update_user",
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


<!-- delete user -->
var delete_user_id;
function getDeleteUserID(id) {
    delete_user_id = id;
    console.log(delete_user_id);
}
$(document).on('click','#deleteUserBtn',function () {
    $.ajax({
        type:"GET",
        url:"/vdc_delete_user",
        data: {"id":delete_user_id},
        success:function(data) {
            // alert('success delete');
            window.location.reload();
        },
        error:function() {
            alert('delete failed')
        }
    });
});