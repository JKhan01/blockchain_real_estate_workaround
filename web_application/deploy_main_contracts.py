import json
from web3 import Web3
import json

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545",request_kwargs={'timeout':60}))

abi_file = open("_registration_test_sol_userRecords.abi")
abi_list = json.loads((abi_file.read()))
abi_file.close()

bin_file = open("_registration_test_sol_userRecords.bin","r")
bin_content = bin_file.read()
bin_file.close()

contract = w3.eth.contract(
        abi=abi_list,
        bytecode=bin_content
    )

tx_hash = contract.constructor().transact({"from":w3.eth.accounts[0]})

tx_receipt = w3.eth.getTransactionReceipt(tx_hash)

print (tx_receipt)



with open("main_transaction_receipt.json","w") as tx_file:
    receipt = {"abi": abi_list, "contract_address": tx_receipt["contractAddress"]}
    json.dump(receipt, tx_file, indent=4)