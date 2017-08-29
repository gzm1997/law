$(document).ready(function() {
    $("#delete").click(function() {
        $("#ensure-delete").css("display", "block");
    });
    $("#cancel").click(function() {
        $("#ensure-delete").css("display", "none");
    });
    $("#ensure").click(function() {
        
        let data = GetData();
        console.log(data);
        
        $.post("/delete_task", data, function(data,status){
            if ("success" in data) {
                window.location.href = "/user?username=" + data.username;
            }
            else {
                alert("删除无效任务。");
            }
        });
    });
    function GetData() {
        data = {
            task_name: $("#task_name").val(),
            task_id: $("#task_id").val()
        };
        return data;
    }
});