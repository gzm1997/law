import mysql.connector


"""
conn = mysql.connector.connect(user='root', password='Gzm20125', database='ikdeer_user')
"""
def change_content_from_dict_to_list(t_type, content_dict):
    table1 = ["case_id", "case_name", "OA_id","company_name", "department", "manager", "phone", "submit_time", "case_type", "case_reason", "case_level", "reception_agency", "judge_phone", "custodian", "plaintiff", "defendant", "third_person", "amount", "request", "to_argue", "serial_number", "attachment_name", "page_num", "yz_way", "registration_details", "w_implement", "register_time", "submit_add_time", "court_time", "get_paper_time", "group_justice_add_advise", "group_manager_filing", "group_doc_filing"]
    table2 = ["case_id", "case_name", "OA_id", "company_name", "department", "manager", "phone", "submit_time", "case_type", "case_reason", "case_level", "reception_agency", "judge_phone", "custodian", "plaintiff", "defendant", "third_person", "amount", "request", "group_justice_advise", "w_need_approval", "group_leader_advise", "manager_register_detail", "w_advise_done", "group_justice_add_advise", "group_manager_filing", "project_doc_filing", "group_doc_filing", "remark"]
    table3 = ["case_id", "case_name", "OA_id", "company_name", "department", "manager", "phone", "submit_time", "case_type", "case_reason", "case_level", "reception_agency", "judge_phone", "custodian", "plaintiff", "defendant", "third_person", "amount", "request", "to_argue", "project_justice_advise", "project_manager_advise", "group_justice_advise", "group_leader_advise", "registration_details", "settlement_agreement_time", "reconciliation_agreement_time", "withdrawal_time", "w_implement", "group_justice_add_advise", "group_justice_filing"]
    result_list = []
    if t_type == "t1":
        for i in table1:
            result_list.append(content_dict[i])
    elif t_type == "t2":
        for i in table2:
            result_list.append(content_dict[i])
    elif t_type == "t3":
        for i in table3:
            result_list.append(content_dict[i])
    return result_list
        

def create_empty_table_list(t_type, case_id, case_name):
    table_list = [case_id, case_name]
    if t_type == "t1":
        for i in range(31):
            table_list.append("")
    elif t_type == "t2":
        for i in range(27):
            table_list.append("")
    elif t_type == "t3":
        for i in range(29):
            table_list.append("")        
    return table_list


