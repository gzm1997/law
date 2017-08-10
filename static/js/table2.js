

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
        t_type: "t2",
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
            group_doc_filing: $("#group_doc_filing").val(),
            // 集团法务部负责人意见
            group_justice_advise: $("#group_justice_advise").val(),
            // 是否需要分管领导审批
            w_need_approval: $("#w_need_approval").val(),
            // 集团分管领导意见
            group_leader_advise: $("#group_leader_advise").val(),
            // 经办人登记
            manager_register_detail: $("#manager_register_detail").val(),
            // 终审意见是否落实
            w_advise_done: $("#w_advise_done").val(),
            // 项目档案室备案
            project_doc_filing: $("#project_doc_filing").val(),
            // 备注
            remark: $("#remark").val()            
        }

    }
}
/*/
function test() {
    alert($("#request").val());
}
*/
