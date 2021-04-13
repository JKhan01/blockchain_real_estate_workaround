from web3 import Web3

w = Web3(Web3.HTTPProvider("http://localhost:8545"))
amount_in_wei = w.toWei(0.02,'ether')
nonce = w.eth.getTransactionCount(w.eth.accounts[1])
txn_dict = {"to":w.eth.accounts[5],"value":amount_in_wei,"gas":2000000,"gasPrice":w.toWei("20","gwei"),"nonce":nonce}
## signed txn parameters: transaction dictionary, sender accounts private key
signed_txn = w.eth.account.signTransaction(txn_dict, 'ca69de7c36171c41a87e5c6392d3367603bde9cf145ce4b8815ddb4289ddf8a8')
txn_hash = w.eth.sendRawTransaction(signed_txn.rawTransaction)
txn_receipt = w.eth.getTransactionReceipt(txn_hash)