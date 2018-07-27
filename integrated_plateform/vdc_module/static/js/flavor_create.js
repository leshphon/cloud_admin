function cancelBtn() {
    window.history.go(-1);
}

// 绑定创建实例类型提交事件
$(document).on('click', '#createFlavor_btn', function () {
    $.ajax({
        type: "POST",
        data: {
            'data_body': JSON.stringify(createVSJsonGet()),
          },
        url : "/vdc_create_server",
        success: function (data) {
            alert('实例类型创建成功!');
            window.location.reload();
        },
        error: function () {
            alert('实例类型创建失败!');
            // alert();
        }
    });
});

// 封装创建虚拟机时需要的json参数
function createVSJsonGet() {
    let p = {};
    let json_param;
    json_param = {
        "name": $('#name').val(),
        "ram": $('#ram').val(),
        "vcpus":$('#vcpus').val(),
        "disk": $('#disk').val(),
        ///os-flavor-access:is_public
    };
    return json_param;
}