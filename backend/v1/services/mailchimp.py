from mailchimp3 import MailChimp
from services.mailchimp_api import key, username, list_id

def register_data(email, first_name):
    print("Email is: " + email + "\nName is: " + first_name)
    client = MailChimp(key, username)
    # add John Doe with email john.doe@example.com to list matching id '123456'
    client.lists.members.create(list_id, {
        'email_address': email,
        'status': 'subscribed',
        'merge_fields': {
            'FNAME': first_name
        },
    })
    print("Added " + first_name + " and " + email + " to the sub newsletter!")
