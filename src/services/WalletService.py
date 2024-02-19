from web3 import Web3
from web3.exceptions import ContractLogicError
from typing import Dict
from ..utils.ABI import ABI
from ..utils.KeyFactor import KeyFactory
import requests
import json
import datetime

class WalletService:

    # Class constructor
    def __init__(self, web3: Web3, contractAddress: str, apiKey: str) -> None:
        self.__web3 = web3
        self.__contractAddress = contractAddress
        self.__apiKey = apiKey

    # Checking balance
    def getBalance(self, address: str) -> Dict:
        contract = self.__web3.eth.contract(address=self.__contractAddress, abi=ABI.ERC20Balance())

        result = {'walletBalanceWORK': {}}
        try:
            balance_wei = contract.functions.balanceOf(address).call()
            balance_ether = Web3.from_wei(balance_wei, 'ether')
            balance_hex = hex(balance_wei)

            result['walletBalanceWORK'] = {
                'WEI': str(balance_wei),
                'Ether': str(balance_ether),
                'Hex': balance_hex
            }

        except ContractLogicError as e:
            result['walletBalanceWORK']['error'] = str(e)

        except Exception as e:
            # General exceptions (e.g., connection issues, wrong ABI)
            result['walletBalanceWORK']['error'] = str(e)

        return result
    
    # Get information about wallet
    def getInformation(self, address: str) -> Dict:

        info = {'nonce': {}}

        try:
            nonce = self.__web3.eth.get_transaction_count(address)
            info['nonce'] = str(nonce)

            # TODO: more informations about the walllet


        except ContractLogicError as e:
            info['nonce']['error'] = str(e)
        except Exception as e:

            # General exceptions (e.g., connection issues, wrong ABI)
            info['walletBalanceWORK']['error'] = str(e)

        return info


    # Create new wallet
    def createWallet(self, words: int) -> Dict:

        result = {}

        seedphrase = KeyFactory.generate_seed_phrase(words)
        result['seedphrase'] = seedphrase['words']

        keys = KeyFactory.generate_keys_from_seed_phrase(seedphrase['entropy'])
        result['privateKey'] = keys['privateKey']
        result['publicKey'] = keys['publicKey']
        # result['publicKeyCompressed'] = keys['publicKeyCompressed']  // Check if there's method for compressing keys
        result['address'] = KeyFactory.generate_address_from_public_key(keys['publicKey'])

        return result
    

    # Get transaction history from given address
    def getHistory(self, address: str) -> Dict:

        history = {}

        # Check whether apiKey was provided
        if not self.__apiKey:
            history['error'] = "Empty API key, please set WORKEN_POLYGONSCAN_APIKEY in your environment variables. You can get it from https://polygonscan.com/apis"
            
        url = (
            f"https://api.polygonscan.com/api"
            f"?module=account"
            f"&action=txlist"
            f"&address={address}"
            f"&startblock=0"
            f"&endblock=99999999"
            f"&sort=asc"
            f"&apikey={self.__apiKey}"
        )

        response = requests.get(url)
        # Check if the response is not empty
        if response.status_code != 200:
            history['error'] = "Error while fetching data from Polygonscan."

        result = json.loads(response.text)

        if result['status'] == '0':
            if result['message'] == 'No transactions found':
                return history
            
            result['error'] = result['message']

        # Check if formated as expected
        history["result"] = []
        for transaction in result['result']:
                timestamp = datetime.datetime.fromtimestamp(int(transaction['timeStamp']))
                history["result"].append({
                    'blockNumber': transaction['blockNumber'],
                    'timeStamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    'hash': transaction['hash'],
                    'nonce': transaction['nonce'],
                    'blockHash': transaction['blockHash'],
                    'transactionIndex': transaction['transactionIndex'],
                    'from': transaction['from'],
                    'to': transaction['to'],
                    'value': transaction['value'],
                    'gas': transaction['gas'],
                    'gasPrice': transaction['gasPrice'],
                    'isError': transaction['isError'],
                    'txreceipt_status': transaction['txreceipt_status'],
                })


        return history

        

        