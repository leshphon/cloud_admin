<!-- update vdc -->
var update_vdc_id;
function getVDCInfo(id,name,desc) {
    update_vdc_id = id;
    $("#update_name").val(name);
    $("#update_desc").val(desc);
}
function updateVDCJsonGet(){
    let update_name = $("#update_name").val();
    let update_desc = $("#update_desc").val();
    let json_param = {
        "name":update_name,
        "desc":update_desc,
        "vdc_id":update_vdc_id,
    };
    console.log(json_param);
    return json_param;
}
$(document).on('click','#updateVDC_btn',function () {
    $.ajax({
        type:"GET",
        url:"/sys_update_VDC",
        data:{"data":JSON.stringify(updateVDCJsonGet())},
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

<!-- delete vdc -->
var delete_vdc_id;
function getDeleteID(id) {
    delete_vdc_id = id;
}
$(document).on('click','#deleteVDCBtn',function () {
    $.ajax({
        type:"GET",
        url:"/sys_delete_VDC",
        data: {"id":delete_vdc_id},
        success:function(data) {
            // alert('success delete');
            window.location.reload();
        },
        error:function() {
            alert('delete failed')
        }
    });
});


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
                '<td>instance</td>' +
                '<td>ram</td>' +
                '<td>volume</td>' +
                '</tr>' +
                '<tr>' +
                '<td>' + data[0].fields.cpu + '</td>' +
                '<td>' + data[0].fields.instances + '</td>' +
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

