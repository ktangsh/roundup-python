import math
import pandas as pd

df = pd.read_json('resources/Test_Transaction_Data.json')
# inputs here are the transaction amounts from GET request JSON file from 'Retrieve Banking Transactions' API.

transaction_amt = df['transactionAmount'].astype(float)
print('These are your transactions to be rounded up: ')
print(transaction_amt.tolist())


def get_roundup_diff(transaction_list):
    diff_list = []
    roundup_multiple = float(input("User Round Up Multiple = "))
    # input here is the value on the 'Automatic Round Up Dollar Multiple'5 column in the User table

    for position in range(len(transaction_list)):
        diff = math.ceil(transaction_list[position] / roundup_multiple) * roundup_multiple - transaction_list[position]
        diff_list.append(diff)

    return diff_list


round_up_list = ['%.2f' % item for item in get_roundup_diff(transaction_amt)]
print('These are the round up amounts:')
print(round_up_list)
