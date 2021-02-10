import psycopg2
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

conn = psycopg2.connect(database="roundup_sg", user="roundup", password="Roundup2020!", host="roundup-postgres.cwa6gmrtdm6r.ap-southeast-1.rds.amazonaws.com", port="5432")

print("Database opened successfully")

cur = conn.cursor()

def create_pandas_table(sql_query, database = conn):
    table = pd.read_sql_query(sql_query, database)
    return table

# Retrieve transaction data from app on other_transactions.

sql_retrieve_df = "select * from other_transactions " \

df = create_pandas_table(sql_retrieve_df)
# df = df.groupby(['user_id']).sum().reset_index()

print(df)


# test user_pool data
test_user_pool = {'user_id1': ['1','2','3','4','5'],
                  'user_pool': ['1500','2250','1270','3500','2600']}

df_user_pool = pd.DataFrame(test_user_pool, columns = ['user_id1', 'user_pool'])

df_user_pool['user_id1'] = df_user_pool['user_id1'].astype(str).astype(int)
df_user_pool['user_pool'] = df_user_pool['user_pool'].astype(str).astype(float)

print(df_user_pool)

df.loc[df['transaction_type'] != 'Withdrawal', 'action'] = df['amount_transacted']
df.loc[df['transaction_type'] == 'Withdrawal', 'action'] = df['amount_transacted']*-1

print(df[['user_id','amount_transacted','action']])

df_user_pool_action = (df.groupby('user_id')['action'].sum().reset_index())

df_action = pd.merge(df_user_pool, df_user_pool_action, left_on='user_id1', right_on='user_id', how='left').drop('user_id', axis=1)

df_action['user_pool'] = df_action.apply(lambda row: row.user_pool + row.action, axis=1)

df_action = df_action.rename({'user_id1': 'user_id'}, axis=1)

print(df_action [['user_id','user_pool']])

conn.commit()
cur.close()
conn.close()