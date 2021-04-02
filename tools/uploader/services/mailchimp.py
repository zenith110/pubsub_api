from mailchimp3 import MailChimp
from services.mailchimp_api import key, username, list_id
from services import newsletter_template
from string import Template

def group_id_fetcher(name: str, interest_group):
    interest_id = 0
    for i in range(0, len(interest_group)):
        if(interest_group[i]["name"] == name):
            interest_id = interest_group[i]["id"]
            return interest_id
        else:
            continue
        
def interest_category(name: str, interest_category):
    interest_category_id = 0
    for i in range(0, len(interest_category)):
        if(interest_category[i]["title"] == name):
            interest_category_id = interest_category[i]["id"]
            return interest_category_id
        else:
            continue


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
    campaign_name, audience_id, from_name, reply_to, client, sub_name, sub_value, interest_id
):
    campaign_name = campaign_name
    audience_id = audience_id
    from_name = from_name
    reply_to = reply_to

    data = {
        "recipients": {"list_id": audience_id},
        "conditions": [
            {
                "condition_type": "Interests",
                "field": "interest-" + interest_id,
                "op": "interestcontains",
                "value": sub_value,
            }
        ],
        "segment_opts": [
            {
                "match": sub_value,
                "conditions": [],
            }
        ],
        "settings": {
            "subject_line": campaign_name,
            "from_name": from_name,
            "reply_to": reply_to,
        },
        "type": "regular",
    }
    data["segment_opts"][0]["conditions"] = data["conditions"]

    new_campaign = client.campaigns.create(data)
    return new_campaign


"""
Sends the email using the specified audience
"""


def send_email(sub_name, date):
    client = MailChimp(key, username)
    campaign_name = "Pubsub Sale notification"

    audience_id = list_id
    """
    Grabs the category id using the interest_category json response
    """
    category = client.lists.interest_categories.all(list_id = list_id, get_all=False)
    category_id = interest_category("pubsub", category["categories"])
    """
    Grabs the group id associated with this sub_name
    """
    interest_groups = client.lists.interest_categories.interests.all(list_id=list_id, category_id=category_id, get_all=False)
    interest_group_id = group_id_fetcher(sub_name, interest_groups["interests"])
    """
    Adds the id to a list for the email
    """
    sub_id = []
    sub_id.append(interest_group_id)
    from_name = "Pubsub-api"
    reply_to = "email.pubsub.api@gmail.com"
    campaign = campaign_creation_function(
        campaign_name, audience_id, from_name, reply_to, client, sub_name, sub_id, category_id
    )
    html_code = newsletter_template.html_code
    html_code = html_code.replace("sub_name", sub_name).replace("dates_of_sub", date)
    customized_template(html_code, campaign["id"], client)
    send_mail(campaign["id"], client)
    print("Campaign is sent!")
