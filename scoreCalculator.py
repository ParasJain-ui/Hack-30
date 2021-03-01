import requests
import datetime

response = requests.get("https://api.covid19india.org/state_district_wise.json")
data=response.json()
data=dict(data)
state=[]
for key,value in data.items():
    state.append(key)
# print(state)
state.remove('State Unassigned')
# print(type(data['Andaman and Nicobar Islands']))
state_cnt={}
for states in state:
    here_case=0
    for city in data[states]['districtData']:
        here_case+=data[states]['districtData'][city]["active"]
    state_cnt[states]=here_case
# def score_calculation(city,state,programme,year,mode_of_travel,
#     branch,college_equip,symptoms,most_recent,cur_date):
def score_calculation(form):
    city = form['city']
    state = form['state']
    programme = form["programme"]
    year = int(form["year"])
    mode_of_travel = form["travel_mode"]
    branch = form["branch"]
    college_equip = form["cllg_equip"]
    symptoms = form["symptoms"]
    most_recent = form["recent_travel_date"]



    ret=0
    if(programme=="BTech"):
        ret+=6
    elif(programme=="MTech"):
        ret+=7
    elif(programme=="MSc"):
        ret+=9
    else:
        ret+=10
    
    ret+=(2*year)
    
    if(mode_of_travel=="Public"):
        ret+=4
    else:
        ret+=7

    if(branch=="Core"):
        ret+=9
    else:
        ret+=5
    
    if(college_equip=="Yes"):
        ret+=8
    else:
        ret+=0
    
    if(symptoms=="No"):
        ret+=10
    else:
        ret+=0

    active_case=state_cnt[state]

    if(active_case<=100):
        ret+=10
    elif(active_case<=1000):
        ret+=8
    elif(active_case<=5000):
        ret+=5
    elif(active_case<=10000):
        ret+=3
    
    # diff=cur_date-most_recent
    
    # if(diff<=7):
    #     ret+=0
    # elif(diff<=14):
    #     ret+=4
    # elif(diff<=28):
    #     ret+=7
    # else:
    #     ret+=10
    
    return ret


# number_days=[31,28,31,30,31,30,31,31,30,31,30,31]  
def convert_date(date):
    date = date.split("-")
    
    return datetime.datetime(int(date[0]), int(date[1]), int(date[2]))

def date_to_string(date):
    year = str(date.year)
    
    if(date.month < 10):
        month = '0'+str(date.month)
    else:
        month = str(date.month)

    if(date.day < 10):
        day = '0'+str(date.day)
    else:
        day = str(date.day)

    return f'{year}-{month}-{day}'

    # while(num>number_days[i]):
    #     num-=number_days[i]
    #     month+=1
    # return datetime.datetime(2021, num, month+1)
# l =[{score: 100, id:10}, {}, {}, {}, {}, {}]

def allot_date(null_dates, available_slots):
    records = null_dates.copy()
    records.sort(key=lambda x: x.score, reverse=True)

    ids = [i.id for i in records]
    preference_1 = [convert_date(i.preference_1) for i in records]
    preference_2 = [convert_date(i.preference_2) for i in records]
    apply_dates = [convert_date(i.apply_date) for i in records]

    num_slots = dict()
    for i in range(len(available_slots)):
        num_slots[convert_date(available_slots[i].date)] = available_slots[i].num_slots


    dates = []

    for i in range(len(records)):
        if(preference_1[i] >= apply_dates[i] and num_slots[preference_1[i]] > 0):
            num_slots[preference_1[i]] -= 1
            dates.append(date_to_string(preference_1[i]))
        elif(preference_2[i] >= apply_dates[i] and num_slots[preference_2[i]] > 0):
            num_slots[preference_2[i]] -= 1
            dates.append(date_to_string(preference_2[i]))

        else:
            for(k, v) in num_slots.items():
                if convert_date(k) > apply_date[i] and v > 0:
                    print("Going inside if")
                    dates.append(date_to_string(k))
                    break


    return ids, dates
                    
    # print(records)


# sorted_score=[]
# for student in sorted_score:
#     student_id=student[0]
#     first=0 # first preference
#     second=0 #second prefrence
#     now=0 # current date
#     start=now+7
#     left=[] # num_slots
#     # now is submitting date
#     if(first>=start and left[first]>0):
#         left[first]-=1
#         return convert_date(first)
#     elif(second>=start and left[second]>0):
#         left[second]-=1
#         return convert_date(second)
#     else:
#         while(left[start]==0):
#             start+=1
#         left[start]-=1
#         return convert_date(start)


    
