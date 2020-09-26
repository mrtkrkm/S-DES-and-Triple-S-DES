from SDES.S_DES import S_DES
from SDES.TripleSDES import TripleSDES
from timeit import default_timer as timer

class Crack(object):
    def __init__(self):
        pass


    def __read_data(self, dir):
        text=''
        with open(dir, 'r') as f:
            text=f.read()
        return text

    def __create_key(self,key_int):
        '''
        Create 10 bit keys with integer input
        :param key_int: Integer Input
        :return: 10 bit key in string Format
        '''
        value = bin(key_int)[2:]
        while len(value) < 10:
            value = '0' + value
        return value

    def create_blocks(self,text):
        '''
        Create 8 bit blocks of Input
        :param text: Whole message
        :return: List of 8 bit message
        '''
        new_text = [''.join(text[i * 8:(i + 1) * 8]) for i in range(0, len(text) // 8)]
        return new_text

    def __check_ascii(self,binary):
        '''
        Check whether value is belong the ascii Characters
        :param binary: 8 bit sequence
        :return: Boolean True,False
        '''
        bin_val = int(binary, 2)
        return (bin_val >= 32 and bin_val <= 126)

    def convert_ascii(self,binary):
        '''
        Convert binary array to Ascii format
        :param binary: 8 bit binary Array
        :return: Ascii character of binary input array
        '''
        len = int(binary, 2)
        text = len.to_bytes((len.bit_length() + 7) // 8, 'big').decode('utf-8', 'surrogatepass')
        return text

    def crack_sdes(self,input):
        '''
        Crack SDES cipher Text by Using brute force
        1- It Generate all 10 bit Key value one by one
        2- Decrypt all blocks by using created key
        3- Check whether decrypt text is proper Ascii characters
        4- If all decrypt texts are proper ascii character then finish loops
        :param input: cipher text message
        :return: Decrypt plain Text message and Key
        '''
        if input[-4:]=='.txt':
            input=self.__read_data(input)

        start = timer()
        blocks = self.create_blocks(input)
        text = ''
        for i in range(1024):
            key = self.__create_key(i)
            sdes = S_DES(key)
            for j in range(0, len(blocks)):
                plain = sdes.decyription(blocks[j])
                if self.__check_ascii(plain) == False:
                    text = ''
                    break
                else:
                    text += self.convert_ascii(plain)
            if j == len(blocks) - 1:
                print('*'*50)
                print(f'Key = {key}')
                print(f'Plain Text = {text}')
                end=timer()
                print(f"Total time for SDES Cracking ={end-start:.2f} second")
                print('*' * 50)
                return key,text
        return None

    def crack_tsdes(self,input):
        '''
        Crack TSDES algorith by using Brute Force method
        1- It starts with generating  10 bit key value for key1
        2- Then generate all possible 10 bit key values for ky2
        3- Decrypt block cipher text value by using key1 and key2
        4- Check whether decrypted text is proper ascii values
        5- If all block texts are meet the condition then end the loop

        :param input: cipher text value
        :return: Plained text value and Key values
        '''
        if input[-4:] == '.txt':
            input = self.__read_data(input)

        start = timer()
        blocks = self.create_blocks(input)
        text = ''
        for i in range(1024):
            key1 = self.__create_key(i)
            for j in range(1024):
                key2 = self.__create_key(j)
                tsdes = TripleSDES(key1, key2)
                for l in range(len(blocks)):
                    plain = tsdes.decryption(blocks[l])
                    if self.__check_ascii(plain) == False:
                        text = ''
                        break
                    else:
                        text += self.convert_ascii(plain)

                if l == len(blocks) - 1:
                    print('*' * 50)
                    print(f'Key1 = {key1}')
                    print(f'Key2 = {key2}')
                    print(f'Plain Text = {text}')
                    end = timer()
                    print(f"Total time for Triple-SDES Cracking ={end - start:.2f} second")
                    print('*' * 50)
                    return key1, key2, text
        return None