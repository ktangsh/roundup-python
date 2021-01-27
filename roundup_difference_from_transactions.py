import psycopg2
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

conn = psycopg2.connect(database="RoundUp", user="postgres", password="roundup", host="127.0.0.1", port="5432")

print("Database opened successfully")

cur = conn.cursor()

def create_pandas_table(sql_query, database = conn):
    table = pd.read_sql_query(sql_query, database)
    return table

sql_retrieve_transaction_data = "select card_transactions.transaction_id, " \
                                "card_transactions.card_number, " \
                                "card_transactions.merchant_name, " \
                                "card_transactions.date_of_transaction, " \
                                "card_transactions.amount_transacted," \
                                "card.user_id, " \
                                "user_account.auto_roundup_multiple " \
                                "from card_transactions " \
                                "inner join card ON card.card_number = card_transactions.card_number " \
                                "inner join user_account on user_account.user_id = card.user_id" \

transaction_data = create_pandas_table(sql_retrieve_transaction_data)

transaction_data['roundup_difference'] = (((transaction_data['amount_transacted'] / transaction_data['auto_roundup_multiple']).apply(np.ceil)) * transaction_data['auto_roundup_multiple']) - transaction_data['amount_transacted']

print("These are the transactions and the round up differences.")

print(transaction_data)

# Pushing user_id, roundup_multiple, roundup_differences into user_transaction table in postgres
rows = zip(transaction_data.transaction_id, transaction_data.user_id, transaction_data.auto_roundup_multiple, transaction_data.roundup_difference)
cur.execute("""CREATE TEMP TABLE codelist (transaction_id INTEGER, user_id INTEGER, roundup_multiple INTEGER, roundup_difference FLOAT) ON COMMIT DROP""")
cur.executemany("""INSERT INTO codelist (transaction_id, user_id, roundup_multiple, roundup_difference) VALUES (%s, %s, %s, %s)""",rows)

cur.execute("""
        UPDATE card_transactions
        SET roundup_difference = codelist.roundup_difference, user_id = codelist.user_id, roundup_multiple = codelist.roundup_multiple
        FROM codelist
        WHERE codelist.transaction_id = card_transactions.transaction_id;
        """)

# calculate user_pool based on user id
user_pool = (transaction_data.groupby('user_id')['roundup_difference'].sum().reset_index())
print(user_pool)  #user_pool will be calculated on the fly, and generated whenever user opens app


conn.commit()
cur.close()
conn.close()



