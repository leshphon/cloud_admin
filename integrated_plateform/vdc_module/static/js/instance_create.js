var image_checked_id;
var net_checked_id;

function cancelBtn() {
    window.history.go(-1);
}

$(document).ready(function () {
    network_get();
    flavor_get();
    image_get();
    keypair_get();
});

function network_get() {
    $.ajax({
        type:'get', //请求方式，默认get
        url :"/vdc_show_net",
        dataType: 'json',
        success:function(data,status){
           $('#netlist').html('');
           // $("#available_zone").empty();
           // $("#available_zone").html("<option value='None'>Any Available Zone</option>");
           $str = '';
           $.each(data.networks,function(i,val){
              $str = $str + '<tr>';
              $str = $str + '<td hidden>' + val.id + '</td>';
              $str = $str + '<td class="hidden_show" style="cursor: pointer"><b class="caret"></b><span>' + val.name + '</span></td>';
              $str = $str + '<td>' + val.shared + '</td>';
              $str = $str + '<td>' + val.admin_state_up + '</td>';
              $str = $str + '<td>' + val.status + '</td>';
              $str = $str + '<td><input class="network_target_selector" type=\"radio\" value="' + val.id + '" name="netlist"></td>';
              $str = $str + '</tr>';
              $str = $str + '<tr hidden>';
              $str = $str + '<td colspan="6">';
              $str = $str + '<div>';
              $str = $str + '<dl class="dl-horizontal">';
              $str = $str + '<dt>ID</dt>';
              $str = $str + '<dd>' + val['id'] + '</dd>';
              $str = $str + '<dt>Project</dt>';
              $str = $str + '<dd>' + val['project_id'] + '</dd>';
              $str = $str + '<dt>External Network</dt>';
              $str = $str + '<dd>' + val['external_network'] + '</dd>';
              $str = $str + '</dl>';
              $str = $str + '</div>';
              $str = $str + '<div class="row">';
              $str = $str + '<dl class="col-sm-4">';
              $str = $str + '<dt>Type</dt>';
              $str = $str + '<dd>' + val['provider:network_type'] + '</dd>';
              $str = $str + '</dl>';
              $str = $str + '<dl class="col-sm-4">';
              $str = $str + '<dt>Segmentation ID</dt>';
              $str = $str + '<dd>' + val['provider:segmentation_id'] + '</dd>';
              $str = $str + '</dl>';
              $str = $str + '<dl class="col-sm-4">';
              $str = $str + '<dt>Physical Network</dt>';
              $str = $str + '<dd>' + val['provider:physical_network'] + '</dd>';
              $str = $str + '</dl>';
              $str = $str + '</td>';
              $str = $str + '</tr>';
              if ( i === 0){
                  $("#network_name").find('b').eq(0).text(val.name);
                  $("#network_desc").text(val.description);
                  net_checked_id = val.id;
              }
           });
           $('#netlist').append($str);
           if(data.networks === "" ||  data.networks === "undefined"){
              $('#netlist').html('<td colspan="10"  style="height:200px;text-align:center;color: #23527c">暂无相关数据...</td>');
           }
        },error:function(data,statsu){
           alert("network发送请求失败！！！");
        }
    });
}

function flavor_get() {
    $.ajax({
        type: 'get',
        url: '/vdc_show_flavors',
        dataType: 'json',
        success: function (data) {
            console.log(data);
            $('#flavor_list').html('');
            $str = '';
            $.each(data.flavors, function(i,val){
                console.log(i);
                $str = '<li class="flavor_item"><a href="#">' +
                    '<input hidden name="flavor_id" value="' + val.id +'">' +
                    '<span><b>' + val.name + '</b></span><br>' +
                    '<span>' + val.ram + 'MB内存， ' + val.vcpus + '个vCPU</span>' +
                    '</a></li>';
                if (i === 0){
                    $('#flavor_name').text(val.name);
                    $('#flavor_detail').find('b').eq(0).text(val.ram + 'MB内存， ' + val.vcpus + '个vCPU');
                    $("#flavor_id").text(val.id);
                }
            });
            $('#flavor_list').append($str);
            if(data.flavors == "" ||  data.flavors == "undefined"){
               $('#flavorlist').html('<td colspan="10"  style="height: 200px;text-align:center;color: #23527c">暂无相关数据...</td>');
             }
        },
        error: function () {
            console.log('flavor request failure');
        }
    })
}

