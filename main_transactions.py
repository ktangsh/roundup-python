from roundup.main_roundup_transactions import MainTransactions
from roundup.other_roundup_transactions import OtherTransactions

if __name__ == '__main__':

    txn_type = input("\nKey in type of transactions to view: Main/Other\n")

    if txn_type.upper() == "MAIN":
        mainTxn = MainTransactions()
        mainTxn.get_main_transactions()
    elif txn_type.upper() == "OTHER":
        otherTxn = OtherTransactions()
        otherTxn.get_other_transactions()
    else:
        print("Please try again. Key in Main or Other to view ")
