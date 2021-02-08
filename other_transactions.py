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
                  'user_pool': ['1500','2250','1270','500','2600']}

df_user_pool = pd.DataFrame(test_user_pool, columns = ['user_id1', 'user_pool'])

df_user_pool['user_id1'] = df_user_pool['user_id1'].astype(str).astype(int)
df_user_pool['user_pool'] = df_user_pool['user_pool'].astype(str).astype(float)

print(df_user_pool)

# Exploring merging test_user_pool to other_transactions dataframe
#
# df_merge = pd.merge(df, df_user_pool, left_on='user_id', right_on='user_id1', how='left').drop('user_id1', axis=1)
# print(df_merge)
#
# df_merge['user_pool'] = df_merge.apply(lambda row: row.one_time_deposit + row.recurring_deposit - row.withdrawal + row.user_pool, axis=1)
# user_pool = (df_merge.groupby('user_id')['user_pool'].sum().reset_index())
# print(user_pool)





conn.commit()
cur.close()
conn.close()