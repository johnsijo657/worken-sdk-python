from src.Worken import Worken


test = Worken()
wallet_address = "0xf68A2B061c1aFC3ed07FafF33c53978F80F54099"

wallet = test.wallet
service = test.network
print(wallet.getBalance(wallet_address))
print(wallet.getInformation(wallet_address))
print(service.getBlockInformation(45652747))

