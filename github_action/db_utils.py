from discord_webhook import webhook
import psycopg2
import json
import mailgun
"""
Allows us to query specific commands
"""


def close(connection):
    # Push the data onto the database
    connection.commit()

    print("Closing connection to the database!")
    # Close the database
    connection.close()


def get_table(db_object):
    return db_object.table


def connect(db_object):
    return psycopg2.connect(
        user=db_object.user,
        password=db_object.password,
        host=db_object.host,
        port=db_object.port,
        database=db_object.database,
    )


def new_sub(cur, pubsub_name, pubsub_date, pubsub_price, pubsub_image, mailgun_obj, db_obj, connection):
    cur.execute(
        "INSERT INTO "
        + get_table(db_obj)
        + "(pubsub_name, dates, on_sale, price, image) VALUES (%s, %s, %s, %s, %s)",
        (
            pubsub_name.replace(" ", "-").lower(),
            pubsub_date,
            True,
            pubsub_price,
            pubsub_image,
        ),
    )
    close(connection)
    mailgun.send_email_and_webhook(
        pubsub_name, pubsub_date, pubsub_price, pubsub_image, webhook, mailgun_obj)

def remove_sub(cur, sub_name, table, db_object, connection):
    update_string = "DELETE FROM {table} WHERE  pubsub_name = '{sub}'"
    update_query = cur.execute(update_string.format(table=get_table(db_object), sub=sub_name))
    close(connection)

def existing_sub(cur, pubsub_name, pubsub_date, pubsub_price, pubsub_image, webhook, mailgun_obj, db_obj, connection):
    update_string = "Update {table} SET on_sale = '{on_sale}', dates = '{dates}', price = '${price}', image = '{image}' WHERE pubsub_name = '{sub}'"
    update_query = cur.execute(
        update_string.format(
            table=get_table(db_obj),
            on_sale="True",
            dates=pubsub_date,
            price=pubsub_price,
            image=pubsub_image,
            sub=pubsub_name.lower().replace(" ", "-"),
        )
    )
    close(connection)
    mailgun.send_email_and_webhook(
        pubsub_name, pubsub_date, pubsub_price, pubsub_image, webhook, mailgun_obj)

def update_sale_date(cur, sub_name, table, db_object, connection, dates):
    update_string = "Update {table} SET dates = '{dates}' WHERE pubsub_name = '{sub}'"
    update_query = cur.execute(update_string.format(table=get_table(db_object), sub=sub_name, dates=dates))
    close(connection)

def sub_check(pubsub_name, pubsub_date, pubsub_price, pubsub_image, cur, webhook, mailgun_obj, db_obj, connection):
    exist_query = "select exists(select 1 from {table} where pubsub_name ='{sub}' limit 1)"
    exist_check = cur.execute(
        exist_query.format(
            table=get_table(db_obj),
            sub=pubsub_name.lower().replace(" ", "-"),
        )
    )
    count = cur.fetchone()[0]
    # Sub exist
    if count == True:
        existing_sub(cur, pubsub_name, pubsub_date,
                     pubsub_price, pubsub_image, webhook, mailgun_obj, db_obj, connection)
    else:
        new_sub(cur, pubsub_name, pubsub_date, pubsub_price,
                pubsub_image, mailgun_obj, db_obj, connection)
