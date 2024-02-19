from mnemonic import Mnemonic
from eth_keys import keys
from eth_utils import to_checksum_address, keccak
from eth_account import Account
import bip32utils
from typing import Dict, List

class KeyFactory:
    
    @staticmethod
    def generate_seed_phrase(words: int) -> Dict:
        if words not in [12, 15, 18, 21, 24]:
            raise ValueError("Invalid number of words for a mnemonic. Allowed values are 12, 15, 18, 21, 24.")
        
        mnemo = Mnemonic("english")
        # Adjusted to directly use the generate method without entropy length calculation
        strength = {12: 128, 15: 160, 18: 192, 21: 224, 24: 256}[words]
        mnemonic_words = mnemo.generate(strength=strength)
        
        response = {
            'words': mnemonic_words.split(),                    # Words in array
            "wordsString": mnemonic_words,                      # Words in string
            "entropy": mnemo.to_entropy(mnemonic_words).hex()   # Entropy of mnemonic, ready for generating private key
        }    
        
        return response
    
    @staticmethod
    def generate_keys_from_seed_phrase(mnemonic_words: List[str]) -> Dict:
        mnemo = Mnemonic("english")
        seed = mnemo.to_seed(mnemonic_words, passphrase="")
        
        BIP44_PATH = "m/44'/60'/0'/0/0"  # BIP44: Ethereum
        bip32_root_key_obj = bip32utils.BIP32Key.fromEntropy(seed)
        bip32_root_key_obj = bip32_root_key_obj.ChildKey(
            44 + bip32utils.BIP32_HARDEN                        # purpose 
        ).ChildKey(
            60 + bip32utils.BIP32_HARDEN                        # coin_type: Etherum
        ).ChildKey(
            0 + bip32utils.BIP32_HARDEN                         # account
        ).ChildKey(
            0                                                   # change
        ).ChildKey(
            0                                                   # address_index
        )
        
        private_key_hex = bip32_root_key_obj.PrivateKey().hex()
        account = Account.from_key(private_key_hex)
        
        response = {
            'privateKey': private_key_hex,
            'publicKey': account._key_obj.public_key.to_hex(),
            # There's no direct method to get compressed public key in eth_account or eth_keys,
            # usually not needed for Ethereum transactions. -> to be checked tho
        }
        
        return response
    
    @staticmethod
    def generate_address_from_public_key(public_key: str) -> str:
        
        if public_key.startswith('0x'):
            public_key = public_key[2:]
        
        # Convert hex to bytes
        public_key_bytes = bytes.fromhex(public_key[2:])
        
        # Compute Keccak-256 of the public key         
        public_key_hash = keccak(public_key_bytes)
        
        # Take the rigth most 20 bytes (40 characters in hex) for the address
        address = to_checksum_address(public_key_hash[-20:])
        return address

# Example usage:
# seed_phrase_info = KeyFactory.generate_seed_phrase(12)
# print(seed_phrase_info)
# print()

# keys_info = KeyFactory.generate_keys_from_seed_phrase(seed_phrase_info['wordsString'])
# print(keys_info)
# print()

# address = KeyFactory.generate_address_from_public_key(keys_info['publicKey'])
# print(address)
# print()