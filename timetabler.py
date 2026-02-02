from tabulate import tabulate
from datetime import date, timedelta
import numpy as np

def get_urgency_score(urgency, days_due):
    return (urgency ** 2) * np.exp(-0.15*days_due)

def get_date(date_str):
    dates = date_str.split("/")
    return date(int(dates[0]), int(dates[1]), int(dates[2]))

def compare_dates(date1, date2):
    d1 = get_date(date1)
    d2 = get_date(date2)
    
    if d1 < d2:
        return
    elif d1 > d2:
        return 1
    else:
        return 0

def period_in_between(date1,date2):
    d1 = get_date(date1)
    d2 = get_date(date2)
        
    return int((d2 - d1).total_seconds() // 86400 + 1)

#Initialize To Do Data
data = {}
start_end = [0,0]

#Initialize Item Count
file = open("ToDo.txt", "r")
linecount = 0

#Initialize Top Job
Top_job = ["", 0]  # [Job String, Urgency Score]

#Get Date Data
for line in file:
    if linecount == 0:
        linecount += 1
        continue
    
    else:
        lineitem = line.strip()
        array = lineitem.split(",")
        
        for i in range(len(array)):
            array[i] = array[i].lstrip()
            array[i] = array[i].rstrip()
        
        if start_end[0] == 0:
            start_end[0] = array[0]
            start_end[1] = array[0]
        else:
            if compare_dates(array[0], start_end[0]) == -1:
                start_end[0] = array[0]
            if compare_dates(array[0], start_end[1]) == 1:
                start_end[1] = array[0] 
        date_key = (get_date(array[0]))
        due_factor = date_key - date.today()
        urgency_factor = int(array[3])
        if get_urgency_score(urgency_factor, due_factor.days) > Top_job[1]:
            Top_job[0] = f"{array[1]} - {array[2]} due on {array[0]}"
            Top_job[1] = get_urgency_score(urgency_factor, due_factor.days)

            
        
        if date_key not in data.keys():
            data[date_key] = {array[1]:[array[2:]]}
        else:
            if array[1] not in data[date_key].keys():
                data[date_key][array[1]] = [array[2:]]
            else:
                data[date_key][array[1]].append(array[2:])
            
file.close()
#Output Top Job
print("Top Priority Task:", Top_job[0])
print("Urgency Score:", Top_job[1])
            
#Replace Missing Dates with Empty Entries               
for i in range(period_in_between(start_end[0], start_end[1])):
    current_date = get_date(start_end[0]) + timedelta(days=i)
    if current_date not in data.keys():
        data[current_date] = {}

starting_weekday = get_date(start_end[0]).weekday()
ending_weekday = get_date(start_end[1]).weekday()

#Generate Header
table = [["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]]

#First row
week_count = 0
week1_array = [""] * 7
for i in range(7):
    if i < starting_weekday:
        week1_array[i] = ""
    else:
        current_date = get_date(start_end[0]) + timedelta(days=week_count)
        if current_date in data.keys():
            day_str = f"{current_date.day}/{current_date.month}\n"
            for subjects, task_list in data[current_date].items():
                day_str += f"{subjects}:\n"
                for task in task_list:
                    day_str += " - " + task[0] + "\n"
            week1_array[i] = day_str.strip()
        else:
            week1_array[i] = ""
        week_count += 1
table.append(week1_array)

#Second Row and beyond
while week_count < period_in_between(start_end[0], start_end[1]):
    week_array = [""] * 7
    for i in range(7):
        current_date = get_date(start_end[0]) + timedelta(days=week_count)
        if current_date in data.keys():
            day_str = f"{current_date.day}/{current_date.month}\n"
            for subjects, task_list in data[current_date].items():
                day_str += f"{subjects}:\n"
                for task in task_list:
                    day_str += " - " + task[0] + "\n"
            week_array[i] = day_str.strip()
        else:
            week_array[i] = ""
        week_count += 1
    table.append(week_array)

with open('timetable.txt', 'w') as outputfile:
    outputfile.write("Top Priority Task: " + str(Top_job[0]) + "\n")
    outputfile.write("Urgency Score: " + str(Top_job[1]) + "\n")
    outputfile.write(tabulate(table,tablefmt="grid"))







    
