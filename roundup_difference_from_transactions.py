# Steps:
# 1. Create 5 users with auto_roundup_multiples. (DONE)
# 2. Create transactions with all 5 user_ids. (DONE)
# 3. Pass transactions to code - extract merchant, date, amount, and based on user id, the auto_roundup_multiple (DONE)
# 4. Compute roundup_difference for each transaction (DONE)
# 5. For each user_id, sum the roundup_difference to get the user_pool (DONE)
# 6. Post date, merchant, amount, auto_roundup_multiple, roundup_difference to user_transaction table (DONE)
# 7. Post user_pool to user_account (DONE)

import psycopg2
import pandas as pd
import numpy as np

# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)

conn = psycopg2.connect(database="RoundUp", user="postgres", password="roundup", host="127.0.0.1", port="5432")

print("Database opened successfully")

cur = conn.cursor()

def create_pandas_table(sql_query, database = conn):
    table = pd.read_sql_query(sql_query, database)
    return table

sql_retrieve_transaction_data = "select user_transaction.transaction_id, " \
                                "user_transaction.user_id, " \
                                "user_account.auto_roundup_multiple, " \
                                "user_transaction.merchant_name, " \
                                "user_transaction.date_of_transaction, " \
                                "user_transaction.amount_transacted " \
                                "from user_transaction inner join user_account on user_transaction.user_id = user_account.user_id"

transaction_data = create_pandas_table(sql_retrieve_transaction_data)

transaction_data['roundup_difference'] = (((transaction_data['amount_transacted'] / transaction_data['auto_roundup_multiple']).apply(np.ceil)) * transaction_data['auto_roundup_multiple']) - transaction_data['amount_transacted']

print("These are the transactions and the round up differences.")

print(transaction_data)


# Pushing roundup_differences into user_transaction table in postgres
rows = zip(transaction_data.transaction_id, transaction_data.roundup_difference)
cur.execute("""CREATE TEMP TABLE codelist (transaction_id INTEGER, roundup_difference FLOAT) ON COMMIT DROP""")
cur.executemany("""INSERT INTO codelist (transaction_id, roundup_difference) VALUES (%s, %s)""",rows)

cur.execute("""
        UPDATE user_transaction
        SET roundup_difference = codelist.roundup_difference
        FROM codelist
        WHERE codelist.transaction_id = user_transaction.transaction_id;
        """)

# calculate user_pool based on user id
user_pool = (transaction_data.groupby('user_id')['roundup_difference'].sum().reset_index())
print(user_pool)

# Pushing user_pool into user_account table in postgres
rows = zip(user_pool.user_id, user_pool.roundup_difference)
cur.execute("""CREATE TEMP TABLE codelist1 (user_id INTEGER, roundup_difference FLOAT) ON COMMIT DROP""")
cur.executemany("""INSERT INTO codelist1 (user_id, roundup_difference) VALUES (%s, %s)""",rows)

cur.execute("""
        UPDATE user_account
        SET user_pool = codelist1.roundup_difference
        FROM codelist1
        WHERE codelist1.user_id = user_account.user_id;
        """)

conn.commit()
cur.close()
conn.close()



