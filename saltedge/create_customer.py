# Sample Request
import json

import requests

APP_ID = "RGJD8nhaIhilQVr1EaTq_FskhlaSHsBGwFgszTaDm4c"
SECRET = "oW1UAXHebuHYxFjhs7KVinC161fdR3e6ccmGgWgcWco"


def create_customer(customer_name):
    url = "https://www.saltedge.com/api/v5/customers"

    payload = \
        "{ \
          \"data\": { \
            \"identifier\": " + "\"" + customer_name + "\"\
          } \
        }"

    headers = {
        'App-id': APP_ID,
        'Secret': SECRET,
        'content-type': "application/json",
        'accept': "application/json"
    }

    res = requests.request("POST", url, data=payload, headers=headers)
    print("Status code: ", res.status_code)
    res.close()

    json_data = json.loads(res.text)
    return json_data


# sample response: {'data': {'id': '445802333939435523', 'identifier': 'Vivien3', 'secret':
# 'p9DkEDFbcFn4ugKgNYRBQXCGUJ0T_agAMOzw2il2Mak'}}
def extract_customer_id(customer_info):
    customer_id = customer_info['data']['id']
    return customer_id


# When creating a connection
# you should check whether the customer already exists to avoid creating new customers with the same connection.
def check_customer(customer_id):
    url = "https://www.saltedge.com/api/v5/customers/" + customer_id

    headers = {
        'App-id': APP_ID,
        'Secret': SECRET,
        'content-type': "application/json",
        'accept': "application/json"
    }

    res = requests.request("GET", url, headers=headers)
    print("Status code: ", res.status_code)
    res.close()

    json_data = json.loads(res.text)
    print(json_data)


customer_info = create_customer("Son")
print(customer_info)
customer_id = extract_customer_id(customer_info)
print(customer_id)