function image_get() {
    $.ajax({
        type:'get', //请求方式，默认get
        url :"/vdc_show_image",
        dataType: 'json',
        success:function(data,status){
           $('#image_list').html('');
           $str = '';
           $.each(data.images,function(i,val){
              $str = $str + '<tr>';
              $str = $str + '<td hidden>'+val.id+'</td>';
              $str = $str + '<td class="hidden_show" style="cursor: pointer"><b class="caret"></b><span>'+val.name+'</span></td>';
              $str = $str + '<td>'+val.status+'</td>';
              $str = $str + '<td>'+val.created_at +'</td>';
              $str = $str + '<td>'+val.disk_format+'</td>';
              $str = $str + '<td>'+val.visibility+'</td>';
              $str = $str + '<td hidden>'+val.description+'</td>';
              $str = $str + '<td><input class="image_target_selector" type=\"radio\" value="' + val.id + '" name="imagelist"></td>';
              $str = $str + '</tr>';
              $str = $str + '<tr hidden>';
              $str = $str + '<td colspan="6">';
              $str = $str + '<div class="row">';
              $str = $str + '<dl class="col-sm-4">';
              $str = $str + '<dt>Min Disk(GB)</dt>';
              $str = $str + '<dd>' + val.min_disk + '</dd>';
              $str = $str + '</dl>';
              $str = $str + '<dl class="col-sm-4">';
              $str = $str + '<dt>Min RAM(MB)</dt>';
              $str = $str + '<dd>' + val.min_ram + '</dd>';
              $str = $str + '</dl>';
              $str = $str + '</div>';
              $str = $str + '</td>';
              $str = $str + '</tr>';
              if (i === 0){
                  $("#image_name").find('b').eq(0).text(val.name);
                  $("#image_desc").text(val.description);
                  image_checked_id = val.id;
              }
           });
           $('#image_list').append($str);
           $('#page_content').html($('#page1_desc').html());
           if(data.images == "" ||   data.images == "undefined"){
              $('#image_list').html('<td colspan="10"  style="height:200px;text-align:center;color: #23527c">暂无相关数据...</td>');
           }
        },error:function(data,statsu){
           alert("image发送请求失败！！！！");
        }
    });
}

function keypair_get() {
    $.ajax({
        type: 'get',
        url: "/vdc_show_keypairs",
        dataType: 'json',
        success: function (data, status) {
            $("#keypair_list").html('');
            $.each(data.keypairs, function (i, val) {
                let keyPairHtml = "<tr>" +
                    "<td class='hidden_show' style='cursor: pointer'><b class='caret'></b>" + val.keypair.name + "</td>" +
                    "<td>" + val.keypair.fingerprint + "</td>" +
                    "<td><input class='keyPair_target_selector' type='radio' value='" + val.keypair.name +"' name='keyPairList'></td>" +
                    "</tr>" +
                    "<tr hidden>" +
                    "<td colspan='2'>" +
                    "<div class='container-fluid'>" +
                    "<hz-detail-row>" +
                    "<dl>" +
                    "<dt>Public Key</dt>" +
                    "<dd>" +
                    "<pre>" +
                    "<code>" +
                     val.keypair.public_key +
                    "</code>" +
                    "</pre>" +
                    "</dd>" +
                    "</dl>" +
                    "</hz-detail-row>" +
                    "</div>" +
                    "</td>" +
                    "</tr>";
                $("#keypair_list").append(keyPairHtml);
                // console.log(val.keypair.public_key);
                // console.log(val.keypair.name);
                // console.log(val.keypair.fingerprint);
            });
            if(data.keypairs == "" ||   data.keypairs == "undefined"){
                $('#keypair_list').html('<td colspan="10"  style="height:200px;text-align:center;color: #23527c">暂无相关数据...</td>');
            }
            // console.log(data);
            // console.log(data.keypairs);
            // console.log(data.keypairs[0].keypair);
            // console.log(data.keypairs[0].keypair.public_key);
        },
        error: function (data) {
            alert("key pair获取失败");
        }
    })
}

