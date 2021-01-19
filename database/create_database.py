import sqlite3
conn = sqlite3.connect('customers.sqlite')
cursor = conn.cursor()
print("Opened database successfully")

# _____________________ Create Table _____________________________________
cursor.execute(''' create table customer
        (Id BLOB primary key not null,
        Name text,
        Entry_time text,
        Entry_angry INT,
        Entry_disgust INT,
        Entry_fear INT,
        Entry_happy INT,
        Entry_sad INT,
        Entry_surprise INT,
        Entry_neutral INT,
        Entry_cnt INT,
        Entry_mood INT,
        Exit_angry INT,
        Exit_disgust INT,
        Exit_fear INT,
        Exit_happy INT,
        Exit_sad INT,
        Exit_surprise INT,
        Exit_neutral INT,
        Exit_time text,
        Exit_cnt INT,
        Result INT,
        Exit_mood INT);''')
cursor.close()
# _______________ comment this secotion if table is already created _______

conn.commit()
conn.close()

