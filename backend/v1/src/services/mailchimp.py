from mailchimp3 import MailChimp
from services.mailchimp_api import key, username, list_id
from mailchimp_marketing.api_client import ApiClientError
def create_interest(client, list_id, checked_subs):
    try:
        interest = client.lists.interest_categories.create(list_id, {"title": checked_subs, "type": "hidden"})
        print("Made the interest group " + checked_subs)
        return interest
    except ApiClientError as error:
        print("Failed to make interest group: " + checked_subs + "\nError: {}".format(error.text))
        return

def register_data(email: str, first_name: str, checked_subs: list):
    print("Email is: " + email + "\nName is: " + first_name)
    client = MailChimp(key, username)
    """
    Adds provided first name with provided email  to pubsub mailing newsletter
    """
    for i in range(0, len(checked_subs)):
        interest = create_interest(client, list_id, checked_subs[i])
    client.lists.members.create(
        list_id,
        {
            "email_address": email,
            "status": "subscribed",
            "merge_fields": {"FNAME": first_name},
            "interest": checked_subs
        },
    )
    
    print("Added " + first_name + " and " + email + " to the sub newsletter!")
    return "Done"