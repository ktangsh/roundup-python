import psycopg2

con = psycopg2.connect(database="RoundUp", user="postgres", password="roundup", host="127.0.0.1", port="5432")

print("Database opened successfully")

cur = con.cursor()
cur.execute('SELECT first_name, last_name, email, user_pool, auto_roundup_multiple from public."User"')
rows = cur.fetchall()

for row in rows:
    print(row)
cur.close()
