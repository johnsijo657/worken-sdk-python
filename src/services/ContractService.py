import requests

class ContractService:
    def __init__(self, web3, contractAddress, apiKey):
        self.web3 = web3
        self.contractAddress = contractAddress
        self.apiKey = apiKey

    def get_contract_status(self):
        result = {}
        response = requests.get(f"https://api-testnet.polygonscan.com/api?module=contract&action=getsourcecode&address={self.contractAddress}&apikey={self.apiKey}")
        if response.status_code != 200:
            result['error'] = "Error while fetching data from Polygonscan."
            return result
        
        data = response.json()
        if data['status'] == '1':
            code = data['result'][0]['bytecode']
            if code != '0x':
                result['status'] = True
            else:
                result['status'] = False
        return result
    
    def get_contract_function(self):
        abi = ""
        response = requests.get(f"https://api-testnet.polygonscan.com/api?module=contract&action=getsourcecode&address={self.contractAddress}&apikey={self.apiKey}")
        if response.status_code != 200:
            return "Error while fetching data from Polygonscan."
        
        data = response.json()
        if data['status'] == '1':
            abi = data['result'][0]['ABI']
        return abi