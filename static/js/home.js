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
            var doneItem = $(this).parent().parent().find('label').text();
            $(this).parent().parent().parent().addClass('remove');
            done(doneItem);
            countTodos();
        }
    });

    //从已经完成的返回到未完成的
    $('#done-items').on('click', '.remove-item' ,function() {
        var text = ($(this).parent().text());
        createTodo(text);
        console.log(text);
        removeItem($(this));
    });
    
    //delete done task from "already done"
    $('.todolist not-done').on('click', '.remove-item', function () {
        removeItem(this);
    });

    // count tasks
    function countTodos() {
        var count = $("#sortable li").length;
        $('.count-todos').html(count);
    }

    //create task
    function createTodo(text) {
        var markup = '<li class="ui-state-default"><div class="checkbox"><label><input type="checkbox" value="" />' + text + '</label></div></li>';
        $('#sortable').append(markup);
        $('.add-todo').val('');
    }

    //mark task as done
    function done(doneItem) {
        var done = doneItem;
        console.log(done);
        var markup = "<li>" + done + "<button class=\"remove-item btn btn-default btn-xs pull-right\"><span class=\"glyphicon glyphicon-remove\"></span></button><button class=\"remove-item remove-back btn btn-default btn-xs pull-right\"><span class=\"glyphicon glyphicon-plus\"></span></button></li>";
        $('#done-items').append(markup);
        $('.remove').remove();
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
