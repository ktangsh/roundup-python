import math
import pandas as pd

df = pd.read_json('Test_Transaction_Data.json')
# inputs here are the transaction amounts from GET request JSON file from 'Retrieve Banking Transactions' API.

transaction_amt = df['transactionAmount'].astype(float)
print('These are your transactions to be rounded up: ')
print(transaction_amt)

def roundup_transactions(transaction_list):
    roundup_multiple = float(input("User Round Up Multiple = "))
    # input here is the value on the 'Automatic Round Up Dollar Multiple' column in the User table

    for position in range(len(transaction_list)):
       transaction_list[position] = (math.ceil(transaction_list[position]/roundup_multiple)*roundup_multiple)

roundup_transactions(transaction_amt)
print ('These are the rounded up transactions ', transaction_amt)