// $(document).on('click', '#test001', function () {
//     console.log('网路测试');
//     // $.ajax({
//     //     type: 'get',
//     //     url: '/vdc_show_net',
//     //     dataType: 'json',
//     //     success: function (data) {
//     //         console.log(data);
//     //     },
//     //     error: function () {
//     //         console.log('net request failure');
//     //     }
//     // })
//     //
//     $.ajax({
//         type:'get', //请求方式，默认get
//         url :"/vdc_show_net",
//         dataType: 'json',
//         success:function(data,status){
//            $('#netlist').html('');
//            // $("#available_zone").empty();
//            // $("#available_zone").html("<option value='None'>Any Available Zone</option>");
//            $str = '';
//            $.each(data.networks,function(i,val){
//               $str = $str + '<tr>';
//               $str = $str + '<td hidden>' + val.id + '</td>';
//               $str = $str + '<td class="hidden_show" style="cursor: pointer"><b class="caret"></b>' + val.name + '</td>';
//               $str = $str + '<td>' + val.shared + '</td>';
//               $str = $str + '<td>' + val.admin_state_up + '</td>';
//               $str = $str + '<td>' + val.status + '</td>';
//               $str = $str + '<td><input class="network_target_selector" type=\"radio\" value="' + val.id + '" name="netlist"></td>';
//               $str = $str + '</tr>';
//               $str = $str + '<tr hidden>';
//               $str = $str + '<td colspan="6">';
//               $str = $str + '<div>';
//               $str = $str + '<dl class="dl-horizontal">';
//               $str = $str + '<dt>ID</dt>';
//               $str = $str + '<dd>' + val['id'] + '</dd>';
//               $str = $str + '<dt>Project</dt>';
//               $str = $str + '<dd>' + val['project_id'] + '</dd>';
//               $str = $str + '<dt>External Network</dt>';
//               $str = $str + '<dd>' + val['external_network'] + '</dd>';
//               $str = $str + '</dl>';
//               $str = $str + '</div>';
//               $str = $str + '<div class="row">';
//               $str = $str + '<dl class="col-sm-4">';
//               $str = $str + '<dt>Type</dt>';
//               $str = $str + '<dd>' + val['provider:network_type'] + '</dd>';
//               $str = $str + '</dl>';
//               $str = $str + '<dl class="col-sm-4">';
//               $str = $str + '<dt>Segmentation ID</dt>';
//               $str = $str + '<dd>' + val['provider:segmentation_id'] + '</dd>';
//               $str = $str + '</dl>';
//               $str = $str + '<dl class="col-sm-4">';
//               $str = $str + '<dt>Physical Network</dt>';
//               $str = $str + '<dd>' + val['provider:physical_network'] + '</dd>';
//               $str = $str + '</dl>';
//               $str = $str + '</td>';
//               $str = $str + '</tr>';
//               //available_zone options add
//               // for (var k = 0; k < val.availability_zones.length; k++){
//               //      var selectDom = document.getElementById("available_zone");
//               //      var option = document.createElement("option");
//               //      option.value = val.availability_zones[k];
//               //      option.innerHTML = val.availability_zones[k];
//               //      selectDom.appendChild(option);
//               //      // var optionsHtml = "<option value='" + val.availability_zones[k] + "'>val.availability_zones[k]</option>";
//               //      // $("#available_zone").append(optionsHtml);
//               // }
//            });
//            $('#netlist').append($str);
//            if(data.networks === "" ||  data.networks === "undefined"){
//               $('#netlist').html('<td colspan="10"  style="height:200px;text-align:center;color: #23527c">暂无相关数据...</td>');
//            }
//         },error:function(data,statsu){
//            alert("network发送请求失败！！！");
//         }
//     });
// });
//
// $(document).on('click', '#test002', function () {
//     console.log('flavoyr测试');
//     $.ajax({
//         type: 'get',
//         url: '/vdc_show_flavors',
//         dataType: 'json',
//         success: function (data) {
//             console.log(data);
//             $('#flavor_list').html('');
//             $str = '';
//             $.each(data.flavors, function(i,val){
//                 console.log(i);
//                 $str = '<li id="flavor_item"><a href="#"><span><b>' + val.name + '</b></span><br><span>' + val.ram + 'MB内存，' + val.vcpus + '个vCPU</span></a></li>'
//             });
//             $('#flavor_list').append($str);
//             if(data.flavors === "" ||  data.flavors === "undefined"){
//                $('#flavorlist').html('<td colspan="10"  style="height: 200px;text-align:center;color: #23527c">暂无相关数据...</td>');
//              }
//         },
//         error: function () {
//             console.log('flavor request failure');
//         }
//     })
// });
//
// $(document).on('click', '#test003', function () {
//     console.log('image测试');
//     // $.ajax({
//     //     type: 'get',
//     //     url: '/vdc_show_image',
//     //     dataType: 'json',
//     //     success: function (data) {
//     //         console.log(data);
//     //     },
//     //     error: function () {
//     //         console.log('flavor request failure');
//     //     }
//     // })
//
//     $.ajax({
//         type:'get', //请求方式，默认get
//         url :"/vdc_show_image",
//         dataType: 'json',
//         success:function(data,status){
//            $('#imagelist').html('');
//            $str = '';
//            $.each(data.images,function(i,val){
//               $str = $str + '<tr>';
//               $str = $str + '<td hidden>'+val.id+'</td>';
//               $str = $str + '<td class="hidden_show" style="cursor: pointer"><b class="caret"></b>'+val.name+'</td>';
//               $str = $str + '<td>'+val.status+'</td>';
//               $str = $str + '<td>'+val.created_at +'</td>';
//               $str = $str + '<td>'+val.disk_format+'</td>';
//               $str = $str + '<td>'+val.visibility+'</td>';
//               $str = $str + '<td><input class="image_target_selector" type=\"radio\" value="' + val.id + '" name="imagelist"></td>';
//               $str = $str + '</tr>';
//               $str = $str + '<tr hidden>';
//               $str = $str + '<td colspan="6">';
//               $str = $str + '<div class="row">';
//               $str = $str + '<dl class="col-sm-4">';
//               $str = $str + '<dt>Min Disk(GB)</dt>';
//               $str = $str + '<dd>' + val.min_disk + '</dd>';
//               $str = $str + '</dl>';
//               $str = $str + '<dl class="col-sm-4">';
//               $str = $str + '<dt>Min RAM(MB)</dt>';
//               $str = $str + '<dd>' + val.min_ram + '</dd>';
//               $str = $str + '</dl>';
//               $str = $str + '</div>';
//               $str = $str + '</td>';
//               $str = $str + '</tr>';
//            });
//            $('#imagelist').append($str);
//            $('#page_content').html($('#page1_desc').html());
//            if(data.images == "" ||   data.images == "undefined"){
//               $('#imagelist').html('<td colspan="10"  style="height:200px;text-align:center;color: #23527c">暂无相关数据...</td>');
//            }
//         },error:function(data,statsu){
//            alert("image发送请求失败！！！！");
//         }
//     });
// });

