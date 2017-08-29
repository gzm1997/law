$(document).ready(function () {
    
    function get_task_data() {
        return {
            task_name: $("#task_name").val(),
            task_id: $("#task_id").val(),
            task_state: $("#task_state").val(),
            task_type: $("#task_type").val(),
            manager: $("#manager").val(),
            deadline: $("#deadline").val(),
            completion_date: $("#completion_date").val(),
            time_required: $("#time_required").val()
        }
    }

    $('.form_date').datetimepicker({
        language: 'fr',
        weekStart: 1,
        todayBtn: 1,
        autoclose: 1,
        todayHighlight: 1,
        startView: 2,
        minView: 2,
        forceParse: 0
    });

    $("#add-button").click(function (event) {
        event.preventDefault();
        $("#todo-modal").modal('show');
    });
    
    $("#save_task").click(function() {
        var data = get_task_data()
        if ($("#deadline").val() == "") {
            $("#deadline_remind").css("display", "block");
            $("#deadline_remind").text("截至日期不能缺失！")
        }      
        else {
            $.post("/task", data, function(data,status) {
                alert("数据：" + data.message + "\n状态：" + status);
                $('#todo-modal').modal('hide');
                if ("judge_url" in data) {
                    window.location.href = data.judge_url;
                }
            });     
            //$("#deadline_remind").css("display", "none");
            //$("#completion_date_remind").css("display", "none");
        }

    });



});


