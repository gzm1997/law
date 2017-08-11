$(document).ready(function () {

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
    //create todo
    $('.add-todo').on('keypress', function (e) {
        e.preventDefault
        if (e.which == 13) {
            if ($(this).val() != '') {
                var todo = $(this).val();
                createTodo(todo);
                countTodos();
            } else {
                // some validation
            }
        }
    });
    //create todo
    $('.add-todo').on('keypress', function (e) {
        e.preventDefault
        if (e.which == 13) {
            if ($(this).val() != '') {
                var todo = $(this).val();
                createTodo(todo);
                countTodos();
            } else {
                // some validation
            }
        }
    });
    // mark task as done
    $('.todolist').on('change', '#sortable li input[type="checkbox"]', function () {
        if ($(this).prop('checked')) {
            //            var doneItem = $(this).parent().parent().find('label').text();
            //            $(this).parent().parent().parent().addClass('remove');
            var undoname = $(".undo-name").text();
            var undonumber = $(".undo-number").text();
            var undotime = $(".undo-time").text();
            done(undonumber, undoname, undotime);
            countTodos();
        }
    });

    //从已经完成的返回到未完成的
    $('#done-items').on('click', '.remove-item', function () {
        var text = ($(this).parent().text());
        createTodo(text);
        console.log(text);
        removeItem($(this));
    });

    //delete done task from "already done"
    $('.todolist not-done').on('click', '.remove-item', function () {
        removeItem(this);
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
        var state = $(".task-state-select").val();
        //        console.log($(".task-state-select").val());
        // 获取任务的截止日期
        var endtime = $(".task-end-time").val();
        // 任务的完成时间
        var finishtime = $(".task-finish-time").val();
        // 任务需要时间
        var needtime = $(".task-need-time").val();
        createTodo(todoname, todonumber, operator, state, endtime, finishtime, needtime);
    });

    // count tasks
    function countTodos() {
        var count = $("#sortable li").length - 1;
        $('.count-todos').html(count);
    }

    // 创建任务
    function createTodo(todoname, todonumber, operator, state, endtime, finishtime, needtime) {
        var markup = '<li class="undo-task"><div class="col-md-2 undo-number"><label class="undo-number">' + todonumber + '</label></div><div class="col-md-10"><div class="col-md-8 undo-name"><label >' + todoname + '</label></div><div class="col-md-2 undo-time"><label class="undo-time">' + needtime + '</label></div><div class="col-md-2 undo-finish"><label><input type="checkbox" value="" /></label></div><div class="undo-state"></div><div class="undo-ddl"></div><div class="undo-finishtime"></div><div class="undo-type"></div></div></li>'
        $('#sortable').append(markup);
        $('.add-todo').val('');
        countTodos();
    }
    //create task
    //    function createTodo(text) {
    //        var markup = '<li class="ui-state-default"><div class="checkbox"><label><input type="checkbox" value="" />' + text + '</label></div></li>';
    //        $('#sortable').append(markup);
    //        $('.add-todo').val('');
    //    }

    //mark task as done
    function done(undonumber, undoname, undotime) {
        console.log(undoname);
        var markup = '<li class="undo-task"><div class="col-md-2 undo-number"><label class="undo-number">' + undonumber + '</label></div><div class="col-md-10"><div class="col-md-8 undo-name"><label >' + undoname + '</label></div><div class="col-md-2 undo-time"><label class="undo-time">' + undotime + '</label></div><div class="col-md-2 undo-finish"><label><input type="checkbox" value="" /></label></div><div class="undo-state"></div><div class="undo-ddl"></div><div class="undo-finishtime"></div><div class="undo-type"></div></div></li>'
        $('#done-items').append(markup);
        $('.remove').remove();
        countTodos();
    }

    //mark all tasks as done
    function AllDone() {
        var myArray = [];

        $('#sortable li').each(function () {
            myArray.push($(this).text());
        });

        // add to done
        for (i = 0; i < myArray.length; i++) {
            $('#done-items').append('<li>' + myArray[i] + '<button class="btn btn-default btn-xs pull-right  remove-item"><span class="glyphicon glyphicon-remove"></span></button></li>');
        }

        // myArray
        $('#sortable li').remove();
        countTodos();
    }

    //remove done task from list
    function removeItem(element) {
        $(element).parent().remove();
    }
});
