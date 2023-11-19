from datetime import date, datetime, timedelta

def close_birthday_users(users, start, end):
    now = date.today()
    result = []
    for user in users:
        birthday = user.get('birthday').replace(year=now.year)
        if birthday < now:
            birthday = birthday.replace(year=now.year + 1)
        if now <= birthday <= end:
            result.append(user)
    return result

def get_birthdays_per_week(users):
    WEEKDAYS = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',)
    now = date.today()
    current_week_day = now.weekday()

    if not users:
        return {} 

    start_date = now
    end_date = now + timedelta(days=7)
    birthday_users = close_birthday_users(users, start=start_date, end=end_date)
    result_dict = {}
    for user in birthday_users:
        user_birthday = user.get('birthday').replace(year=now.year)
        if user_birthday < now:
            user_birthday = user_birthday.replace(year=now.year + 1)
        user_birthday_weekday = user_birthday.weekday()
        try:
            user_happy_day = WEEKDAYS[user_birthday_weekday]
        except IndexError:
            user_happy_day = WEEKDAYS[0]
        if user_happy_day not in result_dict:
            result_dict[user_happy_day] = []
        result_dict[user_happy_day].append(user.get('name'))
    return result_dict 



# USERS = [
#     {'name': 'Bill', 'birthday': datetime(year=2023, month=10, day=27).date()},
#     {'name': 'Andrew', 'birthday': datetime(year=2023, month=11, day=15).date()},
#     {'name': 'Jill', 'birthday': datetime(year=2023, month=11, day=30).date()},
#     {'name': 'Till', 'birthday': datetime(year=2023, month=11, day=15).date()},
#     {'name': 'Jan', 'birthday': datetime(year=2023, month=11, day=19).date()},
# ]

users = [
            {
                "name": "John",
                "birthday": (datetime(year=2006, month=11, day=18).date()),
            },
            {
                "name": "Doe",
                "birthday": (datetime(year=2023, month=11, day=19).date()),
            },
            {
                "name": "Alice",
                "birthday": (datetime(2021, 11, 24)).date(),
            },
        ]

resulted = get_birthdays_per_week(users)
print(resulted)
for day_name, names in resulted.items():
    print(f'{day_name}:{",".join(names)}')





