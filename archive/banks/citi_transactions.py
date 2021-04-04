import http.client
import uuid
import base64 as b64encode
import json

client_id = "c5444f5f-3faf-4fb9-a744-e6d7fd9ee5d3"
client_secret = "xF3vR3rX7cC7gY5eS3pU5lH2nE6aB0eD5jK2tP8gQ3lJ4rJ1wO"
ACCEPT_JSON = "application/json"
ngrok_link = "https://bebe047a2d13.ngrok.io"
authorization_code = "AALmgn_dc5cAzfpLCoT_R8D3XSufBdaL9smfgeDQthANwygZ231bARotQNN4aEjhMg1Dh_0K-oTfhpNnZBHofJZSyxWPXCFxDv2xhV6no0QpWsOXbR9LzzkrltLs0MBAFacls3pwkBaZJ9pBhOlIooH9daFClyglOz4J41N3szvk0jHy068SFfDF0kakpcdQvqEoiauYUd05B_Yi4fJ1upbabckwYSXPu9TSfJid0Dm48EAfh651Ea8sAYTkq9iU-hB7PMIK80i2L7m2AeYy0GIT"

conn = http.client.HTTPSConnection("sandbox.apihub.citi.com")


# Link to retrieve authorisation token
# https://sandbox.apihub.citi.com/gcb/api/authCode/oauth2/authorize?response_type=code&client_id=c5444f5f-3faf-4fb9-a744-e6d7fd9ee5d3&scope=accounts_statements&countryCode=SG&businessCode=GCB&locale=en_SG&state=12093&redirect_uri=https://bebe047a2d13.ngrok.io

class CitiCustomerDetails:

    def get_access_token(self):
        user_and_pass = b64encode.b64encode(
            b"c5444f5f-3faf-4fb9-a744-e6d7fd9ee5d3:xF3vR3rX7cC7gY5eS3pU5lH2nE6aB0eD5jK2tP8gQ3lJ4rJ1wO").decode("ascii")

        payload = "grant_type=authorization_code&code=" + authorization_code + "&redirect_uri=" + ngrok_link

        headers = {
            'authorization': 'Basic %s' % user_and_pass,
            'content-type': "application/x-www-form-urlencoded",
            'accept': "application/json"
        }

        conn.request("POST", "/gcb/api/authCode/oauth2/token/us/gcb", payload, headers)

        res = conn.getresponse()
        data = res.read()

        print(res.status, res.reason)
        print(data.decode("utf-8"))
        conn.close()

        json_data = json.loads(data)
        return json_data

    def get_account_summary(self):
        headers = {
            'authorization': "Bearer %s" % access_token,
            'uuid': str(uuid.uuid4()),
            'client_id': client_id,
            'accept': ACCEPT_JSON
        }

        conn.request("GET", "/gcb/api/v1/accounts", headers=headers)

        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
        conn.close()



    def refresh_access_token(self):
        user_and_pass = b64encode.b64encode(
            b"c5444f5f-3faf-4fb9-a744-e6d7fd9ee5d3:xF3vR3rX7cC7gY5eS3pU5lH2nE6aB0eD5jK2tP8gQ3lJ4rJ1wO").decode("ascii")

        payload = "grant_type=refresh_token&refresh_token=AAIUooL9t95qQrTNATThTU5xjgdsmPE6SJTeWelO8rSV7mt-IU830m4bY0JDS3tqrCODd7t2Bs5Onwo9KGFxkkSX8OD4p__I88D5tm6XtL6prSe7NPTI401k75emtU6A-0HmbcHYlv4PS4uNRUoCW8s0fO26GMGeVx3dDCMYOElq73BamCWxCYWHyQG5MErtCVE6m-NcrCaDcFwTBTqtdUEowl-oc9qy4-YzUj2yAHbnTL5BaTUR26QEVMUANXNcK1tXQ5HC8KgGuZf3uoII-jE4OZ5XF-gJidw3I1QJ4hWjEEAHo0o_06dmVDvkx1oLLDo1xZftJjz9a_2ySnkVRpsgMd0lvqoPuWVF3FwGkyXJIw"

        headers = {
            'authorization': 'Basic %s' % user_and_pass,
            'content-type': "application/x-www-form-urlencoded",
            'accept': ACCEPT_JSON
        }

        conn.request("POST", "/gcb/api/authCode/oauth2/refresh", payload, headers)

        res = conn.getresponse()
        data = res.read()
        print(res.status, res.reason)
        print(data.decode("utf-8"))
