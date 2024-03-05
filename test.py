from src.Worken import Worken


test = Worken()
wallet_address = "0xf68A2B061c1aFC3ed07FafF33c53978F80F54099"

#testing network and service
wallet = test.wallet
service = test.network
print(wallet.getBalance(wallet_address))
print(wallet.getInformation(wallet_address))
print(service.getBlockInformation(45652747))

#testing contract function
contract = test.contract
print(contract.get_contract_status())
print(contract.get_contract_function())

#testing transaction function
transaction = test.transaction
print(transaction.getTransactionStatus("0x2446f1fd773fbb9f080e674b60c6a033c7ed7427b8b9413cf28a2a4a6da9b56c"))
print(transaction.send_transaction(0x02b4632d08485ff1df2db55b9dafd23347d1c47a,0x123456789abcdef,0xabcdef123456789,1000000000000000000))
