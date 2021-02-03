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

# Retrieve transaction data from GET Request, and append user_id (from card_number) and roundup_multiple if auto_roundup_multiple >0.

sql_retrieve_df = "select card_transactions.transaction_id, " \
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


df = create_pandas_table(sql_retrieve_df)

df.loc[df['auto_roundup_multiple'] < 1, 'manual_roundup_multiple'] = (input("Key in either 1, 3, or 5 for the manual roundup multiple: "))

print(df)

df['roundup_difference'] = (((df['amount_transacted'] / df['auto_roundup_multiple']).apply(np.ceil)) * df['auto_roundup_multiple']) - df['amount_transacted']

# Converting NaN values from auto_roundup_multiple = 0 from NaN datatype to float datatype
df.replace(np.NaN, 0, inplace=True)

df['manual_roundup_multiple'] = df['manual_roundup_multiple'].astype(str).astype(int)

print(df.dtypes)

df.loc[df['roundup_difference'] <= 0, 'roundup_difference'] = (((df['amount_transacted'] / df[
        'manual_roundup_multiple']).apply(np.ceil)) * df['manual_roundup_multiple']) - df[
                                                 'amount_transacted']

print("These are the transactions and the round up differences.")

print(df)

# Pushing user_id, roundup_multiple, roundup_differences into user_transaction table in postgres
rows = zip(df.transaction_id, df.user_id, df.auto_roundup_multiple, df.manual_roundup_multiple, df.roundup_difference)
cur.execute("""CREATE TEMP TABLE codelist (transaction_id INTEGER, user_id INTEGER, auto_roundup_multiple INTEGER, manual_roundup_multiple INTEGER, roundup_difference FLOAT) ON COMMIT DROP""")
cur.executemany("""INSERT INTO codelist (transaction_id, user_id, auto_roundup_multiple, manual_roundup_multiple, roundup_difference) VALUES (%s, %s, %s, %s, %s)""",rows)

cur.execute("""
        UPDATE card_transactions
        SET roundup_difference = codelist.roundup_difference, user_id = codelist.user_id, auto_roundup_multiple = codelist.auto_roundup_multiple, manual_roundup_multiple = codelist.manual_roundup_multiple
        FROM codelist
        WHERE codelist.transaction_id = card_transactions.transaction_id;
        """)

# calculate user_pool based on user id
user_pool = (df.groupby('user_id')['roundup_difference'].sum().reset_index())
print(user_pool)  #user_pool will be calculated on the fly, and generated whenever user opens app


conn.commit()
cur.close()
conn.close()



