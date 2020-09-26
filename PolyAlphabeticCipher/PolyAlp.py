import PolyAlphabeticCipher.Constants as constants
import operator
from timeit import default_timer as timer
from operator import itemgetter

class PolyAlphcipher(object):

    def __init__(self, enc_input, max_key, alphabet=None, alphabet_freq=None):
        '''

        :param enc_dir: File directory of Encrypted Message
        :param max_key: Maximum Key length
        :param alphabet: Custom alphabet
        :param alphabet_freq: Custom alphabet_freq
        '''

        self.enc_input=enc_input
        self.max_key=max_key
        self.read_data()

        if alphabet is not None:
            self.alphabet=alphabet
        else:
            self.__set_alphabet()

        if alphabet_freq is not None:
            self.alphabet_freq=alphabet_freq
        else:
            self.__set_alphabet_freq()
        self.first_time=True

    def read_data(self):
        '''
        Read cipher text
        '''
        if self.enc_input[-4:]==".txt":
            with open(self.enc_input,'r') as file:
                raw_text=file.read()
        else:
            raw_text=self.enc_input

        text=raw_text.replace('\n','')
        self.cipher=text.replace(' ','')

    def __set_alphabet(self):
        '''
        Set the english alphabet  as alphabet  if alphabet  is None
        :return:
        '''
        self.alphabet=constants.ENGLISH_ALPHABET

    def __set_alphabet_freq(self):
        '''
        Set the english alphabet frequency as alphabet frequencey if alphabet frequencey is None
        :return:
        '''
        self.alphabet_freq=constants.ENGLISH_ALPH_FREQ

    def __get_blocks(self,text, key_s):
        '''
        Divide Text into number of key block
        :param text: Text for dividing
        :param key_s: Number of block and also represent the number of jump in list
        :return: List of blocks with length of key_s
        '''
        return [text[i::key_s] for i in range(key_s)]

    def __get_freq(self,text):
        '''
        Find frequency for each character
        :param text: Message that will be used
        :return: Frequency dictionary
        '''
        freq={}

        for i in text:
            if i not in freq.keys():
                freq[i]=1
            else:
                freq[i] +=1
        return freq

    def find_key_length(self):
        '''
        Find length of the key by using Index of Coincidence method
        :return: Length of key
        '''

        alph_len=len(self.alphabet)
        Av_ioc = []
        for i in range(1,self.max_key+1):
            start=timer()
            blocks=self.__get_blocks(self.cipher,i)
            avg=0
            for block in blocks:
                freq_dic=self.__get_freq(block)
                freq=list(freq_dic.values())
                freq_m=list(map(lambda x:x-1, freq))
                multiply=list(map(operator.mul,freq,freq_m))
                sum_num=sum(multiply)
                N=len(block)
                ioc=sum_num/(N*(N-1)/alph_len)
                avg +=ioc/len(blocks)
            Av_ioc.append(avg)
            end=timer()
            if self.first_time:
                print(f'Total time for {i} length key is {end-start}')
        index=Av_ioc.index(max(Av_ioc))
        self.first_time=False
        return index+1


    def __ioc(self,text):
        '''
        Index of Coincedence calculation for each block
        :param text: Block message
        :return: Score of ioc
        '''
        freq_dic=self.__get_freq(text)

        s=0
        for letter in self.alphabet:
            if letter in freq_dic.keys():
                s +=(freq_dic[letter]/len(text))*self.alphabet_freq[letter]

        return s

    def __to_numeric(self,text):
        '''
        Transform text into numeric representation
        :param text: String text message
        :return: List of numeric index in alphabet
        '''
        numeric_index = [self.alphabet.index(letter) for letter in text]
        return numeric_index

    def __to_text(self,numeric):
        '''
        Transform numeric index into text representation
        :param numeric: Index of letter in alphabet
        :return: List of letters
        '''
        text_list=[self.alphabet[ind] for ind in numeric]
        return text_list

    def __shift_text(self,text,value):
        '''
        Left shift text by value
        :param text: Text will be shifted
        :param value: Shift value
        :return: Left shifted text
        '''
        org=[self.alphabet.index(letter) for letter in text]
        new=list(map(lambda x:(x-value)%26,org))
        new_text_list=[self.alphabet[ind] for ind in new]

        return ''.join(new_text_list)

    def __blocks_analysis(self,text):
        '''
        Analyse each block for finding key
        :param text: Block of cipher text
        :return: Key letter
        '''

        scores=[]
        for i,candidate_key in enumerate(self.alphabet):
            score=self.__ioc(text)
            scores.append(score)
            text=self.__shift_text(text,1)

        max_ind=scores.index(max(scores))

        letter=self.alphabet[max_ind % len(self.alphabet)]

        return letter

    def find_key(self):
        '''
        Finding the key by using IOC for each block
        :return: key value
        '''
        key_length=self.find_key_length()
        blocks=self.__get_blocks(self.cipher,key_length)

        key=[]
        for block in blocks:
            key.append(self.__blocks_analysis(block))

        self.key=''.join(key)
        return ''.join(key)


    def decrypt_text(self, key=None):
        '''

        Decrypt the cipher text.

        :param key: key value
        :return: Plain text
        '''

        if key is None:
            keys=self.find_key()
        else:
            keys=key
        keys_num=self.__to_numeric(keys)
        numeric=self.__to_numeric(self.cipher)

        new_numeric=[]
        for i in range(len(numeric)):
            new_n=(numeric[i]-keys_num[i%len(keys)])%26
            new_numeric.append(new_n)

        text_list=self.__to_text(new_numeric)

        return ''.join(text_list)

    def encrypt_text(self, keys):
        '''
        Encrypt the plain text.

        :param keys: key value
        :return: Cipher text
        '''
        print(keys)
        keys_num=self.__to_numeric(keys)
        numeric=self.__to_numeric(self.cipher)

        new_numeric=[]
        for i in range(len(numeric)):
            new_n=(numeric[i]+keys_num[i%len(keys)])%26
            new_numeric.append(new_n)

        text_list=self.__to_text(new_numeric)

        return ''.join(text_list)

    def save_file(self,name,text):
        '''
        Save text into file
        :param name: Name of the file
        :param text:  Content
        '''
        with open(name,'w+') as f:
            f.write(text)
