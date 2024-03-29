from roundup.archive.banks.dbs_transactions import DBSCustomerDetails

if __name__ == '__main__':
    dbs_customer = DBSCustomerDetails()
    json_data = dbs_customer.get_access_token()
    print(json_data)

    access_token = ''
    party_id = ''
    if 'access_token' in json_data:
       access_token = json_data['access_token']

    if 'party_id' in json_data:
        party_id = json_data['party_id']

    print("access_token: ", access_token)
    print("party_id: ", party_id)

    # card_id = "04210926930000"  # from test persona
    # dbs_customer.get_card_details(card_id, access_token)
    dbs_customer.get_card_summary(party_id, access_token)

    # citi_customer = CitiCustomerDetails()
    # json_data = citi_customer.get_access_token()
    # print(json_data)
