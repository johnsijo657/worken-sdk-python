
from .services.WalletService import WalletService
from .services.NetworkService import NetworkService
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
        
        self.wallet = WalletService(self.__web3, self.__contractAddress, self.__apiKey)
        self.network = NetworkService(self.__web3, self.__contractAddress, self.__apiKey)