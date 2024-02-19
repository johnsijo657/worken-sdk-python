from typing import Dict

class ABI:
    
    @staticmethod
    def ERC20Balance() -> Dict:
        return [
            {
              "constant": True,
              "inputs": [{"name": "_owner", "type": "address"}],
              "name": "balanceOf",
              "outputs": [{"name": "balance", "type": "uint256"}],
              "type": "function"
            }
          ]