from datetime import date
from datetime import datetime, timedelta

WEEKDAYS = ('\nMonday', '\nTuesday', '\nWednesday', '\nThursday', '\nFriday',)
USERS = [
    {'name': 'Bill', 'birthday': datetime(year=2023, month=10, day=27).date()},
    {'name': 'Andrew', 'birthday': datetime(year=2023, month=11, day=15).date()},
    {'name': 'Jill', 'birthday': datetime(year=2023, month=11, day=30).date()},
    {'name': 'Till', 'birthday': datetime(year=2023, month=11, day=15).date()},
    {'name': 'Jan', 'birthday': datetime(year=2023, month=11, day=19).date()},
]

def close_birthday_users(users, start, end):
    now = datetime.today().date()
    result = []
    for user in users:
        birthday = user.get('birthday').replace(year=now.year)
        if start <= birthday <= end:
            result.append(user)
    return result


def get_birthdays_per_week(users):
    now = datetime.today().date()
    current_week_day = now.weekday()
    if current_week_day >= 5:
        start_date = now - timedelta(days=(7-current_week_day))
    elif current_week_day == 0:
        start_date = now - timedelta(days=2)
    else:
        start_date = now
    days_ahead = 4 - current_week_day
    if days_ahead < 0:
        days_ahead += 7
    end_date = now +timedelta(days=days_ahead)
    birthday_users = close_birthday_users(users, start=start_date, end=end_date)
    weekday = None
    for user in sorted(birthday_users, key=lambda x: x['birthday'].replace(year=now.year)):
        user_birthday = user.get('birthday').replace(year=now.year).weekday()

        try:
            user_happy_day = WEEKDAYS[user_birthday]
        except IndexError:
            user_happy_day = WEEKDAYS[0]

        if weekday != user_happy_day:
            weekday = user_happy_day
            print(weekday)
            print('!' * 5)
        print(user.get('name'))


get_birthdays_per_week(USERS)