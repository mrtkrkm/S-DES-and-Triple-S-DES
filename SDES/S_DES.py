import SDES.Constants as constants

class S_DES(object):
    def __init__(self, raw_key):
        '''

        :param raw_key: The key
        '''
        self.raw_key=raw_key
        self.keys=self.__generate_key()
        #self.cipher=self.__generate_cipher()

    def __permutate_bits(self,input, permutate_index):

        '''
        Permutate the input by using pre-defined permutation index
        :param input: list of input
        :param permutate_index: pre-defined permutation index
        :return: permutated list
        '''

        return [input[ind] for ind in permutate_index]

    def __shift_value(self,input,number_of_shift):

        '''
        Left shift input list by number_of_Shift value

        :param input: original list
        :param number_of_shift: value for shifting
        :return: shifted list
        '''

        return input[number_of_shift:]+input[:number_of_shift]

    def __generate_key(self):
        '''
        Key generation for S-DES
        :return: generated keys
        '''

        keys=[]
        temp = self.__permutate_bits(self.raw_key, constants.KEY_P10)
        templ, tempr = temp[:5], temp[5:]
        for i in range(1,3):
            templ, tempr=self.__shift_value(templ,i), self.__shift_value(tempr,i)
            key=self.__permutate_bits(templ+tempr,constants.KEY_P8)
            keys.append(key)
        return keys

    def __xor__(self, first, sec):
        '''
        Element-wise XOR logical operation.
        :param first: first input
        :param sec: second input
        :return: xor results
        '''
        return [str(int(i!=y)) for i,y in zip(first,sec)]

    def __convertDec(self,val):
        '''
        Convert text to decimal
        :param val: String value
        :return: decimal value
        '''
        return int(''.join(val),2)

    def __convertStr(self,val):
        '''

        :param val: binary value
        :return: string representation of binary value.
        '''

        result= bin(val)[2:]
        if result=='0' or result=='1':
            result= '0'+result
        return result

    def __find_colandRow(self,value):
        '''
        Finding row and column index for value.
        In order to find corresponding value in predefined S0, S1 matrices.

        :param value: original list
        :return: row and column index
        '''
        row_value=self.__convertDec(value[0]+value[3])
        col_value=self.__convertDec(value[1]+value[2])
        return row_value,col_value


    def __multiply_with_table(self, value1, value2):
        '''
        Finding corresponding values in predefined S0 and S1 matrices

        :param value1: Left part values
        :param value2: right part values
        :return: Bunary representation of values.
        '''
        value1_row, value1_col=self.__find_colandRow(value1)
        value2_row, value2_col = self.__find_colandRow(value2)
        new_value1=self.__convertStr(constants.S0[value1_row][value1_col])
        new_value2 = self.__convertStr(constants.S1[value2_row][value2_col])
        return list(new_value1+new_value2)

    def __f_func(self, input,pos,keys):

        '''
        F function operation for SDES rounds.
        :param input: list of values
        :param pos: number of round. For using corresponding generated key
        :param keys: Generated key values
        :return: list of values
        '''

        left,right=input[:4], input[4:]
        e_p=self.__permutate_bits(right,constants.P_TEXT_P2)
        res_xor=self.__xor__(e_p,keys[pos])
        xor_left, xor_right = res_xor[:4], res_xor[4:]
        p4=self.__multiply_with_table(xor_left, xor_right)
        p4=self.__permutate_bits(p4,constants.P_TEXT_P3)

        sw1=self.__xor__(p4,left)
        sw=right+sw1
        if pos==0:
            sw=right+sw1
        else:
            sw=sw1+right
        return sw

    def generate_cipher(self, plain_text):
        '''

        :param plain_text: Original Text to encryption
        :return: Encrypt cipher text
        '''

        cipher=self.__permutate_bits(plain_text,constants.P_TEXT_P1)

        for i in range(2):
            cipher=self.__f_func(cipher,i,self.keys)

        cipher=self.__permutate_bits(cipher, constants.P_TEXT_P4)
        return ''.join(cipher)

    def decyription(self,cipher_text):
        '''

        :param cipher_text: TExt to decrypt
        :return: Plain Text
        '''

        plain_text = self.__permutate_bits(cipher_text, constants.P_TEXT_P1)

        for i in range(2):
            plain_text = self.__f_func(plain_text, i,self.keys[::-1])

        plain_text = self.__permutate_bits(plain_text, constants.P_TEXT_P4)
        return ''.join(plain_text)

