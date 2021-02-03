# If auto roundup is disabled, auto_roundup_multiple in user_account = 0
# Order of flow
# 1. When transaction data for user_id comes in, if auto_roundup_multiple >0, use auto_roundup_multiple for calculating roundup_difference.
# 2. Else, get user_input to get roundup_multiple manually. This input will be used to calculate roundup_difference.

# auto_roundup_multiple = int(input("RoundUp Multiple: "))
# if auto_roundup_multiple > 0:
#     print ("You have auto roundups enabled")
#
# else:
#     roundup_multiple = int(input("Manual RoundUp Multiple: "))
#     print(roundup_multiple * 16.78)

import psycopg2
import pandas as pd
import numpy as np
import math

# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)

conn = psycopg2.connect(database="RoundUp", user="postgres", password="roundup", host="127.0.0.1", port="5432")

print("Database opened successfully")

cur = conn.cursor()

def create_pandas_table(sql_query, database = conn):
    table = pd.read_sql_query(sql_query, database)
    return table

# Retrieve transaction data from GET Request, and append user_id (from card_number) and roundup_multiple if auto_roundup_multiple >0.

sql_retrieve_transaction_data = "select card_transactions.transaction_id, " \
                                "card_transactions.card_number, " \
                                "card_transactions.merchant_name, " \
                                "card_transactions.date_of_transaction, " \
                                "card_transactions.amount_transacted," \
                                "card.user_id, " \
                                "user_account.auto_roundup_multiple, "\
                                "card_transactions.manual_roundup_multiple "\
                                "from card_transactions " \
                                "inner join card ON card.card_number = card_transactions.card_number " \
                                "inner join user_account on user_account.user_id = card.user_id" \


transaction_data = create_pandas_table(sql_retrieve_transaction_data)

transaction_data.loc[transaction_data['auto_roundup_multiple'] < 1, 'manual_roundup_multiple'] = (input("Key in either 1, 3, or 5 for the manual roundup multiple: "))

print(transaction_data)

transaction_data['roundup_difference'] = (((transaction_data['amount_transacted'] / transaction_data['auto_roundup_multiple']).apply(np.ceil)) * transaction_data['auto_roundup_multiple']) - transaction_data['amount_transacted']

# Converting NaN values from auto_roundup_multiple = 0 from NaN datatype to float datatype
transaction_data.replace(np.NaN, 0, inplace=True)

transaction_data['manual_roundup_multiple'] = transaction_data['manual_roundup_multiple'].astype(str).astype(int)

print(transaction_data.dtypes)

transaction_data.loc[transaction_data['roundup_difference'] <= 0, 'roundup_difference'] = (((transaction_data['amount_transacted'] / transaction_data[
        'manual_roundup_multiple']).apply(np.ceil)) * transaction_data['manual_roundup_multiple']) - transaction_data[
                                                 'amount_transacted']

print("These are the transactions and the round up differences.")

print(transaction_data)

