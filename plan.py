from law.manager_time import get_month_str, get_localdate_json
from law.manager_data import task_manager, user_manager, case_manager
import calendar
import datetime
from law import setting
#25 August 2017
def get_month_task_json(manager):
    task_data = task_manager.Task_manager(account = setting.MYSQL_ACCOUNT, password = setting.MYSQL_PASSWORD)
    m_str = get_month_str().strip()
    num_day = int(m_str[m_str.rfind(" ") + 1:])
    month_year = m_str[:m_str.find("\n")]
    result = {}
    for i in range(1, num_day + 1):
        if len(str(i)) == 1:
            day = "0" + str(i)
        else:
            day = str(i)
        task_day = task_data._search_task(manager = manager, deadline = day + " " + month_year)
        num_done = 0
        num_undone = 0
        for task in task_day:
            if task["task_state"] == "undone":
                num_undone = num_undone + 1
            elif task["task_state"] == "done":
                num_done = num_done + 1
        if num_undone == 0:
            day_state = "done"
        elif num_done == 0 and num_undone != 0:
            day_state = "undone"
        elif num_done != 0 and num_undone != 0:
            day_state = "halfdone"
        result[str(i)] = {"num": len(task_day), "url": "/each_day_task?username=" + manager + "&date=" + str(i) + "-" + month_year.replace(" ", "-"), "day_state": day_state}
    return result

def get_week_task_json(manager):
    weekday_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    task_data = task_manager.Task_manager(account = "root", password = "Gzm20125")
    today = datetime.date.today()
    monday_delta = datetime.timedelta(today.weekday())
    Monday = today - monday_delta
    this_week = []
    for i in range(7):
        delta = datetime.timedelta(-i)
        this_week_day = Monday - delta
        if len(str(this_week_day.day)) == 1:
            day = "0" + str(this_week_day.day)
        else:
            day = str(this_week_day.day)
        this_week.append(day + " " + str(month_list[this_week_day.month - 1]) + " " + str(this_week_day.year))
    print("this week", this_week)
    result = {}
    index = 0
    for weekday in this_week:
        task_list = task_data._search_task(manager = manager, deadline = weekday)
        for task in task_list:
            task["task_detail_url"] = "/task_detail?task_id=" + task["task_id"]
        result[weekday_list[index]] = task_list
        index = index + 1
    return result


def show_today():
    week_day = ["none", "none", "none", "none", "none", "none", "none"]
    today_date = get_localdate_json()
    index = calendar.weekday(today_date["year"], today_date["month"], today_date["day"])
    week_day[index] = "block"
    return week_day

if __name__ == "__main__":
    print(get_week_task_json(manager = "gzm1997"))