class Case_manager(object):
    """docstring for Case_managerr"""
    def __init__(self, account, password):
        self._conn = mysql.connector.connect(user = account, password = password, database = "law")

    #搜索law_case
    def _search_law_case(self, username = "", case_id = "", case_name = ""):
        cursor = self._conn.cursor(dictionary = True)
    
        sql_word = "select * from law_case where "
        variables = []

        if username != "":
            sql_word = sql_word + "username = %s "
            variables.append(username)

        if case_id != "" and sql_word.find("=") == -1:
            sql_word = sql_word + "case_id = %s "
            variables.append(case_id)
        elif case_id != "" and sql_word.find("=") != -1:
            sql_word = sql_word + "and case_id = %s "
            variables.append(case_id)
            
        if case_name != "" and sql_word.find("=") == -1:
            sql_word = sql_word + "case_name = %s "
            variables.append(case_name)
        elif case_name != "" and sql_word.find("=") != -1:
            sql_word = sql_word + "and case_name = %s "
            variables.append(case_name)            
        if sql_word.find("=") == -1:
            sql_word = sql_word[:sql_word.find(" where")]
        sql_word = sql_word + ";"
        cursor.execute(sql_word, variables)

        result = cursor.fetchall()
        self._conn.commit()
        cursor.close()
        if len(result):
            for case in result:
                for i in case:
                    if type(case[i]) == bytearray:
                        case[i] = case[i].decode("utf-8")
            return result
        else:
            return []     

    #增加或者删除一个case，增加或者删除的同时会删除case对应的table
    def _edit_law_case(self, username, case_id, case_name, to_do = "create"):
        cursor = self._conn.cursor()
        if to_do == "create":
            if self._search_law_case(case_id = case_id) == []:
                cursor.execute("insert into law_case value(%s, %s, %s, False);", [username, case_id, case_name])

                cursor.execute("insert into t1 value(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", create_empty_table_list("t1", case_id, case_name))
                cursor.execute("insert into t2 value(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", create_empty_table_list("t2", case_id, case_name))
                cursor.execute("insert into t3 value(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", create_empty_table_list("t3", case_id, case_name))
                self._conn.commit()
                cursor.close()
            return True
        elif to_do == "delete":
            if self._search_law_case(username = username, case_id = case_id, case_name = case_name) != []:
                cursor.execute("delete from law_case where username=%s and case_id=%s and case_name=%s;", [username, case_id, case_name])
                cursor.execute("delete from t1 where case_id=%s and case_name=%s;", [case_id, case_name])
                cursor.execute("delete from t2 where case_id=%s and case_name=%s;", [case_id, case_name])   
                cursor.execute("delete from t3 where case_id=%s and case_name=%s;", [case_id, case_name]) 
                cursor.execute("delete from comment where case_id=%s;", [case_id])
                self._conn.commit()
                cursor.close()
                return True
        return False
    #搜索表格1
    def _search_table(self, t_type, case_id):
        cursor = self._conn.cursor(dictionary = True)
        if t_type == "t1":
            cursor.execute("select * from t1 where case_id=%s;", [case_id])
        elif t_type == "t2":
            cursor.execute("select * from t2 where case_id=%s;", [case_id])
        elif t_type == "t3":
            cursor.execute("select * from t3 where case_id=%s;", [case_id])
        result = cursor.fetchall()
        self._conn.commit()
        cursor.close()
        if len(result):
            result = result[0]
            for i in result:
                if type(result[i]) == bytearray:
                    result[i] = result[i].decode("utf-8")
            return result
        else:
            return {}

    #更新表格t1，根据case_id更新
    def _update_t1(self, case_id, content_dict):
        update_content = change_content_from_dict_to_list("t1", content_dict)[2:]
        update_content.append(case_id)
        cursor = self._conn.cursor()
        if self._search_table("t1", case_id) != {}:
            cursor.execute("update t1 set OA_id=%s, company_name=%s, department=%s, manager=%s, phone=%s, submit_time=%s, case_type=%s, case_reason=%s, case_level=%s, reception_agency=%s, judge_phone=%s, custodian=%s, plaintiff=%s, defendant=%s, third_person=%s, amount=%s, request=%s, to_argue=%s, serial_number=%s, attachment_name=%s, page_num=%s, yz_way=%s, registration_details=%s, w_implement=%s, register_time=%s, submit_add_time=%s, court_time=%s, get_paper_time=%s, group_justice_add_advise=%s, group_manager_filing=%s, group_doc_filing=%s where case_id=%s;", update_content)
        self._conn.commit()
        cursor.close()

    #更新表格t2，根据case_id更新
    def _update_t2(self, case_id, content_dict):
        update_content = change_content_from_dict_to_list("t2", content_dict)[2:]
        update_content.append(case_id)
        cursor = self._conn.cursor()
        if self._search_table("t2", case_id) != {}:
            cursor.execute("update t2 set OA_id=%s, company_name=%s, department=%s, manager=%s, phone=%s, submit_time=%s, case_type=%s, case_reason=%s, case_level=%s, reception_agency=%s, judge_phone=%s, custodian=%s, plaintiff=%s, defendant=%s, third_person=%s, amount=%s, request=%s, group_justice_advise=%s, w_need_approval=%s, group_leader_advise=%s, manager_register_detail=%s, w_advise_done=%s, group_justice_add_advise=%s, group_manager_filing=%s, project_doc_filing=%s, group_doc_filing=%s, remark=%s where case_id=%s;", update_content)
        self._conn.commit()
        cursor.close()        

    #更新表格t3，根据case_id更新
    def _update_t3(self, case_id, content_dict):
        update_content = change_content_from_dict_to_list("t3", content_dict)[2:]
        update_content.append(case_id)
        cursor = self._conn.cursor()
        if self._search_table("t3", case_id) != {}:
            cursor.execute("update t3 set OA_id=%s, company_name=%s, department=%s, manager=%s, phone=%s, submit_time=%s, case_type=%s, case_reason=%s, case_level=%s, reception_agency=%s, judge_phone=%s, custodian=%s, plaintiff=%s, defendant=%s, third_person=%s, amount=%s, request=%s, to_argue=%s, project_justice_advise=%s, project_manager_advise=%s, group_justice_advise=%s, group_leader_advise=%s, registration_details=%s, settlement_agreement_time=%s, reconciliation_agreement_time=%s, withdrawal_time=%s, w_implement=%s, group_justice_add_advise=%s, group_justice_filing=%s where case_id=%s;", update_content)
        self._conn.commit()
        cursor.close()

    def _read_comment(self, case_id):
        print("case_id to be read:")
        print(case_id)
        cursor = self._conn.cursor()
        cursor.execute("update law_case set num_nr=0 where case_id=%s", [case_id])
        self._conn.commit()
        cursor.close()

    def _unread_comment(self, case_id):
        print("case_id to be read:")
        print(case_id)
        cursor = self._conn.cursor()
        target_case = self._search_law_case(case_id = case_id)[0]
        num_ur_message = target_case["num_nr"] + 1
        cursor.execute("update law_case set num_nr=%s where case_id=%s", [num_ur_message, case_id])
        self._conn.commit()
        cursor.close() 

