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


def new_sub(
    cur,
    pubsub,
    db_obj,
    webhook,
    mailgun_obj,
):
    print(pubsub.zipcodes)
    cur.execute(
        "INSERT INTO "
        + get_table(db_obj)
        + "(pubsub_name, dates, on_sale, price, image, zipcodes, cities, states, prices, datesArray, closeststore) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (
            pubsub.pubsub_name.replace(" ", "-").lower(),
            pubsub.date,
            "True",
            pubsub.price,
            pubsub.image,
            ",".join(pubsub.zipcodes),
            ",".join(pubsub.cities),
            ",".join(pubsub.states),
            ",".join(pubsub.dates),
            ",".join(pubsub.prices),
            ",".join(pubsub.closest_stores),
        ),
    )
    # mailgun.send_email_and_webhook(
    #     pubsub_name, pubsub_date, pubsub_price, pubsub_image, webhook, mailgun_obj
    # )


def remove_sub(cur, sub_name, table, db_object, connection):
    update_string = "DELETE FROM {table} WHERE  pubsub_name = '{sub}'"
    update_query = cur.execute(
        update_string.format(table=get_table(db_object), sub=sub_name)
    )
    close(connection)


def existing_sub(
    cur,
    pubsub,
    db_obj,
    webhook,
    mailgun_obj,
):
    update_string = "Update {table} SET on_sale = '{on_sale}', dates = '{dates}', price = '${price}', image = '{image}', zipcodes = '{zipcodes}', cities = '{cities}', states = '{states}', datesArray = '{datesArray}', prices = '{prices}', closeststore = '{closest_store}' WHERE pubsub_name = '{sub}'"
    update_query = cur.execute(
        update_string.format(
            table=get_table(db_obj),
            on_sale="True",
            dates=pubsub.date,
            price=pubsub.price,
            image=pubsub.image,
            zipcodes=",".join(pubsub.zipcodes),
            cities=",".join(pubsub.cities),
            states=",".join(pubsub.states),
            datesArray=",".join(pubsub.dates),
            prices=",".join(pubsub.prices),
            closest_store=",".join(pubsub.closest_stores),
            sub=pubsub.pubsub_name.lower().replace(" ", "-"),
        )
    )
    mailgun.send_email_and_webhook(pubsub, webhook, mailgun_obj)


def update_sale_date(cur, sub_name, table, db_object, connection, dates):
    update_string = "Update {table} SET dates = '{dates}' WHERE pubsub_name = '{sub}'"
    update_query = cur.execute(
        update_string.format(table=get_table(db_object), sub=sub_name, dates=dates)
    )
    close(connection)


def update_state(cur, sub_name, table, db_object, connection, on_sale):
    update_string = (
        "Update {table} SET on_sale = '{on_sale}' WHERE pubsub_name = '{sub}'"
    )
    update_query = cur.execute(
        update_string.format(table=get_table(db_object), sub=sub_name, on_sale=on_sale)
    )
    close(connection)


def sub_check(
    pubsub,
    cur,
    db_obj,
    webhook,
    mailgun_obj,
):
    exist_query = (
        "select exists(select 1 from {table} where pubsub_name ='{sub}' limit 1)"
    )
    exist_check = cur.execute(
        exist_query.format(
            table=get_table(db_obj),
            sub=pubsub.pubsub_name.lower().replace(" ", "-"),
        )
    )
    count = cur.fetchone()[0]
    # Sub exist
    if count == True:
        print(pubsub.pubsub_name + " is going to be modified")
        existing_sub(
            cur,
            pubsub,
            db_obj,
            webhook,
            mailgun_obj,
        )
    else:
        new_sub(
            cur,
            pubsub,
            db_obj,
            webhook,
            mailgun_obj,
        )
