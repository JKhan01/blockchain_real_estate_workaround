import json
from web3 import Web3
import json

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545",request_kwargs={'timeout':60}))

abi_file = open("_transfer_test_sol_transferMoney.abi")
abi_list = json.loads((abi_file.read()))
abi_file.close()

bin_file = open("_transfer_test_sol_transferMoney.bin","r")
bin_content = bin_file.read()
bin_file.close()

contracts_info = []
contract = w3.eth.contract(
        abi=abi_list,
        bytecode=bin_content
    )

for i in range(1,10):
    tx_hash = contract.constructor().transact({"from":w3.eth.accounts[i]})

    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)

    print (tx_receipt)
    receipt = {"abi": abi_list, "contract_address": tx_receipt["contractAddress"]}
    contracts_info.append(receipt)

with open("transfer_transaction_receipt.json","w") as tx_file:
    # receipt = {"abi": abi_list, "contract_address": tx_receipt["contractAddress"]}
    json.dump(contracts_info, tx_file, indent=4) 