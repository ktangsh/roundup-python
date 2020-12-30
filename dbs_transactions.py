import base64 as b64encode
import uuid
import requests
import json

client_info = "c5444f5f-3faf-4fb9-a744-e6d7fd9ee5d3:xF3vR3rX7cC7gY5eS3pU5lH2nE6aB0eD5jK2tP8gQ3lJ4rJ1wO"
redirect_link = "https%3A%2F%2Fwww.dbs.com%2Fdevelopers%2F%23%2Fall-products%2Fplay-ground"

# dbs app constants
dbs_client_id = "e9218b31-b089-4e01-ace6-09094460fbe7"
dbs_client_secret = "4a90d99c-f358-4fb0-8181-21400b23e386"
authorization_code = "%2FeVAwlSE9L55USDok6DDudfFRcc%3D"


class DBSCustomerDetails:

    def get_access_token(self):
        url = "https://www.dbs.com/sandbox/api/sg/v1/oauth/tokens"

        user_and_pass = b64encode.b64encode(
            b"e9218b31-b089-4e01-ace6-09094460fbe7:4a90d99c-f358-4fb0-8181-21400b23e386").decode("ascii")

        payload = "code=" + authorization_code + "&grant_type=authorization_code&redirect_uri=" + redirect_link

        headers = {
            'authorization': 'Basic %s' % user_and_pass,
            'content-type': "application/x-www-form-urlencoded",
            'uuid': str(uuid.uuid4()),
            'accept': "application/json",
            'cache-control': "no-cache"
        }

        # conn.request("POST", "/sandbox/api/sg/v1/oauth/tokens", payload, headers=headers)
        res = requests.request("POST", url, data=payload, headers=headers)
        print("Status code: ", res.status_code)
        res.close()

        json_data = json.loads(res.text)
        return json_data


    def get_card_summary(self, partyId, accessToken):
        url = "https://www.dbs.com/sandbox/api/sg/v1/parties/" + partyId + "/cards"

        # user_and_pass = b64encode.b64encode(
        #     b"e9218b31-b089-4e01-ace6-09094460fbe7:4a90d99c-f358-4fb0-8181-21400b23e386").decode("ascii")

        headers = {
            'clientId': dbs_client_id,
            'accessToken': accessToken,
            'uuid': str(uuid.uuid4())
            # 'accept': "application/json"
        }

        # conn.request("POST", "/sandbox/api/sg/v1/oauth/tokens", payload, headers=headers)
        res = requests.request("GET", url, headers=headers)
        print("Status code: ", res.status_code)
        res.close()

        json_data = json.loads(res.text)
        print(json_data)


    def get_card_details(self, cardId, accessToken):
        url = "https://www.dbs.com/sandbox/api/sg/v1/cards/" + cardId

        headers = {
            'clientId': dbs_client_id,
            'accessToken': accessToken,
            'uuid': str(uuid.uuid4())
            # 'accept': "application/json"
        }

        res = requests.request("GET", url, headers=headers)
        print("Status code: ", res.status_code)
        res.close()

        json_data = json.loads(res.text)
        print(json_data)