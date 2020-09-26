from FlaskWeb import flaskMain
from PolyAlphabeticCipher.PolyAlp import PolyAlphcipher
from SDES.S_DES import S_DES as sdes
from SDES.TripleSDES import TripleSDES as tsdes
from SDES.Cracking import Crack as crack

######################################### PART 1 ##########################################################################
######### TASK 1-TASK 2 ############
poly=PolyAlphcipher('data/part1-text1.txt',max_key=10)
print('*' * 50+'PART 1- TASK 1-TASK 2 '+'*'*20)
print(f'The length of the key is {poly.find_key_length()}')
print(f'The  the key is {poly.find_key()}')
plain_text=poly.decrypt_text()
print(f'The  the key is {plain_text}')
poly.save_file('data/part1_decrypt.txt',plain_text)
print(len(plain_text))

##########TASK 3############
print('*' * 50+'PART 1- TASK 3 '+'*'*20)
poly=PolyAlphcipher('data/part1-text2.txt' , max_key=10)
Task3_text=poly.decrypt_text('BDLAEKCY')
poly=PolyAlphcipher(Task3_text , max_key=10)
print(poly.find_key())
print(poly.decrypt_text())

######################################### PART 2 ##########################################################################
#############TASK 1##############

print('*' * 50+'PART 2- TASK 1 '+'*'*20)
Raw_keys=['0000000000','0000011111','0010011111','0010011111','1111111111','0000011111','1000101110','1000101110']
Operation=['encryption']*4 +['decryption']*4
inputs=['00000000','11111111','11111100','10100101','00001111','01000011','00011100','11000010']

output_encrypt=[]
output_decrypt=[]
for key, input, operation in zip(Raw_keys,inputs, Operation):
    sde=sdes(key)
    if operation=="encryption":
        output_encrypt.append(sde.generate_cipher(input))
    else:
        output_decrypt.append(sde.decyription(input))

print("SDES  Table 1 Encryption Results")
print(output_encrypt)
print("SDES  Table 1 Decryption Results")
print(output_decrypt)

#############TASK 2##############

Raw_keys1=['1000101110','1000101110','1111111111','0000000000','1000101110','1011101111','1111111111','0000000000']
Raw_keys2=['0110101110','0110101110','1111111111','0000000000','0110101110','0110101110','1111111111','0000000000']
Operation=['encryption']*4 +['decryption']*4
inputs=['11010111','10101010','00000000','01010010','11100110','01010000','00000100','11110000']

print('*' * 50+'PART 2- TASK 2'+'*'*20)
output_encrypt=[]
output_decrypt=[]
for key1, key2, input, operation in zip(Raw_keys1, Raw_keys2, inputs, Operation):
    tsde=tsdes(key1,key2)
    if operation=="encryption":
        output_encrypt.append(tsde.encryption(input))
    else:
        output_decrypt.append(tsde.decryption(input))

print("Triple SDES  Table 2 Encryption Results")
print(output_encrypt)
print("Triple SDES  Table 2 Decryption Results")
print(output_decrypt)

#############TASK 3 #############
print('*' * 50+'PART 2- TASK 3'+'*'*20)
crack_ins=crack()
crack_ins.crack_sdes('data/ctx1.txt')
crack_ins.crack_tsdes('data/ctx1.txt')

############TASK 4###############
print('*' * 50+'PART 2- TASK 4'+'*'*20)
flaskMain.run()

