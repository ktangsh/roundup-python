import http.client
import base64 as b64encode

# citi app constants
client_info = "c5444f5f-3faf-4fb9-a744-e6d7fd9ee5d3:xF3vR3rX7cC7gY5eS3pU5lH2nE6aB0eD5jK2tP8gQ3lJ4rJ1wO"
ngrok_link = "https://2b6d23cf35f1.ngrok.io"

# dbs app constants
dbs_client_id = "e9218b31-b089-4e01-ace6-09094460fbe7"
dbs_client_secret = "4a90d99c-f358-4fb0-8181-21400b23e386"

def dbs_get_authorisation_code():
    conn = http.client.HTTPSConnection("dbs.com")
    headers = {'accept': "application/json"}

    conn.request("GET",
                 "/sandbox/api/sg/v1/oauth/authorize?client_id=" + dbs_client_id +
                 "&scope=Read"
                 "&response_type=code"
                 "&redirect_uri=" + ngrok_link +
                 "&state=123"
                 "&login_page=IBCustomer.DBS",
                 headers=headers)

    res = conn.getresponse()
    print(res.status, res.reason)
    data = res.read()

    print(data.decode("utf-8"))

def dbs_get_access_token():
    conn = http.client.HTTPSConnection("dbs.com")

    payload = "code=2Rdu8eTKCL6W9kbjXrFbgFAG2JU%3D&redirect_uri=" + ngrok_link + "&grant_type=code"

    userAndPass = b64encode.b64encode(b"e9218b31-b089-4e01-ace6-09094460fbe7:4a90d99c-f358-4fb0-8181-21400b23e386").decode("ascii")
    print(userAndPass)

    headers = {
        'authorization': 'Basic %s' % userAndPass,
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache"
    }

    conn.request("POST", "/sandbox/api/sg/v1/oauth/tokens", payload, headers)
    res = conn.getresponse()
    data = res.read()

    print(res.status, res.reason)
    print(data.decode("utf-8"))



def citi_get_authorisation_code():
    conn = http.client.HTTPSConnection("sandbox.apihub.citi.com")
    #
    headers = {'accept': "application/json"}

    conn.request("GET",
                 "/gcb/api/authCode/oauth2/authorize?response_type=code&client_id=c5444f5f-3faf-4fb9-a744-e6d7fd9ee5d3&scope=customers_profiles&countryCode=US&businessCode=GCB&locale=en_US&state=12093&redirect_uri=https://49c786424af9.ngrok.io",
                 headers=headers)

    res = conn.getresponse()
    print(res.status, res.reason)
    data = res.read()

    print(data.decode("utf-8"))


def citi_get_access_token():
    conn = http.client.HTTPSConnection("sandbox.apihub.citi.com")

    userAndPass = b64encode.b64encode(
        b"c5444f5f-3faf-4fb9-a744-e6d7fd9ee5d3:xF3vR3rX7cC7gY5eS3pU5lH2nE6aB0eD5jK2tP8gQ3lJ4rJ1wO").decode("ascii")
    print(userAndPass)

    payload = "grant_type=authorization_code&code=AAJohHlgM42tW7vbH0G4NhkN9L0ZvdbQoj3ePH2-KvVBYsYRYV5xMMUVtEbj3gFhxFudbB1hrLjwN1Fwrivq0apWMJuENnoJgYnq9xEYHhMPxtCalFs86ja9cAi6W-UyFD3_RznrIQPYuGIc9qTCwU6hSToMdODzIgyWNQhvaUwKMHRi3o1CoPL1dx2ZGeHxAKtqv6fyOQoCTt3GuZ2rY64RR2DeBKoNY1dPJa3l0guBfFsXwBaAaRKeDlIaHjUzK_28Qshg2QpNeU3L439kezhb&redirect_uri=" + ngrok_link

    headers = {
        'authorization': 'Basic %s' % userAndPass,
        'content-type': "application/x-www-form-urlencoded",
        'accept': "application/json"
    }

    conn.request("POST", "/gcb/api/authCode/oauth2/token/us/gcb", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(res.status, res.reason)
    print(data.decode("utf-8"))

def citi_retrieve_transactions():
    conn = http.client.HTTPSConnection("sandbox.apihub.citi.com")

    bearer_token = "AAIkYzU0NDRmNWYtM2ZhZi00ZmI5LWE3NDQtZTZkN2ZkOWVlNWQzFGlipPyYuVeqDb-6DOQJpkRt65SRTE3BvZcsYZ6V0svuMci11ImoSwXf3nNE_i_VT9ibktkh43Z2HDmLeivcoZxrmcRSms0SKxivBpwK9Piz7tmMPu589R5YWWmX7oCsztew26bVaxn0Cl7U0xL_t1WnAzWNWAImoKExH0nXLMAfxD0vbGzI-Jyxn55w4FF6tbgsIGIW7CxVDqx8xVzzPJ-IcA94zsRrHxNBs3v8cUYkSaR-GN4uHpze27HWD3vxgtsV8ezoDgzI23-g24xVk8EzYWQVRpk_7WwSXijMrSgB0etwXWnyxHB9-kHHzQqVF2TXMUbDGzGxCcg2azbOtQ"

    headers = {
        'authorization': "Bearer %s" % bearer_token,
        'uuid': "06c23685-2de1-4578-8b64-9c31128727c8",
        'client_id': "c5444f5f-3faf-4fb9-a744-e6d7fd9ee5d3",
        'accept': "application/json"
    }

    conn.request("GET",
                 "/gcb/api/v1/accounts/8035a60debb671e89bd451c9ad0f283e8f1b8868dd4dc65520ceb7bdfeb4142999f574c9db37917ef0edfae296745142543e3ad2bc034887f37212ecbde83ee0/transactions?"
                 "transactionFromDate=2019-01-01"
                 "&transactionToDate=2019-07-30",
                 headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(res.status, res.reason)
    print(data.decode("utf-8"))

def citi_retrieve_account_details():
    conn = http.client.HTTPSConnection("sandbox.apihub.citi.com")

    bearer_token = "AAIkYzU0NDRmNWYtM2ZhZi00ZmI5LWE3NDQtZTZkN2ZkOWVlNWQzLnaLXOv1tRXM-_gicXuBJYbEdZcONUmkszLRwSSe9OSIQDVbzbCblUmLNvCaPii99IuqwlFMcuXYUaVOuKfiipHRzPLrJ6phpYv_HzmhTxh4-2fjQTKOVBA4_ykqVC7Imy9GMQs4RdYogYRhVFnkYokA0uMd9wjrb7Gw6u55yz3AHQxi7JK8Uh2FxZ1LSLSyBIRkuQo2gPPhXtNPunN50Jf9WYEqraI8Htvrw5aDOYJOstaFRCBUCzHP1nmj16g2OxU_4AzDulhnhvTHx-r0RSMOD13bhEI13WlDYHbzFJ_o2wEVoMU5sU67AZzK1h2C8jBNh_rgrT_jGh_wb9th9g"

    headers = {
        'authorization': "Bearer %s" % bearer_token,
        'uuid': "06c23685-2de1-4578-8b64-9c31128727c8",
        'client_id': "c5444f5f-3faf-4fb9-a744-e6d7fd9ee5d3",
        'accept': "application/json"
    }

    conn.request("GET", "/gcb/api/v2/accounts/details", headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(res.status, res.reason)
    print(data.decode("utf-8"))

if __name__ == '__main__':
    # citi_get_access_token()
    citi_retrieve_transactions()
    # citi_retrieve_account_details()

    # dbs_get_authorisation_code()
    # dbs_get_access_token()