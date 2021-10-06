import requests, re

# the new implementation using Requests

def scrape_publix_job():
    # todo >> add os.getenv for zipcode
    sub_sale_list = parse_publix_deli_page("33131")
    print(sub_sale_list)

def find_closest_publix(zipCode):
    # Make a request to the publix servics endpoint to get the closest location
    response = requests.request("GET", "https://services.publix.com/api/v1/storelocation", data="", headers={}, params={"types":"R,G,H,N,S","option":"","count":"15","includeOpenAndCloseDates":"true","isWebsite":"true","zipCode":zipCode})    
    
    # check status code
    if response.status_code != 200:
        raise ValueError('excepted 200 status for finding closest publix, was given ' + str(response.status_code) + ' for zip: ' + zipCode)

    # range over response if successful
    for store_value in response.json()["Stores"]:
        return [shave_zeros(store_value["KEY"]), store_value["NAME"]] # after the first iteration, return


def grab_end_date(product_id, publix_collection):
    # create the store cookie sub value using the store name
    store_cookie = store_to_cookie(publix_collection[1])

    headers = {
    'Cookie': 'Store={%22StoreName%22:%22' + store_cookie + '%22%2C%22StoreNumber%22:' + str(publix_collection[0]) + '%2C%22Option%22:%22ACDFJNORTUV%22%2C%22ShortStoreName%22:%22' + store_cookie + '%22}'    
    }

    response = requests.request("GET", "https://www.publix.com/pd/" + str(product_id), headers=headers, data={})
    
    # check status code
    if response.status_code != 200:
        raise ValueError('excepted 200 status for grabbing product page, was given ' + str(response.status_code) + ' for product id: ' + product_id)

    # prepare regex
    regex = r":&amp;quot;Valid Through [\w\s]+"

    # range over the match groups
    for matchNum, match in enumerate(re.finditer(r":&amp;quot;Valid Through [\w\s]+", response.text, re.MULTILINE), start=0):
        return match.group()


def parse_publix_deli_page(zipCode):

    try:
        closest_publix = find_closest_publix(zipCode) 
        print("Store found: " + closest_publix[1]) # debug
    except:
        print("an unexpected exception occured grabbing the closest publix at: " + zipCode)

    response = requests.request("GET", "https://services.publix.com/api/v3/product/SearchMultiCategory?" +
    "storeNumber=" + closest_publix[0] + "&sort=popularityrank+asc,+titlecopy+asc&rowCount=60&orderAheadOnly=true&facet=onsalemsg::On+Sale&categoryIdList=d3a5f2da-3002-4c6d-949c-db5304577efb", data="", headers={}, params={})

    if response.status_code != 200:
        raise ValueError('excepted 200 status for grabbing on sale page, was given ' + str(response.status_code))

    sub_dict = []    
    # find product valid thru date
    for product in response.json()[0]:
        if "Sub" in product["title"]: # find subs only
            temp_dict = []

            try:
                end_date = grab_end_date(product["Productid"], closest_publix)
            except:
                print("an unexpected exception occured grabbing the end date of sub: " + product["title"])


            temp_dict.append(product["title"])      
            temp_dict.append(str(product["savingmsg"]))
            temp_image_holder = str(product["productimages"]).split("-")
            temp_dict.append(temp_image_holder[0] + "-600x600-" + temp_image_holder[2])
            try:
                temp_dict.append(str(end_date).split("&amp;quot;Valid Through")[1].strip())
            except:
                print("an unexpected exception occured appending the valid through (end date) to: " + product["title"])


            sub_dict.append(temp_dict)

    return sub_dict


def shave_zeros(raw_store):
    store_id = ""
    for char in raw_store:
        # if there is a trailing zero in the store_id, don't include it
        if char != "0":
            store_id += str(char)

    return store_id

def store_to_cookie(store):
    return str(store).replace(" ", "%20")

if __name__ == "__main__":
    scrape_publix_job()
