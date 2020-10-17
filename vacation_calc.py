from datetime import date, timedelta


class Person:
    # '2019-12-04' YYYY-MM-DD
    def __init__(self, date_iso: str) -> None:
        # added default values for comfort. maybe db later?
        self.spent_days = {'2020-04-16': 7, '2020-07-01': 14}
        self.first_day = date.fromisoformat(date_iso)
        print(f'Setting up. First day of work is {self.first_day}')


    # first day of vacation. YYYY-MM-DD
    def add_spent_days(self, amount: int, when: str) -> dict:
        self.spent_days[when] = amount

        return self.spent_days


    def calculate(self, date_iso: str) -> tuple:
        day = date.fromisoformat(date_iso)
        # every 4th year it's 366 so it's a bit more accurate to calc with 365.25
        days_per_day = 28/365.25
        days_spent = sum(self.spent_days.values())
        # basically days remaining is days between dates * vacation days per day - spent vacation days
        days_between = (day - self.first_day).days
        vacation_days = (days_between-days_spent)*days_per_day-days_spent

        return vacation_days, days_between, days_spent