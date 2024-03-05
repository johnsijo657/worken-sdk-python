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
            if 'result' in data and len(data['result']) > 0:
                code = data['result'][0].get('bytecode')
                if code and code != '0x':
                    result['status'] = True
                else:
                    result['status'] = False
            else:
                result['error'] = "No contract information found in the response."
        else:
            result['error'] = "Status is not 1."
        
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