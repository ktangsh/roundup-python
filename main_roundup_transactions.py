import numpy as np

from roundup.model.card_txn import CardTxn
from roundup.utility.database_connect import intialise_connection, create_pandas_table

# Retrieve transaction data from GET Request, and append user_id (from card_number) and roundup_multiple if
# auto_roundup_multiple >0.
sql_retrieve_df = "select txn.transaction_id, " \
                  "txn.card_number, " \
                  "txn.merchant_name, " \
                  "txn.date_of_transaction, " \
                  "txn.amount_transacted," \
                  "card.user_id, " \
                  "uacct.auto_roundup_multiple, " \
                  "txn.manual_roundup_multiple " \
                  "from card_transactions as txn " \
                  "inner join card ON card.card_number = txn.card_number " \
                  "inner join user_account as uacct on uacct.user_id = card.user_id"


class MainTransactions:

    def calculate_auto_roundup_amount(self, auto_df):
        auto_df.loc[auto_df['auto_roundup_multiple'] < 1, 'manual_roundup_multiple'] = (
            input("\nKey in either 1, 3, or 5 for the manual roundup multiple: \n"))
        self.get_roundup_amount(auto_df)
        # Converting NaN values from auto_roundup_multiple = 0 from NaN datatype to float datatype3
        auto_df.replace(np.NaN, 0, inplace=True)
        auto_df['manual_roundup_multiple'] = auto_df['manual_roundup_multiple'].astype(str).astype(int)
        return auto_df

    def calculate_manual_roundup_amount(self, manual_df):
        self.get_roundup_amount(manual_df, False)
        return manual_df

    def get_roundup_amount(self, calculate_df, is_auto=True):
        if is_auto:
            calculate_df[CardTxn.ROUNDUP_DIFF] = (((calculate_df[CardTxn.AMOUNT_TXN] / calculate_df[
                CardTxn.AUTO_ROUNDUP_MULTIPLE]).apply(np.ceil)) * calculate_df[CardTxn.AUTO_ROUNDUP_MULTIPLE]) - \
                                                 calculate_df[CardTxn.AMOUNT_TXN]

        else:
            calculate_df.loc[calculate_df[CardTxn.ROUNDUP_DIFF] <= 0, CardTxn.ROUNDUP_DIFF] = \
                (((calculate_df[CardTxn.AMOUNT_TXN] / calculate_df[
                    CardTxn.MANUAL_ROUNDUP_MULTIPLE]).apply(np.ceil)) * calculate_df[CardTxn.MANUAL_ROUNDUP_MULTIPLE]) - \
                calculate_df[CardTxn.AMOUNT_TXN]

        return calculate_df

    def update_card_transaction_table(self, df, cur):
        # Pushing user_id, roundup_multiple, roundup_differences into card_transaction table in postgres
        rows = zip(df.transaction_id, df.user_id, df.auto_roundup_multiple, df.manual_roundup_multiple,
                   df.roundup_difference)
        cur.execute(
            """CREATE TEMP TABLE codelist (transaction_id INTEGER, user_id INTEGER, auto_roundup_multiple INTEGER, 
            manual_roundup_multiple INTEGER, roundup_difference FLOAT) ON COMMIT DROP""")
        cur.executemany(
            """INSERT INTO codelist (transaction_id, user_id, auto_roundup_multiple, manual_roundup_multiple, 
            roundup_difference) VALUES (%s, %s, %s, %s, %s)""",
            rows)
        cur.execute("""
        UPDATE card_transactions SET roundup_difference = codelist.roundup_difference, user_id = 
        codelist.user_id, auto_roundup_multiple = codelist.auto_roundup_multiple, manual_roundup_multiple = 
        codelist.manual_roundup_multiple FROM codelist WHERE codelist.transaction_id = card_transactions.transaction_id; 
        """)

    def get_main_transactions(self):

        conn = intialise_connection()
        with conn, conn.cursor() as cur:  # start a transaction and create a cursor
            df = create_pandas_table(sql_retrieve_df, conn)
            print("\nThese are all the transactions\n")
            print(df.to_string())

            self.calculate_auto_roundup_amount(df)
            # Calculating roundup_difference for transactions with manual_roundup_multiple
            self.calculate_manual_roundup_amount(df)

            # Printing all transactions and their roundup_differences
            print("\nThese are the transactions and the round up differences.\n")
            print(df.to_string())

            self.update_card_transaction_table(df, cur)

            # # calculate user_pool based on user id
            user_pool = (df.groupby(CardTxn.USER_ID)[CardTxn.ROUNDUP_DIFF].sum().reset_index())
            user_pool = user_pool.rename({CardTxn.ROUNDUP_DIFF: 'user_pool'}, axis=1)

            print(user_pool)  # user_pool will be calculated on the fly, and generated whenever user opens app

        conn.close()
