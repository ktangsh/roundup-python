import pandas as pd

from roundup.model.other_txn import OtherTxn
from roundup.utility.database_connect import create_pandas_table, intialise_connection


class OtherTransactions:

    def get_test_user_pool_data(self):
        test_user_pool = {
            'user_id1': [1, 2, 3, 4, 5],
            'user_pool': [1500.0, 2250.0, 1270.0, 3500.0, 2600.0]
        }
        return pd.DataFrame(test_user_pool, columns=['user_id1', 'user_pool'])

    def insert_action_column_based_on_txn_type(self, df):
        df.loc[df[OtherTxn.TRANSACTION_TYPE] != 'Withdrawal', 'action'] = df[
            OtherTxn.AMOUNT_TRANSACTED]
        df.loc[df[OtherTxn.TRANSACTION_TYPE] == 'Withdrawal', 'action'] = df[OtherTxn.AMOUNT_TRANSACTED] * -1
        print(df[[OtherTxn.USER_ID, OtherTxn.AMOUNT_TRANSACTED, 'action']])

    def add_pool_amount_to_user_pool(self, df_test_user_pool, df):
        df_user_pool_action = (df.groupby(OtherTxn.USER_ID)['action'].sum().reset_index())
        df_action = pd.merge(df_test_user_pool, df_user_pool_action, left_on='user_id1',
                             right_on=OtherTxn.USER_ID,
                             how='left').drop(
            OtherTxn.USER_ID, axis=1)
        df_action['user_pool'] = df_action.apply(lambda row: row.user_pool + row.action, axis=1)
        df_action = df_action.rename({'user_id1': OtherTxn.USER_ID}, axis=1)
        print(df_action[[OtherTxn.USER_ID, 'user_pool']])

    def get_other_transactions(self):
        conn = intialise_connection()
        with conn, conn.cursor() as cur:  # start a transaction and create a cursor
            # Retrieve transaction data from app on other_transactions table
            global df_other_txn
            sql_retrieve_df = "select * from other_transactions"
            df_other_txn = create_pandas_table(sql_retrieve_df, conn)
            print(df_other_txn)
        conn.close()

        df_user_pool = self.get_test_user_pool_data()
        print(df_user_pool)

        self.insert_action_column_based_on_txn_type(df_other_txn)
        self.add_pool_amount_to_user_pool(df_user_pool, df_other_txn)
