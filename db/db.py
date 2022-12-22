import datetime
import psycopg2


def db_connect():
    connection = psycopg2.connect(user="andrey",
                                  password="SpkSpkSpk1979",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="bot_db",
                                  connect_timeout=60)
    return connection


def db_insert_stikers(title: str, pack_url: str, stik_count: str, stikers: list):
    connection = db_connect()
    with connection:
        with connection.cursor() as cursor:
            create_table_pack_query = '''CREATE TABLE IF NOT EXISTS stiker_pack
                                    (pack_url VARCHAR PRIMARY KEY NOT NULL,
                                    title TEXT,
                                    stik_count VARCHAR);'''

            create_table_stikers_query = '''CREATE TABLE IF NOT EXISTS stikers 
                                                (pack_url VARCHAR not null references stiker_pack(pack_url),
                                                stik_url VARCHAR);'''

            # Execute a command: this creates a new table
            cursor.execute(create_table_pack_query)
            cursor.execute(create_table_stikers_query)

            stiker_pack_tuple = (title, pack_url, stik_count)
            insert_query = """ INSERT INTO stiker_pack (title,  pack_url, stik_count) VALUES (%s, %s, %s)"""
            cursor.execute(insert_query, stiker_pack_tuple)

            for stiker in stikers:
                stiker_tuple = (pack_url, stiker)
                insert_query = """ INSERT INTO stikers (pack_url, stik_url) VALUES (%s, %s)"""
                cursor.execute(insert_query, stiker_tuple)




            # query = """select url, title from memes LIMIT 20"""
            # cursor.execute(query)
            # record = cursor.fetchall()
            # print(record[0][0])
            # Itemprice = int(record)
            #
            # # find customer's ewallet balance
            # query = """select balance from ewallet where userId = 23"""
            # cursor.execute(query)
            # record = cursor.fetchone()[0]
            # ewalletBalance = int(record)
            # new_EwalletBalance = ewalletBalance
            # new_EwalletBalance -= Itemprice
            #
            # # Withdraw from ewallet now
            # sql_update_query = """Update ewallet set balance = %s where id = 23"""
            # cursor.execute(sql_update_query, (new_EwalletBalance,))
            #
            # # add to company's account
            # query = """select balance from account where accountId = 2236781258763"""
            # cursor.execute(query)
            # record = cursor.fetchone()
            # accountBalance = int(record)
            # new_AccountBalance = accountBalance
            # new_AccountBalance += Itemprice
            #
            # # Credit to  company account now
            # sql_update_query = """Update account set balance = %s where id = 2236781258763"""
            # cursor.execute(sql_update_query, (new_AccountBalance,))
            # print("Transaction completed successfully ")


def db_select_count():
    connection = db_connect()
    with connection:
        with connection.cursor() as cursor:
            query = """select count(*) from mames"""
            cursor.execute(query)
            count = cursor.fetchone()[0]
            return count
