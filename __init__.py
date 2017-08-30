#-*- coding=utf-8 -*-
from flask import Flask, render_template, request, session, jsonify, abort, redirect, url_for
from law.manager_data import user_manager, case_manager, task_manager, comment_manager
from law import manager_time
from law import send_email
from law import plan
from law import setting
import os

application = Flask(__name__)
user_data = user_manager.User_manager(setting.MYSQL_ACCOUNT, setting.MYSQL_PASSWORD)
case_data = case_manager.Case_manager(setting.MYSQL_ACCOUNT, setting.MYSQL_PASSWORD)
task_data = task_manager.Task_manager(setting.MYSQL_ACCOUNT, setting.MYSQL_PASSWORD)
comment_data = comment_manager.Comment_manager(setting.MYSQL_ACCOUNT, setting.MYSQL_PASSWORD)


@application.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(application.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@application.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        comfirmpassword = request.form["comfirmpassword"]
        #print(username, password, comfirmpassword)
        if password != comfirmpassword:
            return jsonify(comfirmpassword="password and comfirmpassword are different")

        check_user_email = user_data._search_user(email=email)
        check_user_username = user_data._search_user(username=username)
        if check_user_email != {}:
            #print("email double")
            return jsonify(email="email have been signup")
        if check_user_username != {}:
            #print("username double")
            return jsonify(username="username have been signup")
        try:
            vertifycode = send_email.send_vertify_email(email)
        except:
            vertifycode = "email err"
            return jsonify(email="your email is wrong")

        #print("vertifycode", vertifycode)
        if user_data._insert_r_user(email, username, password, vertifycode) == 0:
            return jsonify(warn="signup successfully and need to go to your email")
        else:
            return jsonify(warn="sign up failed")


@application.route("/vertify")
def vertify():
    vertifycode = request.args.get('vertifycode')
    result = user_data._search_r_user(vertifycode=vertifycode)
    if result == {}:
        return "no such a vertifycode"
    #print("result", result)
    #print("email", result["email"])
    #print("username", result["username"])
    #print("password", result["password"])
    if result != {}:
        if user_data._insert_user(email=result["email"], username=result["username"], password=result["password"]):
            session['username'] = result["username"]
            return redirect(url_for('user', username=result["username"]))
        else:
            return "vertify err"


@application.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        # if "username" in session:
            # session.pop["username"]

        #print("this is post")
        email = request.form["email"]
        password = request.form["password"]
        #print("email:", email)
        #print("password:", password)
        result = user_data._search_user(email=email)
        #print(result)
        if result == {}:
            #print("no such account")
            return jsonify(email="no such a account!")
        elif result != {} and result["password"] != password:
            #print("password wrong")
            return jsonify(password="password is wrong")
        elif result != {} and result["password"] == password:
            #print("login successfully")
            session['username'] = result["username"]
            return jsonify(success=result["username"])




@application.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@application.route("/edit_case", methods=["POST"])
def add_case():
    #print(request.form)
    case_id = request.form["case_id"]
    case_name = request.form["case_name"]
    username = session["username"]


    if case_data._search_law_case(case_id=case_id) != []:
        return jsonify(case_id="case_id has been used")
    if case_data._search_law_case(case_name=case_name) != []:
        return jsonify(case_name="case_name has been used")
    case_data._edit_law_case(username = username, case_id = case_id, case_name = case_name)
    return jsonify(success="create case successfully!", case_id = case_id)


#/table?case_id=2017-8-10&t_type=t1
@application.route("/table", methods=["GET", "POST"])
def table():
    if request.method == "GET":
        case_id = request.args.get("case_id")
        t_type = request.args.get('t_type')
        #print("show table case_id:", case_id, "t_type:", t_type)

        target_case = case_data._search_law_case(case_id = case_id)
        #print("target case:")
        #print(target_case)

        if target_case != []:
            if "username" in session and target_case[0]["username"] == session["username"]:
                own = True
            else:
                own = False

            if t_type == "t1":
                #print("case_id:")
                #print(case_id)
                tc = case_data._search_table(t_type = "t1", case_id = case_id)
                #print("this is table to show:")
                #print(tc)
                return render_template("table1.html", tc = tc, own = own)
            elif t_type == "t2":
                tc = case_data._search_table(t_type = "t2", case_id = case_id)
                #print("this is table to show:")
                #print(tc)
                return render_template("table2.html", tc = tc, own = own)

            elif t_type == "t3":
                tc = case_data._search_table(t_type = "t3", case_id = case_id)
                #print("this is table to show:")
                #print(tc)
                return render_template("table3.html", tc = tc, own = own)
        abort(401)
    elif request.method == "POST":
        ##print(request.form)
        content_dict = dict(request.form)
        for i in content_dict:
            content_dict[i] = content_dict[i][0]
        t_type = content_dict["t_type"]
        content_dict.pop("t_type")
        #print(content_dict)
        if t_type == "t1":
            case_data._update_t1(content_dict["case_id"], content_dict)
            return "update table1 successfully!"
        elif t_type == "t2":
            case_data._update_t2(content_dict["case_id"], content_dict)
            return "update table2 successfully!"
        elif t_type == "t3":
            case_data._update_t3(content_dict["case_id"], content_dict)
            return "update table3 successfully!"
        return "update table error"



#/user?username=gzm
@application.route("/user")
def user():
    #print("this is user detail get")
    username = request.args.get('username')

    week_task_json = plan.get_week_task_json(manager = username)
    #print("week_task_json", week_task_json)
    weekday_show = plan.show_today()


    if "username" in session:
        login = True
        user_url = "/user?username=" + session["username"]
        task_url = "/task?username=" + session["username"]
    else:
        login = False

    #print("username", username)
    target_user = user_data._search_user(username=username)
    if ("username" not in session) or ("username" in session and session["username"] != username):
        own = False
    elif "username" in session and session["username"] == username:
        own = True

    #print("own in user page is:", own)

    if target_user != {}:
        email = target_user["email"]
        #print("email", email)

        case_list = case_data._search_law_case(username=username)
        task_list = task_data._search_task(manager = username)

        for case in case_list:
            case["case_detail_url"] = "/case?case_id=" + case["case_id"]
        for task in task_list:
            task["task_detail_url"] = "/task_detail?task_id=" + task["task_id"]        

        
        if login:
            return render_template("index.html", login = login, user_url = user_url, username = session["username"], Myemail=email, Myusername=username, case_list=case_list, task_list = task_list, own = own, task_url = task_url, week_task_json = week_task_json, weekday_show = weekday_show)
        else:
            return render_template("index.html", login = login, Myemail=email, Myusername=username, case_list=case_list, task_list = task_list, own = own, week_task_json = week_task_json, weekday_show = weekday_show)            
    else:
        return "此用户不存在!"
    abort(401)


@application.route("/home")
def home():
    if "username" in session:
        #print("already login")
        user_url = "/user?username=" + session["username"]
        return render_template("home.html", login = True, user_url = user_url , username = session["username"])
    else:
        #print("not login yet")
        return render_template("home.html", login = False)

#/case?case_id=2017-8-10
@application.route("/case")
def case():
    case_id = request.args.get('case_id')
    table_urls = ["/table?case_id=" + case_id + "&t_type=" + "t1", "/table?case_id=" + case_id + "&t_type=" + "t2", "/table?case_id=" + case_id + "&t_type=" + "t3"]
    case_manager = case_data._search_law_case(case_id = case_id)
    if case_manager != []:
        manager_name = case_manager[0]["username"]
        manager_detail_url = "/user?username=" + manager_name
    else:
        manager_name = ""
        manager_detail_url = "#"

    comment_list = comment_data._search_comment(case_id = case_id)
    for c in comment_list:
        c["user_url"] = "/user?username=" + c["username"]
    #print("comment_list:")
    #print(comment_list)

    if "username" in session and session["username"] == case_data._search_law_case(case_id = case_id)[0]["username"]:
        case_data._read_comment(case_id = case_id)

    if "username" in session:
        login = True
        username = session["username"]
        user_url = "/user?username=" + username
        if manager_name == session["username"]:
            own = True
        else:
            own = False
        return render_template("case.html", table_urls = table_urls, login = login, user_url = user_url, username = username, manager_detail_url = manager_detail_url, manager_name = manager_name, case_id = case_id, comment_list = comment_list, own = own)
    else:
        login = False
        return render_template("case.html", table_urls = table_urls, login = login, manager_detail_url = manager_detail_url, manager_name = manager_name, case_id = case_id, comment_list = comment_list, own = False)


#展示所有人的所有案件
@application.route("/all_case")
def function():
    all_case = case_data._search_law_case()
    for case in all_case:
        case["detail_url"] = "/case?case_id=" + case["case_id"]
    if "username" in session:
        login = True
        username = session["username"]
        user_url = '/user?username=' + username
        for case in all_case:
            if case["username"] == username:
                case["w_own"] = True
            else:
                case["w_own"] = False
        return render_template("all_case.html", case_list = all_case, login = login, user_url = user_url, username = username)
    else:
        login = False
        return render_template("all_case.html", case_list = all_case, login = login)


#接受评论
@application.route("/comment", methods = ["POST"])
def comment():
    ##print(request.form)
    username = request.form["username"]
    case_id = request.form["case_id"]
    content = request.form["content"]
    c_time = manager_time.get_localtime_str()
    comment_data._insert_comment(username = username, case_id = case_id, c_time = c_time, content = content)
    if session["username"] != case_data._search_law_case(case_id = case_id)[0]["username"]:
        case_data._unread_comment(case_id = case_id)
    return redirect(url_for("case", case_id = request.form["case_id"]))










@application.route("/all_task")
def alltasks():
    all_task = task_data._search_task()
    #print(all_task)
    for task in all_task:
        task["detail_url"] = "/task_detail?task_id=" + task["task_id"]

    if "username" in session:
        login = True
        username = session["username"]
        user_url = '/user?username=' + username
        for task in all_task:
            if task["manager"] == username:
                task["w_own"] = True
            else:
                task["w_own"] = False
        return render_template("all_task.html", task_list = all_task, login = login, user_url = user_url, username = username, list_name = "所有用户所有案件")
    else:
        login = False
        for task in all_task:
            task["w_own"] = False
        return render_template("all_task.html", task_list = all_task, login = login, list_name = "所有用户所有案件")

#/task_detail?task_id=2017-8-25
@application.route("/task_detail")
def task_detail():
    task_id = request.args.get('task_id')

    #case_manager = case_data._search_law_case(case_id = case_id)
    task_manager = task_data._search_task(task_id = task_id)
    if task_manager != []:
        manager_name = task_manager[0]["manager"]
        manager_detail_url = "/user?username=" + manager_name
    else:
        manager_name = ""
        manager_detail_url = "#"


    if "username" in session:
        login = True
        username = session["username"]
        user_url = "/user?username=" + username

        if manager_name == session["username"]:
            own = True
        else:
            own = False
        return render_template("task.html", login = login, user_url = user_url, username = username, manager_detail_url = manager_detail_url, task_obj = task_data._search_task(task_id = task_id)[0], own = own)
    else:
        login = False
        return render_template("task.html", login = login, manager_detail_url = manager_detail_url, task_obj = task_data._search_task(task_id = task_id)[0], own = False)
    

@application.route("/task", methods = ["GET", "POST"])
def task():
    if request.method == "GET":
        if "username" in session:
            login = True
            user_url = "/user?username=" + session["username"]
            return render_template("todolist.html", login = login, username = session["username"], user_url = user_url)
        else:
            login = False
            return render_template("todolist.html", login = login)

    elif request.method == "POST":
        #print(request.form)
        task_name = request.form["task_name"]
        task_id = request.form["task_id"]
        task_state = request.form["task_state"]
        task_type = request.form["task_type"]
        manager = request.form["manager"]
        deadline = request.form["deadline"]
        completion_date = request.form["completion_date"]
        time_required = request.form["time_required"]
        if task_data._insert_task(task_name = task_name, task_id = task_id, task_state = task_state, task_type = task_type, manager = manager, deadline = deadline, completion_date = completion_date, time_required = time_required) == True:
            #print("judge_url:", "/task_detail?task_id=" + task_id)
            return jsonify(message = "task is created successfully", judge_url = "/task_detail?task_id=" + task_id)
        else:
            if task_data._update_task(task_name = task_name, task_id = task_id, task_state = task_state, task_type = task_type, manager = manager, deadline = deadline, completion_date = completion_date, time_required = time_required):
                return jsonify(message = "task update successfully", judge_url = "/task_detail?task_id=" + task_id)
            return jsonify(message = "task update failed")
        return jsonify(message = "task is created failed")


#/get_month_task?username=gzm1997
@application.route("/get_month_task")
def get_month_task():
    manager = request.args.get('username')
    return jsonify(plan.get_month_task_json(manager = manager))
    

#/get_week_task?username=gzm1997
@application.route("/get_week_task")
def get_week_task():
    manager = request.args.get('username')
    return jsonify(plan.get_week_task_json(manager = manager))


#/each_day_task?username=gzm1997&date=7-August-201
@application.route("/each_day_task")
def each_day_task():
    target_username = request.args.get('username')
    date = request.args.get('date').replace("-", " ")
    #print("username:", target_username)
    #print("date:", date)
    index = date.find(" ")
    if len(date[:index]) == 1:
        date = "0" + date
    all_task = task_data._search_task(manager = target_username, deadline = date)
    #print(all_task)
    for task in all_task:
        task["detail_url"] = "/task_detail?task_id=" + task["task_id"]

    if "username" in session:
        login = True
        username = session["username"]
        user_url = '/user?username=' + username
        for task in all_task:
            if task["manager"] == username:
                task["w_own"] = True
            else:
                task["w_own"] = False
        return render_template("all_task.html", task_list = all_task, login = login, user_url = user_url, username = username, list_name = "用户" + target_username + "于" + date + "的所有案件")
    else:
        login = False
        for task in all_task:
            task["w_own"] = False
        return render_template("all_task.html", task_list = all_task, login = login, list_name = "用户" + target_username + "于" + date + "的所有案件")


#删除案件
@application.route("/delete_case", methods = ["POST"])
def detele_case():
    #print(request.form)
    case_id = request.form["case_id"]
    target_case = case_data._search_law_case(case_id = case_id)
    if (target_case != []) and ("username" in session) and (session["username"] == target_case[0]["username"]):
        target_case = target_case[0]
        #_edit_law_case(self, username, case_id, case_name, to_do = "create"):
        if case_data._edit_law_case(username = target_case["username"], case_id = case_id, case_name = target_case["case_name"], to_do = "delete"):
            return jsonify(success = "delete case successfully!", username = target_case["username"])
        else:
            return jsonify(fail = "delete case failed!")
    else:
        abort(401)

#删除任务
@application.route("/delete_task", methods = ["POST"])
def delete_task():
    #print(request.form)
    task_name = request.form["task_name"]
    task_id = request.form["task_id"]
    target_task = task_data._search_task(task_name = task_name, task_id = task_id)
    if (target_task != []) and ("username" in session) and (session["username"] == target_task[0]["manager"]):
        if task_data._delete_task(task_name = task_name, task_id = task_id):
            return jsonify(success = "delete task successfully!", username = target_task[0]["manager"])
        else:
            return jsonify(fail = "delete task failed!")
    return jsonify(fail = "delete task failed!")

application.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


if __name__ == "__main__":
    application.run(debug = True, host="0.0.0.0", port=8888)
