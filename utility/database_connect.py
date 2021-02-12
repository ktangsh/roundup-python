import pandas as pd
import psycopg2


def create_pandas_table(sql_query, database):
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    table = pd.read_sql_query(sql_query, database)
    return table


def intialise_connection():
    try:
        conn = psycopg2.connect(database="roundup_sg", user="roundup", password="Roundup2020!",
                                host="roundup-postgres.cwa6gmrtdm6r.ap-southeast-1.rds.amazonaws.com", port="5432")
        print("Database opened successfully")
    except psycopg2.Error as error:
        raise ValueError(f"UNABLE TO CONNECT TO DATABASE: \n{error}") from None

    return conn
