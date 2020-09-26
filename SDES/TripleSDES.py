from SDES.S_DES import S_DES as sdes

class TripleSDES(object):
    def __init__(self, raw_key1, raw_key2):
        '''

        :param raw_key1: First key values
        :param raw_key2: Second key value
        '''
        self.key1=raw_key1
        self.key2=raw_key2

    def encryption(self,plain_text):

        '''
        Operations for create cipher text
        :param plain_text: Original text
        :return: CIpher text
        '''

        part1=sdes(self.key1).generate_cipher(plain_text)
        part2=sdes(self.key2).decyription(part1)
        part3=sdes(self.key1).generate_cipher(part2)
        return part3

    def decryption(self,cipher_text):

        '''
        Operations for create plain text
        :param cipher_text: Encrypted message
        :return: Original message
        '''

        part1 = sdes(self.key1).decyription(cipher_text)
        part2 = sdes(self.key2).generate_cipher(part1)
        part3 = sdes(self.key1).decyription(part2)
        return part3
