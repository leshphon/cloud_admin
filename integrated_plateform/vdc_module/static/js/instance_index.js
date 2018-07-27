$(document).ready(function () {
    $('#instance_table').dataTable({
        "autoWidth": false,
	    "serverSide": true,
        "aaSorting" : [ [ 1, "desc" ] ],
        // "processing" : true,
        // "paginationType":"full_numbers",
        "columnDefs": [
             {
                 "targets": 0,//这一列是id，但是不想再前端显示，"visible": false,表示隐藏
                 "visible": false
			 }
            // {"orderable":false,"aTargets":[0,3]}
             // {
             //     "targets": 5,//根据样式fa-pencil-square，把第8列显示为一个图标的样式
             //      render: function (data, type, row) {
				// 	   return '<div class="btn-group">' +
             //        '<a href="#" class="btn btn-white btn-sm dropdown-toggle" onclick="showOperateOpts(' + i + ',' + "\'" + val.id + "\'" + ',' + "\'" + virStatus + "\'" +')" data-toggle="dropdown"><span class="glyphicon glyphicon-wrench"></span></a>' +
             //        '<ul id="instanceOperateOpts_' + i + '" class="dropdown-menu">' +
             //        '</ul>' +
             //        '</div>'
             //     }
             // },
             // {
             //     "targets": 6,//根据样式fa-pencil-square，把第8列显示为一个图标的样式
             //      render: function (data, type, row) {
				// 	   return '<input class="instance_target_selector" type=\"checkbox\" name="' + val.status +'" value="' + val.id  + '">'
             //     }
             // }
	    ]
    });
    // getVirList();
});

// 获取实例信息，并写成HTML表格形式
// function getVirList() {
//     $.ajax({
//         type:'get', //请求方式，默认get
//         url :"/vdc_instance_show",
//         success:function(data){
//             $.each(data.servers,function(i, val){
//                 let virStatus;
//                 let net_info;
//                 let addr_obj;
//                 if ( val['OS-EXT-STS:task_state'] === null ){        // 判断是否有正在执行的task
//                     virStatus = val.status;
//                 }
//                 else {
//                     virStatus = val['OS-EXT-STS:task_state'];
//                 }
//                 net_info = val.addresses;
//                 addr_obj = get_items(net_info);
//                 let msgObj = JSON.parse({"":});
//
//
//                 $('#instance_table').dataTable().fnClearTable();   //将数据清除
//                 $('#instance_table').dataTable().fnAddData(packagingdatatabledata(msgObj),true);  //数据必须是json对象或json对象数组
//                 $('#instance_table').dataTable( {
//                     "processing": true,
//                     "ajax": "data/objects_deep.txt",
//                     "columnDefs": [ {
//                         "targets": -1,
//                         "data": null,
//                         "defaultContent": "<button>Click!</button>"
//                      } ]
//                 } );


                // $str = $str + '<tr>';
                // $str = $str + '<td hidden>' + val.id + '</td>';
                // $str = $str + '<td>' + val.name + '</td>';
                // $str = $str + '<td id="ip_box_' + i + '"></td>';
                // $str = $str + '<td>' + virStatus + '</td>';
                // $str = $str + '<td><div class="btn-group">' +
                //     '<a href="#" class="btn btn-white btn-sm dropdown-toggle" onclick="showOperateOpts(' + i + ',' + "\'" + val.id + "\'" + ',' + "\'" + virStatus + "\'" +')" data-toggle="dropdown"><span class="glyphicon glyphicon-wrench"></span></a>' +
                //     '<ul id="instanceOperateOpts_' + i + '" class="dropdown-menu">' +
                //     '</ul>' +
                //     '</div></td>';
                // $str = $str + '<td><input class="instance_target_selector" type=\"checkbox\" name="' + val.status +'" value="' + val.id  + '"></td>';
                // $str = $str + '</tr>';
                // $('#instance_list').append($str);
                // insert_ip_addr(addr_obj, i);
