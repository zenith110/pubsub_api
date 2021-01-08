from mailchimp3 import MailChimp
from services.mailchimp_api import key, username, list_id


def register_data(email: str, first_name: str):
    print("Email is: " + email + "\nName is: " + first_name)
    client = MailChimp(key, username)
    """
    Adds provided first name with provided email  to pubsub mailing newsletter
    """
    client.lists.members.create(
        list_id,
        {
            "email_address": email,
            "status": "subscribed",
            "merge_fields": {"FNAME": first_name},
        },
    )
    print("Added " + first_name + " and " + email + " to the sub newsletter!")