if __name__ == "__main__":
    m = Case_manager("root", "Gzm20125")
    t1 = {
        "case_id": "2017-8-8",
        "case_name": "test_case",
        "OA_id": "OA_id",
        "company_name": "company_name",
        "department": "department",
        "manager": "manager",
        "phone": "phone",
        "submit_time": "submit_time",
        "case_type": "case_type",
        "case_reason": "case_reason",
        "case_level": "case_level",
        "reception_agency": "reception_agency",
        "judge_phone": "judge_phone",
        "custodian": "custodian",
        "plaintiff": "plaintiff",
        "defendant": "defendant",
        "third_person": "third_person",
        "amount": "amount",
        "request": "request",
        "to_argue": "to_argue",
        "serial_number": "serial_number",
        "attachment_name": "attachment_name",
        "page_num": "page_num",
        "yz_way": "yz_way",
        "registration_details": "registration_details",
        "w_implement": "w_implement",
        "register_time": "register_time",
        "submit_add_time": "submit_add_time",
        "court_time": "court_time",
        "get_paper_time": "get_paper_time",
        "group_justice_add_advise": "group_justice_add_advise",
        "group_manager_filing": "group_manager_filing",
        "group_doc_filing": "group_doc_filing"    
    }

    t2 = {
        "case_id": "2017-8-8",
        "case_name": "test_case",
        "OA_id": "OA_id",
        "company_name": "company_name",
        "department": "department",
        "manager": "manager",
        "phone": "phone",
        "submit_time": "submit_time",
        "case_type": "case_type",
        "case_reason": "case_reason",
        "case_level": "case_level",
        "reception_agency": "reception_agency",
        "judge_phone": "judge_phone",
        "custodian": "custodian",
        "plaintiff": "plaintiff",
        "defendant": "defendant",
        "third_person": "third_person",
        "amount": "amount",
        "request": "request",
        "group_justice_advise": "group_justice_advise",
        "w_need_approval": "w_need_approval",
        "group_leader_advise": "group_leader_advise",
        "manager_register_detail": "manager_register_detail",
        "w_advise_done": "w_advise_done",
        "group_justice_add_advise": "group_justice_add_advise",
        "group_manager_filing": "group_manager_filing",
        "project_doc_filing": "project_doc_filing",
        "group_doc_filing": "group_doc_filing",
        "remark": "remark"
    }

    t3 = {
        "case_id": "2017-8-8",
        "case_name": "test_case",
        "OA_id": "OA_id",
        "company_name": "company_name",
        "department": "department",
        "manager": "manager",
        "phone": "phone",
        "submit_time": "submit_time",
        "case_type": "case_type",
        "case_reason": "case_reason",
        "case_level": "case_level",
        "reception_agency": "reception_agency",
        "judge_phone": "judge_phone",
        "custodian": "custodian",
        "plaintiff": "plaintiff",
        "defendant": "defendant",
        "third_person": "third_person",
        "amount": "amount",
        "request": "request",
        "to_argue": "to_argue",
        "project_justice_advise": "project_justice_advise",
        "project_manager_advise": "project_manager_advise",
        "group_justice_advise": "group_justice_advise",
        "group_leader_advise": "group_leader_advise",
        "registration_details": "registration_details",
        "settlement_agreement_time": "settlement_agreement_time",
        "reconciliation_agreement_time": "reconciliation_agreement_time",
        "withdrawal_time": "withdrawal_time",
        "w_implement": "w_implement",
        "group_justice_add_advise": "group_justice_add_advise",
        "group_justice_filing": "group_justice_filing"
    }

    print(m._edit_law_case("gzm1997", "2017-8-8", "test_case", to_do = "create"))
    print(m._edit_law_case("gzm1997", "2017-8-8", "first case", to_do = "delete"))
    print(m._search_law_case("gzm1997", "2017-8-8", "first case"))
    m._update_t1("2017-8-8", t1)
    m._update_t2("2017-8-8", t2)
    m._update_t3("2017-8-8", t3)
    print(m._edit_law_case("gzm1997", "2017-8-9", "second_case", to_do = "create"))
    print("search law_case by username:")
    print(m._search_law_case(username = "gzm1997"))
