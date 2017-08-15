import time
import calendar

def get_localdate_json():
    l_time = time.localtime()
    year = l_time.tm_year
    month = l_time.tm_mon
    day = l_time.tm_mday
    return {"year": year, "month": month, "day": day}

def get_localtime_json():
    l_time = time.localtime()
    year = l_time.tm_year
    month = l_time.tm_mon
    day = l_time.tm_mday
    hour = l_time.tm_hour
    minute = l_time.tm_min 
    return {"year": year, "month": month, "day": day, "hour": hour, "minute": minute}

def get_month_str():
    l_time = get_localdate_json()
    return calendar.month(l_time["year"], l_time["month"])
#2017-08-15-11-11
def get_localtime_str():
    l_time = time.localtime()
    year = str(l_time.tm_year)
    month = str(l_time.tm_mon)
    day = str(l_time.tm_mday)
    hour = str(l_time.tm_hour)
    if len(hour) == 1:
        hour = "0" + hour
    minute = str(l_time.tm_min)
    if len(minute) == 1:
        minute = "0" + minute
    return hour + ":" + minute + " " + month + "/" + day + "/" + year

def format_localtime_json(time_str):
    return {"year": time_str[0:4], "month": time_str[5:7], "day": time_str[8:10], "hour": time_str[11:13], "minute": time_str[14:16]}

if __name__ == "__main__":
    print("local date is:")
    print(get_localdate_json())
    print("local time json is:")
    print(get_localtime_json())
    print("local time str is:")
    print(get_localtime_str())
    print("local month calendar:")
    print(get_month_str())
    print(format_localtime_json(get_localtime_str()))


