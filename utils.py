from datetime import datetime

def validate_dates(start_date, end_date):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        now = datetime.now()

        if start < now:
            print("Start date cannot be in the past.")
            return False
        if start > end:
            print("Start date must be before end date.")
            return False
        return True
    except ValueError:
        print("Date format should be YYYY-MM-DD.")
        return False
