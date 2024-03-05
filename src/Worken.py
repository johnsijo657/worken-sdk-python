
from .services.WalletService import WalletService
from .services.NetworkService import NetworkService
from .services.ContractService import ContractService
from .services.TransactionService import TransactionService
from web3 import Web3
from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Worken:

    def __init__(self) -> None:
        self.__contractAddress = "0x3AE0726b5155fCa70dd79C0839B07508Ce7F0F13"
        self.__nodeUrl = "https://rpc-mumbai.maticvigil.com/"
        self.__apiKey = getenv("WORKEN_POLYGONSCAN_APIKEY")
        self.__web3 = Web3(Web3.HTTPProvider(self.__nodeUrl))
        self.__wallet = "0xf68A2B061c1aFC3ed07FafF33c53978F80F54099"
        
        self.wallet = WalletService(self.__web3, self.__contractAddress, self.__apiKey)
        self.network = NetworkService(self.__web3, self.__contractAddress, self.__apiKey)
        self.contract = ContractService(self.__web3, self.__contractAddress, self.__apiKey)
        self.transaction = TransactionService(self.__web3, self.__wallet, self.network, self.__contractAddress, self.__apiKey)
