import time
import calendar

def get_localtime_json():
    l_time = time.localtime()
    year = l_time.tm_year
    month = l_time.tm_mon
    day = l_time.tm_mday
    return {"year": year, "month": month, "day": day}

def get_month_str():
    l_time = get_localtime_json()
    return calendar.month(l_time["year"], l_time["month"])


if __name__ == "__main__":
    print("local time is:")
    print(get_localtime_json())
    print("local month calendar:")
    print(get_month_str())


