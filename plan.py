from law.manager_time import get_month_str, get_localdate_json
from law.manager_data import task_manager, user_manager, case_manager
import calendar

#25 August 2017
def get_month_task_json(manager):
    task_data = task_manager.Task_manager(account = "root", password = "Gzm20125")
    m_str = get_month_str().strip()
    num_day = int(m_str[m_str.rfind(" ") + 1:])
    month_year = m_str[:m_str.find("\n")]
    result = {}
    for i in range(1, num_day + 1):
        task_day = task_data._search_task(manager = manager, deadline = str(i) + " " + month_year)
        result[str(i)] = {"num": len(task_day), "url": "/each_day_task?username=" + manager + "&date=" + str(i) + "-" + month_year.replace(" ", "-")}
    return result

def get_week_task_json(manager):
    weekday_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    task_data = task_manager.Task_manager(account = "root", password = "Gzm20125")
    m_str = get_month_str().strip()
    num_day = int(m_str[m_str.rfind(" ") + 1:])
    month_year = m_str[:m_str.find("\n")]
    today = get_localdate_json()["day"]
    today_index = m_str.rfind(str(today))
    start_index = m_str[:today_index].rfind("\n")
    end_index = m_str[today_index:].find("\n") + today_index
    this_week = m_str[start_index + 1: end_index].split(" ")
    result = {}
    index = 0
    for weekday in this_week:
        task_list = task_data._search_task(manager = manager, deadline = weekday + " " + month_year)
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
    print(get_week_task_json())