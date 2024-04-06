from src.Worken import Worken

test = Worken()
wallet_address = "0xf68A2B061c1aFC3ed07FafF33c53978F80F54099"

# Testing network and service
wallet = test.wallet
service = test.network

# Verify the balance of the wallet address
balance = wallet.getBalance(wallet_address)
if balance is not None:
    print("Wallet balance:", balance)
else:
    print("Failed to retrieve wallet balance.")

# Get information about the wallet address
wallet_info = wallet.getInformation(wallet_address)
if wallet_info is not None:
    print("Wallet information:", wallet_info)
else:
    print("Failed to retrieve wallet information.")

# Get information about a specific block
block_info = service.getBlockInformation(45652747)
if block_info is not None:
    print("Block information:", block_info)
else:
    print("Failed to retrieve block information.")

# Testing contract function
contract = test.contract
contract_status = contract.get_contract_status()
contract_function = contract.get_contract_function()

if contract_status is not None:
    print("Contract status:", contract_status)
else:
    print("Failed to retrieve contract status.")

if contract_function is not None:
    print("Contract function:", contract_function)
else:
    print("Failed to retrieve contract function.")

# Testing transaction function
transaction = test.transaction

# Get transaction status
transaction_id = "0x2446f1fd773fbb9f080e674b60c6a033c7ed7427b8b9413cf28a2a4a6da9b56c"
transaction_status = transaction.getTransactionStatus(transaction_id)
if transaction_status is not None:
    print("Transaction status:", transaction_status)
else:
    print("Failed to retrieve transaction status.")

# Send transaction
# Corrected hexadecimal values by enclosing them in quotes
sender_address = "0x02b4632d08485ff1df2db55b9dafd23347d1c47a"
recipient_address = "0x123456789abcdef"
amount = 1000000000000000000

# Ensure proper error handling for transactions
try:
    result = transaction.send_transaction(sender_address, recipient_address, amount)
    print("Transaction sent successfully. Transaction hash:", result)
except Exception as e:
    print("Failed to send transaction:", e)
