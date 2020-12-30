import math
import pandas as pd

print('Key in your transactions: ')
# inputs here are the transaction amounts from GET request JSON file from 'Retrieve Banking Transactions' API.

df = pd.read_json('/Users/clee/Desktop/Transaction_Data_Test.json')
print(df)

transaction_amt = df['transactionAmount'].astype(float)
print(transaction_amt)

# try:
#     transaction_list = []
#     while True:
#         transaction_list.append(float(input()))
    # if the input is not an integer nor float, print the list
# except:
print('These are your transactions to be rounded up: ', transaction_amt)


def roundup_transactions(transaction_list):
    roundup_multiple = float(input("User Round Up Multiple = "))
    # input here is the value on the 'Automatic Round Up Dollar Multiple' column in the User table

    for position in range(len(transaction_list)):
       transaction_list[position] = (math.ceil(transaction_list[position]/roundup_multiple)*roundup_multiple)

roundup_transactions(transaction_amt)
print ('These are the rounded up transactions ', transaction_amt)
