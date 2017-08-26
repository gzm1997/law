from law.manager_time import get_month_str, get_localdate_json
from law.manager_data import task_manager, user_manager, case_manager


#25 August 2017
def get_month_task_json(manager):
    task_data = task_manager.Task_manager(account = "root", password = "Gzm20125")
    m_str = get_month_str().strip()
    num_day = int(m_str[m_str.rfind(" ") + 1:])
    month_year = m_str[:m_str.find("\n")]
    result = {}
    for i in range(1, num_day + 1):
        result[str(i)] = task_data._search_task(manager = manager, deadline = str(i) + " " + month_year)
    return result


if __name__ == "__main__":
    print(get_month_task_json(manager = "google"))
    print(get_month_task_json(manager = "gzm1997"))