from web3 import Web3
from typing import Dict
import requests
import json
from ..utils.ABI import ABI


class NetworkService:
    
    # Class constructor
    def __init__(self, web3: Web3, contractAddress: str, apiKey: str) -> None:
        self.__web3 = web3
        self.__contractAddress = contractAddress
        self.__apiKey = apiKey
        self.__contract = self.__web3.eth.contract(address=self.__contractAddress, abi=ABI.ERC20Balance())


    def getBlockInformation(self, blockNumber: int) -> Dict:

        url = (
            f"https://api.polygonscan.com/api"
            f"?module=account"
            f"&action=tokentx"
            f"&contractaddress={self.__contractAddress}"
            f"&startblock={blockNumber}"
            f"&endblock={blockNumber}"
            f"&sort=asc"
            f"&apikey={self.__apiKey}"  
        )

        response = requests.get(url)
        result = json.loads(response.text)
        if response.status_code != 200:
            result['error'] = "Error while fetching data from Polygonscan."
        else:
            if result['status'] == '1' and result['message'] == 'OK':
                return int(result['result'])
            else:
                result['error'] = result['message']
                
        return result
        
        
    def getEstimatedGas(self, from_address: str, to_address: str, amount: str) -> Dict:
        
        amountInWei = Web3.to_wei(amount, 'ether')
        data = self.__contract.encodeABI(fn_name='transfer', args=[to_address, amountInWei])
    
        transaction = {
            'from': from_address,
            'to': self.__contractAddress,
            'data': data
        }

        try:
            estimated_gas = self.__web3.eth.estimateGas(transaction)

        except Exception as e:
            result = {'error': str(e)}

        if 'error' in result:
            return result
    
        result = {
            'estimateGas': {
                'WEI': str(estimated_gas),
                'Ether': self.__web3.fromWei(estimated_gas, 'ether'),
                'Hex': hex(estimated_gas)
            }
        }
        return result
    
    def getNetworkStatus(self) -> Dict:
        latest_block = self.__web3.eth.block_number
        hashrate = self.__web3.eth.hashrate
        gas_price = self.__web3.eth.gas_rice
        syncing = self.__web3.eth.syncing
        
        status = {
            'latestBlock': latest_block,
            'hashrate': str(hashrate),
            'gasPrice': {
                'WEI': str(gas_price),
                'Ether': self.__web3.fromWei(gas_price, 'ether'),
                'Hex': hex(gas_price)
            },
            'syncStatus': syncing
        }
        return status
    
    def monitorCongension(self) -> Dict:
        gasOracleUrl = "https://api.polygonscan.com/api?module=gastracker&action=gasoracle&apikey={self.__apiKey}";
        response = requests.get(gasOracleUrl)
        gasData = response.json()

        status = {}
        
        if response.status_code != 200:
            status['GasPrice']['error'] = "Error while fetching data from Polygonscan."
        else:
            if gasData['status'] == '1' and 'result' in gasData:
                status['GasPrice'] = {
                    'Safe': float(gasData['result']['SafeGasPrice']),
                    'Propose': float(gasData['result']['ProposeGasPrice']),
                    'Fast': float(gasData['result']['FastGasPrice'])
                }
            else: 
                status['GasPrice']['error']  = 'Could nto retrieve gas price data'

        return status
        
        
 
# from_address = "0xf68A2B061c1aFC3ed07FafF33c53978F80F54099"
# to_address = '0xYourToAddressHere'
# amount = '0.01'  # Ether
# estimated_gas = NetworkService.getEstimatedGas(from_address, to_address, amount)
# print("Estimated Gas:", estimated_gas)       
        