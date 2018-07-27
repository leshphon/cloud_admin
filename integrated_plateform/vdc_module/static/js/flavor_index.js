$(document).ready(function () {
    flavor_get();
});

function flavor_get() {
    $.ajax({
        type: 'get',
        url: '/vdc_flavor_show',
        dataType: 'json',
        success: function (data) {
            console.log(data);
            $('#flavor_list').html('');
            $str = '';
            $.each(data.flavors, function (i, val) {
                console.log(i);
                $str = $str + '<tr>';
                $str = $str + '<td hidden>' + val.id + '</td>';
                $str = $str + '<td>' + val.name + '</td>';
                $str = $str + '<td>' + val.vcpus + '</td>';
                $str = $str + '<td>' + val.ram + '</td>';
                $str = $str + '<td>' + val.disk + '</td>';
                $str = $str +  '<td>' + '<div class="btn-group">' +
                       '<a href="#" class="btn btn-white btn-sm dropdown-toggle" data-toggle="dropdown"><span class="glyphicon glyphicon-wrench"></span></a>' +
                       '<ul class="dropdown-menu">' +
                       '<li><a class="btn" href="#" onclick="">删除</a></li>' +
                       '</ul>' +
                       '</div>' +
                       '</td>';
                $str = $str + '<td><input class="instance_target_selector" type=\"checkbox\" name="' + val.status +'" value="' + val.id  + '"></td>';

                $str = $str + '</tr>';
                $('#flavor_list').append($str);
            });
            if (data.flavors == "" || data.flavors == "undefined") {
                $('#flavorlist').html('<td colspan="10"  style="height: 200px;text-align:center;color: #23527c">暂无相关数据...</td>');
            }
        },
        error: function () {
            console.log('flavor request failure');
        }
    })
}
