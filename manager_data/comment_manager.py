import mysql.connector

class Comment_manager(object):
    """docstring for Comment_manager"""
    def __init__(self, account, password):
        self._conn = mysql.connector.connect(user = account, password = password, database = "law")

    def _search_comment(self, username = "", case_id = "", c_time = ""):
        cursor = self._conn.cursor(dictionary = True)
        sql_word = "select * from comment where "
        variables = []

        if username != "":
            sql_word = sql_word + "username = %s "
            variables.append(username)

        if case_id != "" and sql_word.find("=") == -1:
            sql_word = sql_word + "case_id = %s"
            variables.append(case_id)
        elif case_id != "" and sql_word.find("=") != -1:
            sql_word = sql_word + "and case_id = %s"
            variables.append(case_id)

        if c_time != "" and sql_word.find("=") == -1:
            sql_word = sql_word + "c_time = %s"
            variables.append(c_time)
        elif c_time != "" and sql_word.find("=") != -1:
            sql_word = sql_word + "and c_time = %s"
            variables.append(c_time)

        if sql_word.find("=") == -1:
            sql_word = sql_word[:sql_word.find(" where")]
        sql_word = sql_word + ";"
        cursor.execute(sql_word, variables)

        result = cursor.fetchall()
        self._conn.commit()
        cursor.close()
        if len(result):
            for each_c in result:
                for i in each_c:
                    if type(each_c[i]) == bytearray:
                        each_c[i] = each_c[i].decode("utf-8")
            return result
        else:
            return []      

    def _insert_comment(self, username, case_id, c_time, content):
        cursor = self._conn.cursor()
        cursor.execute("insert into comment(username, case_id, c_time, content) value(%s, %s, %s, %s);", [username, case_id, c_time, content])
        self._conn.commit()
        cursor.close()           


if __name__ == "__main__":
    c = Comment_manager("root", "Gzm20125")
    c._insert_comment("gzm", "123221", "2017-8-15", "haha")
    c._insert_comment("gzm", "123221", "2017-8-15", "lala")
    comment_list = c._search_comment(case_id = "123221")
    print(comment_list)