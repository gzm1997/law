import mysql.connector

class Task_manager(object):
    """docstring for Task_manager"""
    def __init__(self, account, password):
        self._conn = mysql.connector.connect(user = account, password = password, database = "law")

    def _search_task(self, task_name = "", task_type = "", manager = "", deadline = "", completion_date = "", time_required = ""):
        cursor = self._conn.cursor(dictionary = True)
        sql_word = "select * from task_table where "
        variables = []

        if task_name != "":
            sql_word = sql_word + "task_name = %s "
            variables.append(task_name)

        if task_type != "" and sql_word.find("=") == -1:
            sql_word = sql_word + "task_type = %s"
            variables.append(task_type)
        elif task_type != "" and sql_word.find("=") != -1:
            sql_word = sql_word + "and task_type = %s"
            variables.append(task_type) 
            
        if manager != "" and sql_word.find("=") == -1:
            sql_word = sql_word + "manager = %s"
            variables.append(manager)
        elif manager != "" and sql_word.find("=") != -1:
            sql_word = sql_word + "and manager = %s"
            variables.append(manager)  

        if deadline != "" and sql_word.find("=") == -1:
            sql_word = sql_word + "deadline = %s"
            variables.append(deadline)
        elif deadline != "" and sql_word.find("=") != -1:
            sql_word = sql_word + "and deadline = %s"
            variables.append(deadline) 

        if completion_date != "" and sql_word.find("=") == -1:
            sql_word = sql_word + "completion_date = %s"
            variables.append(completion_date)
        elif completion_date != "" and sql_word.find("=") != -1:
            sql_word = sql_word + "and completion_date = %s"
            variables.append(completion_date)

        if time_required != "" and sql_word.find("=") == -1:
            sql_word = sql_word + "time_required = %s"
            variables.append(time_required)
        elif time_required != "" and sql_word.find("=") != -1:
            sql_word = sql_word + "and time_required = %s"
            variables.append(time_required) 

        sql_word = sql_word + ";"
        cursor.execute(sql_word, variables)

        result = cursor.fetchall()
        self._conn.commit()
        cursor.close()
        if len(result):
            for each_task in result:
                for i in each_task:
                    if type(each_task[i]) == bytearray:
                        each_task[i] = each_task[i].decode("utf-8")
            return result
        else:
            return [] 
    #任务的task_type和task_name以及manager不可以重复
    def _insert_task(self, task_name, task_type, manager, deadline, completion_date, time_required):
        cursor = self._conn.cursor()
        if self._search_task(task_name = task_name, task_type = task_type, manager = manager) == []:
            cursor.execute("insert into task_table value(%s, %s, %s, %s, %s, %s);", [task_name, task_type, manager, deadline, completion_date, time_required])
            self._conn.commit()
            cursor.close()
            return True
        return False

    def _delete_task(self, task_name, task_type, manager):
        if self._search_task(task_name = task_name, task_type = task_type, manager = manager) != []:
            cursor = self._conn.cursor()
            cursor.execute("delete from task_table where task_name=%s and task_type=%s and manager=%s;", [task_name, task_type, manager])
            self._conn.commit()
            cursor.close()
            return True
        return False



if __name__ == "__main__":
	task_data = Task_manager("root", "Gzm20125")
	print(task_data._insert_task(task_name = "first task", task_type = "uknown", manager = "gzm1997", deadline = "2017-8-11", completion_date = "2017-8-12", time_required = "1"))