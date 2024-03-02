from decimal import Decimal

class Converter:
    def convert_wei_to_ether(Wei):
        return Decimal(Wei) / 10 ** 18