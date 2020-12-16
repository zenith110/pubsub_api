import requests
from mailchimp3 import MailChimp
from services.mailchimp_api import key, username

def register_data(email, first_name):
    print("Email is: " + email + "\nName is: " + first_name)
    client = MailChimp(key, username)
    print(client.list.all())