//             });
//             if(data.servers === "" || data.servers === "undefined"){
//                 $('#instance_list').html('<td colspan="10"  style="height:200px;text-align:center;color: #23527c">暂无相关数据...</td>');
//             }
//         },error:function(data,statsu){
//            alert("获取信息失败！！！！！");
//         }
//     });
// }

function insert_ip_addr(obj, i) {
    var IP_place = document.getElementById("ip_box_" + i);
    var ip_html = '';
    $.each(obj, function (n, val) {
        console.log(val.addr);
        ip_html += '<span>' + val['OS-EXT-IPS:type'] + '</span>&ensp;<span>' + val.addr + '</span><br>';
    });
    // console.log(ip_html);
    // $('#ip_box_' + i).append('123');
    IP_place.innerHTML = ip_html;
}

// 点击operate按钮后自动生成对应于不同status下的操作选项函数
function showOperateOpts(j, server_id, status) {
    console.log(status);
    console.log(server_id);
    var operateOptsUl = document.getElementById('instanceOperateOpts_' + j);
    var curRole = $("#current_role").text();
    console.log('current role is ' + curRole);
    $.ajax({
        type: 'get', //请求方式，默认get
        url: "/vdc_getStatusAction",
        success: function (data) {
            var optsHtml = '';
            if (data[status] === undefined) {
                $.each(data['OTHER'], function (i, val) {
                   let action_id = val['name'].replace(/\s/ig, '');
                    let action = val['cn_name'].replace(/\s/ig, '');
// optsHtml += "<li><a href='" + val.href + "/" + server_id + "' class='btn-sm' id='" + val.action.replace(/\s/ig,'') + "'>" + val.action + "</a></li>";
                        optsHtml += '<li><a href="#" class="btn btn-sm" id="' + action_id +
                            '"' +
                            ' onclick="show_cur_status(' +
                            '\'' +
                            server_id +
                            '\'' +
                            ',' +
                            '\'' +
                            val.href +
                            '\'' +
                            ',' +
                            j +
                            ',' +
                            '\'' +
                            action_id +
                            '\'' +
                            // '' +
                            // '' +
                            ')"' +
                            ' name="' +
                            server_id +
                            '">' + action + '</a></li>';
                })
            }
            else {
                $.each(data[status], function (i, val) {
                    let action_id = val['name'].replace(/\s/ig, '');
                    let action = val['cn_name'].replace(/\s/ig, '');
                    // console.log(action);
                    // console.log(action_id);
                    if (curRole === "vdc_user" && val.role === "vdc_user") {
// optsHtml += "<li><a href='" + val.href + "/" + server_id + "' class='btn-sm' id='" + val.action.replace(/\s/ig,'') + "'>" + val.action + "</a></li>";
                        optsHtml += '<li><a href="#" class="btn btn-sm" id="' + action_id +
                            '"' +
                            ' onclick="show_cur_status(' +
                            '\'' +
                            server_id +
                            '\'' +
                            ',' +
                            '\'' +
                            val.href +
                            '\'' +
                            ',' +
                            j +
                            ',' +
                            '\'' +
                            action_id +
                            '\'' +
                            // '' +
                            // '' +
                            ')"' +
                            ' name="' +
                            server_id +
                            '">' + action + '</a></li>';
                    }
                    if (curRole === "vdc_admin") {
                        optsHtml += '<li><a href="#" class="btn btn-sm" id="' + action_id +
                            '"' +
                            ' onclick="show_cur_status(' +
                            '\'' +
                            server_id +
                            '\'' +
                            ',' +
                            '\'' +
                            val.href +
                            '\'' +
                            ',' +
                            j +
                            ',' +
                            '\'' +
                            action_id +
                            '\'' +
                            // '' +
                            // '' +
                            ')"' +
                            ' name="' +
                            server_id +
                            '">' + action + '</a></li>';
                        // optsHtml += "<li><a href='" + val.href + "/" + server_id + "' class='btn-sm' id='" + val.action.replace(/\s/ig,'') + "' name='" + server_id + "'>" + val.action + "</a></li>";
                    }
                });
            }
            operateOptsUl.innerHTML = optsHtml;
        }
    });
}

