def sms(connect_db):
    connection = connect_db.connect()   
    cur = connection.cursor()
    query = "SELECT phone_number FROM {table} WHERE phone_number is not null"
    cur.execute(query.format(table = connect_db.get_table()))
    records = cur.fetchall()    
    print(records)