/*

    countTodos();
    // all done btn
    $("#checkAll").click(function () {
        AllDone();
    });
    $("#add-button").click(function (event) {
        event.preventDefault();
        $("#todo-modal").modal('show');
    });
    $('.form_date').datetimepicker({
        language: 'fr',
        weekStart: 1,
        todayBtn: 1,
        autoclose: 1,
        todayHighlight: 1,
        startView: 2,
        minView: 2,
        forceParse: 0
    });
    // 修改item
    $('#sortable').on('click', '.undo-save-button', function () {
        //        console.log($(this).parent().find("input[name=\"input-task-name\"]").val());
        // 修改每个item的thumb的内容
        // 修改标题
        var newTitle = $(this).parent().find("input[name=\"input-task-name\"]").val();
        ($(this).parent().prev().find('.undo-name').text(newTitle));
        // 修改编号
        var newNumber = $(this).parent().find('input[name=\"input-task-number\"]').val();
        ($(this).parent().prev().find('.undo-number').text(newNumber));
        // 修改需要时间
        var newNeedTime = $(this).parent().find('input[name=\"task-need-time\"]').val();
        $(this).parent().prev().find('.undo-time').text(newNeedTime);
        //        $(this).parent().prev().find('.undo-number').text() = $(this).parent().find("input[name=\"input-task-number\"]").val();
        //        $(this).parent().prev().find('.undo-time').text() = $(this).parent().find("input[name=\"task-need-time\"]").val();
    });

    // 是否显示item
    $('#sortable').on('click', '.undo-name', function () {
        if ($(this).parent().parent().next().css('display') == 'block')
            $(this).parent().parent().next().css('display', 'none');
        else
            $(this).parent().parent().next().css('display', 'block');
    });

    // 保存按钮
    $('.button-group-window').on('click', '.save-button', function () {
        // 获取任务名称
        var todoname = $("input[name=input-task-name]").val();
        // 获取任务编号
        var todonumber = $("input[name=input-task-number]").val();
        // 获取经办人
        var operator = $("input[name=input-operator]").val();
        // 获取任务状态
        var state = $(".modal-body .task-state-select").val();

        var type = $(".modal-body .task-type-select").val();
        // 获取任务的截止日期
        var endtime = $(".task-end-time").val();
        // 任务的完成时间
        var finishtime = $(".task-finish-time").val();
        // 任务需要时间
        var needtime = $(".task-need-time").val();
        createTodo(todoname, todonumber, operator, state, type, endtime, finishtime, needtime);
        $("#todo-modal").modal('hide');
    });

    // count tasks
    function countTodos() {
        var count = $("#sortable li").length - 1;
        $('.count-todos').html(count);
    }

    // 创建任务
    function createTodo(todoname, todonumber, operator, state, type, endtime, finishtime, needtime) {
        var markup = '<li class="undo-task"><div class="thumb"><div class="col-md-2 undo-number"><label class="undo-number">' + todonumber + '       </label></div><div class="col-md-10"><div class="col-md-6 undo-name"><label>' + todoname + '            </label></div><div class="col-md-3 undo-time"><label class="undo-time">' + needtime + '</label></div><div class="col-md-3 undo-finish"><label><input type="checkbox" value="" /></label></div></div></div><div class="detail"><div class="task-name"><label class="control-label">' + '任务名称:' + '</label><input name="input-task-name" value = ' + '\"' + todoname + '\"' + '></div><div><label class="control-label task-number">' + '任务编号:</label><input name="input-task-number" + value=' + '\"' + todonumber + '\"' + '></div><div><label class="control-label task-state">' + '任务状态:</label><select task-state-select >';
        console.log(type);
        if (state == "已办") {
            markup += '<option selected="selected">已办</option><option>待办</option> </select>';
        } else {
            markup += '<option>已办</option><option selected="selected">待办</option> </select>';
        }
        markup += '<label class="control-label task-type">任务类型:</label><select>';
        //        console.log(type);
        if (type == "类型1") {
            markup += '<option selected = "selected">类型1</option><option>类型2</option><option>类型3</option><option>类型4</option>';
        } else if (type == "类型2") {
            markup += '<option>类型1</option><option selected = "selected">类型2</option><option>类型3</option><option>类型4</option>';
        } else if (type == "类型3") {
            markup += '<option>类型1</option><option>类型2</option><option  selected = "selected">类型3</option><option>类型4</option>';
        } else if (type == "类型4") {
            markup += '<option>类型1</option><option>类型2</option><option>类型3</option><option  selected = "selected">类型4</option>';
        }
        markup += '</select> </div><label class="control-label task-operator">经办人</label>' + '<input name="input-operator"' + 'value = ' + '\"' + operator + '\"' + '><br/>' + '<div class="form-group time-select"><label class="control-label end-time">截止日期</label><div class="input-group date form_date col-md-8" data-date="" data-date-format="dd MM yyyy" data-link-field="dtp_input2" data-link-format="yyyy-mm-dd"><input class="form-control" size="16" type="text" value="' + endtime + '" readonly><span class="input-group-addon"><span class="glyphicon glyphicon-remove"></span></span><span class="input-group-addon"><span class="glyphicon glyphicon-calendar"></span></span></div><input type="hidden" class="task-end-time" id="dtp_input2" value="" /><br/></div>' + '<div class="form-group time-select"><label class="control-label finish-time">完成日期</label><div class="input-group date form_date col-md-8" data-date="" data-date-format="dd MM yyyy" data-link-field="dtp_input2" data-link-format="yyyy-mm-dd"><input class="form-control" size="16" type="text" value="" readonly><span class="input-group-addon"><span class="glyphicon glyphicon-remove"></span></span><span class="input-group-addon"><span class="glyphicon glyphicon-calendar"></span></span></div><input type="hidden" class="task-finish-time" id="dtp_input2" value="" /><br/></div>' + '<div class="button-group-window"><label class="control-label need-time">所需时间</label><input class="task-need-time"' + 'value="' + needtime + '"></div>' + '<div class="undo-save-button"><button class="button button-primary button-small">保存</button></div></div></li>';
        $('#sortable').append(markup);
        $('.add-todo').val('');
        countTodos();
    }
    //mark task as done

    $('#sortable').on('click', '.undo-finish', function () {
        $(this).parent().parent().next().css('display', 'none');
        console.log($(this));
        $(this).empty();
        $(this).append('<button class="delete-item btn btn-default btn-xs pull-right"><span class="glyphicon glyphicon-plus"></span></button><button class="remove-item btn btn-default btn-xs pull-right"><span class="glyphicon glyphicon-remove"></span></button>');
        $('#done-items').append($(this).parent().parent().parent());
        countTodos();
    });

    function removeButtons(element) {
        $(element).empty();
        $(element).append('<label><input type="checkbox" value="" /></label>');
    }
    $('#done-items').on('click', '.delete-item', function () {
        console.log($(this)); $('#sortable').append($(this).parent().parent().parent().parent().parent());
        removeButtons($(this).parent());
    });

    //remove done task from list
    function removeItem(element) {
        $(element).parent().remove();
    }
*/