//全局变量
var server_id;
var server_href;
// instance实例处以某个action操作后， 提交对应的ID至该操作的URL  并返回提交是否成功的参数， 若提交成功，继续请求该实例的及时状态 并显示在页面上
function show_cur_status(target_id, target_href, instance_row_number, cur_action) {
    console.log(instance_row_number);
    console.log(target_id);
    console.log(cur_action);
    server_href = target_href;
    if(cur_action !== 'Createsnapshot' && cur_action !== 'Edit' && cur_action !== 'Resize' && cur_action !== 'Rebuild' ){
        $.ajax({
        type: 'POST',
        data: {
            'server_id': target_id,
        },
        url: target_href,       // 进入被点击的action的处理函数
        // dataType: 'json',    //添加此行后显示failure
        success: function (data) {
            console.log(data.detect.code);
                if (data.detect.code === 1){   // action提交成功并被处理时 返回 1
                    // $("#success_alert").show();
                    // setTimeout(hideAlert, 3000);   // 这里调用hideAlert函数不能加括号，否则设置的消失时间3000没有效果
                    $.ajax({                   // 进入views中显示被操作的server的状态的函数 并返回给前端
                        type: 'POST',
                        data: {
                            'id': target_id,
                        },
                        url: '/vdc_instance_show',
                        success: function (data) {     // 后台返回结果
                            let task_state_flag;       // 块级变量 task_state 监控参数
                            let server_task_check;      // 申明的块级变量 之后的定时函数会使用
                            console.log('operation in process....');
                            console.log(data.server['OS-EXT-STS:task_state']);     // 控制台记录返回的task_state
                            task_state_flag = data.server['OS-EXT-STS:task_state'];  // task_state 赋值给 flag
                            console.log(task_state_flag);
                            if (task_state_flag){
                                $("#instance_list").find('tr').eq(instance_row_number).find('td').eq(4).html(task_state_flag);
                                server_task_check = setInterval(function(){         // 进入一个定时函数， 这里设置每隔3秒检测一个任务是否完成
                                    $.ajax({
                                        type: 'POST',
                                        data: {
                                            'id': target_id,
                                        },
                                        url: '/vdc_instance_show',
                                        success: function (data) {
                                            task_state_flag = data.server['OS-EXT-STS:task_state'];
                                            console.log('控制台内部检测task:');
                                            console.log(task_state_flag);
                                            if (task_state_flag === null){     //  操作任务完成后 flag会变为null 这时将定时函数停止
                                                clearInterval(server_task_check);  //  停止定时函数
                                                getVirList();                     //  重新刷新instance实例信息 显示最新状态
                                            }
                                        },
                                        error: function () {
                                            alert('定时函数内部出错')
                                        }
                                    })
                                }, 3000);
                            }
                            else {
                                console.log('操作完成间隔很短，未进入定时函数');
                                getVirList();
                            }
                        },
                        error: function () {
                            alert('instance status 访问出错')
                        }
                    })
                }
                else{
                    console.log('任务提交失败，error：' + data.detect.msg);
                    // $("#failure_alert").show();
                    // setTimeout(hideAlert, 3000);
                }
            },
        error: function () {
            alert('operate failure');
        }
    })
    }
    else {
        console.log('no operation')
    }
}

//get items in object
function get_items(obj) {
    let obj_array = [];
    for (i in obj){
        // key_array.push(i);
        obj_array.push(obj[i]); // 解析二级以上的对象
        // console.log(i);           //获得属性
        // alert(test[i]);  //获得属性值
    }
    console.log(obj_array[0]);
    return obj_array[0];
}