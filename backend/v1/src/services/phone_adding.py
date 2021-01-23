import connect_db
import json


def add_phone(phone_number: str, subs_selected: list):
    """
    Ignores the numbers or special characters
    """
    subs_selected = ", ".join(subs_selected)
    print(subs_selected)
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
        update_string = "Update {table} SET category = '{subs_selection}' WHERE phone_number = '{phone}'"
        update_query = cur.execute(
                update_string.format(
                    table=connect_db.get_table(),
                    subs_selection = subs_selected,
                    phone = phone_number
                )
            )
        print("We finished adding data!")
        return "we updated!"
    else:
        print("Inserting " + phone_number + " into the db!")
        cur.execute(
            "INSERT INTO "
            + connect_db.get_table()
            + "(phone_number, category) VALUES (%s, %s)",
            (phone_number, subs_selected),
        )
        connect_db.close(connection)
    return "Phone data now complete!"
