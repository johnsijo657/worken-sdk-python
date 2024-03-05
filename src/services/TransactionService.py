from web3 import Web3
from web3.contract import Contract
from ..services.WalletService import WalletService
from ..services.NetworkService import NetworkService
from ..utils.ABI import ABI

class TransactionService:
    def __init__(self, web3: Web3, wallet_service: WalletService, network_service: NetworkService, contract_address: str, api_key: str):
        self.web3 = web3
        self.contract_address = contract_address
        self.wallet_service = wallet_service
        self.network_service = network_service
        self.contract = self.web3.eth.contract(address=contract_address, abi=ABI.ERC20Balance())
        self.api_key = api_key
    
    '''
     * Send transaction
     * 
     * @param string $privateKey Sender private key
     * @param string $from Sender address in Hex
     * @param string $to Receiver address in Hex
     * @param string $amount Amount to send in WEI
     * @return array
    '''
    def send_transaction(self, private_key: str, _from: str, _to: str, amount: str):
        status = {}
        data = '0x' + self.contract.encodeABI(fn_name='transfer', args=[_to, amount])

        wallet_info = self.wallet_service.getInformation(_from)
        if 'error' in wallet_info.get('nonce', {}):
            return wallet_info['nonce']
        else:
            nonce = wallet_info['nonce'] + 1
            nonce = self.web3.to_hex(nonce)

        gas = self.network_service.getEstimatedGas(_from, _to, amount)
        if 'error' in gas:
            return gas
        else:
            gas = gas['Hex']

        gas_price = self.network_service.get_monitor_congestion()
        if 'error' in gas_price:
            return gas_price
        else:
            gas_price = str(round(gas_price['Safe']))

        transaction = {
            'nonce': nonce,
            'gasPrice': self.web3.to_wei(gas_price, 'gwei'),
            'gas': gas,
            'to': self.contract_address,
            'value': 0,
            'data': data,
            'chainId': 80001    #80001 testnet, 137 mainnet
        }

        signed_transaction = self.web3.eth.account.sign_transaction(transaction, private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_transaction)
        status['txHash'] = tx_hash.hex()
        return status
    
    '''
     * Get transaction status
     * 
     * @param string $txHash Transaction hash
     * @return int 0 - success, 1 - fail, 2 - pending or not found
     '''
    def getTransactionStatus(self, tx_hash: str):
        status = ""
        receipt = self.web3.eth.get_transaction_receipt(tx_hash)
        if receipt is None:
            status = 2          #pending or not found
        else:
            if receipt['status'] == 1:
                status = 0      #success
            else:
                status = 1      #fail
        return status