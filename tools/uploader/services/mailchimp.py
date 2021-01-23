from mailchimp3 import MailChimp
from services.mailchimp_api import key, username, list_id
from services import newsletter_template
from string import Template


def customized_template(html_code, campaign_id, client):

    html_code = html_code
    campaign_id = campaign_id
    string_template = Template(html_code).safe_substitute()

    try:
        client.campaigns.content.update(
            campaign_id=campaign_id,
            data={"message": "Campaign message", "html": string_template},
        )
    except Exception as error:

        print(error)


def send_mail(campaign_id, client):
    try:
        client.campaigns.actions.send(campaign_id=campaign_id)
    except Exception as error:
        print(error)


def campaign_creation_function(
    campaign_name, audience_id, from_name, reply_to, client, sub_name
):
    campaign_name = campaign_name
    audience_id = audience_id
    from_name = from_name
    reply_to = reply_to

    data = {
        "recipients": {"list_id": audience_id},
        "segment_opts": {
            "match": "any",
            "conditions": [
                {
                    "condition_type": "Interests",
                    "field": sub_name,
                    "op": "interestcontains",
                }
            ],
        },
        "settings": {
            "subject_line": campaign_name,
            "from_name": from_name,
            "reply_to": reply_to,
        },
        "type": "regular",
    }

    new_campaign = client.campaigns.create(data)
    return new_campaign


"""
Sends the email using the specified audience
"""


def send_email(sub_name, date):
    client = MailChimp(key, username)
    campaign_name = "Pubsub Sale notification"
    audience_id = list_id
    from_name = "Pubsub-api"
    reply_to = "abrahannevarez@gmail.com"
    campaign = campaign_creation_function(
        campaign_name, audience_id, from_name, reply_to, client, sub_name
    )
    html_code = newsletter_template.html_code
    html_code = html_code.replace("sub_name", sub_name).replace("dates_of_sub", date)
    customized_template(html_code, campaign["id"], client)
    send_mail(campaign["id"], client)
    print("Campaign is sent!")
