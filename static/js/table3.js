

$(document).ready(function(){
  $(".btn-success").click(function(){
    var data = getData();
    $.post("/table", data,
    function(data,status){
      alert("数据：" + data + "\n状态：" + status);
    });
  });
});

function getData() {
    return {
        t_type: "t3",
        table_content: {
            case_id: $("#case_id").val(),
            case_name: $("#case_name").val(),
            OA_id: $("#OA_id").val(),
            company_name: $("#company_name").val(),
            department: $("#department").val(),
            manager: $("#manager").val(),
            phone: $("#phone").val(),
            submit_time: $("#submit_time").val(),
            case_type: $("#case_type").val(),
            case_reason: $("#case_reason").val(),
            case_level: $("#case_level").val(),
            reception_agency: $("#reception_agency").val(),
            judge_phone: $("#judge_phone").val(),
            custodian: $("#custodian").val(),
            plaintiff: $("#plaintiff").val(),
            defendant: $("#defendant").val(),
            third_person: $("#third_person").val(),
            amount: $("#amount").val(),
            request: $("#request").val(),
            to_argue: $("#to_argue").val(),
            serial_number: $("#serial_number").val(),
            attachment_name: $("#attachment_name").val(),
            page_num: $("#page_num").val(),
            yz_way: $("#yz_way").val(),
            registration_details: $("#registration_details").val(),
            w_implement: $("#w_implement").val(),
            register_time: $("#register_time").val(),
            submit_add_time: $("#submit_add_time").val(),
            court_time: $("#court_time").val(),
            get_paper_time: $("#get_paper_time").val(),
            group_justice_add_advise: $("#group_justice_add_advise").val(),
            group_manager_filing: $("#group_manager_filing").val(),
            group_doc_filing: $("#group_doc_filing").val()            
        }

    }
}
/*/
function test() {
    alert($("#request").val());
}
*/
