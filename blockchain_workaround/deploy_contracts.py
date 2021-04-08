import json
from web3 import Web3
import json

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545",request_kwargs={'timeout':60}))

abi_file = open("stringUtils_sol_StringUtils.abi")
abi_list = json.loads((abi_file.read()))
abi_file.close()

bin_file = open("stringUtils_sol_StringUtils.bin","r")
bin_content = bin_file.read()
bin_file.close()

contract = w3.eth.contract(
        abi=abi_list,
        bytecode=bin_content
    )
# Get transaction hash from deployed contract
# tx_hash =contract.deploy(transaction={'from':w3.eth.accounts[1]})
# Get tx receipt to get contract address

tx_hash = contract.constructor().transact({"from":w3.eth.accounts[1]})

tx_receipt = w3.eth.getTransactionReceipt(tx_hash)

print (tx_receipt)
