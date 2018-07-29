// 点击operate按钮后自动生成对应于不同status下的操作选项函数
function showOperateOpts(server_id, status, task_status) {
    // console.log(server_id);
    // console.log(status);
    // console.log(task_status);
    $.ajax({
        type: "POST",
        data: {
            'status': status,
            'task_status': task_status
        },
        url: "/vdc_getStatusAction",
        success: function (data) {
            var optsHtml = '';
            // console.log(optsHtml);
            $.each(data, function (i, val) {
                let action_id = val['name'].replace(/\s/ig, '');
                let action = val['cn_name'].replace(/\s/ig, '');
                // console.log(action_id);
                // // console.log(action);
                // console.log(val.href);
                var target_model;
                var target_url;
                // console.log(optsHtml);
                if (val.href === '/vdc_updateServer')
                {
                    target_model = "#updateModal";
                    optsHtml += '<li><a data-toggle="modal" data-target="' + target_model + '"' + ' onclick="addID2Models(' + "\'" + server_id + "\'" + ')"' + ' class="btn btn-sm">' + action + '</a></li>';
                }
                if (val.href === '/vdc_manipulateServer')
                {
                    target_model = "#" + action_id + "Modal";
                    optsHtml += '<li><a data-toggle="modal" data-target="' + target_model + '"' + ' class="btn btn-sm" id="' + action_id +  '">' + action + '</a></li>';
                }
                if (val.href === '/vdc_manipulateServerNoParams')
                {
                    target_url = '/vdc_manipulateServerNoParams';
                    optsHtml += '<li><a class="btn btn-sm" onclick="no_params_action(' + "\'" + server_id + "\'" + "," + "\'" + target_url + "\'" + "," + "\'" + action_id + "\'" + ')"' + ' id="'
                                 + action_id +  '">' + action + '</a></li>';
                }
                if (val.href === '/vdc_deleteServer')
                {
                    target_url = '/vdc_deleteServer';
                    optsHtml += '<li><a class="btn btn-sm" onclick="no_params_action(' + "\'" + server_id + "\'" + "," + "\'" + target_url + "\'" + "," + "\'" + action_id + "\'" + ')"' + ' id="'
                                 + action_id +  '">' + action + '</a></li>';
                }
                });
             var sub_button = "subbutton" + server_id;
             // console.log(optsHtml);
             document.getElementById(sub_button).innerHTML = optsHtml;
            }
    })
}

function addID2Models(server_id) {
    $("#update_instance_id").val(server_id);
    
}


function no_params_action(server_id, target_url, action_id) {
    // console.log(server_id);
    // console.log(target_url);
    // console.log(action_id);
    // $.ajax({
    //     type: 'POST',
    //     data: {
    //         'server_id': server_id,
    //         'action': action_id
    //     },
    //     url: target_url,       // 进入被点击的action的处理函数
    //     success: function (data) {
    //         console.log(data.detect.code);
    //             if (data.detect.code === 1){   // action提交成功并被处理时 返回 1
    //                 // $("#success_alert").show();
    //                 // setTimeout(hideAlert, 3000);   // 这里调用hideAlert函数不能加括号，否则设置的消失时间3000没有效果
    //                 $.ajax({                   // 进入views中显示被操作的server的状态的函数 并返回给前端
    //                     type: 'POST',
    //                     data: {
    //                         'id': target_id
    //                     },
    //                     url: '/vdc_instance_show',
    //                     success: function (data) {     // 后台返回结果
    //                         let task_state_flag;       // 块级变量 task_state 监控参数
    //                         let server_task_check;      // 申明的块级变量 之后的定时函数会使用
    //                         console.log('operation in process....');
    //                         console.log(data.server['OS-EXT-STS:task_state']);     // 控制台记录返回的task_state
    //                         task_state_flag = data.server['OS-EXT-STS:task_state'];  // task_state 赋值给 flag
    //                         console.log(task_state_flag);
    //                         if (task_state_flag){
    //                             $("#instance_list").find('tr').eq(instance_row_number).find('td').eq(4).html(task_state_flag);
    //                             server_task_check = setInterval(function(){         // 进入一个定时函数， 这里设置每隔3秒检测一个任务是否完成
    //                                 $.ajax({
    //                                     type: 'POST',
    //                                     data: {
    //                                         'id': target_id,
    //                                     },
    //                                     url: '/vdc_instance_show',
    //                                     success: function (data) {
    //                                         task_state_flag = data.server['OS-EXT-STS:task_state'];
    //                                         console.log('控制台内部检测task:');
    //                                         console.log(task_state_flag);
    //                                         if (task_state_flag === null){     //  操作任务完成后 flag会变为null 这时将定时函数停止
    //                                             clearInterval(server_task_check);  //  停止定时函数
    //                                             getVirList();                     //  重新刷新instance实例信息 显示最新状态
    //                                         }
    //                                     },
    //                                     error: function () {
    //                                         alert('定时函数内部出错')
    //                                     }
    //                                 })
    //                             }, 3000);
    //                         }
    //                         else {
    //                             console.log('操作完成间隔很短，未进入定时函数');
    //                             getVirList();
    //                         }
    //                     },
    //                     error: function () {
    //                         alert('instance status 访问出错')
    //                     }
    //                 })
    //             }
    //             else{
    //                 console.log('任务提交失败，error：' + data.detect.msg);
    //                 // $("#failure_alert").show();
    //                 // setTimeout(hideAlert, 3000);
    //             }
    //         },
    //     error: function () {
    //         alert('operate failure');
    //     }
    // })
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
            'server_id': target_id
        },
        url: target_href,       // 进入被点击的action的处理函数
        success: function (data) {
            console.log(data.detect.code);
                if (data.detect.code === 1){   // action提交成功并被处理时 返回 1
                    // $("#success_alert").show();
                    // setTimeout(hideAlert, 3000);   // 这里调用hideAlert函数不能加括号，否则设置的消失时间3000没有效果
                    $.ajax({                   // 进入views中显示被操作的server的状态的函数 并返回给前端
                        type: 'POST',
                        data: {
                            'id': target_id
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