$(document).on('click', '.flavor_item', function () {
    $('#flavor_name').text($(this).find('span').eq(0).text());
    $('#flavor_detail').find('b').text($(this).find('span').eq(1).text());
    $('#flavor_id').text($(this).find('a').find('input').val());
    // console.log($(this).find('a').eq(0).find('input').val());
});


$(document).on('click', '#selected_image', function () {
    let image_name = $("input[name=imagelist]:checked").parent().parent().find('td').eq(1).find('span').html();
    let image_desc = $("input[name=imagelist]:checked").parent().parent().find('td').eq(6).html();
    image_checked_id = $("input[name=imagelist]:checked").parent().parent().find('td').eq(0).html();
    console.log(image_checked_id);
    $("#image_name").find('b').text(image_name);
    $("#image_desc").text(image_desc);
    // $(this).attr('data-dismiss', 'modal');
    $('#myModal').modal('hide');
});

$(document).on('click', '#selected_net', function () {
    let net_name = $("input[name=netlist]:checked").parent().parent().find('td').eq(1).find('span').html();
    net_checked_id = $("input[name=netlist]:checked").parent().parent().find('td').eq(0).html();
    console.log(net_checked_id);
    $("#network_name").find('b').text(net_name);
    // $(this).attr('data-dismiss', 'modal');
    $('#myModal_network').modal('hide');
});

// 详细框显示与收起
$(document).on('click', ".hidden_show", function () {
    $(this).parent().next().fadeToggle();
});

// 绑定创建虚拟机提交事件
$(document).on('click', '#createVS_btn', function () {
    $.ajax({
        type: "POST",
        data: {
            'data_body': JSON.stringify(createVSJsonGet()),
            'amount': $("#server_amount").val(),
        },
        // data: JSON.stringify(createVSJsonGet()),
// <<<<<<< HEAD
//         url : "/createVir",
//         // dataType: 'json',    //添加此行后显示提交出错
// =======
        url : "/vdc_create_server",
        // dataType: 'json',
// >>>>>>> ff98e41d34f0c7ef7ea1c7b73f4b30feec2ce7af
        success: function (data) {
            alert('New Server Created!');
            window.location.reload();
        },
        error: function () {
            alert('false');
            // alert();
        }
    });
});

// 封装创建虚拟机时需要的json参数
function createVSJsonGet() {
    let p = {};
    let flavor_checked_id = $("#flavor_id").text();
    // let key_pair_name = $("input[name='keyPairList']:checked").val();
    // let available_zone = $("#available_zone").val();
    let json_param = {
        "server_name": $('#server_name').val(),
        // 'server_available_zone' : $("#available_zone").val(),
        "server_imageRef": image_checked_id,
        "server_flavorRef": flavor_checked_id,
        "network_uuid": net_checked_id,
        // "server_key_name": key_pair_name,

    };
    // if (available_zone != 'None'){
    //     json_param['server_availability_zone'] = available_zone;
    // }
    return json_param;
}