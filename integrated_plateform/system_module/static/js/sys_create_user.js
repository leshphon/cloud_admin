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

// function getUserInfo(name,email) {
//     $.ajax({
//         type:'get',
//         url: "/project_info",
//         dataType:'json',
//         success: function (data) {
//             // console.log(data);
//             var array0;
//             for(var i=0;i<data.length;i++){
//                 if (data[i][0] == ide_id){
//                     array0 = data[i];
//                     break;
//                 }
//             }
//             // console.log(array0);
//             $("#update_name").val(name);
//             $("#update_email").val(email);
//         }
//     })
// }
function getUserInfo(name) {

    console.log("this is qianduan name",name);
    // console.log("this is qianduan email",email);
    $("#update_name").val(name);
    // $("#update_email").val(email);

}

function updateIdeJsonGet(){
    let ide_update_name = $("#update_name").val();
    let ide_update_description = $("#update_email").val();
    let ide_update_id = $("#update_id").val();
    console.log(ide_update_id);
    let json_param = {
        "name":ide_update_name,
        "description":ide_update_description,
        "id":ide_update_id,
    };
    console.log(json_param);
    return json_param;
}

$(document).on('click','#updatePrj_btn',function () {
    $.ajax({
        type:"GET",
        url:"/ide_update",
        data:{"data":JSON.stringify(updateIdeJsonGet())},

        success:function (data) {
            window.location.reload();
        },
        error:function () {
            alert("update error");
            // console.log(data["data"]);
        }
    });
});