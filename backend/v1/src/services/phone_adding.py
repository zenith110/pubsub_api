import connect_db
import json


def add_phone(phone_number: str):
    """
    Ignores the numbers or special characters
    """
    getVals = list([val for val in phone_number if val.isnumeric()])
    """
    Joins back the list into a string to print at the end
    """
    phone_number = "".join(getVals)
    connection = connect_db.connect()
    cur = connection.cursor()
    """
    Checks to see if that row exist
    """
    exist_query = (
        "select exists(select 1 from {table} where phone_number ='{phone}' limit 1)"
    )
    exist_check = cur.execute(
        exist_query.format(table=connect_db.get_table(), phone=phone_number)
    )
    count = cur.fetchone()[0]
    if count == True:
        print("Phone number within database, skipping!")
    else:
        print("Inserting " + phone_number + " into the db!")
        cur.execute(
            "INSERT INTO "
            + connect_db.get_table()
            + "(phone_number) VALUES ("
            + phone_number
            + ")"
        )
        connect_db.close(connection)
    return "Phone data now complete!"
