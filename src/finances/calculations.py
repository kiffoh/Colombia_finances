import sys
sys.path.append("../src")

from gmail.read_message import *

import re
from datetime import datetime
import pytz
import pandas as pd

""" class Wallet:
    def __init__(self):
        self.total = 0
    
Colombia = Wallet()
# Colombia.total = 5024.15 """

total_balance, start_balance = 5324.15, 5324.15
Colombia_finances = []

# Assuming Colombia is in the 'America/Bogota' timezone
Colombia_start_date = pytz.utc.localize(datetime(2023, 8, 9, 16))
Colombia_finish_date = pytz.utc.localize(datetime(2023, 11, 3))
total_days = (Colombia_finish_date - Colombia_start_date).days

# Takes out the total amount spend on Accomodation
remaining_accom_budget = (Colombia_finish_date - pytz.utc.localize(datetime(2023,10,6))).days * 20
accomodation_spent = 1069.65
total_accom_budget = remaining_accom_budget + accomodation_spent
daily_budget = round((total_balance - total_accom_budget) / total_days, 2)

def extract_currency_amount(text):
    match = re.search(r'([£$€]\s*\d+(\.\d{2})?)', text)
    return float(match.group(1)[1:]) if match else 0.00

def operation(text):
    # re.search returns a Match object, not the actual matched string. In your case, op is a Match object, 
    # not the string "withdrew" or any of the other keys in your outcome dictionary. You can fix this by 
    # using op.group() to get the matched string from the Match object. Here's the corrected code:
    
    outcome = {"withdrew": "-", "deposited": "+", "interest": "+"}
    op = re.search(r'withdrew|interest|deposited', text)
    return (outcome[op.group()], op.group())

def change(oper, total_balance):
    if oper == "-":
        total_balance -= amount
        amount = amount * -1
    else:
        total_balance += amount
    return round(total_balance, 2)

# Use the service to get a list of messages from "Chip" and from messages I have individual 
# id's I can use in read_message()
results = service.users().messages().list(userId='me', q='from:hello@getchip.uk').execute()
messages = results.get('messages', [])

for message in reversed(messages):
    Colomb_dict = {}
    Date_dict = {}
    # Using the message id we obtained in the list function above (Stored in results) we can obtain the remainder
    # of the required data and store it in msg
    msg = service.users().messages().get(userId='me', id=message["id"], format='full').execute()
    
    # Find the "Date" header
    date_header = next(header for header in msg["payload"]["headers"] if header["name"] == "Date")
    # Extract the value (date) from the header
    date_value = date_header["value"]
    # Define the format of the date string
    date_format = "%a, %d %b %Y %H:%M:%S %z (%Z)"
    # Parse the date string into a datetime object
    parsed_date = datetime.strptime(date_value, date_format)
    # Now 'parsed_date' contains the date as a datetime object
    if parsed_date < Colombia_start_date:
        continue

    # Calculates the amount of withdrawal or deposit
    amount = extract_currency_amount(msg["snippet"])

    # Determines whether it was an addition or subtraction to the total
    oper, reason = operation(msg["snippet"])

     # Calculation of change to total balance
    if oper == "-":
        total_balance -= amount
        amount = amount * -1
    else:
        total_balance += amount
    total_balance = round(total_balance,2)

    # Calculation of number of days in Colombia
    days_left = (Colombia_finish_date - parsed_date).days + 1
    days_present = (parsed_date - Colombia_start_date).days + 1


    # Variables to check the amount of Money saved
    if Colombia_finances:
        # Calculates the amount allocated to the differing days
        total_spend = round(start_balance - total_balance, 2)
        spend_after_accom = round(total_spend - accomodation_spent, 2)
        daily_spend = round(spend_after_accom / days_present, 2)
        side = round(days_present * (daily_budget - daily_spend), 2)
    else:
        side = 0
    # Appends the amount change and total balance to temporary dict so it can be stored in relation to the date
    Colomb_dict["Amount"] = amount
    Colomb_dict["Total"] = total_balance
    Colomb_dict["Reason"] = reason
    Colomb_dict["Days In Colombia"] = days_present
    Colomb_dict["Side Pot"] = side

    Date_dict[parsed_date] = Colomb_dict

    Colombia_finances.append(Date_dict)

    """"
    print(f"There was a change in the balance of: {oper}{amount}")
    print("The total side amount is {}".format(side))
    print("The updated total is: {}".format(total_balance))
    print("="*50)
    """

# print(Colombia_finances)

# £20 is my budget for night, therefore the difference in 
def accomodation_allowance(days, overall_cost, Colombia_finances, today):
    temp = {}
    temp[today] = list(Colombia_finances[-1].values())[0]
    temp[today]["Reason"] = "Difference in Accomodation"
    difference = days * 20 - overall_cost
    temp[today]["Side Pot"] += difference
    # print(temp, difference)
    Colombia_finances.append(temp)


# Colombia_start_date is set with timezone information using pytz.utc.localize()
# so it is explicitly set as timezone-aware. To resolve this issue, make sure that 
# today is indeed a timezone-aware datetime object. 

today = pytz.utc.localize(pd.Timestamp.today())


# San Gil - SAMS VIP
accomodation_allowance(3, 19.5, Colombia_finances, today)

# Taganga - Ocean lovers hostel
accomodation_allowance(2, 0, Colombia_finances, today)

# Tayrona - Mama tayrona
accomodation_allowance(1, 12, Colombia_finances, today)

# Baritara - Rio hostel
accomodation_allowance(2, 54, Colombia_finances, today)

# Palomino - Dreamer
accomodation_allowance(2, 22, Colombia_finances, today)

# Minca
accomodation_allowance(1,15,Colombia_finances, today)

# Cartegena
accomodation_allowance(3, 13.5*3, Colombia_finances, today)

# print(list(Colombia_finances[-1].values())[0]["Side Pot"])

total = list(Colombia_finances[-1].values())[0]['Total']

def days_since_last_update(today, previous_date):
    difference = today.day - previous_date.day
    return difference if not None else None

def difference_in_side(total, today, side_last):
    total_balance = total
    days_present = (today - Colombia_start_date).days + 1
    total_spend = round(start_balance - total_balance, 2)
    spend_after_accom = round(total_spend - accomodation_spent, 2)
    daily_spend = round(spend_after_accom / days_present, 2)
    side_pot_today = round(days_present * (daily_budget - daily_spend), 2)
    return side_pot_today - side_last


ending = {1:"st",2:"nd",3:"rd"}
if today.day in ending:
    letters = ending[today.day]
else:
    letters = "th"

current_side = list(Colombia_finances[-1].values())[0]["Side Pot"]
print(f"As of {today.day}{letters} of {today.strftime('%B')} you have a total balance of: {total}.")
print(f"with a side pot of: {current_side}")
if days_since_last_update(today, parsed_date):
    print(f"Over the last {days_since_last_update(today, parsed_date)} days there has been a change of {difference_in_side(total, today, current_side)}.")
else:
    print(f"The last withdrawal was today.")

# Need to do a line for goals.