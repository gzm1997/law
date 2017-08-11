#-*- coding=utf-8 -*-
from flask import Flask, render_template, request, session, jsonify, abort, redirect, url_for
from data_manager import user_manager, case_manager, task_manager
import send_email

app = Flask(__name__)
user_data = user_manager.User_manager("root", "Gzm20125")
case_data = case_manager.Case_manager("root", "Gzm20125")
task_data = task_manager.Task_manager("root", "Gzm20125")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        comfirmpassword = request.form["comfirmpassword"]
        print(username, password, comfirmpassword)
        if password != comfirmpassword:
            return jsonify(comfirmpassword="password and comfirmpassword are different")

        check_user_email = user_data._search_user(email=email)
        check_user_username = user_data._search_user(username=username)
        if check_user_email != {}:
            print("email double")
            return jsonify(email="email have been signup")
        if check_user_username != {}:
            print("username double")
            return jsonify(username="username have been signup")
        try:
            vertifycode = send_email.send_vertify_email(email)
        except:
            vertifycode = "email err"
            return jsonify(email="your email is wrong")

        print("vertifycode", vertifycode)
        if user_data._insert_r_user(email, username, password, vertifycode) == 0:
            return jsonify(warn="signup successfully and need to go to your email")
        else:
            return jsonify(warn="sign up failed")


@app.route("/vertify")
def vertify():
    vertifycode = request.args.get('vertifycode')
    result = user_data._search_r_user(vertifycode=vertifycode)
    if result == {}:
        return "no such a vertifycode"
    print("result", result)
    print("email", result["email"])
    print("username", result["username"])
    print("password", result["password"])
    if result != {}:
        if user_data._insert_user(email=result["email"], username=result["username"], password=result["password"]):
            session['username'] = result["username"]
            return redirect(url_for('user', username=result["username"]))
        else:
            return "vertify err"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        # if "username" in session:
            # session.pop["username"]

        print("this is post")
        email = request.form["email"]
        password = request.form["password"]
        print("email:", email)
        print("password:", password)
        result = user_data._search_user(email=email)
        print(result)
        if result == {}:
            print("no such account")
            return jsonify(email="no such a account!")
        elif result != {} and result["password"] != password:
            print("password wrong")
            return jsonify(password="password is wrong")
        elif result != {} and result["password"] == password:
            print("login successfully")
            session['username'] = result["username"]
            return jsonify(success=result["username"])




@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/edit_case", methods=["POST"])
def add_case():
    print(request.form)
    create_delete_case = request.form["create_delete_case"]
    case_id = request.form["case_id"]
    case_name = request.form["case_name"]

    if "username" not in session:
        return jsonify(offline="fail because of offline now")
    if case_data._search_law_case(case_id=case_id) != []:
        return jsonify(case_id="case_id has been used")
    if case_data._search_law_case(case_name=case_name) != []:
        return jsonify(case_name="case_name has been used")

#/table?case_id=2017-8-10&t_type=t1
@app.route("/table", methods=["GET", "POST"])
def table():
    if request.method == "GET":
        case_id = request.args.get("case_id")
        t_type = request.args.get('t_type')
        print("show table case_id:", case_id, "t_type:", t_type)

        target_case = case_data._search_law_case(case_id = case_id)

        if target_case != []:
            if "username" in session and target_case[0]["username"] == session["username"]:
                own = True
            else:
                own = False

            if t_type == "t1":
                return render_template("table1.html", tc = case_data._search_table(t_type = "t1", case_id = case_id), own = own)
            elif t_type == "t2":
                return render_template("table2.html", tc = case_data._search_table(t_type = "t2", case_id = case_id), own = own)

            elif t_type == "t3":
                return render_template("table3.html", tc = case_data._search_table(t_type = "t3", case_id = case_id), own = own)
        abort(401)
    elif request.method == "POST":
        #print(request.form)
        content_dict = dict(request.form)
        for i in content_dict:
            content_dict[i] = content_dict[i][0]
        t_type = content_dict["t_type"]
        content_dict.pop("t_type")
        print(content_dict)
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

@app.route("/task", methods = ["GET", "POST"])
def task():
    if request.method == "GET":
        pass
    elif request.method == "POST":
        task_name = request.form["task_name"]
        task_type = request.form["task_type"]
        manager = request.form["manager"]
        deadline = request.form["deadline"]
        completion_date = request.form["completion_date"]
        time_required = request.form["time_required"]
        if task_data._insert_task(task_name, task_type, manager, deadline, completion_date, time_required) == False:
            return jsonify(feedback = "this is task has been created!")
        return jsonify(feedback = "task is created successfully")


@app.route("/user")
def user():
    print("this is user detail get")
    username = request.args.get('username')
    if "username" in session and username == session["username"]:
        print("username", username)
        email = user_data._search_user(username=username)["email"]
        print("email", email)

        case_list = case_data._search_law_case(username=username)
        task_list = task_data._search_task(manager = username)

        for case in case_list:
            case["case_detail_url"] = "/case?case_id=" + case["case_id"]

        user_url = "/user?username=" + session["username"]
        return render_template("index.html", login = True, user_url = user_url, username = session["username"], Myemail=email, Myusername=username, case_list=case_list, task_list = task_list)
    abort(401)


@app.route("/home")
def home():
    if "username" in session:
        print("already login")
        user_url = "/user?username=" + session["username"]
        return render_template("home.html", login = True, user_url = user_url , username = session["username"])
    else:
        print("not login yet")
        return render_template("home.html", login = False)

#/case?case_id=2017-8-10
@app.route("/case")
def case():
    case_id = request.args.get('case_id')
    table_urls = ["/table?case_id=" + case_id + "&t_type=" + "t1", "/table?case_id=" + case_id + "&t_type=" + "t2", "/table?case_id=" + case_id + "&t_type=" + "t3"]

    if "username" in session:
        login = True
        username = session["username"]
        user_url = "/user?username=" + username
    return render_template("case.html", table_urls = table_urls, login = login, user_url = user_url, username = username)




app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


if __name__ == "__main__":
    app.run(debug = True, host="0.0.0.0", port=8888)
