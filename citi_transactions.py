import http.client
import uuid
import base64 as b64encode

client_id = "c5444f5f-3faf-4fb9-a744-e6d7fd9ee5d3"
client_secret = "xF3vR3rX7cC7gY5eS3pU5lH2nE6aB0eD5jK2tP8gQ3lJ4rJ1wO"
ACCEPT_JSON = "application/json"
ngrok_link = "https://bebe047a2d13.ngrok.io"

conn = http.client.HTTPSConnection("sandbox.apihub.citi.com")
access_token = "AAIkYzU0NDRmNWYtM2ZhZi00ZmI5LWE3NDQtZTZkN2ZkOWVlNWQzj-9vIJ2x0PDOieygxzw1XKCRrcQKNKKzSp4ANTJiZBwrwcitApO2c5ywYzxxA7pFc4JTQXRsl2QHOrjbxBnBwRWnSZx1RGdzhK0HdJu7Xf4MP3UBYI8N7rv_EDE7CrhIENuxFCdKirhjZ-35cQ8hI9jWycKK7jccP_YRRNhSUvHd4vGdLqCA3vf87OLSx0NEcb7936Ge07PjM1tc7py_dQCULVpKQHvC461MGFMMvjgteDgKbWwF0QF2gRYYUMVyUbrl9wx382nK0Q4boOk9euD3-Xc-6issXuh0L6RYeXAw8Eyx_rYNswMjBwq7Va7eIN1jpRLDXImd86RahlZ0_w"
authorization_code = "AALzUHDzBTgDaJiNAkCyPAgc6eAbZm9kCh3TvLDoec8T5KlQoztBupFuDdkFNBrKcGH9wpTa7fAfnNsFiv5ycztnzIL2VgvzP6wez6wnC5sUUjA_QfqwtzonMagg_C3rsrOQncMQYlzHdd0RfP2jwqBl9HZJFUOoaBjX6gDlTby8pIqm_SlI2xlUZVEynApJSnUomNF9vrVcijw-Qv5bVxaVWkzHkjbxEKNE6AOo5VBvboarfdycFy2wNZy6r5b206orEG-wbgEBSVEOZfd0P53r"


# Link to retrieve authorisation token
# https://sandbox.apihub.citi.com/gcb/api/authCode/oauth2/authorize?response_type=code&client_id=c5444f5f-3faf-4fb9-a744-e6d7fd9ee5d3&scope=accounts_statements&countryCode=SG&businessCode=GCB&locale=en_SG&state=12093&redirect_uri=https://bebe047a2d13.ngrok.io

class CitiCustomerDetails:

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
