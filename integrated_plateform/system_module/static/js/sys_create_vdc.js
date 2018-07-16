$(document).on('click', '#sys_create_vdc_user_sub', function () {
    if ($('#password_1').val() === $('#password_2').val()){
        // document.getElementById('sys_create_vdc_admin_form').submit();
        $.ajax({
            type: 'POST',
            data: {
                'username': $("input[name=username]").val(),
                'email': $("input[name=email]").val(),
                'password': $("input[name=password]").val(),
                'user_role': $("#assign_admin_to_vdc").val(),
            },
            url: '/sys_create_vdc_admin',       // 进入被点击的action的处理函数
            dataType: 'json',
            success: function (data) {
                alert('vdc管理员创建成功');
                for (let n = 0; n < data.length; n++ ) {
                    console.log(data[n]);
                    let item = data[n];
                    // let fields = data[n].fields;
                    let vdc_admin_html;
                    vdc_admin_html = '<option value="' + item.id +'">' +
                        item['fields'].name +
                        '</option>';
                    let admin_list_box = $("#vdc_admin_list");
                    admin_list_box.prepend(vdc_admin_html);
                    console.log(admin_list_box);
                    console.log(item);
                    $('#create_vdc_admin').modal('hide');
                    $('#vdc_admin_list').val(item['fields'].name);
                }
            },
            error: function () {
                alert('vdc admin创建失败')
            }
        })
    }
    else {
        alert('两次输入的密码不一致');
    }
});

function createVDC() {
    document.getElementById('vdc_create_form').submit();
}

function get_quota(id) {
    console.log('target quota id is ' + id);
    $.ajax({
        type: 'POST',
        data: {'quota_id': id},
        url: '/sys_get_quota',
        dataType: 'json',
        success: function (data) {
            console.log(data);
            let pop_box = document.getElementById('quota_' + id);
            // console.log(pop_box.getAttribute('data-title'));
            console.log(pop_box.dataset.title);
            pop_box.setAttribute('data-content', '<table class="table table-striped table-bordered m-b-xs table-hover">' +
                '<tr>' +
                '<td>cpu</td>' +
                '<td>ram</td>' +
                '<td>disk</td>' +
                '</tr>' +
                '<tr>' +
                '<td>' + data[0].fields.cpu + '</td>' +
                '<td>' + data[0].fields.ram + '</td>' +
                '<td>' + data[0].fields.volume + '</td>' +
                '</tr>' +
                '</table>');
            $('#quota_' + id).popover('toggle')
        },
        error: function () {
            alert('quota get failure');
        }
    })
}

